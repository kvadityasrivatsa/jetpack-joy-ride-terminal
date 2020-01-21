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
FRAME_SPD = 0.02
BULLET_VEL = 0.02
GUN_TEMP = 5

#-------------------------------------------------------------------------------------#
#								      | METHODS |								      #
#-------------------------------------------------------------------------------------#

def setup():

	colorama.init()
	for j in range(SCRN_WIDTH):
		for i in range(SCRN_HEIGHT):
			plot(i,j," ","","BLACK","NORMAL")
	print("\033[2J" + "\033[0;0H")

	i=0
	while(i<=SCRN_WIDTH-4):
		plot(i,GAME_BOUNDARY_D+1,"[]","BLUE","","NORMAL")
		plot(i,WALL_WIDTH,"[]","BLUE","","NORMAL")
		i+=2
#----------------------------------------#

def plot_text(y,x,string):
	print("\033[" + str(x) + ";" + str(y) + "H" + Fore.WHITE + Fore.BLACK , string)

#----------------------------------------#	

def plot(y,x,string,fore_col,back_col,style):

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

	if(style == "NORMAL"):
		style_str = Style.NORMAL
	elif(style == "BRIGHT"):
		style_str = Style.BRIGHT
	elif(style == "DIM"):
		style_str = Style.DIM
	else:
		style_str = ""

	print("\033[" + str(int(x)) + ";" + str(int(y)) + "H" + fore_col_str + back_col_str + style_str + string)

def plot_obj(obj, mode):	#obj MUST have a body array (rel_x,rel_y,ascii,fore_col,back_col)
	
	if(mode=="plot"):
		for i in obj.body_array:
			plot(obj.pos_x+i[0],obj.pos_y+i[1],i[2],i[3],i[4],i[5])
	elif(mode=="clear"):
		for i in obj.body_array:
			plot(obj.pos_x+i[0],obj.pos_y+i[1]," ","","BLACK","NORMAL")

#----------------------------------------#

def token_generator():
	print("henlo")

#----------------------------------------#

def terminate():
	plot(SCRN_HEIGHT,0,"","","","")

#-------------------------------------------------------------------------------------#
#								    | CLASSES |								          #
#-------------------------------------------------------------------------------------#

class Game():

	def __init__(self,spd):
		self.speed = spd
		self.token_list = []
		self.bullet_list = []
		self.bullet_count = 0	# total shots fired
		self.ammo = 20
		self.mode = "NORMAL"

	def change_game_speed(self,new_spd):
		self.speed = new_spd

	def ret_game_speed(self):
		return self.speed

	def fire_bullet(self,player):
		self.bullet_count += 1
		bullet = Bullet(player.bound_R+player.pos_x+1,player.pos_y,BULLET_VEL,self.bullet_count)
		self.ammo -= 1
		self.bullet_list.append(bullet)

	def is_ammo(self):
		if(self.ammo>0):
			return True
		else:
			return False

	def display_ammo(self):
		plot_text(50,1,"                  ")
		plot_text(50,1,"Ammo: "+str(self.ammo))

	def bullet_out(self,bullet):
		if(bullet.pos_x>GAME_BOUNDARY_R):
			return True
		else:
			return False


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
		plot(self.pos_x, self.pos_y, " ", "", "BLUE","NORMAL")

	def define_pos(self,x,y):
		plot(self.pos_x, self.pos_y, " ", "", "BLACK","NORMAL")
		self.pos_x = x
		self.pos_y = y

	def disp_vects(self):
		plot(0,0,"vel="+str(self.vel_y)+" acc_y="+str(self.acc_y), "WHITE", "BLACK", "NORMAL")

#----------------------------------------#

class Kinitos(Entity):
	def __init__(self,x,y):
		Entity.__init__(self,x,y)
		self.damage = 0

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

	def if_hit_token(self,tok):
		for i in self.body_array:
			if(tok.if_collision(i[0]+self.pos_x,i[1]+self.pos_y)):
				return True

	def if_hit_kinitos(self,kino):	# if bullet hits a kinito
		for i in self.body_array:
			for j in kino.body_array:
				if(int(kino.pos_x + j[0]) == int(self.pos_x + i[0]) and int(kino.pos_y + j[1]) == int(self.pos_y + i[1])):
					return True

	def hit_confirmed(self,kino): # kino(agent) here may be a bullet or a quasar
		self.health -= kino.damage

#----------------------------------------#

class Token(Entity):	# Fire beams, Magnets & COINS$$
	def __init__(self,frame_loc,y):
		Entity.__init__(self,0,y)	# self.x is not applicable till token is rendered
		self.frame_loc = frame_loc
		self.status = False
		self.token_type = ""

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

	def redact(self):
		plot_obj(self,"clear")

#----------------------------------------#

