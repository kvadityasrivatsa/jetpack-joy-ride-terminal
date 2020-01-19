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
GAME_BOUNDARY_R = SCRN_WIDTH - 5
VY_CONST = 2.7
VX_CONST = 1
A_CONST = 1
GAME_SPD = 100

#-------------------------------------------------------------------------------------#
#								      | METHODS |								      #
#-------------------------------------------------------------------------------------#

def setup():

	colorama.init()
	for j in range(SCRN_WIDTH):
		for i in range(SCRN_HEIGHT):
			plot(i,j," ","","BLACK")
	print("\033[2J" + "\033[0;0H")

	i=0
	while(i<=SCRN_WIDTH-4):
		plot(i,GAME_BOUNDARY_D+1,"[]","BLUE","")
		plot(i,WALL_WIDTH,"[]","BLUE","")
		i+=2
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

def plot_obj(obj):	#obj MUST have a body array (rel_x,rel_y,ascii,fore_col,back_col)
	

#----------------------------------------#

# def deploy_tokens():
# 	fire_beam = []
# 	for i in range(10):
# 		fire_beam.append(Token(0,10,(i+1)*100))
# 	return fire_beam

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

		self.vel_x = 0
		self.vel_y = 0

		self.acc_x = 0
		self.acc_y = 0

		self.body_array = [[self.pos_x,self.pos_y]]

	def render_test(self):
		plot(self.pos_x, self.pos_y, " ", "", "BLUE")

	def define_pos(self,x,y):
		plot(self.pos_x, self.pos_y, " ", "", "BLACK")
		self.pos_x = x
		self.pos_y = y

	def disp_vects(self):
		plot(0,0,"vel="+str(self.vel_y)+" acc_y="+str(self.acc_y), "WHITE", "BLACK")

#----------------------------------------#

class Kinitos(Entity):
	def __init__(self,x,y):
		Entity.__init__(self,x,y)
		self.gravity = 0.00002
		self.acc_y += -1 * self.gravity

	def update_pos(self):
		plot(self.pos_x, self.pos_y, " ", "", "BLACK")
		self.pos_x = self.pos_x + self.vel_x*VX_CONST
		self.pos_y = self.pos_y + self.vel_y*VY_CONST
		if(self.pos_y>GAME_BOUNDARY_D):
			self.vel_y=0
			self.pos_y=GAME_BOUNDARY_D
		elif(self.pos_y<GAME_BOUNDARY_U):
			self.vel_y=0
			self.pos_y=GAME_BOUNDARY_U
		plot(self.pos_x, self.pos_y, " ", "", "WHITE")	#shape

	def update_vel(self):
		self.vel_y -= self.acc_y*A_CONST

	def move_up(self):
			self.vel_y -= 0.00006

#----------------------------------------#

class Token(Entity):	# Fire beams, Magnets & COINS$$
	def __init__(self,frame_loc,y):
		Entity.__init__(self,0,y)	# self.x is not applicable till token is rendered
		self.frame_loc = frame_loc
		self.status = False

	def activate_token(self):
		self.vel_x -= 0.01
		self.pos_x = GAME_BOUNDARY_R
		self.status = True

	def deactivate_token(self):
		self.vel_x = 0
		self.pos_x = -1
		self.status = False

	def if_collision(self,x,y):
		for i in self.body_array:
			if(int(x)==int(i[0]) and int(y)==int(i[1])):
				return 1
		return 0

	def render(self):
		print("{"+"X:"+str(self.pos_x)+","+"Y:"+str(self.pos_y)+",Vx:"+str(self.vel_x)+"}")
		plot(self.pos_x, self.pos_y, " ", "", "BLACK")
		self.pos_x = self.pos_x + self.vel_x*VX_CONST
		plot(self.pos_x, self.pos_y, " ", "", "YELLOW")

#-------------------------------------------------------------------------------------#
#									   | MAIN |										  #
#-------------------------------------------------------------------------------------#

setup()

game = Game(5)	# New game created

box = Kinitos(80,10)

token_list = []
token_list.append(Token(200,20))

while(keyboard.is_pressed('b')==0):
	pass
	
frame_L_pos = 5
frame_R_pos = GAME_BOUNDARY_R - 5

# GAME ON
while(keyboard.is_pressed('z')==0):

	for i in token_list:
		if(i.frame_loc<=frame_R_pos and i.status==False):
			i.activate_token()
		elif(i.frame_loc<=frame_L_pos and i.status==True):
			i.deactivate_token()

	for i in token_list:
		if(i.status==True):
			i.render()

	print(box.pos_x,box.pos_y)

	# if(token_list[0].if_collision(box.pos_x,box.pos_y)):
	# 	print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

	box.update_pos()
	box.update_vel()
	box.disp_vects()

	if(keyboard.is_pressed("w")):
		box.move_up()


	frame_L_pos+=(1/GAME_SPD)	# 1/game spd
	frame_R_pos+=(1/GAME_SPD)	# 1/game spd

	print("L:", frame_L_pos, ", ", "R:", frame_R_pos)

	time.sleep(0.001) 	# game 1/fps
# DED

print("QUIT? press q")
while(keyboard.is_pressed('q')==0):
	pass

terminate()

