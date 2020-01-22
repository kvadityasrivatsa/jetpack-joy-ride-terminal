import colorama
from colorama import Fore, Back, Style
import keyboard
import time
import math
import const
import method

#-------------------------------------------------------------------------------------#
#								    | CLASSES |								          #
#-------------------------------------------------------------------------------------#

class Game():

	def __init__(self,spd):
		self.__speed = spd
		self.__token_list = []
		self.__mode = "NORMAL"

	###############################

	def get_speed(self):
		return self.__speed

	def get_mode(self):
		return self.__mode

	def set_speed(self,new_speed):
		self.__speed = new_speed

	def set_mode(self,new_mode):
		self.__mode = new_mode

	def get_token_list(self):
		return self.__token_list

	def add_token_list(self,token):
		self.__token_list.append(token)

	def remove_token_list(self,token):
		self.__token_list.remove(token)

	###############################


#----------------------------------------#

class Entity():

	def __init__(self,x,y):
		self._pos_x = x
		self._pos_y = y

		self._vel_x = 0
		self._vel_y = 0

		self._acc_x = 0
		self._acc_y = 0

		self._body_array = []
		self._bound_U = 0
		self._bound_D = 0
		self._bound_L = 0
		self._bound_R = 0

	###############################

	def get_pos_x(self):
		return self._pos_x

	def get_pos_y(self):
		return self._pos_y

	def get_body_array(self):
		return self._body_array

	def get_bound_U(self):
		return self._bound_U

	def get_bound_D(self):
		return self._bound_D

	def get_bound_L(self):
		return self._bound_L

	def get_bound_R(self):
		return self._bound_R

	###############################

	def render_test(self):
		method.plot(self._pos_x, self._pos_y, " ", "", "BLUE","NORMAL")

	def define_pos(self,x,y):
		method.plot(self._pos_x, self._pos_y, " ", "", "BLACK","NORMAL")
		self._pos_x = x
		self._pos_y = y

	def disp_vects(self):
		method.plot(0,0,"vel="+str(self._vel_y)+" _acc_y="+str(self._acc_y), "WHITE", "BLACK", "NORMAL")

#----------------------------------------#

class Kinitos(Entity):
	def __init__(self,x,y):
		Entity.__init__(self,x,y)
		self._damage = 0
		self._move_left_val = 0
		self._move_right_val = 0
		self._health = 3000

	###############################

	def get_damage(self):
		return self._damage

	###############################

	def update_pos(self):
		method.plot_obj(self,"clear")
		self._pos_x = self._pos_x + self._vel_x*const.VX_CONST + self._move_left_val + self._move_right_val
		self._pos_y = self._pos_y + self._vel_y*const.VY_CONST
		if(self._pos_y>const.GAME_BOUNDARY_D):
			self._vel_y=0
			self._pos_y=const.GAME_BOUNDARY_D
		elif(self._pos_y<const.GAME_BOUNDARY_U):
			self._vel_y=0
			self._pos_y=const.GAME_BOUNDARY_U

		method.plot_obj(self,"plot")
		self._move_left_val=0 	# both get reset at the end of each iteration
		self._move_right_val=0

	def update_vel(self):
		self._vel_y -= self._acc_y*const.A_CONST

	def move_up(self):
		self._vel_y -= 0.00006

	def move_left(self):
		self._move_left_val = -0.024

	def move_right(self):
		self._move_right_val = 0.024

	def if_hit_token(self,tok):
		for i in self._body_array:
			if(tok.if_collision(i[0]+self._pos_x,i[1]+self._pos_y)):
				return True

	def if_hit_kinitos(self,kino):	# if bullet hits a kinito
		for i in self._body_array:
			for j in kino.get_body_array():
				if(int(kino._pos_x + j[0]) == int(self._pos_x + i[0]) and int(kino.get_pos_y() + j[1]) == int(self._pos_y + i[1])):
					return True

	def hit_confirmed(self,kino): # kino(agent) here may be a bullet or a quasar
		self._health -= kino.get_damage()

#----------------------------------------#

class Token(Entity):	# Fire beams, Magnets & COINS$$
	def __init__(self,_frame_loc,y):
		Entity.__init__(self,0,y)	# self.x is not applicable till token is rendered
		self._frame_loc = _frame_loc
		self._status = False
		self._token_type = ""

	###############################

	def get_frame_loc(self):
		return self._frame_loc

	def get_status(self):
		return self._status

	def get_token_type(self):
		return self._token_type

	###############################

	def activate_token(self):
		self._vel_x -= const.GAME_SPD
		self._pos_x = const.GAME_BOUNDARY_R
		self._status = True
		# print("Token Activated")

	def deactivate_token(self):
		self._vel_x = 0
		self._pos_x = 400
		self._status = False
		method.plot_obj(self,"clear")
		# print("Token Deactivated")

	def if_collision(self,x,y):
		for i in self._body_array:
			if(int(x)==int(i[0]+self._pos_x) and int(y)==int(i[1]+self._pos_y)):
				return True

	def render(self):
		method.plot_obj(self,"clear")
		self._pos_x = self._pos_x + self._vel_x*const.VX_CONST
		method.plot_obj(self,"plot")

	def redact(self):
		method.plot_obj(self,"clear")

