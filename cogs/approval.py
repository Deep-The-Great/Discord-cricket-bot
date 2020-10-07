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


class approval(commands.Cog):
	def __init__(self,bot):
        	self.bot=bot
	@commands.command()
	@commands.guild_only()
	async def accept(self,ctx):
		Team2=ctx.message.author
		Team2_id=ctx.message.author.id
		h1=db2_collection.find_one({"id":ctx.message.author.id})
		if h1==None:
			await ctx.send("You need an account to accept a challenge\nType `c!register` to create an account.")
			return
		x=db1_collection.find_one()
		if x==None:
			pass
		elif ctx.message.author.id in x["ids"]:
			h=db2_collection.find_one({"id":ctx.message.author.id})
			if h==None:
				pass
			else:
				await ctx.send(f"**{Team2.name}** finish your undone match with **{h['now_match']}** or type `c!end` to end the match.")
				return
		x=db_collection.find_one({"Team1_member_id": Team2_id})
		if x==None:
			x=db_collection.find_one({"Team2_member_id": Team2_id})
			if x==None:
				return
			else:
				if x["status"]==0:
					player1=ctx.message.guild.get_member(x["Team2_member_id"])
					player2=ctx.message.guild.get_member(x["Team1_member_id"])
					if player1==None or player2==None:
						await ctx.send("Select Teams by typing `c!select_team`.")	
					else:
						await ctx.send(f"Duel between **{player1.name}** and **{player2.name}** has started.\nCheck the available leagues by `c!leagues`.")
					db_collection.update_one({"Team2_member_id": Team2_id},{"$set":{"status": 1}})
				else:
					return
		else:
			return
		o=db1_collection.find_one()
		player1=ctx.message.guild.get_member(x["Team1_member_id"])
		player2=ctx.message.guild.get_member(x["Team2_member_id"])
		if player1==None:
			pass
		else:
			name=player2.name+"#"+str(player2.discriminator)
			db2_collection.update_one({"id":x["Team1_member_id"]},{"$set":{"now_match": name}})
		if player2==None:
			pass
		else:
			name=player1.name+"#"+str(player1.discriminator)
			db2_collection.update_one({"id":x["Team2_member_id"]},{"$set":{"now_match": name}})
		o["ids"].append(x["Team1_member_id"])
		o["ids"].append(x["Team2_member_id"])
		db1_collection.update_one({},{"$set":{"ids":o["ids"]}})
	@commands.command(aliases=["deny"])
	@commands.guild_only()
	async def decline(self,ctx):
		Team2_id=ctx.message.author.id
		h1=db2_collection.find_one({"id":ctx.message.author.id})
		if h1==None:
			await ctx.send("You need an account to decline a challenge\nType `c!register` to create an account.")
			return
		x=db_collection.find_one({"Team1_member_id": Team2_id})
		if x==None:
			x=db_collection.find_one({"Team2_member_id": Team2_id})
			if x==None:
				return
			else:
				if x["status"]==0:
					player1=ctx.message.guild.get_member(x["Team2_member_id"])
					player2=ctx.message.guild.get_member(x["Team1_member_id"])
					if player1==None or player2==None:
						await ctx.send(f"{player2.mention}, your challenge has been declined.")	
					else:
						await ctx.send(f"{player2.mention}, **{player1.name}** has declined your challenge.")
					db_collection.delete_one({"Team2_member_id": Team2_id})
				else:
					return
		else:
			return
def setup(bot):
	bot.add_cog(approval(bot))
