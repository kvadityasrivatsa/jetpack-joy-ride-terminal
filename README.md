SSAD/ASSIGNMENT-1/2020/2018114018

	This is an attempted rendition of the popular game Jetpack_Joyride©
	
	# SETUP:
		- Install keyboard and colorama library on python3 before running the primary python file "main.py"
		- run the command: "python3 main.py" OR "sudo python3 main.py" dependeing upon your root priveleges.

	# Gameplay:
		- The game is centered around getting your hero - ARES:The god of War till the end of the
		  "Chasm of Death".
		- Ares must maneuver around obstacles without losing all his lives
		- Ares has 5 lives in total, losing all of which will result in losing the game
		- At the end of the path, Ares must fend of the his ultimate enemy - Hades:The god of Hell

	# Controls:
		- Ares:
			- 'w' : move up
			- 'a' : move left
			- 'd' : move right
			- 'p' : shoot bullet (use to shoot down fire beams to gain points)
			- <spacebar> : shield (protects Ares from any damage for 10s, after which the shield cannot 
						be accessed for 60s)

		- General
			- 'b' : begin game
			- 'q' : quit game
		
	# General Code Structure:
		-Game: Controls basic gameplay variables like game speed, 
			cur frame position and tokens suspended

		-Entity: Every element present inside the GAME_BOUNDARIES 
			belongs to this class, it has position, velocity & acceleration

		-Kinitos(Entity): All those Entities that have a non-zero velocity 
			relative to the background frame of the game

		-Tokens(Entity):  All those Entities that are fixed respect to the 
			moving background and interact with Kinitos

		-Player(Kinitos): Ares belongs to this class, which gives him the privelege to experience gravity 
			and be positioned according to the user input

		-Demogorgon(Kinitos): Hades belongs to this class, and can shoot Quasars 
			at Ares while moving only in the y-axis

		-Coin(Token): These can be collected by Ares to increase his score

		-Fire_Beam(Token): These cause Ares to lose a life when he collides with them. 
			They can be destroyed by Ares by shooting bullets at them.

		-Magnet(Token): If Ares comes in proximity of a magnet, he is continuously pulled towards it.

		-Speed_Boost(Token): When collected by Ares, these cause the game speed to increase for a 
			limited amount of time.


	WARNING: This game belongs to KV ADITYA SRIVATSA© and any attempt at plagiarizing the same
			will result in serious repercussions.




			
