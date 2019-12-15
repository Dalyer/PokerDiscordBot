# PokerBot.py

import os
import discord
from discord.ext import commands
from Scripts import seleniumScraper

PLAYER_IDENTIFIERS = ['\'', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '?']
# get tokens
TOKEN = ""
dirName = os.getcwd()
CONFIG_FILE = os.path.join(dirName, 'config.txt')
SCORES_FILE = os.path.join(dirName, 'scores.txt')

config = open(CONFIG_FILE, encoding='utf-8', mode='r')

for line in config:
    if line.startswith("token"):
        tmp = line.split("=")
        TOKEN = tmp[1].strip()
config.close()

# instance of Client()
Client = discord.Client()
# bot prefix it responds to
bot_prefix = "$"
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
    await client.say(
        f"Poker related commands:\n{bot_prefix}start: [no arguments]Generates a new poker game and returns a link\n"
        f"{bot_prefix}end: [no arguments]Updates leader boards and stops tracking the las tgame\n"
        f"{bot_prefix}Display the leader board\n{bot_prefix}get_score[player / player_identifier]"
        f"(noargs = poster's score): More specific individual player stats\n"
        f"{bot_prefix}add[player_name][discord_id][player_identifier]"
        f"(noargs = poster's discord id): add a player to leader board tracking\n")


# placeholder for the let it go meme
@client.command(pass_context=True)
async def let_go(ctx):
    await client.say("https://i.imgur.com/vKcJOHu.jpg")


@client.command(pass_context=True)
async def hulk(ctx):
    await client.say("Hulk would have killed everybody :BibleThump:")


@client.command(pass_context=True)
async def add(ctx, player_iden, discord_name=None):
    # format in the text file (line start)PLAYER_IDENTIFIER,Discord_author,score
    starting_score = 0
    with open(SCORES_FILE, encoding='utf-8', mode='r+') as f:
        if discord_name is None:
            await client.say(f"Added {ctx.message.author} with identifier "
                             f"{player_iden} to the leader board with a score of {starting_score}")
            f.write(f"{player_iden},{ctx.message.author},{starting_score}")
        elif player_iden[0] not in PLAYER_IDENTIFIERS:
            await client.say(f"Please use a valid player identifier from {PLAYER_IDENTIFIERS}")
        elif discord_name is not None:
            await client.say(f"Added {discord_name} with identifier "
                             f"{player_iden} to the leader board with a score of {starting_score}")
            f.write(f"{player_iden},{discord_name},{starting_score}")


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
    await client.say(f"Poker game on: {link} over scores recorded")   # add link soon


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
    await client.change_presence(game=discord.Game(name='type $commands'))


def load_scores():
    scores_file = os.path.join(dirName, 'scores.txt')
    scores = open(scores_file, encoding='utf-8', mode='r+')
    scores.close()


# Give the option to grab scores based on the players, identifiers, or discord ID
def get_scores(player=None, player_iden=None, discord_id=None):
    if (player, player_iden, discord_id) is None:
        raise TypeError  # discord_id should always be provided
    # finish, io's


client.run(TOKEN)
