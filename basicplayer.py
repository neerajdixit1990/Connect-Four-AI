from util import memoize, run_search_function

def basic_evaluate(board):
    """
    The original focused-evaluate function from the lab.
    The original is kept because the lab expects the code in the lab to be modified. 
    """
    if board.is_game_over():
        # If the game has been won, we know that it must have been
        # won or ended by the previous move.
        # The previous move was made by our opponent.
        # Therefore, we can't have won, so return -1000.
        # (note that this causes a tie to be treated like a loss)
        score = -1000
    else:
        score = board.longest_chain(board.get_current_player_id()) * 10
        # Prefer having your pieces in the center of the board.
        for row in range(6):
            for col in range(7):
                if board.get_cell(row, col) == board.get_current_player_id():
                    score -= abs(3-col)
                elif board.get_cell(row, col) == board.get_other_player_id():
                    score += abs(3-col)

    return score


def get_all_next_moves(board):
    """ Return a generator of all moves that the current player could take from this position """
    from connectfour import InvalidMoveException

    for i in xrange(board.board_width):
        try:
            yield (i, board.do_move(i))
        except InvalidMoveException:
            pass

def is_terminal(depth, board):
    """
    Generic terminal state check, true when maximum depth is reached or
    the game has ended.
    """
    return depth <= 0 or board.is_game_over()


# This is the recursive function which would be called to evaluate all the boards

def minimax_helper(board, depth, eval_fn, nodes_exp,
            	   get_next_moves_fn = get_all_next_moves,
            	   is_terminal_fn = is_terminal,
            	   verbose = True):
	if (depth < 0):
		return [0,-1,-1]

	# Initialize the MAX tuple for MAX player and MIN tuple for MIN player
	# 1st value is score
	# 2nd value is the corresponding column number
	# 3rd value is the nodes expanded for arriving at the solution
	max_tup = [-2000, -1, nodes_exp]
	min_tup = [2000, -1, nodes_exp]
	for col in range(board.board_width):
		height = board.get_height_of_column(col)
		#height of -1 indicates that column is full
		if (height != -1):
			if (is_terminal_fn(depth, board)):
				#If terminal node then call the eval function and get score of board
				leaf_score = eval_fn(board)
				nodes_exp = nodes_exp + 1
				curr_score_tup = [leaf_score, col, nodes_exp]
			else:
				#If non-terminal state go to more depth and explore more options
				new_board = board.do_move(col);
				curr_score_tup = minimax_helper(new_board, depth-1, eval_fn, nodes_exp)
			
			nodes_exp = curr_score_tup[2]
			if (depth%2 == 0):		#MAX Player
				# Even depth indicates a MAX player
				if (curr_score_tup[0] > max_tup[0]):
					max_tup[0] = curr_score_tup[0]
					max_tup[1] = curr_score_tup[1]
			elif (depth%2 == 1):		#MIN Player
				# Odd depth indicates a MIN player
				if (curr_score_tup[0] < min_tup[0]):
					min_tup[0] = curr_score_tup[0]
					min_tup[1] = curr_score_tup[1]

	# return appropriate tuple based on MAX or MIN player	
	if (depth%2 == 0):
		max_tup[2] = nodes_exp
		return max_tup
	elif (depth%2 == 1):
		min_tup[2] = nodes_exp
		return min_tup					
				
# Minimax function which would return the column # where the peg is inserted
def minimax(board, depth, eval_fn,
            get_next_moves_fn = get_all_next_moves,
            is_terminal_fn = is_terminal,
            verbose = True):
	
	final_score = minimax_helper(board, depth, eval_fn, 0, get_next_moves_fn,
				     is_terminal_fn, verbose)
	print "MINI-MAX evaluated %s boards (nodes expanded) to select column %s" % (final_score[2], final_score[1])
	return final_score[1]

def rand_select(board):
    """
    Pick a column by random
    """
    import random
    moves = [move for move, new_board in get_all_next_moves(board)]
    return moves[random.randint(0, len(moves) - 1)]


# This is new evaluate which is more smarter than the naive basic_evaluate

# The strategy of the new_evaluate is as follows in descending order of importance:
# 1) Avoid defeat by blocking opponent, block the opponents chain which already have 2 or 3 pegs inline
# 2) Try to maximize the longest chain by current player
#    (Longest chain of 2 and 3 considered)

