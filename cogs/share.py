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

class share(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @commands.command(aliases=["transfer"])
    @commands.guild_only()
    async def share(self,ctx,trainer2: discord.Member=None,amount=None):
        trainer1=ctx.message.author
        if trainer2==None:
            await ctx.send("`Syntax: c!share <@mention> <amount>`")
            return
        if trainer2.bot==True:
            await ctx.send("Don't mention a bot.")
            return
        if amount==None:
            await ctx.send("`Syntax: c!share <@mention> <amount>`")
            return
        if trainer1==trainer2:
            await ctx.send("Wait, buy a piggy bank bruh!")
            return
        try:
            amount=int(amount)
        except:
            await ctx.send("`Syntax: c!share <@mention> <amount>`")
            return
        giver=db2_collection.find_one({"id": trainer1.id})
        taker=db2_collection.find_one({"id": trainer2.id})
        if giver==None:
            await ctx.send("`Oops, Seems like you don't have an account`")
            return
        if taker==None:
            await ctx.send(f"`Oops, Seems like **{trainer2.name}** doesn't have an account`")
            return
        if giver["Credits"]<amount:
            await ctx.send("`Looks like you don't have enough balance. Balance : {:,.2f} cc`".format(giver['Credits']))
            return
        giver["Credits"]-=amount
        taker["Credits"]+=amount
        db2_collection.update_one({"id":trainer2.id},{"$set":{"Credits": taker["Credits"]}})
        db2_collection.update_one({"id":trainer1.id},{"$set":{"Credits": giver["Credits"]}})
        await ctx.send("`Money transfer succesful, Current balance: {:,.2f} cc`".format(giver['Credits']))
        chnl=self.bot.get_channel(733543421712662528)
        await chnl.send(f"Money({amount} cc) transferred from **{ctx.message.author.name}#{ctx.author.discriminator}**({ctx.message.author.id}) to **{trainer2.name}#{trainer2.discriminator}**({trainer2.id})")

def setup(bot):
	bot.add_cog(share(bot))
