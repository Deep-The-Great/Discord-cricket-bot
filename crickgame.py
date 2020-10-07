import discord 
import random
from discord.ext import commands
import os
import datetime
import pymongo
import json
import math
import datetime
import asyncio
bot=commands.Bot(command_prefix='.')
bot.remove_command('help')
os.environ["BOT_TOKEN"]="NTkwNDQzMjk5NzM1NzMyMjI0.XQiTLA.lCZ7h8EEh8Hx1OAPQL_kS2fyq5M"
os.environ["DB_URL"]="mongodb+srv://Shrikar:shrikar123@cricket.u4p4f.mongodb.net/Cricket_bot_personal?retryWrites=true&w=majority"
os.environ["DB2_URL"]="mongodb+srv://Shrikar:shrikar123@personal-cricket.ychhm.mongodb.net/Challenge?retryWrites=true&w=majority"
db_client=pymongo.MongoClient(os.getenv("DB_URL"))
db1_client=pymongo.MongoClient(os.getenv("DB2_URL"))
db_name=db1_client["Challenge"]
db_collection=db_name['Data']
db1_name=db1_client['Running_matches']
db1_collection=db1_name['data']
db2_name=db_client["about"]
db2_collection=db2_name["data"]
db3_name=db1_client["banned_members"]
db3_collection=db3_name["ids"]
db4_name=db_client["Logs"]
db4_collection = db4_name["Channels"]
#loading cogs
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.{filename[:-3]}")
@bot.command()
@commands.guild_only()
async def confirm_team(ctx):
	with open('./cache/swap.json','r') as f,pymongo.MongoClient(os.getenv("DB2_URL")) as db1_client,pymongo.MongoClient(os.getenv("DB_URL")) as db_client:
		d=json.load(f)
		db_name=db1_client["Challenge"]
		db_collection=db_name['Data']
		db2_name=db_client["about"]
		db2_collection=db2_name["data"]
		x=db_collection.find_one({"Team1_member_id": ctx.message.author.id})
		if x==None:
			x=db_collection.find_one({"Team2_member_id": ctx.message.author.id})
			if x==None:
				return
			if len(x['Team2_data']['Lineup'])!=0:
				return
			else:
				team_name=x['Team2_name']
		else:
			if len(x['Team1_data']['Lineup'])!=0:
				return
			team_name=x['Team1_name']
	Note=""
	if str(x['_id']) not in d:
		with open ("./Teams/"+x['league']+".json","r") as f:
			team=json.load(f)
			team=team[team_name][:11]
	else:
		if str(ctx.author.id) not in d[str(x['_id'])]:
			with open ("./Teams/"+x['league']+".json","r") as f:
				team=json.load(f)
				team=team[team_name][:11]
		else:
			team=d[str(x['_id'])][str(ctx.author.id)]['now'][:11]
			y=db2_collection.find_one({"id": ctx.author.id})
			if y['Credits']<len(list(set(d[str(x['_id'])][str(ctx.author.id)]['now'][:11])-set(d[str(x['_id'])][str(ctx.author.id)]['default'][:11])))*500:
				await ctx.send("Your swapped team costs more many than you got.\nTry selecting the team again with less number of swaps.")
				d[str(x['_id'])][str(ctx.author.id)]['now']=d[str(x['_id'])][str(ctx.author.id)]['default']
				with open('./cache/swap.json','w') as f:
					json.dump(d,f)
				return
			else:
				bal=y['Credits']
				y['Credits']=y['Credits']-len(list(set(d[str(x['_id'])][str(ctx.author.id)]['now'][:11])-set(d[str(x['_id'])][str(ctx.author.id)]['default'][:11])))*500
				db2_collection.update_one({"id": ctx.author.id},{"$set":{"Credits":y['Credits']}})
				Note="**NOTE: "+str(bal-y['Credits'])+" have been spent for swapping.**\n"
	players=""+Note
	for i in range(len(team)):
		players+=str(i+1)+" ."+team[i]+"\n"
	embed=discord.Embed(title="Playing XI",description=players)
	await ctx.send(content="This is your playing eleven for this match.",embed=embed)
	if ctx.author.id == x['Team1_member_id']:
		db_collection.update_one({"_id":x['_id']},{"$set":{"Team1_data.Lineup": team}})
	else:
		db_collection.update_one({"_id":x['_id']},{"$set":{"Team2_data.Lineup": team}})
	
	
