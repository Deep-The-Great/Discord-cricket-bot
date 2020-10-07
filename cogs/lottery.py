import discord 
import asyncio
import random
from discord.ext import commands
import os
import datetime
import pymongo
import json
import math
db_client=pymongo.MongoClient(os.getenv("DB_URL"))
db1_client=pymongo.MongoClient(os.getenv("DB2_URL"))

class lottery(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @commands.command(aliases=["lotto"])
    @commands.guild_only()
    async def lottery(self,ctx,key=None):
        x=db3_collection.find_one()
        y=db2_collection.find_one({"id": ctx.message.author.id})
        if y==None:
            await ctx.send("You need to have an account to participate in the lottery.You can register/create an account using `c!register`.")
            return
        
        possible=["buy"]
        if key==None:
            embed=discord.Embed(title="Lottery prize",description=f"The current lottery pool is **{x['pool']}** cc.\nType `c!lottery buy` to buy a ticket.")
            await ctx.send(embed=embed)
            return
        if key.lower() not in possible:
            await ctx.send("Type `c!help lottery` to know about how to use the lottery.")
            return
        
        if key.lower()=="buy":
            if ctx.message.author.id in x["participants"]:
                await ctx.send("You have already bought one ticket, wait patiently for the next lottery.")
                return
            elif y['Credits']<100:
                await ctx.send("You don't have enough balance to buy a lottery ticket.")
                return
            else:
                x["participants"].append(ctx.message.author.id)
                x["pool"]+=100
                db3_collection.update_one({},{"$set":{"pool":x["pool"],"participants":x["participants"]}})
                db2_collection.update_one({"id":y["id"]},{"$set":{"Credits": y["Credits"]-100}})
                await ctx.send(f"You have been given a ticket, your ticket id is {len(x['participants'])}.")
                channel=self.bot.get_channel(732643877009227807)
                xy=db3_collection.find_one()
                await channel.send(f"**{ctx.message.author.name}#{ctx.message.author.discriminator}** has bought a lottery ticket(id: {len(x['participants'])}), current pool: {xy['pool']}")
                return
        
            
def setup(bot):
	bot.add_cog(lottery(bot))
