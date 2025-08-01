import discord
from config_manager import load_config
from router import route_message
from safeguards import should_process

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if not should_process(message):
        return

    await route_message(client, message)

client.run(load_config("BOT_TOKEN"))
