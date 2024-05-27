from random import randrange
import numpy as np

NONE = '.'
RED = 'R'
BLACK = 'B'

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 1
AI = 2

class Game:
	def __init__ (self, cols = COLUMN_COUNT, rows = ROW_COUNT, requiredToWin = 4):
		"""Create a new game."""
		self.cols = cols
		self.rows = rows
		self.win = requiredToWin
		self.board = np.zeros((ROW_COUNT,COLUMN_COUNT), dtype=int)

	def is_valid_location(self, column):
		return self.board[0][column] == 0

	def get_next_open_row(self, col):
		for r in range(ROW_COUNT-1, 0, -1):
			if self.board[r][col] == 0:
				return r

	def insert (self, row, column, color):
		"""Insert the color in the given column."""
		self.board[row][column] = color


	def checkForWin (self, piece):
		"""Check the current board for a winner."""
		w = self.getWinner(piece)
		if w:
			return True

	def getWinner (self, piece):
		"""Get the winner on the current board."""
		# Check horizontal locations for win
		for c in range(COLUMN_COUNT-3):
			for r in range(ROW_COUNT):
				if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
					return True

		# Check vertical locations for win
		for c in range(COLUMN_COUNT):
			for r in range(ROW_COUNT-3):
				if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
					return True

		# Check positively sloped diaganols
		for c in range(COLUMN_COUNT-3):
			for r in range(ROW_COUNT-3):
				if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
					return True

		# Check negatively sloped diaganols
		for c in range(COLUMN_COUNT-3):
			for r in range(3, ROW_COUNT):
				if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
					return True

	def printBoard (self):
		"""Print the board."""
		print('  '.join(map(str, range(self.cols))))
		for y in range(self.rows):
			print('  '.join(str(self.board[y][x]) for x in range(self.cols)))
		print()


if __name__ == '__main__':
	g = Game()
	game_over = False
	turn = PLAYER
	while not game_over:
		g.printBoard()
		while turn == PLAYER:
			row = input('{}\'s turn: '.format('Red' if turn == PLAYER else 'Black'))
			if g.is_valid_location(int(row)):
				r = g.get_next_open_row(int(row))
				g.insert(r, int(row), turn)

				if g.checkForWin(turn):
					print("Red wins!!")
					game_over = True
				turn = AI if turn == PLAYER else PLAYER
			else:
				print("Pick valid row\n")

		while turn == AI:
			row = int(randrange(7))
			if g.is_valid_location(int(row)):
				r = g.get_next_open_row(row)
				g.insert(r, int(row), turn)
				if g.checkForWin(turn):
					print("Black wins!!")
					game_over = True
				turn = AI if turn == PLAYER else PLAYER
	if game_over:
		exit()