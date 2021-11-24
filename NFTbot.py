from logging import raiseExceptions
import discord
import asyncio
from discord.ext import commands
import json
import os
import random

print('Stalker V1.0 is starting up')
intents = discord.Intents.all()


def chance(num):
    x = random.randrange(1,100)
    if x <= num:
        return True
    return False


client = commands.Bot(command_prefix='e!',intents=intents)

@client.event
async def on_ready():
    global target       
    print('Logged on as {0}!'.format(client.user))


@client.command()
async def balance(ctx):
    await open_account(ctx.author)
    
    users = await get_bank_data()

    wallet_amt = users[str(ctx.author.id)]["wallet"]
    bank_amt  = users[str(ctx.author.id)]["bank"]
    lockpicks_amt = users[str(ctx.author.id)]["lockpicks"]

    em = discord.Embed(title =f"{ctx.author.name}'s balance",color = discord.Color.gold())
    em.add_field(name = "Wallet",value = wallet_amt)
    em.add_field(name = "Bank",value = bank_amt)
    em.add_field(name = "Lockpicks",value = lockpicks_amt)
    await ctx.send(embed = em)
    print('message') 
                


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["username"] = user.name
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["lockpicks"] = 0
        # await user.send("New Account created")
    with open("wallets.json","w") as file:
        json.dump(users,file)
    return True

async def get_bank_data():
        with open("wallets.json","r") as file:
            users = json.load(file)
        return users

async def dollar(ctx):
    users = await get_bank_data()
    users[str(ctx.author.id)]["username"] = ctx.author.name
    users[str(ctx.author.id)]['wallet'] += 1
    if chance(20):
        try:
            if str(ctx.author.nick) == 'None':
                raiseExceptions 
            print(f"{ctx.author.nick}, you found a lockpick!")
            await ctx.channel.send(f"{ctx.author.nick}, you found a lockpick!")
        except:
            print(f"{ctx.author.name}, you found a lockpick!")
            await ctx.channel.send(f"{ctx.author.name}, you found a lockpick!")
        users[str(ctx.author.id)]["lockpicks"] += 1

    with open("wallets.json","w") as file:
        json.dump(users,file)

@client.command()
async def steal(ctx):
    victim = ctx.message.mentions[0]
    amount = random.randrange(1,100)
    users = await get_bank_data()
    if users[str(ctx.message.author.id)]['lockpicks'] == 0:
        await ctx.send("You have no Lockpicks!")
        return False

    users[str(victim.id)]["username"] = victim.name
    users[str(victim.id)]['wallet'] -= amount
    if users[str(victim.id)]['wallet'] < 0:
        amount = amount + users[str(victim.id)]['wallet']
        users[str(victim.id)]['wallet'] = 0
    users[str(ctx.author.id)]["username"] = ctx.author.name
    users[str(ctx.author.id)]["lockpicks"] -= 1
    users[str(ctx.author.id)]['wallet'] += amount
    with open("wallets.json","w") as file:
        json.dump(users,file)
        await ctx.send(f"{ctx.author.name} stole {amount} dollars from {victim.name}")
        
@client.command()
async def bank(ctx,arg1):
    arg1 = int(arg1)
    users = await get_bank_data()
    if  arg1 > users[str(ctx.author.id)]['wallet']:
         await ctx.send(f"{ctx.author.name} does not have {arg1} dollars")
         return False
    users[str(ctx.author.id)]["username"] = ctx.author.name
    users[str(ctx.author.id)]['wallet'] -= arg1
    users[str(ctx.author.id)]['bank'] += arg1
         
    with open("wallets.json","w") as file:
        json.dump(users,file)
    await ctx.send(f"{ctx.author.name} banked in {arg1} dollops")
    if users[str(ctx.author.id)]['bank'] < 0:
        await ctx.send(f"{ctx.author.name}, pay back {-users[str(ctx.author.id)]['bank']}.")
    

@client.command()
async def bid(ctx,arg1,artpiece):
    global biddetails
    arg1 = int(arg1)
    users = await get_bank_data()
    with open('nfts.json','r') as nftfile:
        nfts = json.load(nftfile)
    if  arg1 > users[str(ctx.author.id)]['wallet']:
         await ctx.send(f"{ctx.author.name} does not have {arg1} dollars")
         return False
    elif artpiece not in nfts:
        await ctx.send(f"Artpiece {artpiece} does not exist.")
        return False
    elif arg1 <= nfts[artpiece]['value']:
        await ctx.send(f"{nfts[artpiece]['owner']} has the highest bid of {nfts[artpiece]['value']}.")
        return False
    else:
        #return money
        users[str(nfts[artpiece]['ownerid'])]['wallet'] += nfts[artpiece]['value']
        #replace top value
        nfts[artpiece]['value'] = arg1
        #minus from wallet
        users[str(ctx.author.id)]['wallet'] -= arg1
        #change owner
        nfts[artpiece]['owner'] = ctx.author.name
        nfts[artpiece]['ownerid'] = ctx.author.id
        with open('nfts.json','w') as nftfile:
            json.dump(nfts,nftfile)
        with open("wallets.json","w") as file:
            json.dump(users,file)

@client.command()
async def browse(ctx,imagename):
    with open('nfts.json','r') as file:
        nfts = json.load(file)
    with open("NFTS/"+imagename,"rb") as image:
        i = discord.File(image, filename = "NFTS/"+imagename)
        await ctx.send(file = i)
    
    

@client.event
async def on_message(message):
    global target
    print('Message from {0.author}: {0.content}'.format(message))
    mentions = message.mentions

    if message.author == client.user:
        return
    if message.author.bot:
        return
    await open_account(message.author)
    await dollar(message)
    await client.process_commands(message)

token = 'add token here'
client.run('')
