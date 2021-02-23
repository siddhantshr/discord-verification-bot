import discord
from discord.ext import commands
import sqlite3
import time
import datetime

start_time = datetime.datetime.utcnow()

class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Booted up Commands")

    @commands.command()
    async def allow_bots(self, ctx):
        if ctx.author.id == 711444754080071714:
            db = sqlite3.connect("data/allow_bots.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT till FROM allow")
            result = cursor.fetchone()
            if result is None:
                till_time = 300 + time.time()
                sql = "INSERT INTO allow(allow, till) VALUES(?,?)"
                val = ("true", round(till_time))
            if result:
                till_time = 300 + time.time()
                sql = "UPDATE allow SET till = ? WHERE allow = ?"
                val = (round(till_time), "true")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            await ctx.send("I will allow bots for 5 minutes!")
        else:
            await ctx.send(f"You are not Donut :|")

    @commands.command(name="uptime")
    async def uptime(self, ctx):
        current_time = datetime.datetime.utcnow()
        uptime = (current_time - start_time)
        embed = discord.Embed(color=0xFFFFF)
        embed.add_field(name="Bot's Uptime", value=f"I have been up for {uptime}!")
        embed.set_thumbnail(url=self.client.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def verify(self, ctx, member:discord.Member=None):
        if not member:
            await ctx.send("Give a valid member :|")
            return
        else:
            role = member.guild.get_role(742317739406000129)
            role2 = member.guild.get_role(794836199856013332)
            if role not in member.roles:
                await member.add_roles(role)
            if role2 in member.roles:
                await member.remove_roles(role2)
            await ctx.send(f"{member} is successfully verified!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            pass
        elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
            await ctx.send("Please give a valid member!")
        else:
            raise error

def setup(client):
    client.add_cog(Commands(client))