@bot.command()
@commands.guild_only()
async def swap_player(ctx,swap=None,swap_with=None):
#default --d_team
#current --d_now

	with open('./cache/swap.json','r') as f,pymongo.MongoClient(os.getenv("DB2_URL")) as db1_client:
		d=json.load(f)
		db_name=db1_client["Challenge"]
		db_collection=db_name['Data']
		x=db_collection.find_one({"Team1_member_id": ctx.message.author.id})
		if x==None:
			x=db_collection.find_one({"Team2_member_id": ctx.message.author.id})
			if x==None:
				return
			if x['Maximum_overs']!=0:
				await ctx.send("Can't change your lineup after setting overs.")
				return
			else:
				team_name=x['Team2_name']
		else:
			if x['Maximum_overs']!=0:
				await ctx.send("Can't change your lineup after setting overs.")
				return
			team_name=x['Team1_name']
	if str(x['_id']) not in d:
		with open ("./Teams/"+x['league']+".json","r") as f:
			d_details=json.load(f)
			d_team=d_details[team_name]
			d_now=d_team
			to_be_dumped={str(x['_id']):{}}
	else:
		d_team=d[str(x['_id'])][str(ctx.message.author.id)]['default']
		d_now=d[str(x['_id'])][str(ctx.message.author.id)]['now']
		to_be_dumped=d
	swap=int(swap)
	swap_with=int(swap_with)
	prompt=d_now[swap-1] + " swapped with " + d_now[swap_with-1]
	d_now[swap-1],d_now[swap_with-1]=d_now[swap_with-1],d_now[swap-1]
	playing_eleven=d_now[:11]
	bench=d_now[11:]
	creds=len(list(set(d_team[:11])-set(d_now[:11])))*200
	player_list=""
	bench_list=""
	for i in range(len(playing_eleven)):
		player_list+=str(i+1)+". "+playing_eleven[i]+"\n"
	for i in range(len(bench)):
		bench_list+=str(i+12)+". "+bench[i]+"\n"
	embed=discord.Embed(title=f"Team name",description="You can swap players by using `c!swap` command.")
	embed.add_field(name="Swap done",value=prompt,inline=False)
	embed.add_field(name="Playing XI",value=player_list,inline=True)
	embed.add_field(name="Bench players",value=bench_list,inline=True)
	embed.add_field(name="Credits",value=creds,inline=False)
	await ctx.send(embed=embed)
	to_be_dumped[str(x['_id'])][str(ctx.message.author.id)]={"default":d_team,"now":d_now}
	with open('./cache/swap.json','w') as f:
		json.dump(to_be_dumped,f)

@bot.command()
async def match(ctx,*,role=None):
	if role==None:
		await ctx.send("`.match role_name`")
		return
	l=[]
	for i in ctx.guild.members:
		for j in i.roles:
			if j.id==int(role):
				l.append(i.name)
				break
	if len(l)==0:
		await ctx.send("Role not found")
		return
	random.shuffle(l)
	k=[[]]
	p=0
	b=0
	countt=0
	for i in range(0,len(l),2):
		if p==15:
			b+=1
			p=0
			k.append([])
		match="`"+l[i]+"`\tvs\t`"+l[i+1]+"`"
		k[b].append(match)
		p+=1
		countt+=1
	embed=discord.Embed(title=f"PvP List\nNumber of matches : {countt}")
	for i in range(len(k[0])):
		embed.add_field(name=f"Match-{i+1}",value=k[0][i],inline=False)

	await ctx.send(embed=embed)
@bot.event
async def on_ready():
	print("Less go")
	k=0
	while (1):
		if k%2==0:
			global number_of_servers
			number_of_servers=len(bot.guilds)
			if number_of_servers==1:
				game = discord.Game(f"cricket in {number_of_servers} guild.")	
			else:
				game = discord.Game(f"cricket in {number_of_servers} guilds.")
			await bot.change_presence(status=None, activity=game)
		else:
			sizee=db2_collection.find()
			count=0
			for i in sizee:
				count+=1
			game = discord.Game(f"with {count} players.")
			await bot.change_presence(status=None, activity=game)
		k+=1
		await asyncio.sleep(10)
		
