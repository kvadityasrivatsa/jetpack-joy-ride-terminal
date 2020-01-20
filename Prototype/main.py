import colorama
from colorama import Fore, Back, Style
import numpy
import keyboard
import time
import math

#-------------------------------------------------------------------------------------#
#								     | CONSTANTS |								      #
#-------------------------------------------------------------------------------------#

SCRN_WIDTH = 153 # 153
SCRN_HEIGHT = 40
WALL_WIDTH = 4
GAME_BOUNDARY_U = 6
GAME_BOUNDARY_D = SCRN_HEIGHT-WALL_WIDTH+1
GAME_BOUNDARY_L = 2
GAME_BOUNDARY_R = SCRN_WIDTH - 5
VY_CONST = 2.7
VX_CONST = 1
A_CONST = 1
GAME_SPD = 0.02

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

	if(y < GAME_BOUNDARY_L or y > GAME_BOUNDARY_R):
		return 0

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

def plot_obj(obj, mode):	#obj MUST have a body array (rel_x,rel_y,ascii,fore_col,back_col)
	
	if(mode=="plot"):
		for i in obj.body_array:
			plot(obj.pos_x+i[0],obj.pos_y+i[1],i[2],i[3],i[4])
		  	# plot(obj.pos_x, obj.pos_y, " ", "", "YELLOW")
	elif(mode=="clear"):
		for i in obj.body_array:
			plot(obj.pos_x+i[0],obj.pos_y+i[1]," ","","BLACK")
			# plot(obj.pos_x, obj.pos_y, " ", "", "YELLOW")

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

		self.body_array = []
		self.bound_U = 0
		self.bound_D = 0
		self.bound_L = 0
		self.bound_R = 0

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
		plot_obj(self,"clear")
		self.pos_x = self.pos_x + self.vel_x*VX_CONST
		self.pos_y = self.pos_y + self.vel_y*VY_CONST
		if(self.pos_y>GAME_BOUNDARY_D):
			self.vel_y=0
			self.pos_y=GAME_BOUNDARY_D
		elif(self.pos_y<GAME_BOUNDARY_U):
			self.vel_y=0
			self.pos_y=GAME_BOUNDARY_U
		plot_obj(self,"plot")

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
		self.vel_x -= GAME_SPD
		self.pos_x = GAME_BOUNDARY_R
		self.status = True
		# print("Token Activated")

	def deactivate_token(self):
		self.vel_x = 0
		self.pos_x = 400
		self.status = False
		plot_obj(self,"clear")
		# print("Token Deactivated")

	def if_collision(self,x,y):
		for i in self.body_array:
			if(int(x)==int(i[0]+self.pos_x) and int(y)==int(i[1]+self.pos_y)):
				return True

	def render(self):
		plot_obj(self,"clear")
		self.pos_x = self.pos_x + self.vel_x*VX_CONST
		plot_obj(self,"plot")

#----------------------------------------#

class Fire_Beam(Token):
	def __init__(self,frame_loc,y,angle,length):
		Token.__init__(self,frame_loc,y)
		self.token_type = "fire_beam"
		self.damage = 1
		self.health = 1

		if(angle==0):
			for i in range(length):
					self.body_array.append([i,0,"<","BLACK","RED"])
			self.bound_L = 0
			self.bound_R = 10

		# elif(angle==90):
		# 	if()

#----------------------------------------#

class Player(Kinitos):
	def __init__(self,x,y):
		Kinitos.__init__(self,x,y)
		self.body_array = [[0,0," ","","BLUE"],[0,1," ","","MAGENTA"],[1,0," ","","MAGENTA"],[1,1," ","","BLUE"]]

	def if_hit(self,tok):
		for i in self.body_array:
			if(tok.if_collision(i[0]+self.pos_x,i[1]+self.pos_y)):
				return True

#-------------------------------------------------------------------------------------#
#									   | MAIN |										  #
#-------------------------------------------------------------------------------------#

setup()

game = Game(5)	# New game created

ares = Player(30,10)

token_list = []
token_list.append(Fire_Beam(170,20,0,10))
token_list.append(Fire_Beam(200,30,0,10))
token_list.append(Fire_Beam(160,30,0,10))

while(keyboard.is_pressed('b')==0):
	pass
	
frame_L_pos = 0
frame_R_pos = GAME_BOUNDARY_R - 3

# GAME ON
while(keyboard.is_pressed('z')==0):

	for i in token_list:
		if(i.frame_loc+i.bound_L<=frame_R_pos and i.frame_loc>frame_L_pos and i.status==False):
			i.activate_token()
		if(i.frame_loc+i.bound_R<=frame_L_pos and i.status==True):
			i.deactivate_token()

	for i in token_list:
		if(i.status==True):
			i.render()

	ares.update_pos()
	ares.update_vel()
	ares.disp_vects()

	for i in token_list:
		# if(i.status==True):
		if(ares.if_hit(i)==True):
			plot(40,40,'@',"GREEN","CYAN")

	if(keyboard.is_pressed("w")):
		ares.move_up()


	frame_L_pos+=(GAME_SPD)	# 1/game spd
	frame_R_pos+=(GAME_SPD)	# 1/game spd

	# print("L:", frame_L_pos, ", ", "R:", frame_R_pos)

	time.sleep(0.001) 	# game 1/fps
# DED

# print("QUIT? press q")
while(keyboard.is_pressed('q')==0):
	pass

terminate()

