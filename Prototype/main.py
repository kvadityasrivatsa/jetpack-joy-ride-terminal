import colorama
from colorama import Fore, Back, Style
import keyboard
import time
import math
import const
import method
import classes

#-------------------------------------------------------------------------------------#
#									   | MAIN |										  #
#-------------------------------------------------------------------------------------#

method.setup()

game = classes.Game()	# New game created
ares = classes.Player(30,10)
hades = classes.Demogorgon(const.GAME_BOUNDARY_R,20)

game.generate_tokens(const.SCRN_WIDTH+10,1500)

while(keyboard.is_pressed('b')==0):
	pass
	
# frame_L_pos = 0
# frame_R_pos = const.GAME_BOUNDARY_R - 2

# GAME ON
#========================================================================
#========================================================================

while(keyboard.is_pressed('z')==0):

	method.move_background(game.get_frame_L_pos(),game.get_speed())

	if(game.get_mode()=="NORMAL"):

		ares.disp_vects()

		for tok in game.get_token_list():
			tok.check_token_activation(game.get_frame_L_pos(),game.get_frame_R_pos(),game.get_speed())

		for tok in game.get_token_list():	# Token rendering
			if(tok.get_status()==True):
				tok.render()

		for tok in game.get_token_list():	# Update Token speed
			if(tok.get_status()==True):
				tok.set_speed(game.get_speed())

		for tok in game.get_token_list():		# Token interaction
			if(tok.get_status()==True):	

				if(tok.get_token_type()=="coin"):
					if(ares.if_hit_token(tok)==True):
						ares.incerement_treasure(tok.get_reward())
						game.remove_token_list(tok)

				elif(tok.get_token_type()=="fire_beam"):
					if(ares.if_hit_token(tok)==True):
						ares.decrement_health(tok.get_damage())
						game.remove_token_list(tok)
						tok.redact()

				elif(tok.get_token_type()=="magnet"):
					ares.magnet_influence(tok)

				elif(tok.get_token_type()=="speed_boost"):
					if(ares.if_hit_token(tok)==True):
						tok.redact()
						game.speed_boost()
						game.remove_token_list(tok)


		for bullet in ares.get_bullet_list():	# if bullets shot by ares hit a fire beam
			for tok in game.get_token_list():
				if(tok.get_status()==True):
					if(tok.get_token_type()=="fire_beam"):
						if(bullet.if_hit_token(tok)==True):
							tok.redact()	# erase fire beam from screen
							ares.remove_bullet_list(bullet)
							game.remove_token_list(tok)
							ares.incerement_treasure(100)

	elif(game.get_mode()=="DEMOGORGON"):

		for bullet in ares.get_bullet_list():
			if(bullet.if_hit_kinitos(hades)==True):
				hades.hit_confirmed(bullet)	# hades hit by bullets shot by ares
				ares.remove_bullet_list(bullet)
				ares.incerement_treasure(100)

		for quasar in hades.get_quasar_list():
		  	if(quasar.if_hit_kinitos(ares)==True):
		  		ares.hit_confirmed(quasar)	# ares hit by bullets shot by hades
		  		hades.remove_quasar_list(quasar)


		for quasar in hades.get_quasar_list():
			if(hades.quasar_out(quasar)):
				hades.remove_quasar_list(quasar)	# if bullet gone out of scope
			else:
				quasar.update_pos()

		hades.update_pos(ares.get_pos_x(),ares.get_pos_y())
		hades.rain_fire(ares.get_pos_x(),ares.get_pos_y())
		hades.blaster_cooldown()
		hades.display_health()

#*******************************************************************************

	for i in ares.get_bullet_list():
		if(ares.bullet_out(i)):
			ares.remove_bullet_list(i) # if bullet gone out of scope
		else:
			i.update_pos()

	ares.update_pos()
	ares.update_vel()
	ares.gun_cooldown()
	ares.disp_vects()
	ares.display_treasure()
	ares.display_health()
	ares.display_ammo()
	ares.shield_cooldown()

	game.boost_cooldown()

	if(keyboard.is_pressed("w")):
		ares.move_up()
	if(keyboard.is_pressed("a")):
		ares.move_left()
	if(keyboard.is_pressed("d")):
		ares.move_right()
	if(keyboard.is_pressed("s")):
		ares.stop()
	if(keyboard.is_pressed(" ")):
		ares.shields_up()
	if(keyboard.is_pressed("m")):
		game.pause()
	if(keyboard.is_pressed('p') and ares.fetch_gun_temp()<1 and ares.is_ammo()):
		ares.shots_fired()	# raises gun temp so that gun cannot be used ctsly
		ares.add_bullet_list()

	if(ares.get_health()<=0):
		game.over()
		time.sleep(3)
		break;

	if(hades.get_health()<=0):
		game.win()
		time.sleep(3)
		break;

	game.update_frames()	

	if(game.get_frame_R_pos() > 1660 and hades.get_status()==False):
		hades.set_status(True)
		game.set_mode("DEMOGORGON")
		ares.set_ammo(500)

	time.sleep(0.00002/game.get_speed()) 	# game 1/fps

#========================================================================
#========================================================================
# DED


while(keyboard.is_pressed('q')==0):
	pass

method.terminate()

