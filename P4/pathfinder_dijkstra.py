# Navmesh Pathfinder Dijkstra's Algorithm
# Nick Junius
# (based on code written by Aaron Desin and Nick Junius in 2015)

from math import sqrt
from heapq import heappush, heappop

def find_path(source_point, dest_point, mesh):
    src_box = None
    dst_box = None
    
    source_x, source_y = source_point
    dest_x, dest_y = dest_point
    
    visited_nodes = []
    path = []
    
    box_list = mesh["boxes"]
    adj_list = mesh["adj"]
    
    for next_box in box_list:
        next_box_x1, next_box_x2, next_box_y1, next_box_y2 = next_box
        
        if source_x >= next_box_x1 and source_y >= next_box_y1:
            if source_x <= next_box_x2 and source_y <= next_box_y2:
                src_box = next_box
                
        if dest_x >= next_box_x1 and dest_y >= next_box_y1:
            if dest_x <= next_box_x2 and dest_y <= next_box_y2:
                dst_box = next_box
                
    # check trivial paths or lack of paths
    if src_box == None or dst_box == None:
        print("No Path Possible!")
        return([],[])
    
    if src_box == dst_box:
        return([(source_point, dest_point)], [src_box])
        
    path, visited_nodes = a_star_shortest_path(src_box, source_point, dst_box, dest_point, mesh, dist_point_in_box)
    
    return(path, visited_nodes)
    
# single direction a star algorithm  
def a_star_shortest_path(src_box, src_point, dst_box, dst_point, graph, adj):
    frontier = [] # priority queue using A* priority, containing boxes and the destination points for the direction it is searching
    visited_nodes = [] # list of boxes
    detail_points = {} # dict of points with the box containing the point as the keys for searching for dst_point
    cost_so_far = {} # dict of distances with boxes as keys starting with the src_box
    prev = {} # dict of boxes with boxes as keys starting with src_box
    
    cost_so_far[src_box] = 0
    prev[src_box] = None
    detail_points[src_box] = src_point
    
    heappush(frontier, (0, src_box))
    visited_nodes.append(src_box)
    
    current = None
    while frontier:
        # tmp_priority is thrown away, current is a box, goal_point is either src_point or dst_point based on what found it originally
        tmp_priority, current = heappop(frontier)
        
        if current == dst_box:
            path = []
            path.append((dst_point, detail_points[current]))
            
            while prev[current]:
                path.append((detail_points[current], detail_points[prev[current]]))
                current = prev[current]
                
            return (path, visited_nodes)

        
        # check if there are adjacent boxes that have not been visited or have a lower cost
        # next is a box
        for next in graph["adj"][current]:
        
            new_cost, new_point = adj(detail_points[current], next, cost_so_far[current], dst_point)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                prev[next] = current
                heappush(frontier, (new_cost, next))
                visited_nodes.append(next)
                detail_points[next] = new_point

    print("No Path Possible!")
    return([], [])
    
# calculates a new point in a box and its associated distance and priority for use in the priority queue
def dist_point_in_box(point, dst_box, distance_traveled, dst_point):
    point_x, point_y = point
    box_x1, box_x2, box_y1, box_y2 = dst_box
    dx, dy = (0, 0)
    
    dest_x, dest_y = dst_point
    
    if point_x < box_x1:    # set x distance to minimum distance to box in x direction if point is not in box
        dx = box_x1 - point_x
    if point_x > box_x2:    # set x distance to minimum distance to box in x direction if point is not in box
        dx = box_x2 - point_x
    if point_y < box_y1:    # set y distance to minimum distance to box in y direction if point is not in box
        dy = box_y1 - point_y
    if point_y > box_y2:    # set y distance to minimum distance to box in y direction if point is not in box
        dy = box_y2 - point_y
        
    new_pt = (point_x + dx, point_y + dy) # new point's coordinates
    new_dst = distance_traveled + sqrt(dx * dx + dy * dy)
    
    return (new_dst, new_pt)