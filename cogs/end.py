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
class end(commands.Cog):
	def __init__(self,bot):
        	self.bot=bot
	@commands.command()
	@commands.guild_only()
	async def end(self,ctx):
		x=db_collection.find_one({"Team1_member_id": ctx.message.author.id})
		try:
			if x==None:
				x=db_collection.find_one({"Team2_member_id": ctx.message.author.id})
				if x==None:
					await ctx.send("No matches are running")
					return
				else:
					temp=ctx.message.guild.get_member(x["Team1_member_id"])
					if temp==None:
						await ctx.send("Looks like your opponent isn't in this server, try using the command in a different server")
						return
					team1_member=None
					for i in self.bot.guilds:
						for j in i.members:
							if x["Team1_member_id"]==j.id:
								team1_member=j
								break
						if team1_member!=None:
							break
					team2_member=ctx.message.author
					if team1_member==None:
						team1_member.id=x["Team1_member_id"]
						h=db2_collection.find_one({"id":team1_member.id})
						h1=db2_collection.find_one({"id":team2_member.id})
						embed=discord.Embed(title="Request to abandon match",description=f"**{team2_member.name}** has requested to abandon the match between **{h['now_match']}** and **{h1['now_match']}**\nPlease react with ☑️ to abandon match and ❌ to deny the request.")
						embed.set_footer(text=f"Match gets abandoned when {h1['now_match']} reacts with ☑️.")
						m=await ctx.send(embed=embed)
						await m.add_reaction("☑️")
						await m.add_reaction("❌")				
					else:
						
						h=db2_collection.find_one({"id":team1_member.id})
						h1=db2_collection.find_one({"id":team2_member.id})
						embed=discord.Embed(title="Request to abandon match",description=f"**{team2_member.name}** has requested to abandon the match between **{h['now_match']}** and **{h1['now_match']}**\nPlease react with ☑️ to abandon match and ❌ to deny the request.")
						embed.set_footer(text=f"Match gets abandoned when {h1['now_match']} reacts with ☑️.")
						m=await ctx.send(embed=embed)
						await m.add_reaction("☑️")
						await m.add_reaction("❌")
					team1_member_id=team2_member.id
					team2_member_id=team1_member.id
			else:
				temp=ctx.message.guild.get_member(x["Team2_member_id"])
				if temp==None:
					await ctx.send("Looks like your opponent isn't in this server, try using the command in a different server")
					return
				team2_member=None
				for i in self.bot.guilds:
					for j in i.members:
						if x["Team2_member_id"]==j.id:
							team2_member=j
							break
					if team2_member!=None:
						break
				team1_member=ctx.message.author
				if team2_member==None:
					team2_member.id=x["Team2_member_id"]
					h=db2_collection.find_one({"id":team1_member.id})
					h1=db2_collection.find_one({"id":team2_member.id})
					embed=discord.Embed(title="Request to abandon match",description=f"{team1_member.name} has requested to abandon the match between **{h['now_match']}** and **{h1['now_match']}**\nPlease react with ☑️ to abandon match and ❌ to deny the request.")
					embed.set_footer(text=f"Match gets abandoned when {h['now_match']} reacts with ☑️.")
					m=await ctx.send(embed=embed)
					await m.add_reaction("☑️")
					await m.add_reaction("❌")
				
				else:
					h=db2_collection.find_one({"id":team1_member.id})
					h1=db2_collection.find_one({"id":team2_member.id})
					embed=discord.Embed(title="Request to abandon match",description=f"{team1_member.name} has requested to abandon the match between **{h['now_match']}** and **{h1['now_match']}**\nPlease react with ☑️ to abandon match and ❌ to deny the request.")
					embed.set_footer(text=f"Match gets abandoned when {h['now_match']} reacts with ☑️.")
					m=await ctx.send(embed=embed)
					await m.add_reaction("☑️")
					await m.add_reaction("❌")
				team1_member_id=team1_member.id
				team2_member_id=team2_member.id
			def check(reaction,user):
				return (m.id == reaction.message.id and (user.id == team2_member_id and (reaction.emoji=="☑️" or reaction.emoji=="❌")))
			try:
				reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=check)
			except asyncio.TimeoutError:
				o = await ctx.channel.fetch_message(m.id)
				embed=discord.Embed(title="Response Time error",description="Reaction not added.\nMatch has been abandoned due to inactiveness.")
				db2_collection.update_one({"id": team2_member_id},{"$set":{"now_match" :""}})
				db2_collection.update_one({"id": team1_member_id},{"$set":{"now_match" :""}})
				xy=db1_collection.find_one()
				xy["ids"].pop(xy["ids"].index(team1_member_id))
				xy["ids"].pop(xy["ids"].index(team2_member_id))
				db1_collection.update_one({},{"$set":{"ids":xy["ids"]}})
				x=db_collection.find_one({"Team1_member_id": team1_member_id})
				if x==None:
					x=db_collection.find_one({"Team1_member_id": team2_member_id})
					if x==None:
						return
					else:
						db_collection.delete_one({"Team1_member_id": team2_member_id})
				else:
					db_collection.delete_one({"Team1_member_id": team1_member_id})
				embed=discord.Embed(title="Response Time error",description="Reaction not added.\nMatch has been abandoned due to inactiveness.")
				await o.edit(embed=embed)
				await o.clear_reactions()
			else:
				o = await ctx.channel.fetch_message(m.id)
				if reaction.emoji=="☑️":
					db2_collection.update_one({"id": team2_member_id},{"$set":{"now_match" :""}})
					db2_collection.update_one({"id": team1_member_id},{"$set":{"now_match" :""}})
					xy=db1_collection.find_one()
					xy["ids"].pop(xy["ids"].index(team1_member_id))
					xy["ids"].pop(xy["ids"].index(team2_member_id))
					db1_collection.update_one({},{"$set":{"ids":xy["ids"]}})
					x=db_collection.find_one({"Team1_member_id": team1_member_id})
					if x==None:
						x=db_collection.find_one({"Team1_member_id": team2_member_id})
						if x==None:
							return
						else:
							db_collection.delete_one({"Team1_member_id": team2_member_id})
					else:
						db_collection.delete_one({"Team1_member_id": team1_member_id})
					embed=discord.Embed(title="Match has been abandoned")
					await o.clear_reactions()
					await o.edit(embed=embed)
				elif reaction.emoji=="❌":
					embed=discord.Embed(title="Request declined",desription="Request to end the match has been declined.")
					await o.clear_reactions()
					await o.edit(embed=embed)
		except:
			pass	
			

def setup(bot):
	bot.add_cog(end(bot))
