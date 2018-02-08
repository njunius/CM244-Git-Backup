import random
import sys
def gen_dungeon(filename, width, height):
	dungeon_line = ""
	dungeon_level = []
	for row in range(0, height):
		dungeon_level.append([])
	
	dungeon_file = open(filename, "w")
	for row in range(0, height):
		for col in range(0, width):
			if random.random() < 0.7:
				dungeon_level[col].append('.')
			else:
				dungeon_level[col].append('X')
	
	random_waypoint_x = random.randint(0, width - 1)
	random_waypoint_y = random.randint(0, height - 1)
	dungeon_level[random_waypoint_x][random_waypoint_y] = 'a'
	
	random_waypoint_x = random.randint(0, width - 1)
	random_waypoint_y = random.randint(0, height - 1)

	dungeon_level[random_waypoint_x][random_waypoint_y] = 'b'

	for row in range(0, height):
		dungeon_level[row].append('\n')
		dungeon_line = "".join(dungeon_level[row])
		dungeon_file.write(dungeon_line)
	
	dungeon_file.close()


if __name__ == '__main__':
	import sys
	_, filename, width, height = sys.argv
	int_width = int(width)
	int_height = int(height)
	gen_dungeon(filename, int_width, int_height)