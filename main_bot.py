#linecount: utils\
import sys
import emoji
import nextcord as discord
from nextcord.ext import commands
from datetime import datetime
import os
import argparse
import time as time_module
from dotenv import load_dotenv
from nextcord.ext.application_checks import is_owner
from utils import mylogger, embedutil
from utils.antimakkcen import antimakkcen
from utils.levenstein import recommend_words
from data.consts import TESTSERVER_ID as TEST
from data.consts import ADMIN_ID

"""You should take a look at cogs. That is where the commands are stored. Each cog is just like a folder for commands. 
They are separated into cogs just to arbitrarily group them together. Check out basiccog.py for how commands are made
then the others for how things work. The templatecog.py is an empty cog for you to have fun in."""


start = time_module.perf_counter()  # measuring how long it takes to boot up the bot

VERSION = "0.1a"  # whatever you like lol, alpha 0.1, change it as you t
PROJECT_NAME = "Testing bot"  # NAME_YOUR_CHILD (note: this name will not show up as the bot name hehe)
AUTHOR = "sanyi"  # ADD_YOUR_NAME_BE_PROUD
TESTSERVER_ID = "Set in data/consts.py because of imports"  # test commands will only show up in this server
# ADMIN_ID = "Moved to data/consts.py for consistency"  # add your discord user id, used in the is_owner() check
load_dotenv(r"./credentials/main.env")  # loading the bot login token

parser = argparse.ArgumentParser(prog=f"{PROJECT_NAME} V{VERSION}", description='A fancy discord bot.', epilog=f"Written by {AUTHOR}\nTemplate written by theonlypeti.")

"""You can enable and disable each cog by launching this file using the command line arguments below.
Example: python main_bot.py --no_wordle --no_reddit
or in PyCharm the dropdown menu up next to the run button, then edit configuration -> script parameters
You can reload commands if you have edited them while the bot is running by calling /rl in a discord channel."""

parser.add_argument("--minimal", action="store_true", help="Disable most of the extensions.")
parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
parser.add_argument("--no_testing", action="store_true", help="Disable testing module.")
parser.add_argument("--only_testing", action="store_true", help="Add testing module.")
parser.add_argument("--logfile", action="store_true", help="Turns on logging to a text file.")
parser.add_argument("--no_linecount", action="store_true", help="Disabless opening each file to read the linecount.")

for cog in os.listdir("./cogs"):  # adding command line arguments for removing some parts of the bot
    if cog.endswith("cog.py"):
        parser.add_argument(f"--no_{cog.removesuffix('cog.py')}", action="store_true", help=f"Disable {cog} extension.")
        parser.add_argument(f"--only_{cog.removesuffix('cog.py')}", action="store_true", help=f"Enable only the {cog} extension.")

args = parser.parse_args()  # reads the command line arguments
baselogger = mylogger.init(args)  # initializing the logger

# root = os.getcwd()  # current working directory
root = os.path.dirname(os.path.abspath(__file__))

intents = discord.Intents.default()
intents.members = True  # needed so the bot can see server members

# if intents are not turned on in https://discord.com/developers/applications/ (your_bot_id)/bot make sure to do so.
client = commands.Bot(intents=intents, chunk_guilds_at_startup=True, activity=discord.Game(name="Booting up..."), owner_id=ADMIN_ID)
client.logger = baselogger

if ADMIN_ID == 601381789096738863:
    client.logger.warning("Please change the ADMIN_ID in data/consts.py to your own discord user id, this is a placeholder.")


@client.event
async def on_ready():
    await set_linecount_activity()  # careful with on_ready, it could be called many times (potentially once for each server), running code inside it could cause many requests sent
    print(f"Signed in as {client.user.name} at {datetime.now()}")
    baselogger.info(f"{time_module.perf_counter() - start}s Bootup time")


@client.event
async def on_disconnect():  # happens sometimes, ensures on_ready will not display million seconds
    global start
    start = time_module.perf_counter()


@client.listen("on_interaction")
async def oninter(inter: discord.Interaction):
    cmd = inter.application_command
    if isinstance(cmd, discord.SlashApplicationSubcommand):
        cmd = cmd.parent_cmd.name + "/" + cmd.name
        opts = [f'{a["name"]} = {a["value"]}' for a in inter.data.get("options", [])[0]["options"]]
    elif isinstance(cmd, discord.SlashApplicationCommand):
        cmd = cmd.name
        opts = [f'{a["name"]} = {a["value"]}' for a in inter.data.get("options", [])]
    else:
        ...  # probably buttons
        return

    tolog = f"[{inter.user}] called [{cmd} with {opts}]  in: [{inter.guild}/{inter.channel}]"
    tolog = emoji.demojize(antimakkcen(tolog)).encode('utf-8', "ignore").decode()
    baselogger.log(25, tolog)
    # baselogger.log(10, tolog)


@client.listen("on_application_command_error")
async def on_app_error(inter, error):
    await embedutil.error(inter, f"{error.__class__.__name__}:\n {error}", delete=10)


