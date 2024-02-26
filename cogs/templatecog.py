import nextcord as discord
from nextcord.ext import commands


class Template(commands.Cog):
    def __init__(self, client):
        self.logger = client.logger.getChild(f"{self.__module__}")
        self.client = client

    # add your own commands here
    # def ecate():
        ...


def setup(client):
    client.add_cog(Template(client))
