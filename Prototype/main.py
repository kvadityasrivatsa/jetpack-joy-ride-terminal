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
V_CONST = 2
A_CONST = 1

#-------------------------------------------------------------------------------------#
#								      | METHODS |								      #
#-------------------------------------------------------------------------------------#

def setup():

	colorama.init()
	for j in range(SCRN_WIDTH):
		for i in range(SCRN_HEIGHT):
			plot(i,j," ","","BLACK")
	print("\033[2J" + "\033[0;0H")
	background_update(0)

	# for j in range(SCRN_WIDTH-10):
	# 	plot(GAME_BOUNDARY_D,j,"=","WHITE","")

def background_update(offset):
	brick = ['|','_','_','_','_','_']
	margin = 0
	# while(1):
	# if(offset<1):
	# 	offset=5
	i=0
	while(i<=SCRN_WIDTH-4-offset-10):
		plot(offset+i,GAME_BOUNDARY_D-1,"___","BLUE","")
		plot(offset+i,WALL_WIDTH,"_|_","BLUE","")
		i+=1

	for j in range(WALL_WIDTH):		# UPPER BOUNDARY
		i = 0
		if(j%2):
			margin = 0
		else:
			margin = 3
		while(i<=SCRN_WIDTH-6-offset-10):
			plot(offset+i+margin,j,brick[i%len(brick)],"GREEN","")
			i+=1   

	for j in range(WALL_WIDTH):		# LOWER BOUNDARY
		i = 0
		if(j%2):
			margin = 0
		else:
			margin = 3
		while(i<=SCRN_WIDTH-6-offset-10):
			plot(offset+i+margin,j+GAME_BOUNDARY_D,brick[i%len(brick)],"GREEN","")
			i+=1     	      
		# offset-=1
		# time.sleep(0.02)
#----------------------------------------#

def plot(x,y):
	print("\033[" + str(x) + ";" + str(y) + "H" + "" + " ")

#----------------------------------------#	

def plot(y,x,string,fore_col,back_col):

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
		if(self.pos_y>GAME_BOUNDARY_D-1):
			self.vel_y=0
			self.pos_y=GAME_BOUNDARY_D-1
		plot(self.pos_x, self.pos_y, " ", "", "WHITE")	#shape

	def update_vel(self):
		# if(self.vel_x)
		self.vel_y -= self.acc_y*A_CONST

	def move_y(self, direction):

		if(direction == 'up'):
			self.vel_y -= 0.001
		# elif(direction == 'down'):
		# 	self.vel_x += 0.001

	def disp_vects(self):
		plot(0,0,"vel="+str(self.vel_y)+" acc_x="+str(self.acc_y), "WHITE", "BLACK")


class Player(Person):
	def __init__(self,x,y):
		Person.__init__(self,x,y)
		self.gravity = 0.0005
		self.acc_y += -1 * self.gravity

#-------------------------------------------------------------------------------------#
#									   | MAIN |										  #
#-------------------------------------------------------------------------------------#

setup()

game = Game(5)	# New game created

box = Player(40,10)
# box.render_test()
# time.sleep(2)
# box.update_pos(20,10)
# box.render_test()

bcg_counter = 0
bcg_iter = 5

while(keyboard.is_pressed('b')==0):
	pass

while(keyboard.is_pressed('z')==0):

	box.update_pos()
	box.update_vel()
	box.disp_vects()
	if(keyboard.is_pressed('w')):
		box.move_y('up')
	# elif(keyboard.is_pressed('s')):
	# 	box.move_y('down')
	# elif(keyboard.is_pressed('a')):
	# 	box.move('left')
	# elif(keyboard.is_pressed('d')):
	# 	box.move('right')

	bcg_counter+=1
	if(bcg_counter>50):
		background_update(bcg_iter)
		bcg_iter-=1
		if(bcg_iter<0):
			bcg_iter = 5

	time.sleep(0.005)

terminate()

