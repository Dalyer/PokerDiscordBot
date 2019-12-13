from requests_html import HTMLSession

session = HTMLSession()

GAME_LINK = "https://www.pokernow.club/games/XNA3A9xFNPpSuMFbUbz_n3KOY"

g = session.get(GAME_LINK)
g.html.render()   # needed to load the javascript

players = {}

# Make a dictionary of dictionaries for all the players
for i in range(1, 10):
    j = i+2
    player = g.html.find(f'div:nth-child(1) div:nth-child(1) div.main-container.two-color div.table > div.table-player.table-player-{i}:nth-child({j})', first=True).text
    player = player.split('\n')

    if len(player) == 3:        # no restarts
        newdict = dict(status=player[0], name=player[1], score=player[2], restarts=0)
    elif len(player) > 3:       # restarts
        newdict = dict(status=player[0], restarts=player[1], name=player[2], score=player[3])
    else:                       # no player at that slot
        continue
    tmp = "player" + str(i)
    players[tmp] = newdict

# TODO Deal with game states:
# 1. Player Lobby(DONE)
# 2. All Players standing up(Same as 1.DONE)
# 3. Folded players
# 4. The Dealer
# 5. The People with bets
# 6. The people without bets
print(players)

