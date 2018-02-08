# Nick Junius
# CMPM 244 

# Code for loading and displaying levels for use with p1_pathfinder.py

# reads specified file and parses its contents into 
# the categories of objects found in the dungeon
# walls, spaces, and waypoints and returns them in a dict
def load_level(filename):
	walls = {}
	spaces = {}
	waypoints = {}
	with open(filename, "r") as starting_dungeon:
	
		for j, line in enumerate(starting_dungeon.readlines()):
			for i, char in enumerate(line):
				if char == '\n':
					continue
				elif char.isupper():
					walls[(i, j)] = char
				else:
					spaces[(i, j)] = char
					if char.islower():
						waypoints[char] = (i, j)
						
	level = { 
				"walls": walls,
				"spaces": spaces,
				"waypoints": waypoints
			}
	return level
	
# displays level with the found path (if the path exists)
# in the console
# requires a level dictionary with keys as:
#	"walls"
#	"spaces"
#	"waypoints"
# and corresponding values as:
#	{(int i, int j): char}
#	{(int i, int j): char}
#	{char: (int i, int j)}
def show_level(level, path = []):
	
	all_Xs, all_Ys = zip(*(level["spaces"].keys() + level["walls"].keys()))
	x_min = min(all_Xs)
	x_max = max(all_Xs)
	y_min = min(all_Ys)
	y_max = max(all_Ys)
	
	path_cells = set(path)
	
	printable_dungeon = []
	
	for j in range(y_min, y_max + 1):
		for i in range (x_min, x_max + 1):
			
			cell = (i, j)			
			if cell in path_cells:
				printable_dungeon.append('*')
			elif cell in level["walls"]:
				printable_dungeon.append(level["walls"][cell])
			elif cell in level["spaces"]:
				printable_dungeon.append(level["spaces"][cell])
			else:
				printable_dungeon.append(' ')
		
		printable_dungeon.append('\n')
	
	print "".join(printable_dungeon)
	
	return printable_dungeon
	