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

class choose(commands.Cog):
	def __init__(self,bot):
        	self.bot=bot
	@commands.command()
	@commands.guild_only()
	
	async def choose(self,ctx,choice=None):
		if choice==None:
			await ctx.send("Syntax: `c!choose <bowl/bat>`")
			return
		if choice.lower() not in ["bowl","bat"]:
			await ctx.send("Syntax: `c!choose <bowl/bat>`")
			return
		x=db_collection.find_one({"Team1_member_id": ctx.message.author.id})
		if x==None:
			x=db_collection.find_one({"Team2_member_id": ctx.message.author.id})
			if x==None:
				await ctx.send("Type `c!help` to know about how to use the bot!")
				return
			else:
				if x["Now_batting"]!=0:
					return
				if x["Score_card"]["Toss"]==0:
					await ctx.send("Make sure you do the toss before choosing")
					return

				if x["Score_card"]["Toss"]!=ctx.message.author.id:
					await ctx.send("Looks like you didn't win the toss")
					return
				else:
					if choice.lower()=="bat":
						db_collection.update_one({"Team2_member_id": ctx.message.author.id},{"$set":{"Now_batting": ctx.message.author.id}})
						if x["Team2_name"]=="None":
							await ctx.send("Team 2 will be batting first")
						else:
							await ctx.send(f"**{x['Team2_name']}** will be batting first\nChoose players using `c!sp`")
					else:
						db_collection.update_one({"Team2_member_id": ctx.message.author.id},{"$set":{"Now_batting": x["Team1_member_id"]}})
						if x["Team1_name"]=="None":
							await ctx.send("Team 1 will be batting first")
						else:
							await ctx.send(f"**{x['Team1_name']}** will be batting first\nChoose players using `c!sp`")
		else:
			if x["Now_batting"]!=0:
				return
			if x["Score_card"]["Toss"]==0:
				await ctx.send("Make sure you do the toss before choosing")
				return
			if x["Score_card"]["Toss"]!=ctx.message.author.id:
				await ctx.send("Looks like you didn't win the toss")
				return
			else:
				if choice.lower()=="bat":
					db_collection.update_one({"Team1_member_id": ctx.message.author.id},{"$set":{"Now_batting": ctx.message.author.id}})
					if x["Team1_name"]=="None":
						await ctx.send("Team 1 will be batting first")
					else:
						await ctx.send(f"**{x['Team1_name']}** will be batting first\nChoose players using `c!sp`")
				else:
					db_collection.update_one({"Team1_member_id": ctx.message.author.id},{"$set":{"Now_batting": x["Team2_member_id"]}})
					if x["Team2_name"]=="None":
						await ctx.send("Team 2 will be batting first")
					else:
						await ctx.send(f"**{x['Team2_name']}** will be batting first\nChoose players using `c!sp`")
def setup(bot):
	bot.add_cog(choose(bot))
