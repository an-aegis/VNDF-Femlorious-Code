"""
Copyright © 2026

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!BANNANAR", intents=intents) # the prefix is silly because my IDE generates warnings if its set to None

rankval_id = {
    "E-0": 1298370746371801118,
    
    "E-1": 1225563199118774272,
    
    "E-2": 1225563291888128020,
    
    "E-3": 1225563457668120586,
    
    "E-4": 1225563531907436635,
    
    "E-5": 1225563853757218858,
    
    "E-6": 1225564296772321281,
    
    "E-7": 1225564368201060412,
    
    "E-8": 1235143664016031785,
    
    "E-9": 1235143924448759819,
    
    "E-10": 1235144094620323890,
    
    "O-1": 1225816033751863467,
    
    "O-2": 1235144296856948816,
    
    "O-3": 1235144506316423288,
    
    "O-4": 1235144644032200734,
    
    "O-5": 1235144876103045191,
    
    "O-6": 1225776709908041749,
    
    "O-7": 1235151827331190784,
    
    "O-8": 1235152116193038428,
    
    "O-9": 1225564174764081202,
    
    "O-10": 1238572551651856394,
    }

def findname(rankval: str): # this could be a dict, but i felt like a function was prettier
    match rankval:
        case "E-0":
            return "Recruit"
        case "E-1":
            return "PSC"
        case "E-2":
            return "PFC"
        case "E-3":
            return "Specialist"
        case "E-4":
            return "Corporal"
        case "E-5":
            return "Sergeant"
        case "E-6":
            return "Staff Sergeant"
        case "E-7":
            return "Sgnt Mj. B"
        case "E-8":
            return "Sgnt Mj. A"
        case "E-9":
            return "First Sergeant"
        case "E-10":
            return "Command Sergeant"
        case "O-1":
            return "Lieutenant"
        case "O-2":
            return "Captain"
        case "O-3":
            return "Major"
        case "O-4":
            return "Colonel 2nd Cl."
        case "O-5":
            return "Colonel 1st Cl."
        case "O-6":
            return "Brigadier General"
        case "O-7":
            return "Lieutenant General"
        case "O-8":
            return "Major General"
        case "O-9":
            return "General 1st Cl."
        case "O-10":
            return "Field Marshal"

async def get_role(member,ID:int):
    role = member.guild.get_role(ID)
    return role

def hunt_for_rankval(roles:list) -> str:
    id_rankval = {value: (value, key) for key,value in rankval_id.items()} # shush ik its slow
    
    for role in roles:
        if role.id in id_rankval:
            break
    
    #try:
    return id_rankval[role.id]
    #except Exception as e:
    #    raise RuntimeError(e)

class rank:
    def __init__(self, who = None, roles = None, rankval = "", __rankname = ""):
        self.who = who # discord member object
        self.roles = roles
        self.rankval = rankval
        self.rankname = __rankname
        self.displayname = ""
        
        if self.who != None:
            self.displayname = self.who.nick
        
        if self.rankval == "":
            if self.roles == None:
                self.roles = self.who.roles
            
            self.rankval = hunt_for_rankval(self.roles)
        
        self.rankname = findname(self.rankval)
    
    def promo_calc(self, by:int) -> int:
        """
returns int or None (if fail)

will return int id of the new rank, if it is unable to do this (if rank exceeds the limit),
will raise an error
"""
        try:
            ranklist = list(rankval_id)
            newrank = ranklist.index(self.rankval)+by
            return rankval_id[newrank]
        except:
            raise IndexError
    
    async def promote(self,by:int):
        old = await get_role(self.who, rankval_id[self.rankval])
        await self.who.remove_roles(old)
        
        try:
            new_id = self.promo_calc(by)
            await self.who.add_roles(await get_role(self.who, new_id))
        except:
            raise RuntimeError("Promotion cannot promote to an imaginary rank")
        
        

@bot.tree.command(name = "promote", description = "promote a user by N ranks")
async def promote(interaction: discord.Interaction, who:discord.Member, by:int):
    #try:
    await rank(who).promote(by)
    await interaction.response.send_message(f"{who.nick} promoted by {by} ranks", ephemeral=True)
    #except Exception as e:
        #await interaction.response.send_message(f"Error:\n{e}", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
