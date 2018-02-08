# Navmesh Pathfinder Bidirectional A*
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
    
# bidirectional a star algorithm
def a_star_shortest_path(src_box, src_point, dst_box, dst_point, graph, adj):
    frontier = [] # priority queue using A* priority, containing boxes and the destination points for the direction it is searching
    visited_nodes = [] # list of boxes
    forward_detail_points = {} # dict of points with the box containing the point as the keys for searching for dst_point
    backwards_detail_points = {} # dict of points with the box containing the point as the keys for searching for src_point
    forward_cost_so_far = {} # dict of distances with boxes as keys starting with the src_box
    backwards_cost_so_far = {} # dict of distances with boxes as keys starting with dst_box
    forward_prev = {} # dict of boxes with boxes as keys starting with src_box
    backwards_prev = {} # dict of boxes with boxes as keys starting with dst_box
    
    forward_cost_so_far[src_box] = 0
    forward_prev[src_box] = None
    forward_detail_points[src_box] = src_point

    backwards_cost_so_far[dst_box] = 0
    backwards_prev[dst_box] = None
    backwards_detail_points[dst_box] = dst_point
    
    heappush(frontier, (0, src_box, dst_point))
    heappush(frontier, (0, dst_box, src_point))
    visited_nodes.append(src_box)
    visited_nodes.append(dst_box)
    
    current = None
    while frontier:
        # tmp_priority is thrown away, current is a box, goal_point is either src_point or dst_point based on what found it originally
        tmp_priority, current, goal_point = heappop(frontier)
        
        # if the current box is part of the other search's path, go calculate the path
        if goal_point == dst_point:
            if current in backwards_prev or current == dst_box:
                break
                
        if goal_point == src_point:
            if current in forward_prev or current == src_box:
                break
                
        # check if there are adjacent boxes that have not been visited or have a lower cost
        # next is a box
        for next in graph["adj"][current]:
        
            # forward section
            if goal_point == dst_point:
                new_cost, new_priority, new_point = adj(forward_detail_points[current], next, forward_cost_so_far[current], goal_point)
                if next not in forward_cost_so_far or new_cost < forward_cost_so_far[next]:
                    forward_cost_so_far[next] = new_cost
                    forward_prev[next] = current
                    heappush(frontier, (new_priority, next, goal_point))
                    visited_nodes.append(next)
                    forward_detail_points[next] = new_point
                    
            # backwards section
            if goal_point == src_point:
                new_cost, new_priority, new_point = adj(backwards_detail_points[current], next, backwards_cost_so_far[current], goal_point)
                if next not in backwards_cost_so_far or new_cost < backwards_cost_so_far[next]:
                    backwards_cost_so_far[next] = new_cost
                    backwards_prev[next] = current
                    heappush(frontier, (new_priority, next, goal_point))
                    visited_nodes.append(next)
                    backwards_detail_points[next] = new_point
                    
    # calculate the path going from inside to the outside
    if current in forward_prev and current in backwards_prev:
        path = []
                
        # if the source and destination are adjacent
        if current == src_box or current == dst_box:
            path.append((forward_detail_points[current], src_point))
            path.append((forward_detail_points[current], dst_point))
            
        else:
            point_as_box = current
            prev_point_as_box = forward_prev[current]
            path.append((forward_detail_points[current], forward_detail_points[prev_point_as_box]))
            
            # first half of path frome midpoint to source
            while point_as_box != src_box:
                path.append((forward_detail_points[point_as_box], forward_detail_points[prev_point_as_box]))
                point_as_box = forward_prev[point_as_box]
                prev_point_as_box = forward_prev[prev_point_as_box]
            
            point_as_box = current
            prev_point_as_box = backwards_prev[current]
            path.append((backwards_detail_points[current], backwards_detail_points[prev_point_as_box]))
            
            # second half of path from midpoint to destination
            while point_as_box != dst_box:
                path.append((backwards_detail_points[point_as_box], backwards_detail_points[prev_point_as_box]))
                point_as_box = backwards_prev[point_as_box]
                prev_point_as_box = backwards_prev[prev_point_as_box]
                
            #adds the midpoint back into the path drawing
            path.append((forward_detail_points[current], backwards_detail_points[current]))
            
        return (path, visited_nodes)
        
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
    new_pt_x, new_pt_y = new_pt
    new_dst = distance_traveled + sqrt(dx * dx + dy * dy)
    # heuristic for priority queue of distance so far + Euclidean distance from new point to destination
    priority = new_dst + sqrt((dest_x - new_pt_x) * (dest_x - new_pt_x) + (dest_y - new_pt_y) * (dest_y - new_pt_y))
    
    return (new_dst, priority, new_pt)
