import colorama
from colorama import Fore, Back, Style
import keyboard
import time
import math
import const
import method
import random
import art

#-------------------------------------------------------------------------------------#
#								    | CLASSES |								          #
#-------------------------------------------------------------------------------------#

class Game():

	def __init__(self):
		self.__speed = const.GAME_SPD
		self.__token_list = []
		self.__mode = "NORMAL"
		self.__boost_temp = 0
		self.__frame_L_pos = 0
		self.__frame_R_pos = const.GAME_BOUNDARY_R - 2
		self.__time_left = const.DRAGON_TIME # in seconds

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

	def get_frame_L_pos(self):
		return self.__frame_L_pos

	def get_frame_R_pos(self):
		return self.__frame_R_pos

	def update_frames(self):
		self.__frame_L_pos += self.__speed
		self.__frame_R_pos += self.__speed

	def update_time_left(self):
		self.__time_left -= (0.0002)/self.__speed

	def is_time_up(self):
		if(self.__time_left<=0):
			return True
		else:
			return False

	###############################

	def speed_boost(self):
		self.__boost_temp = 100
		self.__speed += const.GAME_SPD*1.3

	def boost_cooldown(self):
		if(self.__boost_temp<1):
			self.__speed = const.GAME_SPD
		self.__boost_temp -= const.GAME_SPD


	def generate_tokens(self,beg,end):
		tok_pos_x = beg
		tok_pos_y = 20
		while(tok_pos_x<end):

			x = random.randrange(0,1000)

			if(0<=x and x<=400):		# coin
				tok_pos_x += random.randrange(0,10)
				tok_pos_y = random.randrange(const.GAME_BOUNDARY_U,const.GAME_BOUNDARY_D)
				length = random.randrange(3,6)
				for i in range(length):
					self.add_token_list(Coin(tok_pos_x+2*i,tok_pos_y))
				tok_pos_x += length*2 + 1

			elif(400<x and x<=900):		# fire beam
				tok_pos_x += random.randrange(0,4)
				tick = random.randrange(0,3)
				length = random.randrange(2,10)
				if(tick==0): # 0
					tok_pos_y = random.randrange(const.GAME_BOUNDARY_U+1,const.GAME_BOUNDARY_D-1)
					self.add_token_list(Fire_Beam(tok_pos_x,tok_pos_y,0,length))
					tok_pos_x += length
				elif(tick==1): # 90
					tok_pos_y = random.randrange(const.GAME_BOUNDARY_U+1,const.GAME_BOUNDARY_D-1)
					self.add_token_list(Fire_Beam(tok_pos_x,tok_pos_y,90,length))
					tok_pos_x += length
				elif(tick==2): # 45
					tok_pos_y = random.randrange(const.GAME_BOUNDARY_U+1,const.GAME_BOUNDARY_D-1)
					self.add_token_list(Fire_Beam(tok_pos_x,tok_pos_y,45,length))
					tok_pos_x += length

			elif(900<x and x<=950):	 	# magnet
				tok_pos_x += random.randrange(0,10)
				tok_pos_y = random.randrange(const.GAME_BOUNDARY_U+2,const.GAME_BOUNDARY_D-2)
				self.add_token_list(Magnet(tok_pos_x,tok_pos_y))
				tok_pos_x += 3
			elif(950<x and x<=1000):	# speed boost
				tok_pos_x += random.randrange(0,10)
				tok_pos_y = random.randrange(const.GAME_BOUNDARY_U+2,const.GAME_BOUNDARY_D-2)
				self.add_token_list(Speed_Boost(tok_pos_x,tok_pos_y))
				tok_pos_x += 3
			# else:						# nothing
			# 	tok_pos_x += random.randrange(0,10)

	def pause(self):
		cursor = 10
		for line in art.game_paused:
			method.plot((const.SCRN_WIDTH-len(line))/2,cursor,line,"WHITE","YELLOW","NORMAL")
			cursor+=1
		while(keyboard.is_pressed("n")==False):	# resume on 'n'
			pass
		self.add_token_list(Fire_Beam(self.__frame_L_pos+6,10,90,8))

	def over(self):
		cursor = 10
		for line in art.game_over:
			method.plot((const.SCRN_WIDTH-len(line))/2,cursor,line,"WHITE","RED","BRIGHT")
			cursor+=1

	def win(self):
		cursor = 10
		for line in art.you_win:
			method.plot((const.SCRN_WIDTH-len(line))/2,cursor,line,"WHITE","GREEN","BRIGHT")
			cursor+=1	

	def render_dashboard(self,player,demogorgon):
		player_lives = player.get_health()
		player_score = player.get_treasure()
		demogorgon_health = demogorgon.get_health()
		demo_time = demogorgon.get_status()
		ammo_string = ""

		method.plot(40,const.GAME_BOUNDARY_D+2,"          ","BLACK","WHITE","BRIGHT")
		method.plot(40,const.GAME_BOUNDARY_D+3,"   ARES   ","BLACK","WHITE","BRIGHT")
		method.plot(40,const.GAME_BOUNDARY_D+4,"          ","BLACK","WHITE","BRIGHT")

		method.plot(5,const.GAME_BOUNDARY_D+5,"LIVES:            ","BLACK","WHITE","BRIGHT")
		for i in range(player_lives):
			method.plot(12+2*i,const.GAME_BOUNDARY_D+5,"❤","RED","WHITE","BRIGHT")

		method.plot(5,const.GAME_BOUNDARY_D+7,"SCORE: "+str(player_score)+"  ","BLACK","WHITE","BRIGHT")					

		method.plot(5,const.GAME_BOUNDARY_D+9,"AMMO:                        ","BLACK","WHITE","BRIGHT")

		if(demo_time==False):

			for i in range(player.get_ammo()):
				ammo_string += "➤"

			percentage_compl = int(self.__frame_L_pos*100/const.PATH_LENGTH)
			method.plot(const.SCRN_WIDTH/2 - 4,const.GAME_BOUNDARY_D+2,"        ","BLACK","WHITE","BRIGHT")
			method.plot(const.SCRN_WIDTH/2 - 4,const.GAME_BOUNDARY_D+3,"        ","BLACK","WHITE","BRIGHT")
			method.plot(const.SCRN_WIDTH/2 - 4,const.GAME_BOUNDARY_D+3,"   "+str(percentage_compl)+"%"+"  ","BLACK","WHITE","BRIGHT")
			method.plot(const.SCRN_WIDTH/2 - 4,const.GAME_BOUNDARY_D+4,"        ","BLACK","WHITE","BRIGHT")
		else:

			health_bars = int(demogorgon_health*40/3000 + 1)
			ammo_string = "∞"

			method.plot(const.SCRN_WIDTH-40,const.GAME_BOUNDARY_D+2,"           ","BLACK","WHITE","BRIGHT")
			method.plot(const.SCRN_WIDTH-40,const.GAME_BOUNDARY_D+3,"   HADES   ","BLACK","WHITE","BRIGHT")
			method.plot(const.SCRN_WIDTH-40,const.GAME_BOUNDARY_D+4,"           ","BLACK","WHITE","BRIGHT")

			method.plot(const.SCRN_WIDTH-55,const.GAME_BOUNDARY_D+7,"                                          :HEALTH ","BLACK","WHITE","BRIGHT")
			for i in range(health_bars):
				method.plot(const.SCRN_WIDTH-14-i,const.GAME_BOUNDARY_D+7,"#","BLACK","WHITE","BRIGHT")

			seconds = str(int(self.__time_left)%60)
			minutes = "0"+str(int(self.__time_left/60))
			time = minutes+":"+seconds
			method.plot(const.SCRN_WIDTH/2 - 4,const.GAME_BOUNDARY_D+2,"         ","BLACK","WHITE","BRIGHT")
			method.plot(const.SCRN_WIDTH/2 - 4,const.GAME_BOUNDARY_D+3,"  "+time+"  ","BLACK","WHITE","BRIGHT")
			method.plot(const.SCRN_WIDTH/2 - 4,const.GAME_BOUNDARY_D+4,"         ","BLACK","WHITE","BRIGHT")
			# method.plot(5,const.GAME_BOUNDARY_D+9,"AMMO: "+player_score+"  ","BLACK","WHITE","BRIGHT")

		method.plot(5,const.GAME_BOUNDARY_D+9,"AMMO: "+ammo_string+"  ","BLACK","WHITE","BRIGHT")

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

	def get_vel_x(self):
		return self._vel_x

	def get_pos_y(self):
		return self._pos_y

	def get_body_array(self):
		return self._body_array

	def set_body_array(self,new_body_array):
		self._body_array = new_body_array

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
		self._health = 0
		self._stronghold = False

	###############################

	def get_damage(self):
		return self._damage

	def get_health(self):
		return self._health

	def is_immune(self):
		return self._stronghold


	###############################

	def update_pos(self):
		method.plot_obj(self,"clear")

		self._pos_x = self._pos_x + self._vel_x*const.VX_CONST #+ self._move_left_val + self._move_right_val
		self._pos_y = self._pos_y + self._vel_y*const.VY_CONST

		method.plot_obj(self,"plot")
		self._move_left_val=0 	# both get reset at the end of each iteration
		self._move_right_val=0

	def update_vel(self):
		self._vel_y -= self._acc_y*const.A_CONST

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
		if(self._stronghold==False):
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

	def set_speed(self,vel):
		self._vel_x = -1*vel

	###############################

	def check_token_activation(self,frame_L_pos,frame_R_pos,cur_spd):
		if(self._status==False and self._frame_loc<=frame_R_pos and self._frame_loc>frame_L_pos):
			self._status = True
			self._vel_x -= cur_spd
			self._pos_x = const.GAME_BOUNDARY_R

		elif(self._status==True and self._bound_R+self._pos_x<= const.GAME_BOUNDARY_L):
			self._vel_x = 0
			self._pos_x = 400
			self._status = False
			method.plot_obj(self,"clear")			

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
		self.__gravity = const.GRAVITY
		self._acc_y += -1 * self.__gravity
		self._health = 5

		self._body_array = []
		self._bound_L = 0		
		self._bound_R = 1
		self._bound_U = 0
		self._bound_D = 1

		self.__treasure = 0
		self.__gun_temp = 0
		self.__ammo = 20
		self.__bullet_count = 0
		self.__bullet_list = []

		self.__shield_temp = 0
		self.__array_package = art.player

	###############################

	def set_ammo(self,val):
		self.__ammo = val

	def incerement_treasure(self,value):
		self.__treasure += value

	def decrement_health(self,value):
		if(self._stronghold==False):
			self._health -= value

	def get_bullet_list(self):
		return self.__bullet_list

	def add_bullet_list(self):	# keeps track of the unique serial no. of every quasar
		self.__bullet_count += 1
		bullet = Bullet(self.get_bound_R()+self.get_pos_x()+1,self.get_pos_y()-1,const.BULLET_VEL,self.__bullet_count)
		self.__ammo -= 1
		self.__bullet_list.append(bullet)

	def remove_bullet_list(self,bullet):
		self.__bullet_list.remove(bullet)

	def set_array_package(self,pack):
		self.__array_package = pack
		self.set_body_array(self.__array_package[0])
		self._bound_U = self.__array_package[1][0]
		self._bound_D = self.__array_package[1][1]
		self._bound_L = self.__array_package[1][2]
		self._bound_R = self.__array_package[1][3]
		# print(self.__array_package[1])

	def get_treasure(self):
		return self.__treasure

	def get_ammo(self):
		return self.__ammo

	###############################

	def update_pos(self):
		method.plot_obj(self,"clear")
		self._pos_x = self._pos_x + self._vel_x*const.VX_CONST + self._move_left_val + self._move_right_val
		self._pos_y = self._pos_y + self._vel_y*const.VY_CONST
		if(self._pos_y+self._bound_D>const.GAME_BOUNDARY_D):
			self._vel_y=0
			self._pos_y=const.GAME_BOUNDARY_D-self._bound_D-1
		elif(self._pos_y+self._bound_U<=const.GAME_BOUNDARY_U):
			self._vel_y=0
			self._pos_y=const.GAME_BOUNDARY_U-self._bound_U
		elif(self._pos_x+self._bound_R>const.PLAYER_BOUND_R):
			self._pos_x=const.PLAYER_BOUND_R
			self._vel_x=0
		elif(self._pos_x+self._bound_L<const.PLAYER_BOUND_L+1):
			self._pos_x=const.PLAYER_BOUND_L-self._bound_L+2
			self._vel_x=0

		method.plot_obj(self,"plot")
		self._move_left_val=0 	# both get reset at the end of each iteration
		self._move_right_val=0

	def move_up(self):
		self._vel_y -= const.MOVE_UP_ACC

	def move_left(self):
		if(self._pos_x < const.PLAYER_BOUND_L):
			self._pos_x = const.PLAYER_BOUND_L + 1
			return 0
		self._move_left_val = -1*const.MOVE_X_VEL

	def move_right(self):
		if(self._pos_x >= const.PLAYER_BOUND_R):
			return 0
		self._move_right_val = const.MOVE_X_VEL

	def stop(self):
		self._vel_x = 0

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

	def bullet_out(self,bullet):
		if(bullet.get_pos_x()>const.GAME_BOUNDARY_R):
			return True
		else:
			return False

	def magnet_influence(self,magnet):
		if(self._pos_x<=const.GAME_BOUNDARY_L):
			self._vel_x = 0
			return 0
		distance = method.dist(self._pos_x,self._pos_y,magnet.get_pos_x(),magnet.get_pos_y())
		if(distance<=10):
			mag_vel_x = (magnet.get_pos_x() - self._pos_x)/distance
			mag_vel_y = (magnet.get_pos_y() - self._pos_y)/distance
			
			self._vel_x += mag_vel_x*magnet.get_MAG_VEL()*3
			self._vel_y += mag_vel_y*magnet.get_MAG_VEL()*0.5

		# else:
		# 	self._vel_x = 0

	# def walk(self,parity):
	# 	if(parity%8<4):
	# 		self.set_body_array(self.__array_package[0])
	# 	else:
	# 		self.set_body_array(self.__array_package[1])

	def shields_up(self):
		if(self.__shield_temp<0):
			self.__shield_temp = const.SHIELD_TEMP
			self._stronghold = True
			self.set_array_package(art.player_shield)

	def shield_cooldown(self):
		self.__shield_temp -= const.GAME_SPD
		if(self.__shield_temp<500):
			self._stronghold = False
			self.set_array_package(art.player)


