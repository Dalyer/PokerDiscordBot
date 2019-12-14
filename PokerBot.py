# PokerBot.py

import os
import discord
from discord.ext import commands
from Scripts import seleniumScraper

# get tokens
TOKEN = ""
dirName = os.getcwd()
CONFIG_FILE = os.path.join(dirName, 'config.txt')

config = open(CONFIG_FILE, encoding='utf-8', mode='r')

for line in config:
    if line.startswith("token"):
        tmp = line.split("=")
        TOKEN = tmp[1].strip()
config.close()

# instance of Client()
Client = discord.Client()
# bot prefix it responds to
bot_prefix = "!"
client = commands.Bot(command_prefix=bot_prefix)


######COMMANDS######

# ping command
@client.command(pass_context=True)
async def ping(ctx):
    await client.say("Pong!")


# logout command
@client.command(pass_context=True)
async def logout(ctx):
    await client.say("Going offline.")
    print("Bot going offline")
    await client.logout()


# list all commands command
@client.command(pass_context=True)
async def commands(ctx):
    # UPDATE THIS LIST
    await client.say(f"Poker related commands:\n{bot_prefix}start: [no arguments]Generates a new poker game and returns a link\n
                     {bot_prefix}end: [no arguments]Updates leaderboards and stops tracking the last game\n
                     {bot_prefix}scores: [no arguments]Display the leaderboard\n
                     {bot_prefix}get_score [player/player_identifier](no args=poster's score): More specfic individual player stats\n
                     {bot_prefix}add [player_name] [discord_id] [player_identifier](no args=poster's discord id): add a player to leaderboard tracking\n
                     ")


# placeholder for the let it go meme
@client.command(pass_context=True)
async def let_go(ctx):
    await client.say("https://i.imgur.com/vKcJOHu.jpg")


@client.command(pass_context=True)
async def hulk(ctx):
    await client.say("Hulk would have killed everybody :BibleThump:")


# Info Poker Start Command
@client.command(pass_context=True)
async def start(ctx):
    link = seleniumScraper.start_poker_game()    # this has significant delay
    await client.say(f"Starting poker game at: {link}")
    # how to get stuff from the end of a message such as a link
    # make a spider to scrape the score from the poker link and check every minute


# Poker End Command
@client.command(pass_context=True)
async def end(ctx):
    await client.say(f"Poker game on: {link} over scores recorded")


# Poker scores
@client.command(pass_context=True)
async def scores(ctx):
    await client.say("scores")


########EVENTS########

# Called when the bot connects to the server
@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    await client.change_presence(game=discord.Game(name='type !commands'))


# Give the option to grab scores based on the players, identifiers, or discord ID
def get_scores(player=None, player_iden=None, discord_id=None):
    if (player, player_iden, disord_id) is None:
        raise InputError # discord_id should always be provided
    # finish, io's
    


    
client.run(TOKEN)

