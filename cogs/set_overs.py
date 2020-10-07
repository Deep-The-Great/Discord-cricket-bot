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
db_name=db1_client["Challenge"]
db_collection=db_name['Data']
db1_name=db1_client['Running_matches']
db1_collection=db1_name['data']
db2_name=db_client["about"]
db2_collection=db2_name["data"]
class set_overs(commands.Cog):
	def __init__(self,bot):
        	self.bot=bot
	@commands.command(aliases=["so","setovers"])
	@commands.guild_only()
	async def set_overs(self,ctx,number=None):
	
		if number==None:
			await ctx.send("Syntax: `c!set_overs <number>`")
			return
		x=db_collection.find_one({"Team1_member_id":ctx.message.author.id})
		if x==None:
			x=db_collection.find_one({"Team2_member_id":ctx.message.author.id})
			if x==None:
				return
			else:
				
				if x["Maximum_overs"]!=0:
					await ctx.send("Can't change the overs once set")
					return
				if x["Team2_name"] =="None" or x["Team1_name"] =="None":
					await ctx.send("Overs can be set only after choosing teams")
					return
				if len(x["Team2_data"]["Lineup"])==0:
					await ctx.send("Looks like you didn't confirm your team, you can do it by typing `c!ct`.\nNow you can also swap players of your team by using `c!swap` command.")
					return
				try:
					number=int(number)		
					db_collection.update_one({"Team2_member_id": ctx.message.author.id},{"$set":{"Team1_data.Lineup": team1,"Team2_data.Lineup": team2,"Maximum_overs":number,"Score_card.Maximum_overs": str(number)+".0"}})
					await ctx.channel.send("Overs set successfully\nNow go for the toss. Syntax: `c!toss <opponent's call>`")
				except:
					await ctx.send("Syntax: `c!set_overs <number>`")
					return
		else:
			if x["Maximum_overs"]!=0:
				await ctx.send("Can't change the overs once set")
				return

			if x["Team2_name"]=="None" or x["Team1_name"]=="None":
				await ctx.send("Overs can be set only after choosing teams")
				return	
			if len(x["Team1_data"]["Lineup"])==0:
				await ctx.send("Looks like you didn't confirm your team, you can do it by typing `c!ct`.\nNow you can also swap players of your team by using `c!swap` command.")
				return
			try:
				number=int(number)		
				db_collection.update_one({"Team1_member_id": ctx.message.author.id},{"$set":{"Team1_data.Lineup": team1,"Team2_data.Lineup": team2,"Maximum_overs": number,"Score_card.Maximum_overs": str(number)+".0"}})
				await ctx.channel.send("Overs set successfully\nNow go for the toss. Syntax: `c!toss <opponent's call>`")
			except:

				await ctx.send("Syntax: `c!set_overs <number>`")
				return

def setup(bot):
	bot.add_cog(set_overs(bot))
