"""This file contains a collection of player classes for comparison with your
own agent and example heuristic functions.

    ************************************************************************
    ***********  YOU DO NOT NEED TO MODIFY ANYTHING IN THIS FILE  **********
    ************************************************************************
"""

from random import randint
import numpy as np
import time
import random
import matplotlib.pyplot as plt



def null_score(game, player):
    """This heuristic presumes no knowledge for non-terminal states, and
    returns the same uninformative value for all other states.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state.
    """

    if game.is_loser(player):
        return 1

    if game.is_winner(player):
        return +1

    return 0.


def multimax(game, player,iteration = 0):
    """The basic evaluation function described in lecture that outputs a score
    equal to the number of moves open for your computer player on the board.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """

    # print "######################"


    iteration += 1;


    if game.is_loser(player):
       _score_list = [+1,+1,+1]
       _score_list[game.get_player()] = -2
       # print "dddd"
       return _score_list, (-1,-1),1
        
    # if game.is_winner(player):
    #    return 1, (-1,-1)
    

    # print game.to_string()
    # time.sleep(1)


    legal_moves = game.get_legal_moves()


    best,score_list,utility_list,move_list,num = 0,[],[],[],0

    for i, move in enumerate(legal_moves):
        _game = game.forecast_move(move)

        _slist, _move, _num = multimax(_game,game.inactive_players[0],iteration)

        score_list.append(_slist[game.get_player()])
        utility_list.append(_slist);
        move_list.append(move)

        num += _num

        # print best,score_list,utility_list,move_list


    best = np.argmax(score_list) 

    return utility_list[best],move_list[best],num
        


class PlayerWithRandom():
    """Player that chooses a move randomly."""

    def get_move(self, game, time_left):
        """Randomly select a move from the available legal moves.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            A randomly selected legal move; may return (-1, -1) if there are
            no available legal moves.
        """
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        # print game.to_string()
        return legal_moves[randint(0, len(legal_moves) - 1)]


class PlayerWithAI():
    """Player that chooses next move to maximize heuristic score. This is
    equivalent to a minimax search agent with a search depth of one.
    """

    def __init__(self, score_fn=multimax):
        self.score = score_fn
        self.num = 0
    def get_num(self):
        return self.num

    def get_move(self, game, time_left):
        """Select the move from the available legal moves with the highest
        heuristic score.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            The move in the legal moves list with the highest heuristic score
            for the current game state; may return (-1, -1) if there are no
            legal moves.
        """
        # legal_moves = game.get_legal_moves()
        # if not legal_moves:
        #     return (-1, -1)
        # _, move = max([(self.score(game.forecast_move(m), self), m) for m in legal_moves])
        _, move,num =  self.score(game,self)
        self.num += num
        # print game.board_state
        #print game.to_string()
        return move


class HumanPlayer():
    """Player that chooses a move according to user's input."""

    def get_move(self, game, time_left):
        """
        Select a move from the available legal moves based on user input at the
        terminal.

        **********************************************************************
        NOTE: If testing with this player, remember to disable move timeout in
              the call to `Board.play()`.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            The move in the legal moves list selected by the user through the
            terminal prompt; automatically return (-1, -1) if there are no
            legal moves
        """
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)

        # print(game.to_string()) #display the board for the human player
        # print(('\t'.join(['[%d] %s' % (i, str(move)) for i, move in enumerate(legal_moves)])))

        valid_choice = False
        while not valid_choice:
            try:
                index = int(input('Select move index:'))
                valid_choice = 0 <= index < len(legal_moves)

                if not valid_choice:
                    print('Illegal move! Try again.')

            except ValueError:
                print('Invalid index! Try again.')

        return legal_moves[index]


if __name__ == "__main__":
    from isolation import Board

    # create an isolation board (by default 7x7)
    player1 = PlayerWithAI()
    player2 = PlayerWithRandom()
    player3 = PlayerWithRandom()
    game_num = 100
    config = [[3,4],[4,3],[4,4],[4,5],[5,4]]

    for i in range(5):
        width = config[i][0]
        height = config[i][1]
        p1_wins = 0
        p2_wins = 0
        p3_wins = 0

        p1_win_arr = []
        p2_win_arr = []
        p3_win_arr = []

        for _ in range(game_num):
            game = Board(player1, player2, player3,width,height)
            m1, m2, m3 = random.sample(range(0, width*height), 3)


            # place player 1 on the board at row 2, column 3, then place player 2 on
            # the board at row 0, column 5; display the resulting board state.  Note
            # that the .apply_move() method changes the calling object in-place.
            game.apply_move((m1/width, m1%width))
            game.apply_move((m2/width, m2%width))
            game.apply_move((m3/width, m3%width))
            # print(game.to_string())

            # get a list of the legal moves available to the active player
            # print(game.get_legal_moves())

            # # get a successor of the current state by making a copy of the board and
            # # applying a move. Notice that this does NOT change the calling object
            # # (unlike .apply_move()).
            # new_game = game.forecast_move((1, 1))

            # print("\nOld state:\n{}".format(game.to_string()))
            # print("\nNew state:\n{}".format(new_game.to_string()))

            # play the remainder of the game automatically -- outcome can be "illegal
            # move", "timeout", or "forfeit"
            winners, history, outcome = game.play()

            # print("\nWinner: {}\nOutcome: {}".format(winners[0], outcome))
            # print("\nWinner: {}\nOutcome: {}".format(winners[1], outcome))
            # # print(game.to_string())
            # print("Move history:\n{!s}".format(history))

            if (id(winners[0]) == id(player1)) or (id(winners[1]) == id(player1)):
                p1_wins += 1
            
            p1_win_arr.append(p1_wins)


            if (id(winners[0]) == id(player2)) or (id(winners[1]) == id(player2)):
                p2_wins += 1
            
            p2_win_arr.append(p2_wins)

            if (id(winners[0]) == id(player3)) or (id(winners[1]) == id(player3)):
                p3_wins += 1
            
            p3_win_arr.append(p3_wins)

        print player1.get_num()

        plt.subplot(1,5,i+1)
        plt.plot(range(0,100), p1_win_arr, label="p1")
        plt.plot(range(0,100), p2_win_arr, label="p2")
        plt.plot(range(0,100), p3_win_arr, label="p3")

        print ("------------------------")
        print (p1_wins,p2_wins,p3_wins)
        print ()

    plt.show()


    
