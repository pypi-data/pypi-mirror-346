from twitchio.ext import commands
from .loader import load_modules

class TwitchBotRunner:
    def __init__(self, token, modules_folder, prefix='!', **kwargs):
        self.token = token
        self.modules_folder = modules_folder
        self.prefix = prefix

        self.bot = commands.Bot(
            token=token,
            prefix=prefix,
            initial_channels=kwargs.get('channels', [])
        )

    def run(self):
        @self.bot.event
        async def event_ready():
            print(f"Twitch bot is online as {self.bot.nick}")
            load_modules(self.bot, platform='twitch', folder=self.modules_folder)

        self.bot.run()
