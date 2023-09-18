import nextcord as discord
from nextcord.ext import commands


class Template(commands.Cog):
    def __init__(self, client):
        global logger
        logger = client.logger.getChild(f"{__name__}Logger")
        self.client = client

    # add your own commands here
    # def ecate():
        ...


def setup(client):
    client.add_cog(Template(client))
