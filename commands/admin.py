import discord
from discord.ext import commands
from utils.quota import check_quota_status
from utils.logger import log_error

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="restart")
    @commands.has_permissions(administrator=True)
    async def restart_bot(self, ctx):
        await ctx.send("Restarting bot...")
        await self.bot.close()

    @commands.command(name="status")
    async def bot_status(self, ctx):
        status = check_quota_status()
        await ctx.send(f"Quota status: `{status}`")

    @commands.command(name="ping")
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! `{latency}ms`")

def setup(bot):
    bot.add_cog(AdminCommands(bot))
