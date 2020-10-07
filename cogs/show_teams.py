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
class show_team(commands.Cog):
	def __init__(self,bot):
        	self.bot=bot
	@commands.command(aliases=["show_team","dt","teams"])
	@commands.guild_only()
	async def show_teams(self,ctx,number1=None):
		arr = os.listdir('./Teams')
		if number1==None:
			await ctx.send("Syntax : `c!show_team <league_id>`")
			return
		team=""
		try:
			number1=int(number1)-1
			if number1>len(arr):
				await ctx.send(f"Choose a number less than {len(arr)}")
				return
			else:
				team=arr[number1]
		except:
			return
		
		with open ("./Teams/"+team) as f:
			d=json.load(f)
		team=team[:-5]
		available_teams=[]
		for i in d:
			available_teams.append(i)
		team_list=""
		print(available_teams)
		for i in range(len(available_teams)):
			team_list+=str(i+1)+". "+available_teams[i]+"\n"
		
		embed=discord.Embed(title="Teams",description=team_list)
		embed.set_footer(text=f"To select a team use `c!select_team {number1+1} <team_id>`")
		await ctx.send(embed=embed)
def setup(bot):
	bot.add_cog(show_team(bot))
