import discord
from discord.ext import commands
import asyncio
from .loader import load_modules

class DiscordBotRunner:
    def __init__(self, token, modules_folder, **kwargs):
        self.token = token
        self.modules_folder = modules_folder
        intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix='!', intents=intents)

    def run(self):
        @self.bot.event
        async def on_ready():
            print(f"Discord bot logged in as {self.bot.user}")
            load_modules(self.bot, platform='discord', folder=self.modules_folder)

        self.client.run(self.token)
