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

class toss(commands.Cog):
	def __init__(self,bot):
        	self.bot=bot
	@commands.command(aliases=["t"])
	@commands.guild_only()
	async def toss(self,ctx,choice=None):
		caller=None
		#toss
		if choice==None:
			pass
		elif choice.title() not in ["Heads","Tails"]:
			await ctx.send("Syntax: `c!toss`")
			return
		x=db_collection.find_one({"Team1_member_id": ctx.message.author.id})
		if x==None:
			x=db_collection.find_one({"Team2_member_id": ctx.message.author.id})
			if x==None:
				pass
			else:
				if x["Maximum_overs"]==0:
					await ctx.send("Toss can be done only after setting overs")
					return
				caller=x["Team1_member_id"]

		else:
			if x["Maximum_overs"]==0:
				await ctx.send("Toss can be done only after setting overs")
				return
			caller=x["Team2_member_id"]
		if caller==None:
			caller=0
		outcomes=["Heads","Tails"]
		answer=random.choice(outcomes)
		embed=discord.Embed(title='Toss')
		embed.set_image(url="https://i.pinimg.com/originals/d7/49/06/d74906d39a1964e7d07555e7601b06ad.gif")
		mess=await ctx.send(embed=embed)
		def check(message):
			return	(message.author.id==caller and (message.content.title() in outcomes))
		try:
			msg = await self.bot.wait_for('message', timeout=7.0, check=check)
		except asyncio.TimeoutError:
			if x==None:
				embed=discord.Embed(title=f'Oh! Its a {answer}')
				await mess.edit(embed=embed)
				return
			if x["Score_card"]["Toss"]!=0:
				embed=discord.Embed(title=f'Oh! Its a {answer}')
				await mess.edit(embed=embed)
				return
			else:
				if choice!=None and x["Score_card"]["Toss"]==0:
					embed=discord.Embed(title=f'Oh! Its a {answer}')
					await mess.edit(embed=embed)
				else:
					embed=discord.Embed(title=f'Response error: No/wrong input given')
					await mess.edit(embed=embed)
					return
				
		else:
			await asyncio.sleep(2)			
			if choice==None:
				choice=msg.content.title()
			if x==None:
				embed=discord.Embed(title=f'Oh! Its a {answer}')
				await mess.edit(embed=embed)
				return
			if choice.title() not in ["Heads","Tails"]:
				embed=discord.Embed(title="Input error: `Invalid input given`")
				await mess.edit(embed=embed)	
				return
			if x["Score_card"]["Toss"]!=0:
				embed=discord.Embed(title=f'Oh! Its a {answer}')
				await mess.edit(embed=embed)
				return
			else:
				embed=discord.Embed(title=f'Oh! Its a {answer}')
				await mess.edit(embed=embed)
		x=db_collection.find_one({"Team1_member_id": ctx.message.author.id})
		if x==None:
			x=db_collection.find_one({"Team2_member_id": ctx.message.author.id})
			if x==None:
				return
			else:
				if x["Team1_member_id"]==ctx.message.author.id:
					caller=x["Team2_name"]
					tosser=x["Team1_name"]
				else:
					tosser=x["Team2_name"]
					caller=x["Team1_name"]
				if choice.title()==answer:
					x=db_collection.update_one({"Team2_member_id": ctx.message.author.id},{"$set":{"Score_card.Toss": x["Team1_member_id"]}})	
					await ctx.send(f"**{caller}** won the toss\n**Note:** Use `c!choose <bat/bowl>` to choose batting or bowling")
				else:
					x=db_collection.update_one({"Team2_member_id": ctx.message.author.id},{"$set":{"Score_card.Toss": x["Team2_member_id"]}})	
					await ctx.send(f"**{tosser}** won the toss\n**Note:** Use `c!choose <bat/bowl>` to choose batting or bowling")
		else:
			if x["Team1_member_id"]==ctx.message.author.id:
				caller=x["Team2_name"]
				tosser=x["Team1_name"]
			else:
				tosser=x["Team2_name"]
				caller=x["Team1_name"]
			if choice.title()==answer:
				x=db_collection.update_one({"Team1_member_id": ctx.message.author.id},{"$set":{"Score_card.Toss": x["Team2_member_id"]}})	
				await ctx.send(f"**{caller}** won the toss\n**Note:** Use `c!choose <bat/bowl>` to choose batting or bowling")
			else:
				x=db_collection.update_one({"Team1_member_id": ctx.message.author.id},{"$set":{"Score_card.Toss": x["Team1_member_id"]}})	
				await ctx.send(f"**{tosser}** won the toss\n**Note:** Use `c!choose <bat/bowl>` to choose batting or bowling")
def setup(bot):
	bot.add_cog(toss(bot))
