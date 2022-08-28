import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import psycopg2
import database
import random
import asyncio

load_dotenv()
token = os.getenv("discord_token")

database.createTable()

client = commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
@client.command()
async def word(message):
    await message.channel.send("command")
    
@client.command()
async def level(message):
    dungeon_info = database.getInfo(message.author.id)
    print(dungeon_info[0][7])
    dungeon_level = "Current Dungeon Level: " + str(dungeon_info[0][7])
    await message.channel.send(dungeon_level)
    dungeon_enemies = 5 * int(dungeon_level[0][7])

# TODO Research double loop for dungeon combat
@client.command()
async def stats(message):
    dungeon_info = database.getInfo(message.author.id)
    await message.channel.send(player_stats(message))

#enemy stats = player stats * 0.75

@client.command()
async def practice_battle(message):
    #global enemy
    
    #enemy encounter
    dungeon_info = database.getInfo(message.author.id)
    r = random.randint(1, 3)
    if r == 1:
        enemy = "orc"
        await message.channel.send("You encountered an orc!")
        multiplier = 0.8
    if r == 2:
        enemy = "goblin"
        await message.channel.send("You encountered a goblin!")
        multiplier = 0.7
    if r == 3:
        enemy = "monster"
        await message.channel.send("You encountered a monster!")
        multiplier = 0.75
    
    #give info on enemy
    enemy_hp_info = "Enemy HP: " + str(dungeon_info[0][2] * multiplier)
    enemy_attack_info = "Enemy Attack: " + str(dungeon_info[0][3] * multiplier)
    enemy_stats = (enemy_hp_info + "\n" + enemy_attack_info)
    await message.channel.send(enemy_stats)
    
    #confirming battle
    await message.channel.send("Enter 'confirm' if you wish to battle:")
    def check(m):
        return m.author == message.author and m.channel == message.channel
    try:
        response = await client.wait_for('message', check = check, timeout = 20.0)
    except asyncio.TimeoutError:
        await message.channel.send("Timed out")
        return
    if response.content.lower() not in ("confirm"):
        await message.channel.send("Invalid message sent")
        return
    
    #actual battle
    dungeon_info = database.getInfo(message.author.id)
    enemy_hp = (dungeon_info[0][2] * 0.75)
    enemy_dmg = (dungeon_info[0][3] * 0.8)
    while enemy_hp > 0 and dungeon_info[0][9] > 0:  
        player_currenthp = dungeon_info[0][9]
        r = random.randint(1, 2)
        if r == 1:
            await message.channel.send("The " + enemy + " swung at you!")
            await message.channel.send("It missed!")
            await message.channel.send(player_stats(message))
        if r == 2:
            await message.channel.send("The " + enemy + " swung at you!")
            await message.channel.send("It hit you!")
            player_currenthp -= enemy_dmg
            await message.channel.send(player_stats(message))
        fight_screen(message, enemy)
        


async def fight_screen(message, enemy_name):
    await message.channel.send("\n")
    await message.channel.send("<===========================================================================>")
    await message.channel.send(message.author.name + ' vs ' + enemy_name)
    await message.channel.send("\n")
    await message.channel.send("")
    await message.channel.send("<===========================================================================>")
    await message.channel.send("\n")       
    
@client.command()
async def register(message):
    print(message.author.id)
    if database.registerUser(message.author.id):
        await message.channel.send("You are already registered")
    else:
        await message.channel.send("You have successfully registered")
    dungeon_info = database.getInfo(message.author.id)

@client.command()
async def command_list(message):
    await message.channel.send(help_list())

@client.command()
async def max_health(message):
    dungeon_info = database.getInfo(message.author.id)
    dungeon_info[0][9] = dungeon_info[0][2]

def player_stats(message):
    dungeon_info = database.getInfo(message.author.id)
    player_hp = "Player Health:" + str(dungeon_info[0][9]) + "/" + str(dungeon_info[0][2])
    player_attack = "Player Attack: " + str(dungeon_info[0][3])
    player_armor = "Player Armor: " + str(dungeon_info[0][4])
    player_level = "Player Level: " + str(dungeon_info[0][5])
    player_money = "Player Money: " + str(dungeon_info[0][1])
    player_stats = (player_hp + "\n" + player_attack + "\n" + player_armor + "\n" + player_level + "\n" + 
player_money)
    return player_stats

def help_list():
    return"List of commands: " + "\n.register\n" + ".word\n" + ".level\n" + ".stats\n" + ".practice_battle\n"

client.run(token)

#battle has error - update the update table in index
#check after every enemy's attack if player's hp is 0
#create function to subtract health from database directly
#make dev commands only accessable to specific roles
#create function to update variables from database
