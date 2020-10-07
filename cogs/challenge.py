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
class challenge(commands.Cog):
	def __init__(self,bot):
        	self.bot=bot
	@commands.command(aliases=["duel"])
	@commands.guild_only()
	async def challenge(self,ctx,Team2:discord.Member=None):
		if Team2==None:
			await ctx.send("Syntax `c!challenge <@mention>`")
			return
		Team1_id=ctx.message.author.id
		Team2_id=Team2.id
		if Team2.bot==True:
			await ctx.send("Tag a human not a bot")
			return
		if Team2.id==Team1_id:
			await ctx.send("Dont tag urself")
			return
		h=db2_collection.find_one({"id":Team2.id})
		h1=db2_collection.find_one({"id":ctx.message.author.id})
		if h1==None or h==None:
			if h1==None:
				await ctx.send("You need to have an account to challenge a person\nType `c!register` to create an account.")
				return
			else:
				await ctx.send(f"{Team2.mention} doesn't have an account\nType `c!register` to create an account.")
				return
		x=db1_collection.find_one()
		if x==None:
			pass
		elif ctx.message.author.id in x["ids"] or Team2_id in x["ids"]:
			
			if ctx.message.author.id in x["ids"]:
				h=db2_collection.find_one({"id":ctx.message.author.id})
				original_name=ctx.author.name
				await ctx.send(f"**{original_name}** finish your undone match with **{h['now_match']}** or type `c!end` to end the match.")
				return
			if Team2_id in x["ids"]:
				h=db2_collection.find_one({"id":Team2.id})
				original_name=Team2.name
				await ctx.send(f"**{original_name}** finish your undone match with **{h['now_match']}** or type `c!end` to end the match.")
				return
		x=db_collection.find_one({"Team1_member_id": Team1_id})
		if x==None:
			x=db_collection.find_one({"Team1_member_id": Team2_id})
			if x==None:
				pass
			else:
				if x["status"]==0:
					await ctx.send("They have challenged a person, please wait for some time")
					return
		else:
			if x["status"]==0:
				await ctx.send("They have challenged a person, please wait for some time")
				return
		outline={
		"league" : "None",
			"Team1_name": "None",
			"Team2_name": "None",
			"Team1_member_id": Team1_id,
			"Team2_member_id": Team2_id,
		"status": 0,
		"Maximum_overs":0,
		"Now_batting": 0,
		"Team1_data":{
		"Lineup":[],
		"Batting": {},
		"Bowling": {},
			"Current_batting": [],
			"Current_bowling": [],
			"Previous_bowler": [],
		"Batsmen_out": []
		},
		"Team2_data":{
		"Lineup":[],
		"Batting": {},
		"Bowling": {},
			"Current_batting": [],
			"Current_bowling": [],
			"Previous_bowler": [],
		"Batsmen_out": []
		},
		"Score_card": {
				"Target": 0,
				"Overs": "0.0",
				"Maximum_overs": "0.0",
				"Last_ball": "0",
				"Score": 0,
				"Wickets": 0,
				"Toss": 0,
				"First_innings_score": [] 
			} ,
		"This_over": "",
		"Maximum_wickets": 10
		}
		db_collection.insert_one(outline)
		await ctx.send(f"{Team2.mention} , **{ctx.message.author.name}** has challenged you!\nType `c!accept` to accept the challenge or `c!decline` to decilne the challenge.")
		await asyncio.sleep(30)
		x=db_collection.find_one({"Team1_member_id": Team1_id})
		if x==None:
			x=db_collection.find_one({"Team1_member_id": Team2_id})
			if x==None:
				return
			else:
				if x["status"]!=0:
					return
				db_collection.delete_one({"Team2_member_id": Team1_id})
				await ctx.send("`Repsonse Error: The opponent failed to respond`")
				return
		else:
			print(x["status"])
			if x["status"]!=0:
				return
			db_collection.delete_one({"Team2_member_id": Team2_id})
			await ctx.send("`Repsonse Error: The opponent failed to respond`")
			return
def setup(bot):
	bot.add_cog(challenge(bot))
