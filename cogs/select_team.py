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
class select_team(commands.Cog):
	def __init__(self,bot):
        	self.bot=bot
	@commands.command(aliases=["st","ct"])
	@commands.guild_only()
	async def select_team(self,ctx,number1=None,number=None):
		t=db1_collection.find_one()
		if ctx.message.author.id not in t["ids"]:
			return
		arr = ["IPL","BBL","CPL","PSL","Vitality Blast"]
		if number1==None:
			await ctx.send("Syntax : `c!select_team <league_id> <team_id>`")
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
		
		with open ("./Teams/"+team+".json") as f:
			d=json.load(f)
		available_teams=[]
		for i in d:
			available_teams.append(i)
		team_list=""
		for i in range(len(available_teams)):
			team_list+=str(i+1)+". "+available_teams[i]+"\n"
		if number==None:
			embed=discord.Embed(title="Teams",description=team_list)
			embed.set_footer(text=f"To select a team use `c!select_team {number1+1} <team_id>`")
			await ctx.send(embed=embed)
			await ctx.send(f"Now select your team, `c!st {number1+1} <team_id>`")
		else:
			try:
				number=int(number)-1
			except:
				return
			x=db_collection.find_one({"Team1_member_id": ctx.message.author.id})
			if x==None:
				x=db_collection.find_one({"Team2_member_id": ctx.message.author.id})
				if x==None:
					return
				else:
					if x["league"]=="None":
						db_collection.update_one({"Team2_member_id": ctx.message.author.id},{"$set":{"league": team}})
					
					if x["Team2_name"]!="None":
						await ctx.send("Can't change your team once after u chose it")
						return
					if (x["Team1_name"]!="None" and x["Team1_name"]==available_teams[number]) or (x["Team1_name"]!="None" and team!=x["league"]):
						if (x["Team1_name"]!="None" and x["Team1_name"]==available_teams[number]):
							await ctx.send(f"The other player already chose {available_teams[number]}\nChoose an other team {ctx.author.mention}")
							return
						else:
							await ctx.send(f"Choose a team from same league {ctx.author.mention}, **{team.title()}**")
							return
					x["Team2_name"]=available_teams[number]
					player_list=""
					bench_list=""
					for i in range(len(d[available_teams[number]][:11])):
						player_list+=str(i+1)+". "+d[available_teams[number]][:11][i]+"\n"
					for i in range(len(d[available_teams[number]][11:])):
						bench_list+=str(i+12)+". "+d[available_teams[number]][11:][i]+"\n"
					embed=discord.Embed(title="Your team",description="You can swap your players using `c!swap` command.")
					embed.add_field(name="Playing XI",value=player_list,inline=True)
					embed.add_field(name="Bench players",value=bench_list,inline=True)
					await ctx.send(content=f"**{available_teams[number]}** selected\n`Here's the team`",embed=embed)
					
					db_collection.update_one({"Team2_member_id": ctx.message.author.id},{"$set":{"Team2_name":available_teams[number]}})
					if x["Team2_name"]!="None" and x["Team1_name"]!="None":
						await ctx.send("Select team using `c!ct` command.`")
						return
			else:
				
				if x["league"]=="None":
					db_collection.update_one({"Team1_member_id": ctx.message.author.id},{"$set":{"league": team}})
				if x["Team1_name"]!="None":
					await ctx.send("Can't change your team once after u chose it")
					return
				if (x["Team2_name"]!="None" and x["Team2_name"]==available_teams[number]) or (x["Team2_name"]!="None" and team!=x["league"]):
					if (x["Team2_name"]!="None" and x["Team2_name"]==available_teams[number]):
						await ctx.send(f"The other player already chose {available_teams[number]}\nChoose an other team {ctx.author.mention}")
						return
					else:
						await ctx.send(f"Choose a team from same league {ctx.author.mention}, **{team.title()}**")
						return
				x["Team1_name"]=available_teams[number]
				player_list=""
				bench_list=""
				for i in range(len(d[available_teams[number]][:11])):
					player_list+=str(i+1)+". "+d[available_teams[number]][:11][i]+"\n"
				for i in range(len(d[available_teams[number]][11:])):
					bench_list+=str(i+12)+". "+d[available_teams[number]][11:][i]+"\n"
				embed=discord.Embed(title="Your team",description="You can swap your players using `c!swap` command.")
				embed.add_field(name="Playing XI",value=player_list,inline=True)
				embed.add_field(name="Bench players",value=bench_list,inline=True)
				await ctx.send(content=f"**{available_teams[number]}** selected\n`Here's the team`",embed=embed)
				
				db_collection.update_one({"Team1_member_id": ctx.message.author.id},{"$set":{"Team1_name":available_teams[number]}})
				if x["Team2_name"]!="None" and x["Team1_name"]!="None":
					await ctx.send("Select team using `c!ct` command.`")
					return

def setup(bot):
	bot.add_cog(select_team(bot))
