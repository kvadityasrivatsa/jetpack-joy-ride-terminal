import random

player = [
		[[0,0,"/","WHITE","BLACK","BRIGHT"],[2,0,"\\","WHITE","BLACK","BRIGHT"],[1,-1," ","WHITE","CYAN","BRIGHT"],[2,-1,"︻","YELLOW","BLACK","BRIGHT"],[3,-1,"╦̵̵͇","YELLOW","BLACK","BRIGHT"]],
		[-3,0,0,0]
		 ]

player_shield = [
		[[0,0,"/","GREEN","BLACK","BRIGHT"],[2,0,"\\","GREEN","BLACK","BRIGHT"],[1,-1," ","GREEN","GREEN","BRIGHT"],[2,-1,"︻","GREEN","BLACK","BRIGHT"],[3,-1,"╦̵̵͇","GREEN","BLACK","BRIGHT"]],
		[-3,0,0,0]
		 ]

def initialize_player_array_package():
	head_array = ["(ಠ_ಠ),(/◉ܫ◉/)","☜(˚▽˚)☞","(ಠ_ಥ)","(▰˘◡˘▰)","(¬_¬)","ƪ(˘⌣˘)ʃ","(~‾▿‾)~","(╥_╥)","ᕕ( ᐛ )ᕗ"]
	head_string = head_array[random.randrange(len(head_array))]
	if(len(head_string)==7):
		player[1][2] = -2
		player[1][3] = 4
		for i in range(7):
			player[0].append([i-2,-2,head_string[i],"WHITE","BLACK","BRIGHT"])
			player_shield[0].append([i-2,-2,head_string[i],"GREEN","BLACK","BRIGHT"])
	else:
		player[1][2] = -1
		player[1][3] = 3
		for i in range(5):
			player[0].append([i-1,-2,head_string[i],"WHITE","BLACK","BRIGHT"])
			player_shield[0].append([i-2,-2,head_string[i],"GREEN","BLACK","BRIGHT"])


#-------------------------------------------------------------------------------------#

game_over = [
			"                                                                            ",
			"  ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗  ",
			" ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗ ",
			" ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝ ",
			" ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗ ",
			" ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║ ",
			"  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝ ",
			"                                                                            "
			]

game_paused = [
			"                                                                                           ",
			"  ██████╗  █████╗ ███╗   ███╗███████╗    ██████╗  █████╗ ██╗   ██╗███████╗███████╗██████╗  ",
			" ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔══██╗██╔══██╗██║   ██║██╔════╝██╔════╝██╔══██╗ ",
			" ██║  ███╗███████║██╔████╔██║█████╗      ██████╔╝███████║██║   ██║███████╗█████╗  ██║  ██║ ",
			" ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██╔═══╝ ██╔══██║██║   ██║╚════██║██╔══╝  ██║  ██║ ",
			" ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ██║     ██║  ██║╚██████╔╝███████║███████╗██████╔╝ ",
			"  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝╚═════╝  ",
			"                                                                                           "
			]

you_win = [
			"                                                        ",
			" ██╗   ██╗ ██████╗ ██╗   ██╗    ██╗    ██╗██╗███╗   ██╗ ",
			" ╚██╗ ██╔╝██╔═══██╗██║   ██║    ██║    ██║██║████╗  ██║ ",
			"  ╚████╔╝ ██║   ██║██║   ██║    ██║ █╗ ██║██║██╔██╗ ██║ ",
			"   ╚██╔╝  ██║   ██║██║   ██║    ██║███╗██║██║██║╚██╗██║ ",
			"    ██║   ╚██████╔╝╚██████╔╝    ╚███╔███╔╝██║██║ ╚████║ ",
			"    ╚═╝    ╚═════╝  ╚═════╝      ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝ ",
			"                                                        "
			]


	  #    (╥_╥)                                                                                                                                         /.-.-.\ /.-.-.\
	  #      █╦̵̵͇   ➤                                                                                                          `      "      `
	  #     / \


      #  	  _   ,_,   _
      # 	 / `'=) (='` \ 
      # 	/.-.-.\ /.-.-.\ 
      # 	`      "      `


demogorgon = [
      [0,0,"`","RED","BLACK","BRIGHT"],[-7,0,'\"',"RED","BLACK","BRIGHT"],[-14,0,"`","RED","BLACK","BRIGHT"],

      [0,-1,"\\","RED","BLACK","BRIGHT"],[-1,-1,".","RED","BLACK","BRIGHT"],[-2,-1,"-","RED","BLACK","BRIGHT"],
      [-3,-1,".","RED","BLACK","BRIGHT"],[-4,-1,"-","RED","BLACK","BRIGHT"],[-5,-1,".","RED","BLACK","BRIGHT"],
      [-6,-1,"/","RED","BLACK","BRIGHT"],[-8,-1,"\\","RED","BLACK","BRIGHT"],
      [-9,-1,".","RED","BLACK","BRIGHT"],[-10,-1,"-","RED","BLACK","BRIGHT"],[-11,-1,".","RED","BLACK","BRIGHT"],
      [-12,-1,"-","RED","BLACK","BRIGHT"],[-13,-1,".","RED","BLACK","BRIGHT"],[-14,-1,"/","RED","BLACK","BRIGHT"],

      [-1,-2,"\\","CYAN","BLACK","BRIGHT"],
      [-3,-2,"`","RED","BLACK","BRIGHT"],[-4,-2,"'","RED","BLACK","BRIGHT"],[-5,-2,"=","YELLOW","BLACK","BRIGHT"],
      [-6,-2,"(","MAGENTA","BLACK","BRIGHT"],[-8,-2,")","MAGENTA","BLACK","BRIGHT"],
      [-9,-2,"=","YELLOW","BLACK","BRIGHT"],[-10,-2,"'","RED","BLACK","BRIGHT"],[-11,-2,"`","RED","BLACK","BRIGHT"],
      [-13,-2,"/","CYAN","BLACK","BRIGHT"],

      [-2,-3,"_","RED","BLACK","BRIGHT"],
      [-6,-3,",","RED","BLACK","BRIGHT"],[-7,-3,"_","RED","BLACK","BRIGHT"],[-8,-3,",","RED","BLACK","BRIGHT"],
      [-12,-3,"_","RED","BLACK","BRIGHT"]
      ]

      # [0,-k,"\\","GREEN","BLACK","BRIGHT"],[-1,-k,".","GREEN","BLACK","BRIGHT"],[-2,-k,"-","GREEN","BLACK","BRIGHT"],
      # [-3,-k,".","GREEN","BLACK","BRIGHT"],[-4,-k,"-","GREEN","BLACK","BRIGHT"],[-5,-k,".","GREEN","BLACK","BRIGHT"],
      # [-6,-k,"/","GREEN","BLACK","BRIGHT"],[-3,-k," ","GREEN","BLACK","BRIGHT"],[-8,-k,"\\","GREEN","BLACK","BRIGHT"],
      # [-9,-k,".","GREEN","BLACK","BRIGHT"],[-10,-k,"-","GREEN","BLACK","BRIGHT"],[-11,-k,".","GREEN","BLACK","BRIGHT"],
      # [-12,-k,"-","GREEN","BLACK","BRIGHT"],[-13,-k,".","GREEN","BLACK","BRIGHT"],[-14,-k,"/","GREEN","BLACK","BRIGHT"]



