import curses
from curses import KEY_DOWN, KEY_UP, KEY_LEFT, KEY_RIGHT

WIDTH = 30
HEIGHT = 30
TIMEOUT = 100
MIN_Y = 1
MIN_X = 1
MAX_Y = HEIGHT - 2
MAX_X = WIDTH - 2
KEY_ESC = 27

class ship(object):
	
	def __init__(self, window, x, y):
		self.alive = True	# indicates if the ship is alive
		self.x = x			# position of the ship
		self.y = y			# position of the ship

		self.window = window	# reference to the curses window
		
		self.direction_map = {	# relations between keys and movement functions
			KEY_UP: self.move_up,
			KEY_DOWN: self.move_down,
			KEY_LEFT: self.move_left,
			KEY_RIGHT: self.move_right
		}

	# A single function for determining which movement function to call
	def handle_move(self, direction):
		self.direction_map[direction]()

	# Movement functions follow the same convention:
	#	check if movement would be inside the window
	#	if yes, move
	# 	else, don't move

	def move_up(self):
		if self.y > MIN_Y:
			self.y -= 1		# curses' y-axis is reversed
	
	def move_down(self):
		if self.y < MAX_Y:
			self.y += 1		# curses' y-axis is reversed

	def move_left(self):
		if self.x > MIN_X:
			self.x -= 1

	def move_right(self):
		if self.x < MAX_X:
			self.x += 1

	def render(self):
		self.window.addstr(self.y, self.x, self.appearance)

class hero_ship(ship):

	def __init__(self, window, x, y):	
		ship.__init__(self, window, x ,y)
		self.appearance = "A"

if __name__ == "__main__":	
	
	# currently, everything is inside a try/except block because
	# 	curses changes terminal settings for the given terminal
	#	session. Unless specifically mentioned in an except block,
	#	program will not reset terminal settings.
	# So basically, I'm just lazy
	try:

		# Basic curses initialization steps. See curses documentation for specifics
		curses.initscr()
		window = curses.newwin(HEIGHT, WIDTH, 0, 0)
		window.timeout(TIMEOUT)
		window.keypad(1)
		curses.noecho()
		curses.curs_set(0)
		window.border(0)

		# The player is created, put at the bottom-left of the screen
		player = hero_ship(window, MIN_X, MAX_Y)

		# Main game loop
		while True:

			# Steps for refreshing the window
			window.clear()
			window.border(0)

			# Make sure to refresh the player's position each time
			player.render()

			# Gets the player's keypress
			event = window.getch()
			
			# If the player presses escape, quit the game
			if event == KEY_ESC:
				break

			# If the player clicks an arrow key, process game movement
			elif event in [KEY_DOWN, KEY_UP, KEY_LEFT, KEY_RIGHT]:
				player.handle_move(event)

		# Upon graceful exit, close the curses session, bringing back
		#  normal terminal settings
		curses.endwin()
	
	except Exception as e:
		curses.endwin()
		print(e)