@bot.event
async def on_message(message):

	x=db3_collection.find_one()
	channel=message.channel
	if message.author.id in x["ids"] and message.content.startswith("c!"):
		await channel.send("You have been banned :muscle:.")
		return
	if message.author.id==732113054921130005 and message.channel.id==732581435353071688:
		content=message.content
		content=content.split("\n")
		if len(content)<2:
			await message.delete()
			embed=discord.Embed(title="A winner couldn't be determined.",description="Due to less number of participants, a winner couldn't be determined.")
			await message.channel.send(embed=embed)
			return
		member=None
		for i in bot.guilds:
			member=i.get_member(int(content[1]))
			if member!=None:
				break
		x=db2_collection.find_one({"id":int(content[1])})
		db2_collection.update_one({"id": x["id"]},{"$set":{"Credits": int(x["Credits"])+int(content[0])}})
		await message.delete()
		if member==None:
			member_name=content[1]
			member_discriminator=""
		else:
			member_name=member.name
			member_discriminator="#"+str(member.discriminator)
		embed=discord.Embed(title="Lottery notification",description=f"**Winner:** {member_name}{member_discriminator}\n**Prize:** {content[0]} cc")
		await message.channel.send(embed=embed)
		if member==None:
			return
		if member.dm_channel==None:
			await member.create_dm()
		channel=member.dm_channel
		await channel.send(f":tada: Congratulations {member.mention}, you have won the lottery. You have won **{content[0]} cc.:tada:**")
	'''if ((message.author.id!=442673891656335372 and message.author.id!=448127767184146432) and message.author!=bot.user ) and message.content.startswith("c!"):
		await channel.send("Updating bot, edt : 10min")
		return'''
	'''if message.guild.id==702193286810435604 and message.content.startswith("c!"):
		await channel.send("oops!, something went wrong")
		return'''
	if bot.user.mentioned_in(message) and message.mention_everyone is False:
		await channel.send("My prefix is `c!` To learn how to use the bot, use the `c!help` command.")
	await bot.process_commands(message)
	
@bot.command(aliases=["p"])
@commands.guild_only()
async def participate(ctx):
	if ctx.message.channel.id!=739112206028767265:
		return
	else:
		for i in ctx.author.roles:
			if i.id==739113180059533373:
				await ctx.send("Looks like you have registered already")
				return
		for i in ctx.message.guild.roles:
			if i.id==739113180059533373:
				break
		await ctx.author.add_roles(i)
		await ctx.send("Registration successfull")
	
@bot.command()
@commands.guild_only()
async def log(ctx,chnl:discord.TextChannel=None):
	if chnl==None:
		await ctx.send("`Synatx: c!log <#channel>`")
		return
	if ctx.message.author.guild_permissions.manage_channels:
		pass
	else:
		return
	x=db4_collection.find_one()
	
	if str(ctx.message.guild.id) in x["ids"]:
		prv_chnl_id=int(x["ids"][str(ctx.message.guild.id)][0])
		x["ids"][str(ctx.message.guild.id)][0]=chnl.id
		db4_collection.update_one({},{"$set":{"ids": x["ids"]}})
		prv_chnl=bot.get_channel(prv_chnl_id)
		if prv_chnl==None or prv_chnl_id==chnl.id:
			await ctx.send(f"The match logs will be sent to {chnl.mention}")
			return
		else:
			await ctx.send(f"The logs channel has been changed from {prv_chnl.mention}, to {chnl.mention}")
	else:
		x["ids"][str(ctx.message.guild.id)]=[]
		x["ids"][str(ctx.message.guild.id)].append(chnl.id)
		x["ids"][str(ctx.message.guild.id)].append(0)
		db4_collection.update_one({},{"$set":{"ids": x["ids"]}})
		await ctx.send(f"The match logs will be sent to {chnl.mention}")
		return
@bot.command()
@commands.guild_only()
async def ban(ctx,person:discord.Member=None):
	ids=[442673891656335372,492711291836956678]
	if ctx.message.author.id not in ids:
		return
	else:
		if person==None:
			return
		else:
			if person.bot==True:
				await ctx.send("Can't ban a bot")
				return
			if person.id in ids:
				await ctx.send("Can't ban the owners sorry.")
				return
			x=db3_collection.find_one()
			x["ids"].append(person.id)
			db3_collection.update_one({},{"$set":{"ids": x["ids"]}})
			await ctx.send(f"{person.mention} banned successfully")

