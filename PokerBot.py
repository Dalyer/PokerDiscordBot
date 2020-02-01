# PokerBot.py

import os
import time
import datetime
import asyncio
import discord
from discord.ext import commands
from Scripts import seleniumScraper

PLAYER_IDENTIFIERS = {'\'', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '?'}
# get tokens
CURRENT_GAME_LINK = None
GAME_DRIVER = None
TOKEN = ""
dirName = os.getcwd()
CONFIG_FILE = os.path.join(dirName, 'config.txt')
SCORES_FILE = os.path.join(dirName, 'scores.txt')
LOG_FILE = os.path.join(dirName, 'logs.txt')

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
    if str(ctx.message.author) == 'Dalyer#5373':
        print("Bot going offline")
        GAME_DRIVER.quit()     # close firefox-esr sessions
        await client.logout()


# list all commands command
@client.command(pass_context=True)
async def commands(ctx):
    # UPDATE THIS LIST
    await client.say(
        f"Poker related commands:\n{bot_prefix}start: [no arguments]Starts a new poker game and returns a link\n"
        f"{bot_prefix}end: [no arguments]Updates leader boards and stops tracking the last game\n"
        f"{bot_prefix}scores Display the leader board\n"
        f"{bot_prefix}add[player_name][discord_id][player_identifier]"
        f"(noargs = poster's discord id): add a player to leader board tracking\n"
        f"{bot_prefix}how: tells ya how\n"
        f"{bot_prefix}errors: Where to send errors")


# placeholder for the let it go meme
@client.command(pass_context=True)
async def let_go(ctx):
    await client.say("https://i.imgur.com/vKcJOHu.jpg")


@client.command(pass_context=True)
async def hulk(ctx):
    await client.say("Hulk would have killed everybody :BibleThump:")


@client.command(pass_context=True)
async def add(ctx, player_iden=None, discord_name=None):
    # format in the text file (line start)PLAYER_IDENTIFIER,Discord_author,score,rounds won
    games_won = 0
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
        if player_iden is None:
            await client.say(f"Please Include an identifier from{PLAYER_IDENTIFIERS - used_identifiers}")
        elif player_iden in used_identifiers:
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
            f.write(f"{player_iden},{discord_name},{starting_score},{games_won}\n")


# Info Poker Start Command
@client.command(pass_context=True)
async def start(ctx):           # TODO major error, can't approve new seats with out the original window
    global CURRENT_GAME_LINK, GAME_DRIVER
    CURRENT_GAME_LINK = seleniumScraper.start_poker_game() # this has significant delay
    await client.say(f"Starting poker game at: {CURRENT_GAME_LINK}")

    # add new players to the game
    while CURRENT_GAME_LINK is not None:
        await asyncio.sleep(5)
        seleniumScraper.accept_seat_requests(GAME_DRIVER)


# Poker End Command
@client.command(pass_context=True)
async def end(ctx):
    global CURRENT_GAME_LINK, GAME_DRIVER
    if CURRENT_GAME_LINK is not None:
        log_lines = seleniumScraper.get_log_lines(CURRENT_GAME_LINK, GAME_DRIVER)
        new_scores = parse_game_log(log_lines)
        update_scores(new_scores)
        GAME_DRIVER.close()
        await client.say(f"Poker game over, scores recorded")
    else:
        await client.say("No poker game active. Use $start to generate a link.")

    CURRENT_GAME_LINK = None
    GAME_DRIVER = None


# Poker scores
@client.command(pass_context=True)
async def scores(ctx):
    response = f"Current leader board:\n"
    with open(SCORES_FILE, encoding='utf-8', mode='r') as f:
        leader_board = []
        for i in f:
            i = i.split(',')
            newdict = dict(id=i[1], score=int(i[2]), identifier=i[0], games_won=i[3])
            leader_board.append(newdict)
    # Sort scores
    print(leader_board)
    leader_board = sorted(leader_board, key=lambda x: x['score'], reverse=True)
    print(leader_board)
    for i in leader_board:          # TODO add a proper table
        temp = f"{i['id']} | Score = {i['score']} | Hands Won = {i['games_won']}\n"
        response += temp
    await client.say(response)


@client.command(pass_context=True)
async def how(ctx):
    await client.say(f"How to get started\n"
                     f"1. Make sure to add yourself to the leader board using the{bot_prefix}add command\n"
                     f"2. Use the {bot_prefix}start command to start a poker game, use the link provided\n"
                     f"3. In order to have your score properly tracked you NEED to include your chosen PLAYER"
                     f" IDENTIFIER at the beginning of your in-game name\n"
                     f"4. Type $startgame in the poker chat once you are ready\n"
                     f"5. Once you want to stop tracking the game use the {bot_prefix}end command")