#----------------------------------------#

class Fire_Beam(Token):
	def __init__(self,_frame_loc,y,angle,length):
		Token.__init__(self,_frame_loc,y)
		self._token_type = "fire_beam"
		self._damage = 1

		if(angle==0):
			for i in range(length):
				self._body_array.append([i,0,"<","BLACK","RED","NORMAL"])
			self._bound_L = 0
			self._bound_R = length

		elif(angle==90):
			if(y<(const.GAME_BOUNDARY_D+const.GAME_BOUNDARY_U)/2):	# upper half
				for i in range(length):
					self._body_array.append([0,i,"<","BLACK","RED","NORMAL"])
			else:
				for i in range(length):
					self._body_array.append([0,-1*i,"<","BLACK","RED","NORMAL"])
			self._bound_L = 0
			self._bound_R = 0

		elif(angle==45):
			if(y<(const.GAME_BOUNDARY_D+const.GAME_BOUNDARY_U)/2):	# upper half
				for i in range(length):
					self._body_array.append([i,i,"<","BLACK","RED","NORMAL"])
			else:
				for i in range(length):					# lower half
					self._body_array.append([i,-1*i,"<","BLACK","RED","NORMAL"])

			self._bound_L = 0
			self._bound_R = length


	###############################

	def get_damage(self):
		return self._damage

	###############################

#----------------------------------------#

class Coin(Token):
	def __init__(self,_frame_loc,y):
		Token.__init__(self,_frame_loc,y)
		self._token_type = "coin"
		self.__reward = 10
		self._body_array = [[0,0,"©","YELLOW","","BRIGHT"]]

	###############################

	def get_reward(self):
		return self.__reward

	###############################

#----------------------------------------#

class Player(Kinitos):
	def __init__(self,x,y):
		Kinitos.__init__(self,x,y)
		self.__gravity = 0.00002
		self._acc_y += -1 * self.__gravity

		self._body_array = [[0,0," ","","BLUE","NORMAL"],[0,1," ","","MAGENTA","NORMAL"],[1,0," ","","MAGENTA","NORMAL"],[1,1," ","","BLUE","NORMAL"]]
		self._bound_L = 0
		self._bound_R = 1

		self.__treasure = 0
		self.__gun_temp = 0
		self.__ammo = 20
		self.__bullet_count = 0
		self.__bullet_list = []

		self.mag_inf_status = False

	###############################

	def incerement_treasure(self,value):
		self.__treasure += value

	def decrement_health(self,value):
		self._health -= value

	def get_bullet_list(self):
		return self.__bullet_list

	def add_bullet_list(self):	# keeps track of the unique serial no. of every quasar
		self.__bullet_count += 1
		bullet = Bullet(self.get_bound_R()+self.get_pos_x()+1,self.get_pos_y(),const.BULLET_VEL,self.__bullet_count)
		self.__ammo -= 1
		self.__bullet_list.append(bullet)

	def remove_bullet_list(self,bullet):
		self.__bullet_list.remove(bullet)

	###############################

	def update_pos(self):
		method.plot_obj(self,"clear")
		self._pos_x = self._pos_x + self._vel_x*const.VX_CONST + self._move_left_val + self._move_right_val
		self._pos_y = self._pos_y + self._vel_y*const.VY_CONST
		if(self._pos_y>const.GAME_BOUNDARY_D):
			self._vel_y=0
			self._pos_y=const.GAME_BOUNDARY_D
		elif(self._pos_y<const.GAME_BOUNDARY_U):
			self._vel_y=0
			self._pos_y=const.GAME_BOUNDARY_U
		elif(self._pos_x>const.PLAYER_BOUND_R):
			self._pos_x=const.PLAYER_BOUND_R
		elif(self._pos_x<const.PLAYER_BOUND_L):
			self._pos_x=const.PLAYER_BOUND_L

		method.plot_obj(self,"plot")
		self._move_left_val=0 	# both get reset at the end of each iteration
		self._move_right_val=0

	def display_treasure(self):
		method.plot_text(100,1,"                  ")
		method.plot_text(100,1,"Treasure: "+str(self.__treasure))

	def display_health(self):
		method.plot_text(20,1,"                  ")
		method.plot_text(20,1,"Health: "+str(self._health))

	def fetch_gun_temp(self):
		return self.__gun_temp

	def shots_fired(self):
		self.__gun_temp = const.GUN_TEMP

	def gun_cooldown(self):
		self.__gun_temp -= const.GAME_SPD

	def is_ammo(self):
		if(self.__ammo>0):
			return True
		else:
			return False

	def display_ammo(self):
		method.plot_text(50,1,"                  ")
		method.plot_text(50,1,"Ammo: "+str(self.__ammo))

	def bullet_out(self,bullet):
		if(bullet.get_pos_x()>const.GAME_BOUNDARY_R):
			return True
		else:
			return False

	def magnet_influence(self,magnet):
		distance = method.dist(self._pos_x,self._pos_y,magnet.get_pos_x(),magnet.get_pos_y())
		# print("distance:",distance)
		if(distance<=10):
			mag_vel_x = (magnet.get_pos_x() - self._pos_x)/distance
			mag_vel_y = (magnet.get_pos_y() - self._pos_y)/distance
			# print("Active")
			
			self._vel_x += mag_vel_x*magnet.get_MAG_VEL()
			self._vel_y += mag_vel_y*magnet.get_MAG_VEL()
			# method.plot_text(0,10,"mag_vel_x:"+str(mag_vel_x)+"mag_vel_y:"+str(mag_vel_y)+"self._vel_x"+str(self._vel_x)+"self._vel_y"+str(self._vel_y))
		else:
			# print("Inactive")
			self._vel_x = 0

