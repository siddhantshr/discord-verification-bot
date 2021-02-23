import discord
from discord.ext import commands
import sqlite3
import time
import datetime
import asyncio
import random

start_time = datetime.datetime.utcnow()

s_nouns = ["A dude", "My mom", "The king", "Some guy", "A cat with rabies", "A sloth", "Your homie", "This cool guy my gardener met yesterday", "Superman"]
p_nouns = ["These dudes", "Both of my moms", "All the kings of the world", "Some guys", "All of a cattery's cats", "The multitude of sloths living under your bed", "Your homies", "Like, these, like, all these people", "Supermen"]
s_verbs = ["eats", "kicks", "gives", "treats", "meets with", "creates", "hacks", "configures", "spies on", "retards", "meows on", "flees from", "tries to automate", "explodes"]
p_verbs = ["eat", "kick", "give", "treat", "meet with", "create", "hack", "configure", "spy on", "retard", "meow on", "flee from", "try to automate", "explode"]
infinitives = ["to make a pie.", "for no apparent reason.", "because the sky is green.", "for a disease.", "to be able to make toast explode.", "to know more about archeology."]

def sing_sen_maker():
    return f"{random.choice(s_nouns)} {random.choice(s_verbs)} {random.choice(s_nouns).lower() or random.choice(p_nouns).lower()} {random.choice(infinitives)}"

class Commands(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Booted up Events")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            db = sqlite3.connect("data/allow_bots.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT till FROM allow")
            result = cursor.fetchone()
            if result is None:
                await member.kick()
                print(f"{member} was kicked!")
            if result is not None:
                print(f"I allowed {member}")
        else:
            await member.send(f"{member} Please verify for donut's cafe!")
            msg = sing_sen_maker()
            await member.send(f"Type Back this: `{msg}`")

            def check(m):
                return m.content == msg
            try:
                await self.client.wait_for('message', timeout=120.0, check=check)
            except asyncio.TimeoutError:
                await member.send("You didnt verify in time :( Still you can rejoin! https://discord.gg/CnhN4Jh")
            else:
                days = (datetime.datetime.utcnow() - member.created_at).days
                if days <= 10:
                    # db
                    unmute_time = 86400 + time.time()
                    db = sqlite3.connect("data/member.sqlite")
                    cursor = db.cursor()
                    cursor.execute(f"SELECT time_to_end FROM quar WHERE member_id = {member.id}")
                    result = cursor.fetchone()
                    if result is None:
                        sql = "INSERT INTO quar(member_id, time_to_end) VALUES(?,?)"
                        val = (member.id, round(unmute_time))
                    if result is not None:
                        sql = "UPDATE quar SET time_to_end = ? WHERE member_id = ?"
                        val = (round(unmute_time), member.id)
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()

                    # roles
                    q_role = member.guild.get_role(794836199856013332)
                    role = member.guild.get_role(742317739406000129)
                    await member.add_roles(q_role)
                    await member.add_roles(role)
                    await member.send(f"Since your account is made {days} days ago, You will be in quarantine for a day")
                else:
                    role = member.guild.get_role(742317739406000129)
                    role2 = member.guild.get_role(794836199856013332)
                    await member.add_roles(role)
                    await member.add_roles(role2)
                    await member.send("You will be verified in 10 minutes! Please wait till then..")
                    await asyncio.sleep(600)
                    await member.remove_roles(role2)

def setup(client):
    client.add_cog(Commands(client))