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
class rich(commands.Cog):
	def __init__(self,bot):
        	self.bot=bot
	@commands.command()
	@commands.guild_only()
	async def rich(self,ctx,m=None):
		if m==None or m.lower() not in ["server","global"]:
			m="server"
		x=db2_collection.find().sort("Credits",-1)
		top_players=[]
		if m.lower()=="server":
			for j in x:
				if len(top_players)==5:
					break
				for i in ctx.message.guild.members:
					if i.id==j["id"]:
						string="**"+i.name+"#"+str(i.discriminator)+"**\n"+"**Wallet: ** "+str("{:,.0f} cc".format(j["Credits"]))+"\n"
						top_players.append(string)
						break
			p=""
			for i in range(len(top_players)):
				p+=str(i+1)+". "+top_players[i]+"\n"	
			embed=discord.Embed(title="Richest players of server",description=p)
			await ctx.send(embed=embed)
		elif m.lower()=="global":
			for j in x:
				if len(top_players)==5:
					break
				
				l=None
				for i in self.bot.guilds:
					l=i.get_member(j["id"])
					if l!=None:
						break
				if l==None:
					pass
				else:
					string="**"+l.name+"#"+str(l.discriminator)+"**\n"+"**Wallet: ** "+str("{:,.0f} cc".format(j["Credits"]))+"\n"
					top_players.append(string)
			p=""
			for i in range(len(top_players)):
				p+=str(i+1)+". "+top_players[i]+"\n"	
			embed=discord.Embed(title="Richest players of discord",description=p)
			await ctx.send(embed=embed)
def setup(bot):
	bot.add_cog(rich(bot))
