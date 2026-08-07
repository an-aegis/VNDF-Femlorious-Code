"""
Copyright © 2026 an-aegis

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# v0.6.1

import discord
from discord.ext import commands
from VNDFHelper import get_role
from VNDFRank import rank
import traceback

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!BANNANAR", intents=intents) # silly prefix to stop debug warnings       

@bot.tree.command(name = "promote", description = "promote a user by N ranks")
async def promote(interaction: discord.Interaction, who:discord.Member, by:int):
    C2 = 1534948457704329266
    C3 = 1534948456572125365
    C4 = 1534948455041073265
    FM = 1534960058813648906 # first marshal
    caller_roles = interaction.user.roles # interaction.user is secretly member
    
    # it is important to note that get_role uses the first argument to get the user guild
    # it does not matter if the user actually has the role
    if await get_role(who, FM) in caller_roles:
        limit = 21 # O-10
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
    
    target = bot.get_channel(1535298462583750746) # sorry about the magical number
    try:
        human = rank(who)
        await human.promote(by, limit)
        await interaction.response.send_message(f"{who.nick} promoted by {by} ranks", ephemeral=True)
        
        #await target.send(f"<@{who.id}> was {'promoted' if by > 0 else 'demoted'} by {abs(by)} rank{'s' if by != 1 else ''} (to {human.rankval})\nPromoter: <@{interaction.user.id}>")
        await target.send(f"<@{who.id}> was promoted to {human.rankval} (from {human.old_rankval}) by <@{interaction.user.id}>")
        
    except Exception as e:
        print(traceback.format_exc())
        await interaction.response.send_message(f"Error: `{e}`", ephemeral=True)
        await target.send(f"<@{who.id}> had a failed promotion/demotion from user <@{interaction.user.id}>\nError: `{e}`")

@bot.tree.command(name = "ssu", description = "the supreme act of courage is to host")
async def host(interaction: discord.Interaction, password:str):
    status_channel = bot.get_channel(1534948722062921908) # test status channel
    password_channel = bot.get_channel(1535337616726040689) # password share channel
    
    channel = bot.get_channel(1535337616726040689)
    messages = channel.history(limit=500)
    async for message in messages:
        await message.delete()
    
    await status_channel.send(f"<@&1534961648920563762> holy shit <@{interaction.user.id}> is hosting\n\n-# cant find it? join the steam group, you can find someone to join off of there https://steamcommunity.com/chat/invite/eOznIFhN")
    await password_channel.send(f"The password is: `{password}`\n\nYes you need to copy the capitalization")
    
@bot.event
async def on_ready():
    await bot.tree.sync()