@client.command(pass_context=True)
async def errors(ctx):
    await client.say("This hasn't been tested properly so I wouldn't be surprised if there is some weird behaviour, also if the poker now website decides to change stuff it will break."
                     "Just send me a DM with any errors at Dalyer#5373 or submit and issue at https://github.com/Dalyer/PokerDiscordBot")


# #######EVENTS########

# Called when the bot connects to the server
@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    global GAME_DRIVER
    GAME_DRIVER = seleniumScraper.start_webdriver()
    print("Starting webdriver")
    print("Live")
    await client.change_presence(game=discord.Game(name='type $commands'))


# #######POKER GAME FUNCTIONS######### #
def parse_game_log(log_lines):
    trackable_players = get_players()

    for i in log_lines:
        for player in trackable_players:
            if i['player'] == player['identifier']:
                score_change = 0
                # determine valid player stack changes
                if i['action_type'] == "win":      # positive stack changes
                    score_change = i['stack_change']
                    player['games_won'] += 1

                elif i['action_type'] == 'calls':  # negative stack changes
                    if player['last_action']['action_type'] == 'blind':
                        if i['betting_cycle'] != player['last_action']['betting_cycle']:
                            score_change = i['stack_change'] * -1
                        else:
                            score_change = (i['stack_change'] - int(player['last_action']['stack_change'])) * -1
                    elif player['last_action']['action_type'] == 'calls':    # case 3
                        # check if new betting round has began or its looped
                        if i['betting_cycle'] == player['last_action']['betting_cycle']:
                            score_change = (i['stack_change'] - int(player['last_action']['stack_change'])) * -1
                        else:
                            score_change = i['stack_change'] * -1
                    elif player['last_action']['action_type'] == 'raises':
                        if i['betting_cycle'] == player['last_action']['betting_cycle']:
                            score_change = (i['stack_change'] - int(player['last_action']['stack_change'])) * -1
                        else:
                            score_change = i['stack_change'] * -1
                    else:
                        score_change = i['stack_change'] * -1

                elif i['action_type'] == 'raises':
                    if player['last_action']['action_type'] == 'blind':
                        if i['betting_cycle'] != player['last_action']['betting_cycle']:
                            score_change = i['stack_change'] * -1
                        else:
                            score_change = (i['stack_change'] - int(player['last_action']['stack_change'])) * -1
                    elif player['last_action']['action_type'] == 'calls':    # case 3
                        # check if new betting round has began or its looped
                        if i['betting_cycle'] == player['last_action']['betting_cycle']:
                            score_change = (i['stack_change'] - int(player['last_action']['stack_change'])) * -1
                        else:
                            score_change = i['stack_change'] * -1
                    elif player['last_action']['action_type'] == 'raises':
                        if i['betting_cycle'] == player['last_action']['betting_cycle']:
                            score_change = (i['stack_change'] - int(player['last_action']['stack_change'])) * -1
                        else:
                            score_change = i['stack_change'] * -1
                    else:
                        score_change = i['stack_change'] * -1
                elif i['action_type'] == 'blind':       # case 1
                    score_change = i['stack_change'] * -1
                player['score'] = player['score'] + score_change
                print(player['score'], player['id'], i['action_type'], (player['last_action']['action_type']),
                      i['betting_cycle'], player['last_action']['betting_cycle'])
                player['last_action'] = i
    return trackable_players


def get_players():
    with open(SCORES_FILE, encoding='utf-8', mode='r') as f:
        players = []
        for i in f:
            i = i.split(',')
            # initialize betting cycles
            newdict = dict(id=i[1], score=int(i[2]), identifier=i[0], games_won=int(i[3]),
                           last_action=dict(action_type=None, betting_cycle=1))
            players.append(newdict)
    return players


def update_scores(new_scores):
    with open(SCORES_FILE, encoding='utf-8', mode='r+') as f:
        f.truncate()
        for player in new_scores:
            f.write(f"{player['identifier']},{player['id']},{player['score']},{player['games_won']}\n")

                    
def log(message):
    time_stamp = time.localtime()
    message = time_stamp.tm_year + "-" + time_stamp.tm_month + "-" + time_stamp.tm_day + "  " + time_stamp.tm_hour ":" + time_stamp.tm_min + ":" + time_stamp.tm_sec + "   " + message + "\n"
    with open(LOG_FILE, encoding='utf-8', mode='r+') as f:
        f.write(message)
    print(message)
                    
client.run(TOKEN)
