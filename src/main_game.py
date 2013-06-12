from grid import Grid, BaseGrid
from config import grid_size, null_char
from random import shuffle

# Represents a single player in the game
# Each player has a personality which decides the strategy
class PlayerHolder(object):
    def __init__(self, personality):
        self.personality = personality
        self.grid = Grid()


class LeaderboardEventHandler(object):
    def letterPlaced(self, player, letter, coord):
        pass

    def gameComplete(self, leaderboard):
        print "Scoreboard:"
        print '\n'.join(["%s - %d [%d]" % (l.personality.name, l.score, l.cum_score) for l in leaderboard])

    def letterChosen(self, player, letter):
        pass
    def newTurn(self, turnNumber):
        print "# Turn", turnNumber


class ConsoleGameEventHandler(object):
    def letterPlaced(self, player, letter, coord):
        print player.personality.name, 'placed', letter, 'at', coord
        print player.grid
    def gameComplete(self, leaderboard):
        print "Scoreboard:"
        print '\n'.join(["%s - %d" % (l.personality.name, l.score) for l in leaderboard])

        for player in leaderboard:
            print '===', player.personality.name, '==='
            print 'Grid:'
            print player.grid
            print 'Words:'
            print ', '.join(["%s %x" % (w, len(w)) for w in player.scoring_words])
            print 'Total:', player.score
    def letterChosen(self, player, letter):
        pass
    def newTurn(self, turnNumber):
        print "# Turn", turnNumber

def playGame(player_personalities, game_event_handler=ConsoleGameEventHandler(), num_games=1):
    players = [PlayerHolder(p) for p in player_personalities]

    for player in players:
        player.cum_score = 0

    def chooseLetter(player):
        letter = player.personality.chooseLetter(player.grid).lower()
        game_event_handler.letterChosen(player, letter)
        return letter

    def placeLetter(player, letter):
        coord = player.personality.placeLetter(player.grid, letter)
        if (player.grid.getLetter(coord[0], coord[1]) != null_char):
            raise InputException("Cannot place letter at %x,%x" % coord)
        game_event_handler.letterPlaced(player, letter, coord)
        return player.grid.setLetter(coord[0], coord[1], letter)

    def completeGame():
        for player in players:
            # take last turn
            letter = chooseLetter(player)
            placeLetter(player, letter)

        for player in players:
            assert null_char not in player.grid.grid
            player.scoring_words = player.grid.getScoringWords()
            player.score = sum([len(x) for x in player.scoring_words])
            player.cum_score += player.score

        leaderboard = sorted(players, key=lambda player: player.cum_score, reverse=True)
        return leaderboard


    def play_game():
        turn = 1
        for player in players:
            player.grid = Grid()
        shuffle(players)

        while True:
            for player in players:
                game_event_handler.newTurn(turn)
                if turn > grid_size * grid_size - 1:
                    leaderboard = completeGame()
                    game_event_handler.gameComplete(leaderboard)
                    return

                turn += 1
                letter = chooseLetter(player)

                for player in players:
                    placeLetter(player, letter)

    for i in xrange(num_games):
        print "Starting game {}".format(i)
        play_game()
