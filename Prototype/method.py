import colorama
from colorama import Fore, Back, Style
import keyboard
import time
import math
import const

#-------------------------------------------------------------------------------------#
#								      | METHODS |								      #
#-------------------------------------------------------------------------------------#

def setup():

	colorama.init()
	for j in range(const.SCRN_WIDTH):
		for i in range(const.SCRN_HEIGHT):
			plot(i,j," ","","BLACK","NORMAL")
	print("\033[2J" + "\033[0;0H")

	i=0
	while(i<=const.SCRN_WIDTH-4):
		plot(i,const.GAME_BOUNDARY_D+1,"[]","BLUE","","NORMAL")
		plot(i,const.WALL_WIDTH,"[]","BLUE","","NORMAL")
		i+=2
#----------------------------------------#

def plot_text(y,x,string):
	print("\033[" + str(x) + ";" + str(y) + "H" + Fore.WHITE + Fore.BLACK , string)

#----------------------------------------#	

def plot(y,x,string,fore_col,back_col,style):

	if(y < const.GAME_BOUNDARY_L or y > const.GAME_BOUNDARY_R):
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

def plot_obj(obj, __mode):	#obj MUST have a body array (rel_x,rel_y,ascii,fore_col,back_col)
	
	if(__mode=="plot"):
		for i in obj.get_body_array():
			plot(obj.get_pos_x()+i[0],obj.get_pos_y()+i[1],i[2],i[3],i[4],i[5])
	elif(__mode=="clear"):
		for i in obj.get_body_array():
			plot(obj.get_pos_x()+i[0],obj.get_pos_y()+i[1]," ","","BLACK","NORMAL")

#----------------------------------------#

def dist(x1,y1,x2,y2):
	return abs(math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)))
	# return abs((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2)**0.5)
#----------------------------------------#

def terminate():
	plot(const.SCRN_HEIGHT,0,"","","","")