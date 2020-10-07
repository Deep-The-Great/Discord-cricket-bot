import discord 
import asyncio
import random
from discord.ext import commands
import os
import datetime
import pymongo
import json
import math
m=None
db_client=pymongo.MongoClient(os.getenv("DB_URL"))
db1_client=pymongo.MongoClient(os.getenv("DB2_URL"))

class guide(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @commands.command()
    @commands.guild_only()
    async def guide(self,ctx,number=None):
        if number==None:
            number=1
        number=int(number)-1
        #registration
        list_of_pages=[]
        embed=discord.Embed(title="Guide",description="**Registration**\n\nIn order to use some features of the bot or challenge others, you need to have an account on your name. You can create an account by using `c!register` command.\nAfter creating an account you can check your profile using `c!profile` command.")
        embed.set_image(url="https://raw.githubusercontent.com/Shrikar-Kota/Personalcrickgame/master/images/register-pic.png")
        embed.set_footer(text="Page : 1/8")
        list_of_pages.append(embed)
        #challenge
        embed=discord.Embed(title="Guide",description="**Challenge**\n\nAfter you are done with creating your account you can now use all the bot's commands and play with it.\nTo play with the other person, either you need to challenge them or they need to challenge you which you can do by using `c!challenge` command tagging the opponent.\nAfter you throw a challenge, the opponent can accept it using `c!accept` or decline it using `c!decline` command.")
        embed.set_footer(text="Page : 2/8")
        embed.set_image(url="https://raw.githubusercontent.com/Shrikar-Kota/Personalcrickgame/master/images/Challenge-pic.png")
        list_of_pages.append(embed)
        #select_team
        embed=discord.Embed(title="Guide",description="**Selecting team**\n\nAfter the opponent accepts the challenge, the bot will prompt you to select a team from default teams.\nYou can check the available leagues by typing `c!leagues`. After checking the available leagues, you can select a league from it by using `c!st league_id`, here league id is the id given by the respective league.\nAfter selecting the league, the bot will prompt you to select a team which you can do by using `c!select_team <league_id> <team_id>`.")
        embed.set_footer(text="Page : 3/8")
        embed.set_image(url="https://raw.githubusercontent.com/Shrikar-Kota/Personalcrickgame/master/images/select-team-pic.png")
        list_of_pages.append(embed)
        #set_overs
        embed=discord.Embed(title="Guide",description="**Setting overs**\n\nAfter you are done with choosing your team, you need to set the overs of the match. This can be done using `c!so` command.")
        embed.set_footer(text="Page : 4/8")
        embed.set_image(url="https://raw.githubusercontent.com/Shrikar-Kota/Personalcrickgame/master/images/set-overs-pic.png")
        list_of_pages.append(embed)
        #toss
        embed=discord.Embed(title="Guide",description="**Toss**\n\nSimilar to the real life cricket game, the teams have to choose what they gonna do first. This can be done by doing toss. Toss can be done using `c!toss` command.\nAfter one of the players type the command, the opponent needs to send his choice in the chat i.e., heads/tails.")
        embed.set_footer(text="Page : 5/8")
        embed.set_image(url="https://raw.githubusercontent.com/Shrikar-Kota/Personalcrickgame/master/images/toss-pic.png")
        list_of_pages.append(embed)
        #choose
        embed=discord.Embed(title="Guide",description="**Choosing**\n\nAfter the toss, the toss-winner should choose either bowling or batting by using `c!choose` command.")
        embed.set_footer(text="Page : 6/8")
        embed.set_image(url="https://raw.githubusercontent.com/Shrikar-Kota/Personalcrickgame/master/images/choose-pic.png")
        list_of_pages.append(embed)
        #select_player
        embed=discord.Embed(title="Guide",description="**Selecting players**\n\nAfter choosing either batting or bowling, the teams can choose their players by using `c!sp` command.")
        embed.set_footer(text="Page : 7/8")
        embed.set_image(url="https://raw.githubusercontent.com/Shrikar-Kota/Personalcrickgame/master/images/select-player-pic.png")
        list_of_pages.append(embed)
        #bowl
        embed=discord.Embed(title="Guide",description="**Selecting players**\n\nAfter choosing your players, now you are all set to play the match. The bowling team needs to use the `c!bowl` command and the batting team needs to wait patiently for their turn to come :wink:.")
        embed.set_footer(text="Page : 8/8")
        embed.set_image(url="https://raw.githubusercontent.com/Shrikar-Kota/Personalcrickgame/master/images/bowl-pic.png")
        list_of_pages.append(embed)        
        global m
        m=await ctx.send(embed=list_of_pages[number])
        await m.add_reaction("⬅️")
        await m.add_reaction("➡️")	
        def check(reaction, user):
            return (user.id==ctx.message.author.id and m.id==reaction.message.id)
        while 1:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                return        
            else:
                m = await ctx.channel.fetch_message(m.id)
                if str(reaction.emoji)=="➡️":
                    e=m.embeds
                    e=str(e[0].footer.text)
                    e=e.split(":")
                    e=e[1].split("/")
                    count=int(e[0])
                    if count>len(list_of_pages)-1:
                        count=0
                    await m.edit(embed=list_of_pages[count])
                    await m.remove_reaction("➡️",user)
                elif str(reaction.emoji)=="⬅️":
                    e=m.embeds
                    e=str(e[0].footer.text)
                    e=e.split(":")
                    e=e[1].split("/")
                    count=int(e[0])-2
                    if count==-1:
                        count=len(list_of_pages)-1
                    await m.edit(embed=list_of_pages[count])
                    await m.remove_reaction("⬅️",user)
                else:
                    await m.remove_reaction(str(reaction.emoji),user)


def setup(bot):
	bot.add_cog(guide(bot))