@bot.command()
@commands.guild_only()
async def unban(ctx,person:discord.Member=None):
	ids=[442673891656335372,492711291836956678]
	if ctx.message.author.id not in ids:
		return
	else:
		if person==None:
			await ctx.send("Mention a user")
			return
		else:
			if person.bot==True:
				return
			
			x=db3_collection.find_one()
			if person.id not in x["ids"]:
				await ctx.send("Looks like they aren't banned")
				return
			x["ids"].pop(x["ids"].index(person.id))
			db3_collection.update_one({},{"$set":{"ids": x["ids"]}})
			await ctx.send(f"{person.mention} unbanned successfully")
@bot.command()
@commands.guild_only()
async def give(ctx,person:discord.Member=None,amt=None):
	ids=[492711291836956678,442673891656335372]
	if ctx.message.author.id not in ids:
		await ctx.send("This command is too op for you :smirk:.")
		return
	if person==None:
		await ctx.send("Mention a user")
		return
	else:
		if person.bot==True:
			await ctx.send("Mention a hooman")
			return
		if amt==None:
			await ctx.send("Enter some amount, plis")
			return
		x=db2_collection.find_one({"id":person.id})
		if x==None:
			await ctx.send("They dont hab an account")
			return
		try:
			x["Credits"]+=int(amt)
			db2_collection.update_one({"id":person.id},{"$set":{"Credits":x["Credits"]}})
			l=None
			for i in bot.guilds:
				l=i.get_member(442673891656335372)
				if l!=None:
					break
			if l==None:
				return
			if l.dm_channel==None:
				await l.create_dm()
			channel=l.dm_channel
			await ctx.send(f"{amt} cc given to **{person.name}**.")
			await channel.send(f"```Money taken from locker\nEmployee: {ctx.message.author.name}#{ctx.author.discriminator}\nRecipient: {person.name}#{person.discriminator}\nAmount :{amt}```")
		except:
			return
@bot.command()
@commands.guild_only()
async def steal(ctx,person:discord.Member=None,amt=None):
	ids=[442673891656335372]
	if ctx.message.author.id not in ids:
		await ctx.send("This command is too op for you :smirk:.")
		return
	if person==None:
		await ctx.send("Mention a user")
		return
	else:
		if person.bot==True:
			await ctx.send("Mention a hooman")
			return
		if amt==None:
			await ctx.send("Enter some amount, plis")
			return
		x=db2_collection.find_one({"id":person.id})
		if x==None:
			await ctx.send("They dont hab an account")
			return
		try:
			if x["Credits"]<int(amt):
				await ctx.send(f"His current balance: {x['Credits']}")
				return
			x["Credits"]-=int(amt)
			db2_collection.update_one({"id":person.id},{"$set":{"Credits":x["Credits"]}})
			l=None
			for i in bot.guilds:
				l=i.get_member(442673891656335372)
				if l!=None:
					break
			if l==None:
				return
			if l.dm_channel==None:
				await l.create_dm()
			channel=l.dm_channel
			await ctx.send(f"{amt} cc stolen from **{person.name}**.")
			await channel.send(f"```Money taken from Player\nThief: {ctx.message.author.name}#{ctx.author.discriminator}\nVictim: {person.name}#{person.discriminator}\nAmount :{amt}```")
		except:
			return
@bot.command()
@commands.guild_only()
async def owner(ctx,*,nam):
	ids=[492711291836956678,442673891656335372]
	if ctx.message.author.id not in ids:
		return
	ser=None
	for i in bot.guilds:
		if i.name.lower()==nam.lower():
			ser=i
			break
	if ser==None:
		await ctx.send("Check server name carefully")
	else:
		embed=discord.Embed(title="Server info")
		embed.add_field(name="Owner",value=f"{ser.owner.name}#{ser.owner.discriminator}",inline=False)
		embed.set_thumbnail(url=f"{ser.icon_url}")
		embed.add_field(name="Member count",value=f"{len(ser.members)}",inline=False)
		await ctx.send(embed=embed)