#----------------------------------------#

class Demogorgon(Kinitos):
	def __init__(self,x,y):
		Kinitos.__init__(self,x,y)

		self._body_array = [[0,0," ","","RED","NORMAL"],[0,1," ","","MAGENTA","NORMAL"],[1,0," ","","MAGENTA","NORMAL"],[1,1," ","","RED","NORMAL"]]
		self._bound_L = 0
		self._bound_R = 1

		self._health = 3000
		self._status = False
		self._vel_y = 0.08 # this is abs _acc_y, dir is given in update_vel acc to player_x
		self.__quasar_list = []
		self.__quasar_count = 0
		self.__blaster_temp = 0

	###############################

	def get_status(self):
		return self._status

	def set_status(self,new_status):
		self._status = new_status

	def get_quasar_list(self):
		return self.__quasar_list

	def add_quasar_list(self,quasar):
		self.__quasar_list.append(quasar)

	def remove_quasar_list(self,quasar):
		self.__quasar_list.remove(quasar)

	###############################

	def display_health(self):
		method.plot_text(70,1,"                  ")
		method.plot_text(70,1,"DD Health: "+str(self._health))

	def update_pos(self,player_x,player_y):
		method.plot_obj(self,"clear")

		if(player_y < self._pos_y):
			self._pos_y -= self._vel_y*(abs(player_y-self._pos_y)+0)*0.04
		else:
			self._pos_y += self._vel_y*(abs(player_y-self._pos_y)+0)*0.04

		method.plot_obj(self,"plot")
		if(self._pos_y>const.GAME_BOUNDARY_D):
			self._vel_y=0
			self._pos_y=const.GAME_BOUNDARY_D
		elif(self._pos_y<const.GAME_BOUNDARY_U):
			self._vel_y=0
			self._pos_y=const.GAME_BOUNDARY_U

	def fire_quasar(self):
		self.add_quasar_list(Quasar(140,self._pos_y,-1*const.BULLET_VEL,self.__quasar_count))
		self.__quasar_count += 1 # keeps track of the unique serial no. of every quasar
		self.__blaster_temp = 5

	def rain_fire(self,player_x,player_y):
		if(abs(self._pos_y - player_y)<3 and self.__blaster_temp < 1):
			# print("shots fired")
			self.fire_quasar()

	def quasar_out(self,quasar):
		if(quasar.get_pos_x()<const.GAME_BOUNDARY_L):
			return True
		else:
			return False

	def blaster_cooldown(self):
		self.__blaster_temp -= 0.01

#----------------------------------------#

class Bullet(Kinitos):
	def __init__(self,x,y,vel,serial_no):
		Kinitos.__init__(self,x,y)
		self.__serial_no = serial_no
		self._body_array = [[0,0,"=","WHITE","","BRIGHT"]]
		self._damage = 500
		self._vel_x = vel # game vel already factored in 

#----------------------------------------#

class Quasar(Kinitos):
	def __init__(self,x,y,vel,__serial_no):
		Kinitos.__init__(self,x,y)
		self.__serial_no = __serial_no
		self._body_array = [[0,0,"@","CYAN","","BRIGHT"]]
		self._damage = 500
		self._vel_x = vel # game vel already factored in 

#----------------------------------------#

class Magnet(Token):
	def __init__(self,_frame_loc,y):
		Token.__init__(self,_frame_loc,y)
		self._token_type = "magnet"

		self._body_array = [[0,0,"M","","RED","NORMAL"],[0,1,"M","","WHITE","NORMAL"],[1,0,"M","","WHITE","NORMAL"],[1,1,"M","","RED","NORMAL"]]
		self._bound_L = 0
		self._bound_R = 1

		self.__MAG_VEL = 0.001

	###############################

	def get_MAG_VEL(self):
		return self.__MAG_VEL

	###############################

