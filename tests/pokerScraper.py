from requests_html import HTMLSession

session = HTMLSession()

GAME_LINK = "https://www.pokernow.club/games/IojGnljcV-evf1fkEEtLHkd5T"

g = session.get(GAME_LINK)
g.html.render()   # needed to load the javascript

players = {}
ROUND_COUNTER = 0

# Make a dictionary of dictionaries for all the players
for i in range(1, 10):
    j = i+2
    #TODO next line doesn't work when scraper is the host?
    player = g.html.find(f'div:nth-child(1) div:nth-child(1) div.main-container.two-color div.table > div.table-player.table-player-{i}:nth-child({j})', first=True).text
    player = player.split('\n')

    if len(player) == 3:        # opening lobby no restarts
        newdict = dict(status=player[0], name=player[1], score=player[2], restarts=0)
    elif len(player) == 6:      # either dealer or restart case
        if (player[3] == 'Dealer'):
            newdict = dict(status="Playing", restarts=0, name=player[4], score=player[5])
        else:               # restarts present
            newdict = dict(status="Playing", restarts=player[3], name=player[4], score=player[5])
    elif len(player) == 5:      # dealer and no restarts
        newdict = dict(status="Playing", restarts=0, name=player[3], score=player[4])
    elif len(player) == 7:      # Case that they are the dealer and have restarts
        newdict = dict(status="Playing", restarts=player[4], name=player[5], score=player[6])
    elif len(player) == 4:       # 2 cases
        if (player[0] == int):  # starting round without restarts
            newdict = dict(status="Playing", restarts=0, name=player[2], score=player[3])
        else:                   # opening lobby with restarts
            newdict = dict(status=player[0], restarts=player[1], name=player[2], score=player[3])
    else:                       # no player at that slot
        print(player)
        continue
    tmp = "player" + str(i)
    players[tmp] = newdict

# TODO Test all the states I'm not sure if they all work:
# 1. Player Lobby(DONE)
# 2. All Players standing up(Same as 1.DONE)
# 3. Folded players(DONE?)
# 4. The Dealer/ buy ins(DONE)
# 5. Dealer with Restarts(DONE)
# 6. Deal with winning state where score is updated
# possibly don't need any of this and can just run off of the log....
print(players)

