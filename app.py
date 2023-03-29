import os

from webex_bot.webex_bot import WebexBot
from webexteamssdk import WebexTeamsAPI

from openai_command import OpenAiCommand

access_token = os.getenv("WEBEX_TEAMS_ACCESS_TOKEN")

# Create a Bot Object
bot = WebexBot(teams_bot_token=access_token,
               approved_users=[os.getenv("WEBEX_EMAIL")],
               bot_name="OpenAI Bot",
               include_demo_commands=False)

webex_api = WebexTeamsAPI(access_token=access_token)

# Grab your API over at https://beta.openai.com/account/api-keys
if os.getenv('OPENAI_API_KEY'):
    bot.commands.clear()
    bot.add_command(OpenAiCommand(os.getenv('OPENAI_API_KEY')))
    bot.help_command = OpenAiCommand(os.getenv('OPENAI_API_KEY'))

bot.run()
