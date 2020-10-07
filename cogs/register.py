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
class register(commands.Cog):
	def __init__(self,bot):
        	self.bot=bot
	@commands.command(aliases=["start","register"])
	@commands.guild_only()
	async def create_account(self,ctx):
		h=db2_collection.find_one({"id":ctx.author.id})
		if h!=None:
			await ctx.send("Seems like you have an account already, type `c!profile` to check profile")
			return
		guild=0
		for i in self.bot.guilds:
			if i.id==723905142646243442:
				guild=i
				break
		if ctx.author not in guild.members:
			embed=discord.Embed(description="You need to be a member of the official server to create an account. Click [here](https://discord.gg/DayDsCV) to join the server ")
			await ctx.send(embed=embed)
			return
		data={
			"about": "I am a cricket lover!",
			"id": ctx.message.author.id,
			"matches_played": 0,
			"won": 0,
			"lost": 0,
			"highest_streak": 0,
			"current_streak": 0,
			"recent_results": [],
			"now_match": "",
			"winning_percentage": 0.00,
			"Credits": 1000
		}
		db2_collection.insert_one(data)
		await ctx.send("Account created successfully!\nType `c!profile` to check the profile")
		chnl=self.bot.get_channel(733542814453071974)
		await chnl.send(f"**{ctx.message.author.name}#{ctx.message.author.discriminator}**({ctx.message.author.id}) has created an account in **{ctx.message.guild.name}** server.")
def setup(bot):
	bot.add_cog(register(bot))
