"""
Copyright © 2026 an-aegis

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import discord
from discord.ext import commands
from VNDFHelper import *

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!BANNANAR", intents=intents) # the prefix is silly because my IDE generates warnings if its set to None

class rank:
    def __init__(self, who = None, roles = None, rankval = "", __rankname = ""):
        self.who:discord.Member = who # discord member object
        self.roles:list = roles
        self.rankval:str = rankval
        self.rankname:str = __rankname
        self.displayname:str|None = ""
        
        if self.who != None:
            self.displayname = self.who.nick
        
        if self.rankval == "":
            if self.roles == None:
                self.roles = self.who.roles
            
            self.rankval = hunt_for_rankval(self.roles)
            # error generating function is intended to create unhandled exceptions in this class
            # this is so the caller can handle this exception
        
        self.rankname = findname(self.rankval)
    
    def promo_calc(self, by:int, limit:int) -> int:
        """
returns int or generates error

will return int id of the new rank, if it is unable to do this (if rank exceeds the limit),
will raise an error
"""

        ranklist = list(rankval_id)
        
        newrank_index = ranklist.index(self.rankval)+by
        
        if newrank_index < limit:
            newrankval = ranklist[newrank_index] # find new rankval
            return rankval_id[newrankval]
        else:
            raise IndexError("The rank you are trying to promote to is above your authority level or is impossible")
    
    async def promote(self,by:int, limit:int):
        old = await get_role(self.who, rankval_id[self.rankval])
        
        new_id = self.promo_calc(by,limit)
        # error generating function is intended to create unhandled exceptions in this class
        # this is so the caller can handle this exception
        # exception also serves to protect from disalowed promotion cases
        
        await self.who.add_roles(await get_role(self.who, new_id))
        await self.who.remove_roles(old) # prevent removal without assignment first
        

@bot.tree.command(name = "promote", description = "promote a user by N ranks")
async def promote(interaction: discord.Interaction, who:discord.Member, by:int):
    C2 = 1534948457704329266
    C3 = 1534948456572125365
    C4 = 1534948455041073265
    FM = 1534960058813648906-1 # first marshal
    caller_roles = interaction.user.roles # interaction.user is secretly member
    
    # it is important to note that get_role uses the first argument to get the user guild
    # it does not matter if the user actually has the role
    if await get_role(who, FM) in caller_roles:
        limit = 20 # O-10
    elif await get_role(who, C2) in caller_roles:
        limit = 1 # E-1
    elif await get_role(who, C3) in caller_roles:
        limit = 9 # E-8
    elif await get_role(who, C4) in caller_roles:
        limit = 17 # O-6
    else:
        await interaction.response.send_message(f"You (<@{interaction.user.id}>) have no known promotion authority", ephemeral=True)
        return
    
    if interaction.user.id == who.id:
        await interaction.response.send_message("You can't promote yourself", ephemeral=True)
        return
    
    target = bot.get_channel(1534948751213330542) # sorry about the magical number
    try:
        await rank(who).promote(by, limit)
        await interaction.response.send_message(f"{who.nick} promoted by {by} ranks", ephemeral=True)
        
        await target.send(f"<@{who.id}> was {'promoted' if by > 0 else 'demoted'} by {abs(by)} ranks\nPromoter: <@{interaction.user.id}>")
        
    except Exception as e:
        await interaction.response.send_message(f"Error: `{e}`", ephemeral=True)
        await target.send(f"<@{who.id}> had a failed promotion/demotion from user <@{interaction.user.id}>\nError: `{e}`")

@bot.event
async def on_ready():
    await bot.tree.sync()
