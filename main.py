"""
Copyright © 2026 an-aegis

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# V0.7.0.3

import discord
from discord.ext import commands
from VNDFHelper import get_role
from VNDFNewRank import NewRank
import traceback

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!BANNANAR", intents=intents) # silly prefix to stop debug warnings       

@bot.tree.command(name = "promote", description = "promote a user by N ranks")
async def promote(interaction: discord.Interaction, who:discord.Member, by:int, publicly_report_here:bool = False, joke:bool = False):
    if interaction.user.id == who.id:
        await interaction.response.send_message("You can't promote yourself", ephemeral=True)
        return
    
    C2 = 1534948457704329266
    C3 = 1534948456572125365
    C4 = 1534948455041073265
    FM = 1534960058813648906 # first marshal
    caller_roles = interaction.user.roles # interaction.user is secretly member
    
    # it is important to note that get_role uses the first argument to get the user guild
    # it does not matter if the user actually has the role
    if await get_role(who, FM) in caller_roles:
        limit = 21 # O-10
        joke_allowed = True
    elif await get_role(who, C2) in caller_roles:
        limit = 5 # E-4
        joke_allowed = False
    elif await get_role(who, C3) in caller_roles:
        limit = 9 # E-8
        joke_allowed = True
    elif await get_role(who, C4) in caller_roles:
        limit = 17 # O-6
        joke_allowed = True
    elif await get_role(who, 1534948496069628084) in caller_roles:
        announcements_channel = bot.get_channel(1534948733396058222) # announcements channel
        await announcements_channel.send("@everyone <@interaction.user.id> (A LITERAL E-0) JUST TRIED TO PROMOTE <@who.id>")
    else:
        await interaction.response.send_message(f"You (<@{interaction.user.id}>) have no known promotion authority", ephemeral=True)
        return
    
    if joke_allowed and joke:
        await interaction.response.send_message(f"promoting <@{who.id}> by {by*10000}", ephemeral=False)
        return
    
    logging_channel = bot.get_channel(1535298462583750746)
    
    try:
        rank = NewRank(who)
        rank.limit = limit
        ids = rank.get_id()
    
        EOrank_old = await get_role(who,ids[0])
        Crank_old = await get_role(who,ids[1]) # E-0 will always get None c rank
        
        if by > 0:
            rank = rank + by
        if by < 0:
            rank = rank - abs(by) # this is for the protections built into subtraction that arent in addition
        ids = rank.get_id()
        
        EOrank = await get_role(who,ids[0])
        Crank = await get_role(who,ids[1]) # E-0 will always get None c rank
        
        await who.add_roles(EOrank)
        await who.remove_roles(EOrank_old)
        
        if Crank != Crank_old:
            if Crank != None:
                await who.add_roles(Crank)
            if Crank_old != None:
                await who.remove_roles(Crank_old)
        
        await logging_channel.send(f"<@{interaction.user.id}> promoted <@{who.id}> by {by} ranks, from {EOrank_old} to {rank.rankval}")
        await interaction.response.send_message(f"{who.nick} promoted by {by} ranks", ephemeral=not publicly_report_here)
    except Exception as e:
        print(traceback.format_exc())
        try:
            if EOrank in who.roles:
                try:
                    await logging_channel.send(f"<@{interaction.user.id}> promoted <@{who.id}> by {by} ranks, from {EOrank_old} to {rank.rankval}")
                    await interaction.response.send_message(f"{who.nick} promoted by {by} ranks", ephemeral=not publicly_report_here)
                except:
                    pass
                    # give up on life, this error handler is fucked
        except:
            print(f"{interaction.user.nick} just failed to promote {who.nick}. Attempted to promote by {by}")
            await logging_channel.send(f"<@{who.id}> had a failed promotion/demotion from user <@{interaction.user.id}>\nError: `{e}`")
        
            try:
                await interaction.response.send_message(f"Error: `{e}`", ephemeral=True)
            except:
                pass
                # just give up, theres nothing that can be done except stop a hard error

@bot.tree.command(name = "ssu", description = "the supreme act of courage is to host")
async def host(interaction: discord.Interaction, password:str):
    if await get_role(interaction.user,1534948522674356234) in interaction.user.roles:
        status_channel = bot.get_channel(1534948734670995566) # status channel
        password_channel = bot.get_channel(1535337616726040689) # password share channel
    
        messages = password_channel.history(limit=500)
        async for message in messages:
            await message.delete()
        
        embed = discord.Embed(title="**Casual Hosting**", description=f"_ _\n**HOLY SHIT <@{interaction.user.id}> IS HOSTING**\n\n\n__Server name:__ ---VNDF Military Roleplay | Read Description---\n-# cant find it? join the [steam group](https://steamcommunity.com/chat/invite/eOznIFhN)", color=0x0000ff)
        await status_channel.send(f"<@&1534961648920563762>",embed=embed) #
        await password_channel.send(f"The password is: ||```{password}```||\n\nYes, you need to copy the capitalization")
        await interaction.response.send_message("Sucessful hosting", ephemeral=True)
    else:
        await interaction.response.send_message("You cannot host :/", ephemeral=True)

@bot.tree.command(name = "ssd", description = "the supreme act of courage is to host (and then give up)")
async def unhost(interaction: discord.Interaction):
    if await get_role(interaction.user,1534948522674356234) in interaction.user.roles:
        status_channel = bot.get_channel(1534948734670995566) # status channel
        password_channel = bot.get_channel(1535337616726040689) # password share channel
    
        messages = password_channel.history(limit=5)
        async for message in messages:
            await message.delete() # DANGEROUS CODE
        
        embed = discord.Embed(title="**SSD**", description=f"_ _\n:(", color=0xff0000)
        await status_channel.send(embed=embed)
        await interaction.response.send_message("Sucessful ssd", ephemeral=True)
    else:
        await interaction.response.send_message("You cannot ssd :/", ephemeral=True)

@bot.tree.command(name = "poke", description = "poke the bear to see if its awake")
async def poke(interaction: discord.Interaction):
    print(f"{interaction.user} just poked me")
    await interaction.response.send_message("yes... im up", ephemeral=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