@client.slash_command(name="rl", description="Reload all bot commands and extensions", guild_ids=TEST)
@is_owner()
async def reload_cogs(interaction, cogs:str=None):
    """Reload a set of cogs"""
    await interaction.response.defer(ephemeral=True)
    if not cogs:
        cogs = interaction.client.coglist
    log = ""
    linecount = 0
    if not args.no_linecount:
        linecount = readlinecount(os.path.join(root, __file__))
    for n, cog in enumerate(interaction.client.coglist, start=1):
        try:
            if not args.no_linecount:
                fpath = os.path.join(root, "cogs", cog)
                linecount += readlinecount(fpath)
            if cog in cogs:
                client.reload_extension("cogs." + cog[:-3])
                # if not args.debug:
                #     sys.stdout.write(
                #         f"\rLoading... {(n / len(cogs)) * 100:.02f}% [{(int((n / len(cogs)) * 10) * '=') + '>':<10}]")
                #     sys.stdout.flush()
                log += f"Successfully reloaded cog {cog}\n"  # TODO consolidate this and reloading into a func?
        except Exception as e:
            log += f"Failed to reload cog {cog}: {e.__class__}: {e}\n"
            interaction.client.logger.error(f"Cog reloading: failed to reload {cog}: {e}")
    await interaction.send(embed=discord.Embed(description=log or "Empty?"), ephemeral=True)
    await set_linecount_activity()


@reload_cogs.on_autocomplete("cogs")
async def cogs_autocomplete(interaction: discord.Interaction, cogs: str):
    if cogs:
        get_near_cog = [i for i in interaction.client.coglist if antimakkcen(i.casefold()).startswith(antimakkcen(cogs.casefold()))][:25]
        if not get_near_cog:
            get_near_cog = recommend_words(cogs, interaction.client.coglist)
        await interaction.response.send_autocomplete(get_near_cog)
    else:
        await interaction.response.send_autocomplete([i for i in interaction.client.coglist[:25]]) #TODO i should really make a func for this autocomplete stuff


async def set_linecount_activity():
    game = discord.CustomActivity(
        name="Custom Status",
        state=f"{client.linecount} lines of code; V{VERSION}!"
    )
    await client.change_presence(activity=game)


def readlinecount(fpath):
    with open(fpath, "r", encoding="UTF-8") as f:  # type: TextIOWrapper
        firstline = f.readline()
        lc = 1
        if firstline.startswith("#linecount:"):
            toopen = firstline.split(":")[1].strip()
            if toopen:
                if toopen.endswith(".py"):
                    toopen = os.path.join(root, toopen)
                    # pipikLogger.debug(f"found file, Opening {toopen}")
                    lc = readlinecount(toopen)
                elif toopen.endswith("\\"):
                    for lroot, dirs, files in os.walk(toopen):
                        for file in files:
                            if file.endswith(".py"):
                                # pipikLogger.debug(f"found folder, Opening {os.path.join(lroot, file)}")
                                lc += readlinecount(os.path.join(lroot, file))
                else:
                    baselogger.debug(f"malformed {fpath}")
                    ...
        lc += len(f.readlines())
        return lc


#-------------------------------------------------#

if __name__ == '__main__':
    os.chdir(root)

    if not args.no_linecount:  # if you don't want to open each file to read the linecount
        client.linecount = readlinecount(os.path.join(root, __file__))
    else:
        client.linecount = "Unknown"

    allcogs = [cog for cog in os.listdir("./cogs") if cog.endswith("cog.py")] + ["testing.py"]
    cogcount = len(allcogs)
    cogs = []

    if not args.minimal:  # if not minimal
        if not [not cogs.append(cog) for cog in allcogs if args.__getattribute__(f"only_{cog.removesuffix('cog.py').removesuffix('.py')}")]: #load all the cogs that are marked to be included with only_*
            cogs = allcogs[:]  # if no cogs are marked to be exclusively included, load all of them
            for cog in reversed(cogs):  # remove the cogs that are marked to be excluded with no_*
                if args.__getattribute__(f"no_{cog.removesuffix('cog.py').removesuffix('.py')}"):  # if the cog is marked to be excluded
                    cogs.remove(cog)  # remove it from the list of cogs to be loaded
    cogs.remove("testing.py") if args.no_testing else None  # remove testing.py from the list of cogs to be loaded if testing is disabled

    client.coglist = cogs  # for use in reload command
    for n, file in enumerate(cogs, start=1):  # its in two loops only because i wouldn't know how many cogs to load and so dont know how to format loading bar
        if not args.no_linecount:
            fpath = os.path.join(root, "cogs", file)
            client.linecount += readlinecount(fpath)
        client.load_extension("cogs." + file[:-3])
        if not args.debug:
            sys.stdout.write(f"\rLoading... {(n / len(cogs)) * 100:.02f}% [{(int((n/len(cogs))*10)*'=')+'>':<10}]")
            sys.stdout.flush()
    sys.stdout.write(f"\r{len(cogs)}/{cogcount} cogs loaded.".ljust(50)+"\n")
    sys.stdout.flush()
    os.chdir(root)

    client.run(os.getenv("MAIN_DC_TOKEN"))
