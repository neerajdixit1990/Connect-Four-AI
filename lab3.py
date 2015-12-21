# Member 1
# Name: Neeraj Dixit
# Email: ndixit@cs.stonybrook.edu

# Member 2
# Name: Arnav Gupta
# Email: 

from util import INFINITY

### 1. Multiple choice

# 1.1. Two computerized players are playing a game. Player MM does minimax
#      search to depth 6 to decide on a move. Player AB does alpha-beta
#      search to depth 6.
#      The game is played without a time limit. Which player will play better?
#
#      1. MM will play better than AB.
#      2. AB will play better than MM.
#      3. They will play with the same level of skill.
ANSWER1 = 0

# 1.2. Two computerized players are playing a game with a time limit. Player MM
# does minimax search with iterative deepening, and player AB does alpha-beta
# search with iterative deepening. Each one returns a result after it has used
# 1/3 of its remaining time. Which player will play better?
#
#   1. MM will play better than AB.
#   2. AB will play better than MM.
#   3. They will play with the same level of skill.
ANSWER2 = 0

### 2. Connect Four
from connectfour import *
from basicplayer import *
from util import *
import tree_searcher
import time

## This section will contain occasional lines that you can uncomment to play
## the game interactively. Be sure to re-comment them when you're done with
## them.  Please don't turn in a problem set that sits there asking the
## grader-bot to play a game!
## 
## Uncomment this line to play a game as white:
#run_game(human_player, basic_player)

## Uncomment this line to play a game as black:
#run_game(basic_player, human_player)


# Play the basic player against a random player
# The number of nodes expanded and excution time are obtained accordingly

'''tic = time.clock()
run_game(basic_player, alphabeta_player)
toc = time.clock()
timeItr = toc - tic
print "Execution time for basic player : " + str(timeItr)'''





## Or watch the computer play against itself:
#run_game(basic_player, basic_player)

## Change this evaluation function so that it tries to win as soon as possible,
## or lose as late as possible, when it decides that one side is certain to win.
## You don't have to change how it evaluates non-winning positions.

def focused_evaluate(board):
    """
    Given a board, return a numeric rating of how good
    that board is for the current player.
    A return value >= 1000 means that the current player has won;
    a return value <= -1000 means that the current player has lost
    """    
    raise NotImplementedError


## Create a "player" function that uses the focused_evaluate function
quick_to_win_player = lambda board: minimax(board, depth=4,
                                            eval_fn=focused_evaluate)

## You can try out your new evaluation function by uncommenting this line:
#run_game(basic_player, quick_to_win_player)


## Write an alpha-beta-search procedure that acts like the minimax-search
## procedure, but uses alpha-beta pruning to avoid searching bad ideas
## that can't improve the result. The tester will check your pruning by
## counting the number of static evaluations you make.
##
## You can use minimax() in basicplayer.py as an example.
def alpha_beta_search(board, depth,
                      eval_fn,
                      # NOTE: You should use get_next_moves_fn when generating
                      # next board configurations, and is_terminal_fn when
                      # checking game termination.
                      # The default functions set here will work
                      # for connect_four.
                      get_next_moves_fn=get_all_next_moves,
		      is_terminal_fn=is_terminal):
	def alpha_beta_helper(board, depth, eval_fn, nodes_exp, alpha, beta, next_moves=get_all_next_moves, is_terminal_fn = is_terminal):
		
	        # Initialize the MAX tuple for MAX player and MIN tuple for MIN player
        	# 1st value in tuple is score
        	# 2nd value in tuple is the corresponding column number
		# 3rd value in tuple is the alpha value
		# 4th value in tuple is the beta value
        	# 5rd value in tuple is the nodes expanded for arriving at the solution

		max_tup = [-2000, -1, alpha, beta, nodes_exp]
		min_tup = [2000, -1, alpha, beta, nodes_exp]

                for col in range(board.board_width):
                        if alpha > beta:
				# Alpha-Beta prunning in action !!!
                        	break

			# Check if column is full by checking height
			height = board.get_height_of_column(col)
			if (height != -1):
	                        if (is_terminal_fn(depth, board)):
					# Evaluate board for terminal position
        	                        leaf_score = eval_fn(board)
					nodes_exp = nodes_exp + 1
        	                        curr_score_tup = [leaf_score, col, alpha, beta, nodes_exp]
                	        else:
                        	        #import pudb
                                	#pudb.set_trace()
					# Go deeper in case of non-terminal node
                                	new_board = board.do_move(col);
                                	curr_score_tup = alpha_beta_helper(new_board, depth-1, eval_fn, nodes_exp, alpha, beta)
				
				nodes_exp = curr_score_tup[4]
                        	if (depth%2 == 0):              #MAX Player
					# Update max tuple and alpha for MAX player
                                	if (curr_score_tup[0] > max_tup[0]):
                                        	max_tup[0] = curr_score_tup[0]
                                        	max_tup[1] = curr_score_tup[1]
						max_tup[2] = curr_score_tup[2]
						alpha = max_tup[2]
                        	elif (depth%2 == 1):            #MIN Player
					# Update min tuple and beta for MIN player
                                	if (curr_score_tup[0] < min_tup[0]):
                                        	min_tup[0] = curr_score_tup[0]
                                        	min_tup[1] = curr_score_tup[1]
						min_tup[3] = curr_score_tup[3]
						beta = min_tup[3]
		
		# return appropriate tuple based on MAX or MIN player	
      		if (depth%2 == 0):
			max_tup[4] = nodes_exp
                	return max_tup
        	elif (depth%2 == 1):
			min_tup[4] = nodes_exp
                	return min_tup

	final_score_tup = alpha_beta_helper(board, depth, eval_fn, 0, -2000, 2000, get_next_moves_fn,
                                     is_terminal_fn) 
	print "Alpha-beta evaluated %s boards (nodes expanded) to select column %s" % (final_score_tup[4], final_score_tup[1])
        return final_score_tup[1]

