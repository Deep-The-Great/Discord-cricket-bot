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

class select_player(commands.Cog):
	def __init__(self,bot):
        	self.bot=bot
	@commands.command(aliases=["sp"])
	@commands.guild_only()
	async def select_player(self,ctx,number=None,number1=None):
		x=db_collection.find_one({"Team1_member_id": ctx.message.author.id})
		if x==None:
			
			x=db_collection.find_one({"Team2_member_id": ctx.message.author.id})
			if x==None:
				await ctx.send("Type `c!help` to know about how to use the bot!")
				return
			else:
				if x["Now_batting"]==0:
					await ctx.send("Type `c!help` to know about how to use the bot!")
					return
				if x["Team2_name"]=="None":
					await ctx.send("Looks like you didn't choose a team!\nType `c!select_team` to choose a team")

				else:
					if number==None:
						if x["Now_batting"]==x["Team2_member_id"]:
							team_list=""
							for i in range(len(x["Team2_data"]["Lineup"])):
								if x["Team2_data"]["Lineup"][i] in x["Team2_data"]["Batsmen_out"]:
									team_list+=str(i+1)+". ~~"+x["Team2_data"]["Lineup"][i]+"~~(out)\n"
								elif x["Team2_data"]["Lineup"][i] in x["Team2_data"]["Current_batting"]:
									team_list+=str(i+1)+". **"+x["Team2_data"]["Lineup"][i]+"**\n"
								else:
									team_list+=str(i+1)+". "+x["Team2_data"]["Lineup"][i]+"\n"
								embed=discord.Embed(title=f"{x['Team2_name']}",description=f"{team_list}")
								if len(x["Team2_data"]["Current_batting"])==0:
									embed.set_footer(text="Type `c!select_player <number1> <number2>` to choose opening batsmen")
								else:
									embed.set_footer(text="Type `c!select_player <number>` to choose batsmen")

						else:
							team_list=""
							max_balls=int(math.ceil(x["Maximum_overs"]/5))*6
							for i in range(len(x["Team2_data"]["Lineup"])):
								if x["Team2_data"]["Lineup"][i] in x["Team2_data"]["Previous_bowler"]:
									team_list+=str(i+1)+". ~~"+x["Team2_data"]["Lineup"][i]+"~~(last over)\n"
									continue
								if x["Team2_data"]["Lineup"][i] in x["Team2_data"]["Current_bowling"]:
									team_list+=str(i+1)+". **"+x["Team2_data"]["Lineup"][i]+"**\n"
									continue
								else:							
									if len(list(x["Team2_data"]["Bowling"].keys()))==0:
										pass
									else:
										if x["Team2_data"]["Lineup"][i] in x["Team2_data"]["Bowling"]:
											if x["Team2_data"]["Bowling"][x["Team2_data"]["Lineup"][i]]["balls_thrown"]==max_balls:
												team_list+=str(i+1)+". ~~"+x["Team2_data"]["Lineup"][i]+"~~(quota over)\n"
												continue
											else:
												pass
										else:
											pass
								team_list+=str(i+1)+". "+x["Team2_data"]["Lineup"][i]+"\n"
							embed=discord.Embed(title=f"{x['Team2_name']}",description=f"{team_list}")
							embed.set_footer(text="Type `c!select_player <number>` to choose bowler")
						await ctx.send(embed=embed)
					else:
						try:
							number=int(number)-1
							if number1==None:
								pass
							else:
								number1=int(number1)-1
						except:
							return
						if x["Now_batting"]==x["Team2_member_id"]:
							if number>10:
								await ctx.send("Choose a number less than 11")
								return
							if number1!=None:
								if number1>10:
									await ctx.send("Choose a number less than 11")
									return

							if len(x["Team2_data"]["Current_batting"])==0:
								if number1==None:
									await ctx.send("Syntax: `c!select_player <number1> <number2>`")
									return
								if number1==number:
									await ctx.send("Enter two different numbers")
									return
								data={x["Team2_data"]["Lineup"][number]:{
									"runs":0,
									"balls_faced":0},x["Team2_data"]["Lineup"][number1]:{
									"runs":0,
									"balls_faced":0}}
								for i in data:
									x["Team2_data"]["Batting"][i]=data[i]
								db_collection.update_one({"Team2_member_id": ctx.message.author.id},{"$set":{"Team2_data.Current_batting":[x["Team2_data"]["Lineup"][number],x["Team2_data"]["Lineup"][number1]],"Team2_data.Batting": x["Team2_data"]["Batting"]}})
								await ctx.send(f"{x['Team2_data']['Lineup'][number]} and {x['Team2_data']['Lineup'][number1]} have been sent to the crease")
							elif len(x["Team2_data"]["Current_batting"])==1:
								if x["Team2_data"]["Lineup"][number] in x["Team2_data"]["Current_batting"]:
									await ctx.send("He is already on the ground")
									return
								elif x["Team2_data"]["Lineup"][number] in x["Team2_data"]["Batsmen_out"]:
									await ctx.send("He got out already")
									return
								else:
									data={x["Team2_data"]["Lineup"][number]:{
									"runs":0,
									"balls_faced":0
									}}
									for i in data:
										x["Team2_data"]["Batting"][i]=data[i]
									x["Team2_data"]["Current_batting"].insert(0,x["Team2_data"]["Lineup"][number])
									db_collection.update_one({"Team2_member_id": ctx.message.author.id},{"$set":{"Team2_data.Current_batting": x["Team2_data"]["Current_batting"],"Team2_data.Batting": x["Team2_data"]["Batting"]}})
									await ctx.send(f"{x['Team2_data']['Lineup'][number]} has been sent to the crease")
							else:
								await ctx.send("No wicket has fallen yet")
								return
						else:
							if len(x["Team2_data"]["Current_bowling"])==1:
								await ctx.send("Over hasnt completed yet")
								return
							else:
								if number>10:
									await ctx.send("Choose a number less than 11")
									return
								if x["Team2_data"]["Lineup"][number] in x["Team2_data"]["Bowling"]:
									max_balls=int(math.ceil(x["Maximum_overs"]/5))*6
									if x["Team2_data"]["Bowling"][x["Team2_data"]["Lineup"][number]]["balls_thrown"]==max_balls:
										await ctx.send("This bowler has already completed his quota")
									elif x["Team2_data"]["Lineup"][number] in x["Team2_data"]["Previous_bowler"]:
										await ctx.send("A bowler cannot bowl 2 consecutive overs, choose someone else")
									else:
										db_collection.update_one({"Team2_member_id": ctx.message.author.id},{"$set":{"Team2_data.Current_bowling": [x["Team2_data"]["Lineup"][number]]}})
										number_of_overs=x["Score_card"]["Overs"].split(".")
										number_of_overs=int(number_of_overs[0])+1
										if number_of_overs==1:
											await ctx.send(f"{x['Team2_data']['Lineup'][number]} will bowl the {number_of_overs}st over")
										elif number_of_overs==2:
											await ctx.send(f"{x['Team2_data']['Lineup'][number]} will bowl the {number_of_overs}nd over")
										elif number_of_overs==3:
											await ctx.send(f"{x['Team2_data']['Lineup'][number]} will bowl the {number_of_overs}rd over")
										else:
											await ctx.send(f"{x['Team2_data']['Lineup'][number]} will bowl the {number_of_overs}th over")

								else:
									data={x["Team2_data"]["Lineup"][number]:{
											"runs": 0,
											"balls_thrown": 0,
											"wickets": 0
										}}
									for i in data:
										x["Team2_data"]["Bowling"][i]=data[i]
									db_collection.update_one({"Team2_member_id": ctx.message.author.id},{"$set":{"Team2_data.Current_bowling": [x["Team2_data"]["Lineup"][number]],"Team2_data.Bowling": x["Team2_data"]["Bowling"]}})
									number_of_overs=x["Score_card"]["Overs"].split(".")
									number_of_overs=int(number_of_overs[0])+1
									if number_of_overs==1:
										await ctx.send(f"{x['Team2_data']['Lineup'][number]} will bowl the {number_of_overs}st over")
									elif number_of_overs==2:
										await ctx.send(f"{x['Team2_data']['Lineup'][number]} will bowl the {number_of_overs}nd over")
									elif number_of_overs==3:
										await ctx.send(f"{x['Team2_data']['Lineup'][number]} will bowl the {number_of_overs}rd over")
									else:
										await ctx.send(f"{x['Team2_data']['Lineup'][number]} will bowl the {number_of_overs}th over")
		else:

			if x["Now_batting"]==0:
				await ctx.send("Type `c!help` to know about how to use the bot!")
				return
			if x["Team1_name"]=="None":
				await ctx.send("Looks like you didn't choose a team!\nType `c!select_team` to choose a team")
			else:
				if number==None and number1==None:
					if x["Now_batting"]==x["Team1_member_id"]:
						team_list=""
						for i in range(len(x["Team1_data"]["Lineup"])):
							if x["Team1_data"]["Lineup"][i] in x["Team1_data"]["Batsmen_out"]:
								team_list+=str(i+1)+". ~~"+x["Team1_data"]["Lineup"][i]+"~~(out)\n"
							elif x["Team1_data"]["Lineup"][i] in x["Team1_data"]["Current_batting"]:
								team_list+=str(i+1)+". **"+x["Team1_data"]["Lineup"][i]+"**\n"
							else:
								team_list+=str(i+1)+". "+x["Team1_data"]["Lineup"][i]+"\n"

						embed=discord.Embed(title=f"{x['Team1_name']}",description=f"{team_list}")
						if len(x["Team1_data"]["Current_batting"])==0:
							embed.set_footer(text="Type `c!select_player <number1> <number2>` to choose opening batsmen")
						else:
							embed.set_footer(text="Type `c!select_player <number>` to choose batsmen")
					else:
						team_list=""
						max_balls=int(math.ceil(x["Maximum_overs"]/5))*6
						for i in range(len(x["Team1_data"]["Lineup"])):
							if x["Team1_data"]["Lineup"][i] in x["Team1_data"]["Previous_bowler"]:
								team_list+=str(i+1)+". ~~"+x["Team1_data"]["Lineup"][i]+"~~(last over)\n"
								continue
							if x["Team1_data"]["Lineup"][i] in x["Team1_data"]["Current_bowling"]:
								team_list+=str(i+1)+". **"+x["Team1_data"]["Lineup"][i]+"**\n"
								continue
							else:
								if len(list(x["Team1_data"]["Bowling"].keys()))==0:
									pass
								else:
									if x["Team1_data"]["Lineup"][i] in x["Team1_data"]["Bowling"]:
										if x["Team1_data"]["Bowling"][x["Team1_data"]["Lineup"][i]]["balls_thrown"]==max_balls:
											team_list+=str(i+1)+". ~~"+x["Team1_data"]["Lineup"][i]+"~~(quota over)\n"
											continue
										else:
											pass
									else:
										pass
							team_list+=str(i+1)+". "+x["Team1_data"]["Lineup"][i]+"\n"
						embed=discord.Embed(title=f"{x['Team1_name']}",description=f"{team_list}")
						embed.set_footer(text="Type `c!select_player <number>` to choose bowler")


					await ctx.send(embed=embed)
				else:
					try:
						number=int(number)-1
						if number1==None:
							pass
						else:
							number1=int(number1)-1
					except:
						return
					if x["Now_batting"]==x["Team1_member_id"]:
						if number>10:
							await ctx.send("Choose a number less than 11")
							return
						if number1!=None:
							if number1>10:
								await ctx.send("Choose a number less than 11")
								return
						if number1==number:
							await ctx.send("Enter two different numbers")
							return
						if len(x["Team1_data"]["Current_batting"])==0:
							if number1==None:
								await ctx.send("Syntax: `c!select_player <number1> <number2>`")
								return
							if number1==number:
								await ctx.send("Enter two different numbers")
								return
							data={x["Team1_data"]["Lineup"][number]:{
								"runs":0,
								"balls_faced":0
							},x["Team1_data"]["Lineup"][number1]:
							{
								"runs":0,
								"balls_faced":0
							}}
							for i in data:
								x["Team1_data"]["Batting"][i]=data[i]
							db_collection.update_one({"Team1_member_id": ctx.message.author.id},{"$set":{"Team1_data.Current_batting":[x["Team1_data"]["Lineup"][number],x["Team1_data"]["Lineup"][number1]],"Team1_data.Batting": x["Team1_data"]["Batting"]}})
							await ctx.send(f"{x['Team1_data']['Lineup'][number]} and {x['Team1_data']['Lineup'][number1]} have been sent to the crease")
						elif len(x["Team1_data"]["Current_batting"])==1:
							if x["Team1_data"]["Lineup"][number] in x["Team1_data"]["Current_batting"]:
								await ctx.send("He is already on the ground")
								return
							elif x["Team1_data"]["Lineup"][number] in x["Team1_data"]["Batsmen_out"]:
								await ctx.send("He got out already")
								return
							else:
								data={x["Team1_data"]["Lineup"][number]:{
								"runs":0,
								"balls_faced":0
								}}
								for i in data:
									x["Team1_data"]["Batting"][i]=data[i]
								x["Team1_data"]["Current_batting"].insert(0,x["Team1_data"]["Lineup"][number])
								db_collection.update_one({"Team1_member_id": ctx.message.author.id},{"$set":{"Team1_data.Current_batting": x["Team1_data"]["Current_batting"],"Team1_data.Batting": x["Team1_data"]["Batting"]}})
								await ctx.send(f"{x['Team1_data']['Lineup'][number]} has been sent to the crease")
						else:
							await ctx.send("No wicket has fallen yet")
							return
					else:

						if len(x["Team1_data"]["Current_bowling"])==1:
							await ctx.send("Over hasnt completed yet")
							return
						else:
							if number>10:
								await ctx.send("Choose a number less than 11")
								return
							if x["Team1_data"]["Lineup"][number] in x["Team1_data"]["Bowling"]:
								max_balls=int(math.ceil(x["Maximum_overs"]/5))*6
								if x["Team1_data"]["Bowling"][x["Team1_data"]["Lineup"][number]]["balls_thrown"]==max_balls:
									await ctx.send("This bowler has already completed his quota")
								elif x["Team1_data"]["Lineup"][number] in x["Team1_data"]["Previous_bowler"]:
									await ctx.send("A bowler cannot bowl 2 consecutive overs, choose someone else")
								else:
									db_collection.update_one({"Team1_member_id": ctx.message.author.id},{"$set":{"Team1_data.Current_bowling": [x["Team1_data"]["Lineup"][number]]}})
									number_of_overs=x["Score_card"]["Overs"].split(".")
									number_of_overs=int(number_of_overs[0])+1
									if number_of_overs==1:
										await ctx.send(f"{x['Team1_data']['Lineup'][number]} will bowl the {number_of_overs}st over")	
									elif number_of_overs==2:
										await ctx.send(f"{x['Team1_data']['Lineup'][number]} will bowl the {number_of_overs}nd over")
									elif number_of_overs==3:
										await ctx.send(f"{x['Team1_data']['Lineup'][number]} will bowl the {number_of_overs}rd over")
									else:
										await ctx.send(f"{x['Team1_data']['Lineup'][number]} will bowl the {number_of_overs}th over")
							else:
								data={x["Team1_data"]["Lineup"][number]:{
										"runs": 0,
										"balls_thrown": 0,
										"wickets": 0
									}}
								for i in data:
									x["Team1_data"]["Bowling"][i]=data[i]
								db_collection.update_one({"Team1_member_id": ctx.message.author.id},{"$set":{"Team1_data.Current_bowling": [x["Team1_data"]["Lineup"][number]],"Team1_data.Bowling": x["Team1_data"]["Bowling"]}})
								number_of_overs=x["Score_card"]["Overs"].split(".")
								number_of_overs=int(number_of_overs[0])+1
								if number_of_overs==1:
									await ctx.send(f"{x['Team1_data']['Lineup'][number]} will bowl the {number_of_overs}st over")
								elif number_of_overs==2:
									await ctx.send(f"{x['Team1_data']['Lineup'][number]} will bowl the {number_of_overs}nd over")
								elif number_of_overs==3:
									await ctx.send(f"{x['Team1_data']['Lineup'][number]} will bowl the {number_of_overs}rd over")
								else:
									await ctx.send(f"{x['Team1_data']['Lineup'][number]} will bowl the {number_of_overs}th over")

def setup(bot):
	bot.add_cog(select_player(bot))
