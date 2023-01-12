import asyncio
import configparser
import datetime
import html
import random
import re
import time
import helper
import emoji
import humanize
import imgkit
import pykakasi
import discord

from io import BytesIO
from discord import Intents, app_commands
from discord.ext import commands
from discord.ext.commands import when_mentioned_or, Context


config = configparser.RawConfigParser()
config.read("secrets/config.ini")
intent = Intents.default()
admins = [int(u) for u in config["bot"]["admins"].split(",")]
test_guild = discord.Object(config["bot"]["test_guild"]) if "test_guilds" in config["bot"].keys() else None
bot = commands.Bot(command_prefix=when_mentioned_or("::"), intents=intent)

funny_msgs = ["どうぞ", "ウイ", "{0}たんのために、特別に早くしました!💫", "はい！🫡"]
call_for_donations = """> furi-sama is a very resource-intensive service. To help pay for our servers, please consider [buying me a coffee](https://ko-fi.com/realmayus)"""

class FuriSama(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot
        self.add_ctx_menu = app_commands.ContextMenu(
            name="Add Furigana",
            callback=self.add_furigana
        )
        self.add_ctx_menu.on_error = self.on_add_furigana_error
        self.bot.tree.add_command(self.add_ctx_menu)
        self.kks = pykakasi.kakasi()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot logged in as {self.bot.user}")

    @commands.command()
    async def sync(self, ctx: Context):
        if ctx.author.id not in admins:
            return await ctx.send("🚫  | You aren't authorized")
        await self.bot.tree.sync(guild=test_guild)
        await ctx.reply("Aight!")

    # @app_commands.guilds(test_guild)
    @app_commands.checks.cooldown(1, 10)
    async def add_furigana(self, interaction: discord.Interaction, message: discord.Message):
        txt = html.escape(emoji.replace_emoji(re.sub(r'((<a?)?:\w+:(\d+>)?)', '', message.content)))
        print(txt)
        if len(txt) > 128:
            return await interaction.response.send_message("🚫  | 失礼ですが、このメッセージは私には長すぎます。")
        html_string = "<body style=\"margin:none; padding:none; background-color: #000000; color:#ffffff; font-size: 60px\"><center>"

        start = time.time()
        results = self.kks.convert(txt)
        for token in results:
            print(token)
            # if token is equal to its hira or kana reading, pass the token itself such that it gets rendered gray.
            # e.g. when orig=ピザ realize that orig=kana and pass ピザ as reading to skip this token in the deconstructor
            reading = token["orig"] if token["orig"] == token["hira"] or token["orig"] == token["kana"] else token[
                "hira"]
            output = helper.deconstruct(token["orig"], reading)
            print(output)
            html_string += helper.deconstruct(token["orig"], reading)
        html_string += "</center></body>"
        start2 = time.time()
        img = imgkit.from_string(html_string, False, options={"format": "png", "disable-javascript": ''})
        duration = humanize.precisedelta(datetime.timedelta(seconds=start2 - start), minimum_unit="microseconds")
        duration2 = humanize.precisedelta(datetime.timedelta(seconds=time.time() - start2), minimum_unit="microseconds")
        print(f"Took {duration} (lexing) and {duration2} (rendering)")
        await interaction.response.send_message(
            call_for_donations + funny_msgs[random.randrange(0, len(funny_msgs))].format(interaction.user.display_name),
            file=discord.File(BytesIO(img), filename="furigana.png"), ephemeral=True)

    async def on_add_furigana_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message("🚫  | " + str(error), ephemeral=True)


instance = FuriSama(bot)


async def main():
    await bot.add_cog(instance)


asyncio.run(main())
bot.run(token=config["bot"]["token"])
