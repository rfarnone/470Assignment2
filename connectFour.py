import random
from random import randrange
import numpy as np
import math

ROW_COUNT = 6
COLUMN_COUNT = 7

EMPTY = 0
PLAYER = 7
AI = 9

WIN_LEN = 4
depth = 5

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT), dtype=int)
	return board

def is_valid_location(board, column):
	"""Validates placement of piece"""
	return board[0][column] == 0

def get_next_open_row(board, col):
	"""Finds the next open row in given column"""
	for r in range(ROW_COUNT-1, 0, -1):
		if board[r][col] == 0:
			return r

def insert (board, row, column, piece):
	"""Insert the color in the given column."""
	board[row][column] = piece

def getWinner (board, piece):
	"""Get the winner on the current board."""
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluate_window(window, piece):
	score = 0
	opp = PLAYER
	if piece == PLAYER:
		opp = AI

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 10
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 5

	if window.count(opp) == 3 and window.count(EMPTY) == 1:
		score -= 8

	return score

def score_position(board, piece):
	"""Scores Positions for AI"""
	score = 0

	# Score center colum
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count*6

	# Score horizontal locations
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WIN_LEN]
			score += evaluate_window(window, piece)

	# Score vertical locations
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WIN_LEN]
			score += evaluate_window(window, piece)

	# Score for positive slope diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WIN_LEN)]
			score += evaluate_window(window, piece)

	# Score for negative slop diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WIN_LEN)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return getWinner(board, PLAYER) or getWinner(board, AI) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if getWinner(board, AI):
				return (None, 10000000)
			elif getWinner(board, PLAYER):
				return (None, -10000000)
			else: #this is a tie
				return (None, 0)
		else:
			return (None, score_position(board, AI))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			copy_board = board.copy()
			insert(copy_board, row, col, AI)
			temp, new_score = minimax(copy_board, depth-1, alpha, beta, False)
			if new_score > value:
				value = new_score
				column = col
			alpha = max(value, alpha)
			if alpha >= beta:
				break
		return column, value

	else: # minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			copy_board = board.copy()
			insert(copy_board, row, col, PLAYER)
			temp, new_score = minimax(copy_board, depth-1, alpha, beta, True)
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def print_board(board):
	for i in board:
		for j in i:
			print(j, end=" ")
		print()
	print()

def get_valid_locations(board):
	"""Checks if locations are available for scoring"""
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):
	"""Picks the best move for the AI"""
	valid_locations = get_valid_locations(board)
	best_score = 0
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		insert(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col


if __name__ == '__main__':
	board = create_board()
	game_over = False
	turn = random.choice([PLAYER, AI])
	while not game_over:
		print_board(board)
		while turn == PLAYER:
			row = input('{}\'s turn: '.format('Red' if turn == PLAYER else 'Black'))
			if is_valid_location(board, int(row)):
				r = get_next_open_row(board, int(row))
				insert(board, r, int(row), turn)

				if getWinner(board, turn):
					print("Red wins!!")
					print_board(board)
					game_over = True
				turn = AI if turn == PLAYER else PLAYER
			else:
				print("Pick valid row\n")
		while turn == AI:
			row, minimax_score = minimax(board, depth, -math.inf, math.inf, True)
			if is_valid_location(board, int(row)):
				r = get_next_open_row(board, row)
				insert(board, r, int(row), turn)
				if getWinner(board, turn):
					print("Black wins!!")
					print_board(board)
					game_over = True
				turn = AI if turn == PLAYER else PLAYER
	if game_over:
		exit()