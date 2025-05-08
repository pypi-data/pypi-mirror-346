import discord
import asyncio
from .loader import load_modules

class DiscordBotRunner:
    def __init__(self, token, modules_folder, **kwargs):
        self.token = token
        self.modules_folder = modules_folder
        intents = discord.Intents.all()
        self.client = discord.Client(intents=intents)

    def run(self):
        @self.client.event
        async def on_ready():
            print(f"Discord bot logged in as {self.client.user}")
            load_modules(self.client, platform='discord', folder=self.modules_folder)

        self.client.run(self.token)
