# PokerBot.py

import os
import discord
from discord.ext import commands
from Scripts import seleniumScraper

PLAYER_IDENTIFIERS = {'\'', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '?'}
# get tokens
CURRENT_GAME_LINK = None
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


# #####COMMANDS######

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
    if discord_name is None:
        discord_name = ctx.message.author
    starting_score = 0
    with open(SCORES_FILE, encoding='utf-8', mode='r+') as f:
        # check if player identifier/discord_name is already in use
        used_identifiers = set()
        used_discord_names = []
        for entry in f:
            entry = entry.split(',')
            used_identifiers.add(entry[0])
            used_discord_names.append(entry[1])
        if player_iden in used_identifiers:
            await client.say(f"Identifier already in use. Choose from: {PLAYER_IDENTIFIERS - used_identifiers}")
        elif discord_name in used_discord_names:
            await client.say("Discord ID already in use.")
        elif discord_name is None:
            await client.say(f"Added {discord_name} with identifier "
                             f"{player_iden} to the leader board with a score of {starting_score}")
            f.write(f"{player_iden},{discord_name},{starting_score}\n")
        elif player_iden[0] not in PLAYER_IDENTIFIERS:
            await client.say(f"Please use a valid player identifier from {PLAYER_IDENTIFIERS}")
        elif discord_name is not None:
            await client.say(f"Added {discord_name} with identifier "
                             f"{player_iden} to the leader board with a score of {starting_score}")
            f.write(f"{player_iden},{discord_name},{starting_score}\n")


# Info Poker Start Command
@client.command(pass_context=True)
async def start(ctx):
    global CURRENT_GAME_LINK
    CURRENT_GAME_LINK = seleniumScraper.start_poker_game()  # this has significant delay
    await client.say(f"Starting poker game at: {CURRENT_GAME_LINK}")


# Poker End Command
@client.command(pass_context=True)
async def end(ctx):
    if CURRENT_GAME_LINK is not None:
        await client.say(f"Poker game on: {CURRENT_GAME_LINK} over, scores recorded")

    else:
        await client.say("No poker game active. Use $start to generate a link.")
    global CURRENT_GAME_LINK
    CURRENT_GAME_LINK = None


# Poker scores
@client.command(pass_context=True)
async def scores(ctx):
    response = f"Current leader board:\n"
    with open(SCORES_FILE, encoding='utf-8', mode='r') as f:
        leader_board = []
        for i in f:
            i = i.split(',')
            newdict = dict(id=i[1], score=int(i[2][0]), identifier=i[0])
            leader_board.append(newdict)
    # Sort scores
    print(leader_board)
    leader_board = sorted(leader_board, key=lambda x: x['score'], reverse=True)
    print(leader_board)
    for i in leader_board:
        temp = f"{i['id']}:{i['score']}\n"
        response += temp
    await client.say(response)


# #######EVENTS########

# Called when the bot connects to the server
@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    await client.change_presence(game=discord.Game(name='type $commands'))


# #######POKER GAME FUNCTIONS######### #
def parse_game_log(log_lines):
    pass


client.run(TOKEN)
