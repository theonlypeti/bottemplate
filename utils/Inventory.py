from typing import Coroutine, Callable
import emoji
import nextcord as discord
from utils.antimakkcen import antimakkcen
from utils.paginator import Paginator


class Inventory(Paginator):
    def __init__(self, items: list = None, on_update: Callable[[], Coroutine] = None):
        super().__init__(
            func=lambda pagi:
            discord.Embed(
                title=f"Words (Page {max(1,pagi.page+1)}/{max(1,pagi.maxpages)})",
                description=("\n".join(pagi.slice_inventory()) or "Looks like you don't have any words yet! Add some with the button below!"),
            ),
            select=self.RemoveWordSelect,
            inv=items,
            itemsOnPage=25)

        self.mergeview(self.AddWordView(self))
        self.on_update = on_update

    class AddWordView(discord.ui.View):
        def __init__(self, pagi):
            super().__init__(timeout=pagi.timeout)
            self.pagi: Inventory = pagi

        @discord.ui.button(label="Add words", style=discord.ButtonStyle.primary, emoji=emoji.emojize(":plus:"))
        async def add_word(self, button: discord.ui.Button, interaction: discord.Interaction):
            # await interaction.response.defer()
            await interaction.response.send_modal(self.AddWordModal(self.pagi))

        @discord.ui.button(label="Clear list", style=discord.ButtonStyle.primary, emoji=emoji.emojize(":cross_mark:", language="alias"))
        async def clear_words(self, button: discord.ui.Button, interaction: discord.Interaction):
            # await interaction.response.defer()
            self.pagi.inv.clear()
            await self.pagi.render(interaction)
            if self.pagi.on_update:
                await self.pagi.on_update()

        class AddWordModal(discord.ui.Modal):
            def __init__(self, pagi):
                super().__init__(title="Add a word")
                self.pagi: Inventory = pagi
                self.input = discord.ui.TextInput(label="Enter words separated by comma (,)",
                                                  min_length=2,
                                                  style=discord.TextInputStyle.paragraph,
                                                  placeholder="word1, word2, word3, ...")
                self.add_item(self.input)

            async def callback(self, interaction: discord.Interaction):
                for w in self.input.value.split(","):
                    if antimakkcen(w) not in map(antimakkcen, self.pagi.inv):
                        self.pagi.inv.append(w)
                await self.pagi.render(interaction)
                if self.pagi.on_update:
                    await self.pagi.on_update()

    class RemoveWordSelect(discord.ui.Select):
        def __init__(self, pagi: "Inventory"):
            super().__init__(min_values=1, max_values=max(1, len(pagi.slice_inventory())),
                             placeholder="Select words to remove",
                             options=([discord.SelectOption(label=word, emoji=emoji.emojize(":cross_mark:")) for word in pagi.slice_inventory()] or [discord.SelectOption(label="None")]),
                             disabled=not pagi.inv)
            self.pagi: Inventory = pagi

        async def callback(self, interaction: discord.Interaction):
            for word in self.values:
                self.pagi.inv.remove(word)
            await self.pagi.render(interaction)
            if self.pagi.on_update:
                await self.pagi.on_update()
