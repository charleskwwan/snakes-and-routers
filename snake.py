# COMP112 Final Project - Snakes and Routers
# 	A distributed game of Snake
# 	by: Peter Lee and Charles Wan
#	on: 11/2/16

import pygame
from constants import *

# SnakePart: represents one secton of the snake (many sections)
class SnakePart(object):
	def __init__(self, cell, color):
		self.col = cell[0]
		self.row = cell[1]
		self.x = self.col * CELL_LEN
		self.y = self.row * CELL_LEN
		self.color = color

	# function to draw on board
	def blit(self, screen):
		part = pygame.Rect(self.x, self.y, CELL_LEN, CELL_LEN)
		pygame.draw.rect(screen, self.color, part)

# Snake represents the entire snake
class Snake(object):
	def __init__(self, cell, length, hd_color, bd_color, direction):
		# positioning
		self.col = cell[0]
		self.row = cell[1]
		self.x = self.col * CELL_LEN
		self.y = self.row * CELL_LEN

		# head details
		self.hd_color = hd_color
		self.head = SnakePart(cell, hd_color)

		# movement details
		self.dir_col = direction[0]
		self.dir_row = direction[1]

		# body details
		self.length = length
		self.tail = []
		self.bd_color = bd_color
		# create snake body
		nxt_col = self.head.col - self.dir_col
		nxt_row = self.head.row - self.dir_row
		for i in range(0, self.length - 1):
			self.tail.append(SnakePart((nxt_col, nxt_row), bd_color))
			nxt_col -= self.dir_col
			nxt_row -= self.dir_row

		# overall details
		self.score = 0
		self.is_dead = False
		self.vulnerable_in = 10 # at 0, snake becomes vulnerable

	# draw snake on screen
	def blit(self, screen):
		for part in self.tail:
			part.blit(screen)
		self.head.blit(screen)

	# move snake, potentially with change in direction
	def move(self):
		# change direction if necessary
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP and self.dir_row != +1:
					self.dir_col = 0
					self.dir_row = -1
				elif event.key == pygame.K_DOWN and self.dir_row != -1:
					self.dir_col = 0
					self.dir_row = +1
				elif event.key == pygame.K_LEFT and self.dir_col != +1:
					self.dir_col = -1
					self.dir_row = 0
				elif event.key == pygame.K_RIGHT and self.dir_col != -1:
					self.dir_col = +1
					self.dir_row = 0
				else:
					continue
				break
		# extend/move snake based on direction
		self.tail.insert(0, SnakePart((self.col, self.row), self.bd_color))
		self.col = (self.col + self.dir_col) % (SCR_WIDTH / CELL_LEN)
		self.row = (self.row + self.dir_row) % (SCR_HEIGHT / CELL_LEN)
		self.x = self.col * CELL_LEN
		self.y = self.row * CELL_LEN
		self.head = SnakePart((self.col, self.row), self.hd_color) # head
		if len(self.tail) > self.length - 1:
			self.tail.pop(len(self.tail) - 1) # remove last part in tail

	# checks if self includes the given cell
	def collidesWith(self, cell):
		for part in [self.head] + self.tail:
			if cell[0] == part.col and cell[1] == part.row:
				return True
		return False

	# checks if this snake has collided with another or itself
	def collideSnake(self, snakes):
		for part in self.tail:
			if self.col == part.col and self.row == part.row:
				return True
		for snake in snakes:
			if self == snake:
				continue
			elif snake.collidesWith((self.col, self.row)):
				return True
		return False

	def increaseLength(self):
		self.score += 1
		self.length += 1

	def update(self, screen):
		self.move()
		self.blit(screen)
