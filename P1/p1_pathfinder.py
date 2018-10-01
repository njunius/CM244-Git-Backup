# Nick Junius
# CMPM 244

# Code for Dijkstras shortest path implementation and main

from p1_level_handler import load_level, show_level
from math import sqrt
from heapq import heappush, heappop


# returns the neighbors of cell in level
# as a dict where:
# 	cell is the key
# 	float (cost) is the value
def navigation_edges(level, cell):
	steps = {}
	x, y = cell
	for dx in [-1, 0, 1]:
		for dy in [-1, 0, 1]:
			next_cell = (x + dx, y + dy)
			dist = sqrt(dx * dx + dy * dy)
			if dist > 0 and next_cell in level["spaces"]:
				steps[next_cell] = dist
				
	return steps

	
# implementation of Dijkstra's Algorithm
# returns a list of cells representing the shortest path
# or an empty list if no such path exists
def dijkstras_shortest_path(src, dst, graph, adj):
	frontier = []
	heappush(frontier, (0, src))
	cost_so_far = {}
	prev = {}
	prev[src] = None

	while frontier:
		cur_cost, current = heappop(frontier)
		cost_so_far[current] = cur_cost
		
		if current == dst:
			path = []
			#print "total cost = {}\n".format(cost_so_far[current])
			while current:
				path.append(current)
				current = prev[current]
			path.reverse()
			return path
			
		for next in adj(graph, current).items():
			next_cell, next_cost = next
			
			new_cost = cost_so_far[current] + next_cost
			if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
				cost_so_far[next_cell] = new_cost
				heappush(frontier, (new_cost, next_cell))
				prev[next_cell] = current
				
	return []

def test_route(filename, src_waypoint, dst_waypoint):
	level = load_level(filename)
	show_level(level)
	src = level["waypoints"][src_waypoint]
	dst = level["waypoints"][dst_waypoint]
	
	path = dijkstras_shortest_path(src, dst, level, navigation_edges)
	
	if path:
		show_level(level, path)
	else:
		print "No Path Possible!"
		
if __name__ == '__main__':
	import sys
	_, filename, src_waypoint, dst_waypoint = sys.argv
	test_route(filename, src_waypoint, dst_waypoint)