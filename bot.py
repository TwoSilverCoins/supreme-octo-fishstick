import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
PREFIX = "!"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Load command modules
EXTENSIONS = [
    "commands.admin",
    "commands.tm"
]

@bot.event
async def on_ready():
    print(f"✅ PolycastBot is online as {bot.user}")
    for ext in EXTENSIONS:
        bot.load_extension(ext)

@bot.event
async def on_message(message):
    from core.filter import is_translatable
    from core.translator import translate
    from utils.cooldown import is_translation_enabled

    if not is_translatable(message):
        return

    if not is_translation_enabled():
        await message.channel.send("⛔ Translation is currently disabled.")
        return

    # Example routing logic (simplified)
    if message.channel.name == "english":
        translated_es = translate(message.content, "es")
        translated_pt = translate(message.content, "pt")
        # Replace with actual channel IDs or routing logic
        await message.guild.get_channel(1234567890).send(translated_es)
        await message.guild.get_channel(9876543210).send(translated_pt)

    await bot.process_commands(message)

bot.run(TOKEN)