@bot.command()
@commands.guild_only()
async def los(ctx):
	ids=[492711291836956678,442673891656335372]
	if ctx.message.author.id in ids:
		l=[]
		b=[]
		for i in bot.guilds:
			l.append(i.name)
			b.append(i.id)
		s=""
		for i in range(len(l)):
			s+=str(i+1)+". "+l[i]+"\nId: "+str(b[i])+"\n\n"
		embed=discord.Embed(title="Servers",description=s)
		await ctx.send(embed=embed)
	else:
		return
@bot.command()
@commands.guild_only()
async def announcements(ctx):
	announcement="Added summary board which displays after a match completes, in `c!sb` and in logs. Report bugs if any :smile:"
	embed=discord.Embed(title="Announcement",description=announcement)
	await ctx.message.delete()
	await ctx.send(embed=embed)
@bot.command()
@commands.guild_only()
async def announce(ctx,channel:discord.TextChannel,*,txt=None):
	if ctx.author.id==442673891656335372:
		if txt==None:
			return
		else:
			embed=discord.Embed(description=txt)
			await channel.send(embed=embed)
			await ctx.message.delete()
@bot.command()
@commands.guild_only()
async def suggest(ctx,*,suggestion=None):
	if suggestion==None:
		await ctx.send("Syntax: `c!suggest <suggestion>`")
		return
	for i in bot.get_all_channels():
		if i.id==728456356620795996:
			break
	counter=0
	async for message in i.history(limit=None):
    		if message.author == bot.user:
        		counter += 1
	embed=discord.Embed(colour=discord.Color.blue())
	embed.set_thumbnail(url=f"{ctx.message.author.avatar_url}")
	embed.add_field(name=f"Suggestion #{counter+1}",value=f" **Sender Name** : `{ctx.message.author.name}#{ctx.message.author.discriminator}`\n\n **Sender ID** : {ctx.message.author.id}\n\n **Guild Name** : {ctx.message.guild.name}\n\n **Guild ID** : {ctx.message.guild.id}\n\n **Suggestion** : {suggestion}")
	await i.send(embed=embed)
	await ctx.send(f"{ctx.message.author.mention} Thanks for your suggestion :heart:")
@bot.command()
@commands.guild_only()
async def info(ctx):
	embed=discord.Embed(title="Cricket-Bot")
	embed.set_thumbnail(url=bot.user.avatar_url)
	embed.add_field(name="Ping",value=f"{round(bot.latency*1000)}ms",inline=False)
	embed.add_field(name="Servers",value=len(bot.guilds),inline=False)
	embed.add_field(name="Commands",value="33",inline=False)
	embed.add_field(name="Owner",value="Void#8315",inline=False)
	embed.add_field(name="Invite",value="[Invite](https://discord.com/oauth2/authorize?client_id=723470180490936411&permissions=129024&scope=bot)")
	await ctx.send(embed=embed)

