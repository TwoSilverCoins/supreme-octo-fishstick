import discord
from discord.ext import commands
from core.memory import insert_tm_entry, get_fuzzy_match
from utils.logger import log_error

class TMCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tm_add")
    async def add_tm(self, ctx, source: str, target: str, lang_pair: str):
        try:
            insert_tm_entry(source, target, lang_pair)
            await ctx.send(f"✅ Added to TM: `{source}` → `{target}` [{lang_pair}]")
        except Exception as e:
            log_error(str(e), {"command": "tm_add"})
            await ctx.send("❌ Failed to add entry.")

    @commands.command(name="tm_match")
    async def match_tm(self, ctx, query: str, lang_pair: str):
        try:
            match = get_fuzzy_match(query, lang_pair)
            if match:
                await ctx.send(f"🔍 Match found: `{match}`")
            else:
                await ctx.send("⚠️ No match found.")
        except Exception as e:
            log_error(str(e), {"command": "tm_match"})
            await ctx.send("❌ Error during matching.")

def setup(bot):
    bot.add_cog(TMCommands(bot))