#----------------------------------------#

class Demogorgon(Kinitos):
	def __init__(self,x,y):
		Kinitos.__init__(self,x,y)

		# self._body_array = [[0,0," ","","RED","NORMAL"],[0,1," ","","MAGENTA","NORMAL"],[1,0," ","","MAGENTA","NORMAL"],[1,1," ","","RED","NORMAL"]]
		self._body_array = art.demogorgon
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
		self.add_quasar_list(Quasar(self._pos_x+self._bound_L-1,self._pos_y,-1*const.QUASAR_VEL,self.__quasar_count))
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
		self._body_array = [[0,0,"➤","GREEN","","BRIGHT"]]
		self._damage = 500
		self._vel_x = vel # game vel already factored in 

#----------------------------------------#

class Quasar(Kinitos):
	def __init__(self,x,y,vel,__serial_no):
		Kinitos.__init__(self,x,y)
		self.__serial_no = __serial_no
		self._body_array = [[0,0,"@","CYAN","","BRIGHT"]]
		self._damage = 1
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

#----------------------------------------#

class Speed_Boost(Token):
	def __init__(self,_frame_loc,y):
		Token.__init__(self,_frame_loc,y)
		self._token_type = "speed_boost"
		self._body_array = [[0,0,"S","","CYAN","NORMAL"],[0,1,"S","","WHITE","NORMAL"],[1,0,"S","","WHITE","NORMAL"],[1,1,"S","","CYAN","NORMAL"]]
	###############################

	def get_boost(self):
		return self.boost

	###############################	

#----------------------------------------#


