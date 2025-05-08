from .bot_discord import DiscordBotRunner
from .bot_twitch import TwitchBotRunner

class StreamBot:
    def __init__(self, bot_type, token, modules_folder='modules', **kwargs):
        self.bot_type = bot_type.lower()
        self.token = token
        self.modules_folder = modules_folder
        self.bot_runner = None
        self.kwargs = kwargs

        if self.bot_type == 'discord':
            self.bot_runner = DiscordBotRunner(self.token, self.modules_folder, **self.kwargs)
        elif self.bot_type == 'twitch':
            self.bot_runner = TwitchBotRunner(self.token, self.modules_folder, **self.kwargs)
        else:
            raise ValueError("Invalid bot type. Use 'Discord' or 'Twitch'.")

    def run(self):
        if self.bot_runner:
            self.bot_runner.run()
