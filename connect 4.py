import numpy as np
import pygame
import sys
import math
#rgb color
GREEN = (0,155,0)
BLACK =(0,0,0)
ORANGE = (255,155,0)
WHITE = (255,255,255)

ROW_COUNT = 6
COLUNM_COUNT = 7

def create_board():
	board = np.zeros((ROW_COUNT,COLUNM_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0 :
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizon for win
	for c in range(COLUNM_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check ventical for win
	for c in range(COLUNM_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positive slope for win
	for c in range(COLUNM_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negative slope for win
	for c in range(COLUNM_COUNT-3):
		for r in range(3 ,ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(board):
	for c in range(COLUNM_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, GREEN , (c*SQUARESIZE , r*SQUARESIZE+SQUARESIZE , SQUARESIZE , SQUARESIZE))
			pygame.draw.circle(screen, BLACK , (int(c*SQUARESIZE+SQUARESIZE/2) , int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

	for c in range(COLUNM_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == 1:
				pygame.draw.circle(screen, ORANGE , (int(c*SQUARESIZE+SQUARESIZE/2) , height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2:
				pygame.draw.circle(screen, WHITE , (int(c*SQUARESIZE+SQUARESIZE/2) , height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUNM_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("Time New Roman", 80)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0,width,SQUARESIZE))
			posx = event.pos[0]-(SQUARESIZE/2)
			if turn == 0:
				pygame.draw.rect(screen, ORANGE , (posx,0,SQUARESIZE,SQUARESIZE))
			else :
				pygame.draw.rect(screen, WHITE , (posx,0,SQUARESIZE,SQUARESIZE))
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0,width,SQUARESIZE))
			#print(event.pos)
			#ask input of p1
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE)) #col = int(input("p1 choose 0-6"))
				
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row ,col, 1)

					if winning_move(board, 1):
						label = myfont.render("Orange win!!!" , 1 ,ORANGE) #print("p1 win!!!")
						screen.blit(label ,(160,20))
						game_over = True


			#ask input of p2
			else:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE)) #col = int(input("p2 choose 0-6"))
				
				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row ,col, 2)

					if winning_move(board, 2):
						label = myfont.render("White win!!!" , 1 ,WHITE) #print("p2 win!!!")
						screen.blit(label ,(190,20))
						game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

			if game_over:
				pygame.time.wait(5000)