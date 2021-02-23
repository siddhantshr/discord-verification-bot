import discord
from discord.ext import commands, tasks
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

    @tasks.loop(seconds=10)
    async def allowing_bots(self):
        db = sqlite3.connect('data/allow_bots.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT till FROM allow")
        results = cursor.fetchone()
        if results:
            if int(results[0]) <= time.time():
                cursor.execute(f"DELETE FROM allow")

        db.commit()
        cursor.close()
        db.close()

    @tasks.loop(seconds=10)
    async def quarantine(self):
        guild = self.client.get_guild(735362818026766438)
        db = sqlite3.connect('data/member.sqlite')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM quar")
        results = cursor.fetchall()
        for result in results:
            if int(result[1]) <= time.time():
                if result is not None:
                    member = guild.get_member(result[0])
                    role = member.guild.get_role(794836199856013332)
                    if role not in member.roles:
                        cursor.execute(f"DELETE FROM quar WHERE member_id = {member.id}")
                    try:
                        await member.remove_roles(role)
                        cursor.execute(f"DELETE FROM quar WHERE member_id = {member.id}")
                    except:
                        pass
                    cursor.execute(f"DELETE FROM quar WHERE member_id = {member.id}")

        db.commit()
        cursor.close()
        db.close()

def setup(client):
    client.add_cog(Commands(client))