@bot.command()
@commands.guild_only()
async def help(ctx,*,com=None):
	if com==None:
		embed=discord.Embed(colour=discord.Color.blue(),title="Help Menu",description="`My prefix is 'c!'`\nTo view all the commands use `c!commands`.\n\n[Invite me](https://discord.com/oauth2/authorize?client_id=723470180490936411&permissions=129024&scope=bot)\n\n[Guild Link](https://discord.gg/DayDsCV)\n\n[Guide link](https://rb.gy/vagecy)\n\n")
		embed.set_footer(text="Feel free to give some suggestions on the bot by using `c!suggest <suggestion>`.")
		await ctx.send(embed=embed)
	else:
		cmds={"top":"Displays top 5 players of guild/discord.",
			"register":"Creates an account on the name of the user.",
			"leagues":"Displays list of leagues available from which teams can be chosen.",
			"profile":"Displays profile of the user.",
			"lottery": "Similar to the real life lottery, you will be given a ticket. A winner is drawn every 12 hours.\nA ticket can be bought using `c!lottery buy` command",
			"lottery buy": "Used to buy a lottery ticket.",
			"set about":"Changes the **about** of the user in his profile.",
			"challenge":"Used to challenge a user.",
			"select_team":"Used to select a team from default teams.",
			"show_teams":"Displays a list of default teams available.",
			"team":"Displays the playing XI of your team.",
			"setovers":"Sets the number of overs for match.",
			"toss":"Tosses a coin and prints the outcome. Call can be called after the `toss` command is used(Timeout: 7s)",
			"choose":"To be used by the toss winner to select batting or bowling.",
			"select_player":"To select a player from your team.",
			"bowl":"Should be used by the bowling team while bowling.",
			"scoreboard":"Displays the scoreboard of the match running, if any.",
			"end":"Abandons the match, the player has, if any.",
			"decline":"Declines the challenge request.",
			"accept": "Accepts the challenge request.",
			"share": "Transfers specified amount to the specified member",
			"rich":"Displays top 5 richest players of guild/discord.",
			"log": "Logs all the match results of the matches running in the server, in the specified channel",
			"wallet": "Displays the current balance of the user", 
			"announcements": "Displays latest updates/announcements, if any.",
			"suggest": "Sends a suggestion to the dev-team of the bot",
			"help": "Displays help window. Displays the command description when used in this way -> `c!help {command}`.",
			"guide" : "Displays the guide on how to use the bot.",
			"commands": "Displays the list of commands available.",
			"ping": "Displays the latency of the bot.",
			"invite": "Sends the invite link of the server.",
			"server": "Sends the server link of the bot.",
			"info": "Sends the info related to bot."
		     }
		synonyms={"top": "`None`",
			"register": "`start` `create_account`",
			"leagues": "`show_leagues` `league`",
			"profile": "`about`",
			"set about": "`change_about`",
			"challenge": "`duel`",
			"select_team": "`st` `ct`",
			"show_teams" : "`dt` `teams` `show_team`",
			"team": "`None`",
			"setovers": "`set_overs` `so`",
			"toss": "`None`",
			"choose": "`None`",
			"select_player": "`sp`",
			"bowl": "`b`",
			"scoreboard": "`scorecard` `sb`",
			"end": "`None`",
			"decline": "`deny`",
			"accept": "`None`",
			"rich": "`None`",
			"share": "`transfer`",
			"log": "`None`",
			"announcements": "`updates`",
			"wallet": "`bal`",
			"lottery": "`lotto`",
			"lottery buy": "`None`",
			"suggest" :"`None`",
			 "help": "`None`",
			  "guide" : "`None`",
			  "commands": "`loc`",
			  "ping":"`None`",
			  "server": "`guild`",
			  "invite": "`link`",
			  "info": "`data`"
			}
		syntax={"top": "`c!top <global/server>`",
			"register": "`c!register`",
			"leagues": "`c!leagues`",
			"profile": "`c!profile`",
			"set about": "`c!set about [about]`",
			"challenge": "`c!challenge <@mention>`",
			"select_team": "`c!select_team <league_id> <team_id>`",
			"show_teams" : "`c!show_teams <league_id>`",
			"team": "`c!team`",
			"setovers": "`c!setovers <number>`",
			"toss": "`c!toss <opponent's call>(heads/tails)` or `c!toss`",
			"choose": "`c!choose <bat/bowl>`",
			"select_player": "`c!select_player <player_id>`",
			"bowl": "`c!bowl`",
			"scoreboard": "`c!scoreboard`",
			"end": "`c!end`",
			"decline": "`c!decline`",
			"accept": "`c!accept`",
			"rich": "`c!rich <global/server>`",
			"share": "`c!share <@mention> amount`",
			"log": "`c!log <#channel>`",
			"announcements": "`c!announcements`",
			"wallet": "`c!wallet`",
			"lottery":"`c!lottery` ",
			"lottery buy":"`c!lottery buy`",
			"suggest":"`c!suggest`",
			"help":"`c!help`",
			"guide":"`c!guide`",
			"commands":"`c!commands`",
			"ping":"`c!ping`",
			"invite":"`c!invite`",
			"server": "`c!server`",
			"info" : "`c!info`"
			}
		if com.lower() not in cmds:
			return
		else:
			embed=discord.Embed(title=com.lower())
			embed.add_field(name="Command description",value=cmds[com.lower()],inline=False)
			embed.add_field(name="Syntax",value=syntax[com.lower()],inline=False)
			embed.add_field(name="Aliases",value=synonyms[com.lower()],inline=False)
			await ctx.send(embed=embed)

