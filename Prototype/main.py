import colorama
from colorama import Fore, Back, Style
import numpy
import keyboard
import time
import math
import classes
import methods

#-------------------------------------------------------------------------------------#
#								     | CONSTANTS |								      #
#-------------------------------------------------------------------------------------#

SCRN_WIDTH = 153
SCRN_HEIGHT = 40
WALL_WIDTH = 4
GAME_BOUNDARY_U = 6
GAME_BOUNDARY_D = SCRN_HEIGHT-WALL_WIDTH+1
GAME_BOUNDARY_L = 28
GAME_BOUNDARY_R = 28
V_CONST = 1

#-------------------------------------------------------------------------------------#
#								      | METHODS |								      #
#-------------------------------------------------------------------------------------#

def setup():

	colorama.init()
	for j in range(SCRN_WIDTH):
		for i in range(SCRN_HEIGHT):
			plot(i,j," ","","BLACK")
	print("\033[2J" + "\033[0;0H")

	# for j in range(WALL_WIDTH):		# UPPER BOUNDARY
	# 	if(j%2):
	# 		i = 0
	# 	else:
	# 		i = 3
	# 	while(i<=SCRN_WIDTH-6):
	# 		plot(j,i,"|_____","GREEN","")
	# 		i+=6   

	# for j in range(WALL_WIDTH):		# LOWER BOUNDARY
	# 	if(j%2):
	# 		i = 0
	# 	else:
	# 		i = 3
	# 	while(i<=SCRN_WIDTH-6):
	# 		plot(j+GAME_BOUNDARY_D,i,"|_____","GREEN","")
	# 		i+=6   	      

#----------------------------------------#

def plot(x,y):
	print("\033[" + str(x) + ";" + str(y) + "H" + "" + " ")

#----------------------------------------#	

def plot(x,y,string,fore_col,back_col):

	if(fore_col == "BLACK"):
		fore_col_str = Fore.BLACK
	elif(fore_col == "RED"):
		fore_col_str = Fore.RED
	elif(fore_col == "GREEN"):
		fore_col_str = Fore.GREEN
	elif(fore_col == "YELLOW"):
		fore_col_str = Fore.YELLOW
	elif(fore_col == "BLUE"):
		fore_col_str = Fore.BLUE
	elif(fore_col == "MAGENTA"):
		fore_col_str = Fore.MAGENTA
	elif(fore_col == "CYAN"):
		fore_col_str = Fore.CYAN
	elif(fore_col == "WHITE"):
		fore_col_str = Fore.WHITE
	else:
		fore_col_str = ""

	if(back_col == "BLACK"):
		back_col_str = Back.BLACK
	elif(back_col == "RED"):
		back_col_str = Back.RED
	elif(back_col == "GREEN"):
		back_col_str = Back.GREEN
	elif(back_col == "YELLOW"):
		back_col_str = Back.YELLOW
	elif(back_col == "BLUE"):
		back_col_str = Back.BLUE
	elif(back_col == "MAGENTA"):
		back_col_str = Back.MAGENTA
	elif(back_col == "CYAN"):
		back_col_str = Back.CYAN
	elif(back_col == "WHITE"):
		back_col_str = Back.WHITE
	else:
		back_col_str = ""

	print("\033[" + str(int(x)) + ";" + str(int(y)) + "H" + fore_col_str + back_col_str + string)

#----------------------------------------#

def terminate():
	plot(SCRN_HEIGHT,0,"","","")

#-------------------------------------------------------------------------------------#
#								    | CLASSES |								          #
#-------------------------------------------------------------------------------------#

class Game():

	def __init__(self,spd):
		self.speed = spd

	def change_game_speed(self,new_spd):
		self.speed = new_spd

	def ret_game_speed(self):
		return self.speed

#----------------------------------------#

class Entity():

	def __init__(self,x,y):
		self.pos_x = x
		self.pos_y = y

	def render_test(self):
		plot(self.pos_x, self.pos_y, " ", "", "BLUE")

#----------------------------------------#

class Person(Entity):

	def __init__(self,x,y):
		Entity.__init__(self,x,y)
		self.vel_x = 0
		self.vel_y = 0

		self.acc_x = 0
		self.acc_y = 0

	def define_pos(self,x,y):
		plot(self.pos_x, self.pos_y, " ", "", "BLACK")
		self.pos_x = x
		self.pos_y = y

	def update_pos(self):
		plot(self.pos_x, self.pos_y, " ", "", "BLACK")
		self.pos_x = self.pos_x + self.vel_x*V_CONST
		self.pos_y = self.pos_y + self.vel_y*V_CONST
		plot(self.pos_x, self.pos_y, " ", "", "WHITE")

	def move(self, direction):

		if(direction == 'up'):
			self.vel_x -= 0.001
		elif(direction == 'down'):
			self.vel_x += 0.001
		elif(direction == 'left'):
			self.vel_y -= 0.001
		elif(direction == 'right'):
			self.vel_y += 0.001


#-------------------------------------------------------------------------------------#
#									   | MAIN |										  #
#-------------------------------------------------------------------------------------#

setup()

game = Game(5)	# New game created

box = Person(10,40)
# box.render_test()
# time.sleep(2)
# box.update_pos(20,10)
# box.render_test()
while(keyboard.is_pressed('z')==0):
	box.update_pos()

	if(keyboard.is_pressed('w')):
		box.move('up')
	elif(keyboard.is_pressed('s')):
		box.move('down')
	elif(keyboard.is_pressed('a')):
		box.move('left')
	elif(keyboard.is_pressed('d')):
		box.move('right')

	time.sleep(0.005)

terminate()