def new_evaluate(board):
	score = 0
    	
	# Check who has won the game
	if board.is_game_over():
		# If board is won, the it is won by previous move
		# This means that opponent has won and that is why we return losing score
		#else
		# we return a winning score
		if board.is_win() == board.get_current_player_id():
			score = -1000
		elif board.is_win() == board.get_other_player_id(): 
        		score = 1000
		return score

	# calculate max chain maintained by current player
	# But this chain can be blocked by opponents move, so we have to check whether
	# the current max chain can be used for winning the board
	# I have considered chains of 2 and 3 pegs inline and adjusted score accordingly

	max_self_chain = board.longest_chain(board.get_current_player_id())
	if max_self_chain >= 2:
		for row in range(6):
            		for col in range(7):
				if board.get_cell(row, col) == board.get_current_player_id():
					# Each of the if conditions consider the formation of longest
					# chain in all directions like (1,1), (1,-1), (0,1) or (-1,0)
					# If this chain can be used for winning then the corresponding
					# column number should be free at that time
					if board._contig_vector_length(row, col, (1,1))+1 == 3 and \
						(row+3) == board.get_height_of_column(col+3):
						score = score + 30
                                        if board._contig_vector_length(row, col, (1,-1))+1 == 3 and \
                                                (row+3) == board.get_height_of_column(col-3):
                                                score = score + 30
                                        if board._contig_vector_length(row, col, (0,-1))+1 == 3 and \
                                                (row) == board.get_height_of_column(col-3):
                                                score = score + 30
                                        if board._contig_vector_length(row, col, (-1,-1))+1 == 3 and \
                                                (row-3) == board.get_height_of_column(col-3):
                                                score = score + 30
                                        if board._contig_vector_length(row, col, (-1,0))+1 == 3 and \
                                                (row-3) == board.get_height_of_column(col):
                                                score = score + 30
                                        if board._contig_vector_length(row, col, (-1,1))+1 == 3 and \
                                                (row-3) == board.get_height_of_column(col+3):
                                                score = score + 30
                                        if board._contig_vector_length(row, col, (0,1))+1 == 3 and \
                                                (row) == board.get_height_of_column(col+3):
                                                score = score + 30
                                        if board._contig_vector_length(row, col, (1,1))+1 == 2 and \
                                                (row+2) == board.get_height_of_column(col+2):
                                                score = score + 20
                                        if board._contig_vector_length(row, col, (1,-1))+1 == 2 and \
                                                (row+2) == board.get_height_of_column(col-2):
                                                score = score + 20
                                        if board._contig_vector_length(row, col, (0,-1))+1 == 2 and \
                                                (row) == board.get_height_of_column(col-2):
                                                score = score + 20
                                        if board._contig_vector_length(row, col, (-1,-1))+1 == 2 and \
                                                (row-2) == board.get_height_of_column(col-2):
                                                score = score + 20
                                        if board._contig_vector_length(row, col, (-1,0))+1 == 2 and \
                                                (row-2) == board.get_height_of_column(col):
                                                score = score + 20
                                        if board._contig_vector_length(row, col, (-1,1))+1 == 2 and \
                                                (row-2) == board.get_height_of_column(col+2):
                                                score = score + 20
                                        if board._contig_vector_length(row, col, (0,1))+1 == 2 and \
                                                (row) == board.get_height_of_column(col+2):
                                                score = score + 20

	# The same logic goes for opponents chain as well
        # calculate max chain maintained by opposite player
        # check whether the current max chain can lead to a winning board
	# If yes, then we deduct score so that we avoid this move

	max_opponent_chain = board.longest_chain(board.get_other_player_id())
	if max_opponent_chain >= 2:
                for row in range(6):
                        for col in range(7):
                                if board.get_cell(row, col) == board.get_other_player_id():
                                        # Each of the if conditions consider the formation of longest as earlier
                                        # If this chain can lead to a losing board, then we deduct score 
                                        if board._contig_vector_length(row, col, (1,1))+1 == 3 and \
                                                (row+3) == board.get_height_of_column(col+3):
                                                score = score - 30
                                        if board._contig_vector_length(row, col, (1,-1))+1 == 3 and \
                                                (row+3) == board.get_height_of_column(col-3):
                                                score = score - 30
                                        if board._contig_vector_length(row, col, (0,-1))+1 == 3 and \
                                                (row) == board.get_height_of_column(col-3): 
                                                score = score - 30
                                        if board._contig_vector_length(row, col, (-1,-1))+1 == 3 and \
                                                (row-3) == board.get_height_of_column(col-3):
                                                score = score - 30
                                        if board._contig_vector_length(row, col, (-1,0))+1 == 3 and \
                                                (row-3) == board.get_height_of_column(col):
                                                score = score - 30
                                        if board._contig_vector_length(row, col, (-1,1))+1 == 3 and \
                                                (row-3) == board.get_height_of_column(col+3):
                                                score = score - 30
                                        if board._contig_vector_length(row, col, (0,1))+1 == 3 and \
                                                (row) == board.get_height_of_column(col+3): 
                                                score = score - 30
					if board._contig_vector_length(row, col, (1,1))+1 == 2 and \
                                                (row+2) == board.get_height_of_column(col+2):
                                                score = score - 20
                                        if board._contig_vector_length(row, col, (1,-1))+1 == 2 and \
                                                (row+2) == board.get_height_of_column(col-2):
                                                score = score - 20
                                        if board._contig_vector_length(row, col, (0,-1))+1 == 2 and \
                                                (row) == board.get_height_of_column(col-2): 
                                                score = score - 20
                                        if board._contig_vector_length(row, col, (-1,-1))+1 == 2 and \
                                                (row-2) == board.get_height_of_column(col-2):
                                                score = score - 20
                                        if board._contig_vector_length(row, col, (-1,0))+1 == 2 and \
                                                (row-2) == board.get_height_of_column(col):
                                                score = score - 20
                                        if board._contig_vector_length(row, col, (-1,1))+1 == 2 and \
                                                (row-2) == board.get_height_of_column(col+2):
                                                score = score - 20
                                        if board._contig_vector_length(row, col, (0,1))+1 == 2 and \
                                                (row) == board.get_height_of_column(col+2): 
                                                score = score - 20
	
	return score	

random_player = lambda board: rand_select(board)
basic_player = lambda board: minimax(board, depth=4, eval_fn=basic_evaluate)
new_player = lambda board: minimax(board, depth=4, eval_fn=new_evaluate)
progressive_deepening_player = lambda board: run_search_function(board, search_fn=minimax, eval_fn=basic_evaluate)