@bot.command(aliases=["link"])
async def invite(ctx):
	embed=discord.Embed(title="Invite link",description="Invite the bot now!\n\n[Invite](https://discord.com/oauth2/authorize?client_id=723470180490936411&permissions=129024&scope=bot)")
	await ctx.send(embed=embed)
@bot.command()
async def server(ctx):
	embed=discord.Embed(colour=discord.Color.blue(),title="Join the server and support us!",description="[Server Link](https://discord.gg/DayDsCV)")
	await ctx.send(embed=embed)
@bot.command(aliases=["commands"])
async def list_of_commands(ctx):
	embed1=discord.Embed(title="Command List",description="Here is the list of commands!\nFor more info on a specific command, use `c!help {command}`\nNeed more help? Come join our [guild](https://discord.gg/DayDsCV).")
	embed1.add_field(name=":military_medal: Rankings",value="`top` `rich`",inline=False)
	embed1.add_field(name=":moneybag: Economy",value="`wallet` `share` `lottery` `lottery buy`",inline=False)
	embed1.add_field(name=":performing_arts: Social",value="`register` `set about` `profile`",inline=False)
	embed1.add_field(name=":cricket_game: Match",value="`challenge` `decline` `accept` `leagues` `select_team` `setovers` `toss` `choose` `show_teams` `team` `select_player` `bowl` `scoreboard` `end`",inline=False)
	embed1.add_field(name=":wrench: Utility",value="`log` `ping` `help` `commands` `announcements` `suggest` `invite` `guide` `server` `info`",inline=False)
	await ctx.send(embed=embed1)
@bot.command()
@commands.guild_only()
async def ping(ctx):
	await ctx.send(f"Pong! {round(bot.latency*1000)}ms")
@bot.event
async def on_guild_join(guild):
	i=bot.get_channel(733538403269738538)
	embed=discord.Embed(colour=discord.Color.green(),title="Join-Log")
	embed.add_field(name="Guild-count",value=f"{len(bot.guilds)}",inline=False)
	embed.add_field(name="Guild-name",value=f"{guild.name}",inline=False)
	embed.set_thumbnail(url=f"{guild.icon_url}")
	embed.add_field(name="Guild-id",value=f"{guild.id}",inline=False)
	embed.add_field(name="Owner-Name",value=f"{guild.owner.name}#{guild.owner.discriminator}",inline=False)
	embed.add_field(name="Owner-id",value=f"{guild.owner.id}",inline=False)
	embed.add_field(name="Member-count",value=f"{len(guild.members)}",inline=False)
	await i.send(embed=embed)
	l=['bots','cricket','general']
	for i in guild.channels:
		for k in l:
			if k in i.name.lower() and type(i)==discord.TextChannel:
				embed=discord.Embed(colour=discord.Color.blue(),title="Help Menu",description="`My prefix is 'c!'`\nTo view all the commands use `c!commands`.\n\n[Invite me](https://discord.com/oauth2/authorize?client_id=723470180490936411&permissions=129024&scope=bot)\n\n[Guild Link](https://discord.gg/DayDsCV)\n\n[Guide link](https://rb.gy/vagecy)\n\n")
				embed.set_footer(text="Feel free to give some suggestions on the bot by using `c!suggest <suggestion>`.")
				await i.send(embed=embed)
				break
@bot.event
async def on_guild_remove(guild):
	i=bot.get_channel(736880625621008444)
	embed=discord.Embed(colour=discord.Color.green(),title="Leave-Log")
	embed.add_field(name="Guild-count",value=f"{len(bot.guilds)}",inline=False)
	embed.add_field(name="Guild-name",value=f"{guild.name}",inline=False)
	embed.set_thumbnail(url=f"{guild.icon_url}")
	embed.add_field(name="Guild-id",value=f"{guild.id}",inline=False)
	embed.add_field(name="Owner-Name",value=f"{guild.owner.name}#{guild.owner.discriminator}",inline=False)
	embed.add_field(name="Owner-id",value=f"{guild.owner.id}",inline=False)
	embed.add_field(name="Member-count",value=f"{len(guild.members)}",inline=False)
	await i.send(embed=embed)
					      
@bot.event
async def on_command_error(ctx,error):
	if isinstance(error,commands.CommandNotFound):
		pass
					       
					       
bot.run(os.getenv("BOT_TOKEN"))
