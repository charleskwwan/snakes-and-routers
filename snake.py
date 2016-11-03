# COMP112 Final Project - Snakes and Routers
# 	A distributed game of Snake
# 	by: Peter Lee and Charles Wan
#	on: 11/2/16

import pygame

CELL_LEN = 10
SCREEN_WID = 50 # cells
SCREEN_HGT = 50

# SnakePart: represents one section of the snake (many sections)
#	assumed: each cell is 10 by 10 pixels
class SnakePart(object):
	# cell_x and cell_y is the x and y of the cell
	# x and y is based on true pixels
	def __init__(self, cell_pos, color):
		self.cell_x = cell_pos[0] # set which cell
		self.cell_y = cell_pos[1]
		self.x = self.cell_x * CELL_LEN # get true x, y
		self.y = self.cell_y * CELL_LEN
		self.color = color

	# function called to draw part on board
	def blit(self, screen):
		part = pygame.Rect(self.x, self.y, CELL_LEN, CELL_LEN)
		pygame.draw.rect(screen, self.color, part)

# Snake: represents an entire snake
class Snake(object):
	def __init__(self, init_cell_pos, init_len, hd_color, bd_color, init_dir):
		# positioning details
		self.cell_x = init_cell_pos[0] # set which cell
		self.cell_y = init_cell_pos[1]
		self.x = self.cell_x * CELL_LEN # get true x, y
		self.y = self.cell_y * CELL_LEN

		# head details
		self.hd_color = hd_color
		self.head = SnakePart((self.cell_x, self.cell_y), self.hd_color)

		# movement details
		self.dir_x = init_dir[0]
		self.dir_y = init_dir[1]

		# body details
		self.length = init_len # does not include head
		self.tail = [] # body parts
		self.bd_color = bd_color
		# create initial snake body, based on initial direction
		nxt_x = self.head.cell_x + self.dir_x
		nxt_y = self.head.cell_y + self.dir_y
		for i in range(0, self.length):
			self.tail.append(SnakePart((nxt_x, nxt_y), bd_color))
			nxt_x += self.dir_x
			nxt_y += self.dir_y

		#overall details
		self.is_dead = False
		self.vulnerable_in = 10 # once at 0, snake becomes vulnerable

	def update(self, screen, snakes):
		self.move()
		self.blit(screen)
		# if self.vulnerable_in > 0:
		# 	self.vulnerable_in -= 1
		# self.move()
		# self.blit(screen)
		# if self.vulnerable_in <= 0:
		# 	for s in snakes:
		# 		if self.collideWithSnake(s):
		# 			self.is_dead = True
		# 			self.die()

	# actions to be completed if the snake dies, respawn
	def die(self):
		print "Dead!" # todo: respwan snake at new random positionE

	# checks if self has collided with a given snake
	#	need to run thru every part of self against every part of other snake
	#	since invulnerability at beginning
	def collideWithSnake(self, snake):
		self_parts = [self.head] + self.tail
		other_parts = [snake.head] + snake.tail
		for s in self_parts:
			for o in other_parts:
				if s.x == o.x and s.y == o.y:
					return True
		return False

	# to be used when eating fruit
	def increaseLength(self):
		self.length += 1

	# update position based on user key
	def move(self, dt):

		key = pygame.key.get_pressed()
		if key[pygame.K_UP] and self.dir_y != +1:
			self.dir_x = 0
			self.dir_y = -1
		elif key[pygame.K_DOWN] and self.dir_y != -1:
			self.dir_x = 0
			self.dir_y = +1
		elif key[pygame.K_LEFT] and self.dir_x != +1:
			self.dir_x = -1
			self.dir_y = 0
		elif key[pygame.K_RIGHT] and self.dir_x != -1:
			self.dir_x = +1
			self.dir_y = 0
		print "DIR {} {}".format(self.dir_x, self.dir_y)
		# extend snake
		self.tail.insert(0, SnakePart((self.cell_x, self.cell_y), self.bd_color)) # add head to tail
		self.cell_x += self.dir_x # todo: wrap around screen
		self.cell_x += self.dir_y 
		self.head = SnakePart((self.cell_x, self.cell_y), self.hd_color) # move head
		if len(self.tail) > self.length:
			self.tail.pop(len(self.tail) - 1) # remove last part in tail

	def blit(self, screen):
		self.head.blit(screen)
		for p in self.tail:
			p.blit(screen)
