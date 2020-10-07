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
class team(commands.Cog):
	def __init__(self,bot):
        	self.bot=bot
	@commands.command()
	@commands.guild_only()
	async def team(self,ctx,number=None):

		x=db_collection.find_one({"Team1_member_id":ctx.message.author.id})
		if x==None:
			x=db_collection.find_one({"Team2_member_id":ctx.message.author.id})
			if x==None:
				return
			if x["Team2_name"]=="None":
				return

			if len(x["Team2_data"]["Lineup"])==0:
				await ctx.send("Team can be viewed only after confirming your team using `c!ct`.")
				return
			player_list=""
			for i in range(len(x["Team2_data"]["Lineup"])):
				player_list+=str(i+1)+". "+x["Team2_data"]["Lineup"][i]+"\n"
			embed=discord.Embed(title=f"{x['Team2_name']} Playing XI",description=player_list)
			await ctx.send(embed=embed)
		else:
			if x["Team1_name"]=="None":
				return
			if len(x["Team1_data"]["Lineup"])==0:
				await ctx.send("Team can be viewed only after setting confirming your team using `c!ct`.")
				return
			player_list=""
			for i in range(len(x["Team1_data"]["Lineup"])):
				player_list+=str(i+1)+". "+x["Team1_data"]["Lineup"][i]+"\n"
			embed=discord.Embed(title=f"{x['Team1_name']} Playing XI",description=player_list)
			await ctx.send(embed=embed)
def setup(bot):
	bot.add_cog(team(bot))