class Fire_Beam(Token):
	def __init__(self,frame_loc,y,angle,length):
		Token.__init__(self,frame_loc,y)
		self.token_type = "fire_beam"
		self.damage = 1
		self.health = 1

		if(angle==0):
			for i in range(length):
				self.body_array.append([i,0,"<","BLACK","RED","NORMAL"])
			self.bound_L = 0
			self.bound_R = length

		elif(angle==90):
			if(y<(GAME_BOUNDARY_D+GAME_BOUNDARY_U)/2):	# upper half
				for i in range(length):
					self.body_array.append([0,i,"<","BLACK","RED","NORMAL"])
			else:
				for i in range(length):
					self.body_array.append([0,-1*i,"<","BLACK","RED","NORMAL"])
			self.bound_L = 0
			self.bound_R = 0

		elif(angle==45):
			if(y<(GAME_BOUNDARY_D+GAME_BOUNDARY_U)/2):	# upper half
				for i in range(length):
					self.body_array.append([i,i,"<","BLACK","RED","NORMAL"])
			else:
				for i in range(length):					# lower half
					self.body_array.append([i,-1*i,"<","BLACK","RED","NORMAL"])

			self.bound_L = 0
			self.bound_R = length

#----------------------------------------#

class Coin(Token):
	def __init__(self,frame_loc,y):
		Token.__init__(self,frame_loc,y)
		self.token_type = "coin"
		self.reward = 10

		self.body_array = [[0,0,"©","YELLOW","","BRIGHT"]]

#----------------------------------------#

class Player(Kinitos):
	def __init__(self,x,y):
		Kinitos.__init__(self,x,y)
		self.gravity = 0.00002
		self.acc_y += -1 * self.gravity

		self.body_array = [[0,0," ","","BLUE","NORMAL"],[0,1," ","","MAGENTA","NORMAL"],[1,0," ","","MAGENTA","NORMAL"],[1,1," ","","BLUE","NORMAL"]]
		self.treasure = 0
		self.health = 3000
		self.gun_temp = 0

	def display_treasure(self):
		plot_text(100,1,"                  ")
		plot_text(100,1,"Treasure: "+str(self.treasure))

	def display_health(self):
		plot_text(20,1,"                  ")
		plot_text(20,1,"Health: "+str(self.health))

	def fetch_gun_temp(self):
		return self.gun_temp

	def shots_fired(self):
		self.gun_temp = GUN_TEMP

	def gun_cooldown(self):
		self.gun_temp -= GAME_SPD

#----------------------------------------#

class Demogorgon(Kinitos):
	def __init__(self,x,y):
		Kinitos.__init__(self,x,y)
		self.body_array = [[0,0," ","","RED","NORMAL"],[0,1," ","","MAGENTA","NORMAL"],[1,0," ","","MAGENTA","NORMAL"],[1,1," ","","RED","NORMAL"]]
		self.health = 3000
		self.gun_temp = 0
		self.status = False
		self.vel_y = 0.08 # this is abs acc_y, dir is given in update_vel acc to player_x
		self.quasar_list = []
		self.quasar_count = 0
		self.blaster_temp = 0

	def display_health(self):
		plot_text(70,1,"                  ")
		plot_text(70,1,"DD Health: "+str(self.health))

	def update_pos(self,player_x,player_y):
		plot_obj(self,"clear")

		if(player_y < self.pos_y):
			self.pos_y -= self.vel_y*(abs(player_y-self.pos_y)+0)*0.04
		else:
			self.pos_y += self.vel_y*(abs(player_y-self.pos_y)+0)*0.04

		plot_obj(self,"plot")
		if(self.pos_y>GAME_BOUNDARY_D):
			self.vel_y=0
			self.pos_y=GAME_BOUNDARY_D
		elif(self.pos_y<GAME_BOUNDARY_U):
			self.vel_y=0
			self.pos_y=GAME_BOUNDARY_U

	def fire_quasar(self):
		self.quasar_list.append(Quasar(140,self.pos_y,-1*BULLET_VEL,self.quasar_count))
		self.quasar_count += 1
		self.blaster_temp = 5

	def rain_fire(self,player_x,player_y):
		if(abs(self.pos_y - player_y)<3 and self.blaster_temp < 1):
			# print("shots fired")
			self.fire_quasar()

	def quasar_out(self,quasar):
		if(quasar.pos_x<GAME_BOUNDARY_L):
			return True
		else:
			return False

	def blaster_cooldown(self):
		self.blaster_temp -= 0.01

#----------------------------------------#

class Bullet(Kinitos):
	def __init__(self,x,y,vel,serial_no):
		Kinitos.__init__(self,x,y)
		self.serial_no = serial_no
		self.body_array = [[0,0,"=","WHITE","","BRIGHT"]]
		self.damage = 1	
		self.vel_x = vel # game vel already factored in 

