from room import Room
from player import Player
from world import World

from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = {}

# we have a starting vertex
# start at 0 and taverse until that route dead ends
# once there is no where else to go we need to back up to the next available room 

# build a stack 
s = Stack()
# add starting room to the stack
#print(player.current_room)
s.push([player.current_room.id])

while len(player.current_room.get_exits()) != 1:
    path = s.pop()
    #print(path)
    curr_room = path[-1]

    if curr_room not in visited:
        visited[curr_room] = {}
        for direction in player.current_room.get_exits():
            #print(direction)
            visited[curr_room][direction] = '?'
            #print(visited)
    ran_dir = random.choice(list(visited[curr_room].keys()))
    visited[curr_room][ran_dir] = player.current_room.get_room_in_direction(ran_dir).id

    # move the ran dir
    old_room = curr_room
    player.travel(ran_dir)
    traversal_path.append(ran_dir)
    visited[curr_room]

    print(visited)
# print('traversal_path:',traversal_path)
# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