## Now you should be able to search twice as deep in the same amount of time.
## (Of course, this alpha-beta-player won't work until you've defined
## alpha-beta-search.)
#alphabeta_player = lambda board: alpha_beta_search(board,
#                                                   depth=8,
#                                                   eval_fn=focused_evaluate)
alphabeta_player = lambda board: alpha_beta_search(board, depth=4, eval_fn=new_evaluate)


## This player uses progressive deepening, so it can kick your ass while
## making efficient use of time:
ab_iterative_player = lambda board: \
    run_search_function(board,
                        search_fn=alpha_beta_search,
                        eval_fn=focused_evaluate, timeout=5)






# Play the alpha-beta player against a random player
# The number of nodes expanded and excution time are obtained accordingly

'''tic = time.clock()
run_game(new_player, basic_player)
toc = time.clock()
timeItr = toc - tic
print "Execution time for new player : " + str(timeItr)'''




tic = time.clock()
run_game(alphabeta_player, basic_player)
toc = time.clock()
timeItr = toc - tic
print "Execution time for Alpha-Beta player : " + str(timeItr)



## Finally, come up with a better evaluation function than focused-evaluate.
## By providing a different function, you should be able to beat
## simple-evaluate (or focused-evaluate) while searching to the
## same depth.

#def better_evaluate(board):
#    raise NotImplementedError

# Comment this line after you've fully implemented better_evaluate
better_evaluate = memoize(basic_evaluate)

# Uncomment this line to make your better_evaluate run faster.
# better_evaluate = memoize(better_evaluate)

# For debugging: Change this if-guard to True, to unit-test
# your better_evaluate function.
if False:
    board_tuples = (( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,0,0,0,0,0,0 ),
                    ( 0,2,2,1,1,2,0 ),
                    ( 0,2,1,2,1,2,0 ),
                    ( 2,1,2,1,1,1,0 ),
                    )
    test_board_1 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 1)
    test_board_2 = ConnectFourBoard(board_array = board_tuples,
                                    current_player = 2)
    # better evaluate from player 1
    print "%s => %s" %(test_board_1, better_evaluate(test_board_1))
    # better evaluate from player 2
    print "%s => %s" %(test_board_2, better_evaluate(test_board_2))

## A player that uses alpha-beta and better_evaluate:
your_player = lambda board: run_search_function(board,
                                                search_fn=alpha_beta_search,
                                                eval_fn=better_evaluate,
                                                timeout=5)

#your_player = lambda board: alpha_beta_search(board, depth=4,
#                                              eval_fn=better_evaluate)

## Uncomment to watch your player play a game:
#run_game(your_player, your_player)

## Uncomment this (or run it in the command window) to see how you do
## on the tournament that will be graded.
#run_game(your_player, basic_player)

## These three functions are used by the tester; please don't modify them!
def run_test_game(player1, player2, board):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return run_game(globals()[player1], globals()[player2], globals()[board])
    
def run_test_search(search, board, depth, eval_fn):
    assert isinstance(globals()[board], ConnectFourBoard), "Error: can't run a game using a non-Board object!"
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=globals()[eval_fn])

## This function runs your alpha-beta implementation using a tree as the search
## rather than a live connect four game.   This will be easier to debug.
def run_test_tree_search(search, board, depth):
    return globals()[search](globals()[board], depth=depth,
                             eval_fn=tree_searcher.tree_eval,
                             get_next_moves_fn=tree_searcher.tree_get_next_move,
                             is_terminal_fn=tree_searcher.is_leaf)
    
## Do you want us to use your code in a tournament against other students? See
## the description in the problem set. The tournament is completely optional
## and has no effect on your grade.
COMPETE = (None)

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "20 hours"
WHAT_I_FOUND_INTERESTING = "Min Max algorithm"
WHAT_I_FOUND_BORING = "The design for new eval funtion as we did not have much knowledge"
NAME = "Neeraj Dixit"
EMAIL = "ndixit@cs.stonybrook.edu"