#----------------------------------------#

class Quasar(Kinitos):
	def __init__(self,x,y,vel,serial_no):
		Kinitos.__init__(self,x,y)
		self.serial_no = serial_no
		self.body_array = [[0,0,"@","CYAN","","BRIGHT"]]
		self.damage = 1	
		self.vel_x = vel # game vel already factored in 

#-------------------------------------------------------------------------------------#
#									   | MAIN |										  #
#-------------------------------------------------------------------------------------#

setup()

game = Game(5)	# New game created

ares = Player(30,10)
hades = Demogorgon(145,20)

# token_list = []
game.token_list.append(Fire_Beam(160,20,0,10))
game.token_list.append(Fire_Beam(180,30,0,10))
game.token_list.append(Fire_Beam(200,30,90,10))
game.token_list.append(Fire_Beam(220,10,45,10))
game.token_list.append(Fire_Beam(240,21,45,10))
game.token_list.append(Fire_Beam(260,30,45,10))
game.token_list.append(Fire_Beam(280,10,90,20))
game.token_list.append(Coin(180,25))
game.token_list.append(Coin(182,25))
game.token_list.append(Coin(184,25))
game.token_list.append(Coin(186,25))
game.token_list.append(Coin(188,25))
game.token_list.append(Coin(190,25))

# token_list = token_generator()

hades.quasar_list.append(Quasar(140,20,-0.02,139))

while(keyboard.is_pressed('b')==0):
	pass
	
frame_L_pos = 0
frame_R_pos = GAME_BOUNDARY_R - 2

# GAME ON
#========================================================================
#========================================================================

while(keyboard.is_pressed('z')==0):

	if(game.mode=="NORMAL"):

		for i in game.token_list:
			if(i.frame_loc+i.bound_L<=frame_R_pos and i.frame_loc>frame_L_pos and i.status==False):
				i.activate_token()
			if(i.frame_loc+i.bound_R<=frame_L_pos and i.status==True):
				i.deactivate_token()

		for i in game.token_list:
			if(i.status==True):
				i.render()

		for i in game.token_list:
			if(i.status==True):
				if(ares.if_hit_token(i)==True):
					if(i.token_type=="coin"):
						ares.treasure+=i.reward
						game.token_list.remove(i)
					elif(i.token_type=="fire_beam"):
						ares.health-=i.damage

		for bullet in game.bullet_list:
			for tok in game.token_list:
				if(tok.status==True):
					if(tok.token_type=="fire_beam"):
						if(bullet.if_hit_token(tok)==True):
							tok.redact()	# erase fire beam from screen
							game.bullet_list.remove(bullet)
							game.token_list.remove(tok)

	elif(game.mode=="DEMOGORGON"):

		for bullet in game.bullet_list:
			if(bullet.if_hit_kinitos(hades)==True):
				hades.hit_confirmed(bullet)
				game.bullet_list.remove(bullet)

		for quasar in hades.quasar_list:
		  	if(quasar.if_hit_kinitos(ares)==True):
		  		ares.hit_confirmed(quasar)
		  		hades.quasar_list.remove(quasar)


		for quasar in hades.quasar_list:
			if(hades.quasar_out(quasar)):
				hades.quasar_list.remove(quasar)	# if bullet gone out of scope
			else:
				quasar.update_pos()

		hades.update_pos(ares.pos_x,ares.pos_y)
		hades.rain_fire(ares.pos_x,ares.pos_y)
		hades.blaster_cooldown()
		hades.display_health()

#*******************************************************************************

	for i in game.bullet_list:
		if(game.bullet_out(i)):
			game.bullet_list.remove(i) # if bullet gone out of scope
		else:
			i.update_pos()

	ares.update_pos()
	ares.update_vel()
	ares.gun_cooldown()
	ares.disp_vects()
	ares.display_treasure()
	ares.display_health()

	game.display_ammo()



	if(keyboard.is_pressed("w")):
		ares.move_up()

	if(keyboard.is_pressed('p') and ares.fetch_gun_temp()<1 and game.is_ammo()):
		ares.shots_fired()	# raises gun temp so that gun cannot be used ctsly
		game.fire_bullet(ares)


	print(int(frame_L_pos),int(frame_R_pos))

	frame_L_pos+=(FRAME_SPD)	# 1/game spd
	frame_R_pos+=(FRAME_SPD)	# 1/game spd

	if(frame_R_pos > 450 and hades.status==False):
		hades.status==True
		game.mode = "DEMOGORGON"

	time.sleep(0.00002/GAME_SPD) 	# game 1/fps

#========================================================================
#========================================================================
# DED


while(keyboard.is_pressed('q')==0):
	pass

terminate()

