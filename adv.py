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
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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

#reverse helper 
def reverse(direction):
    if direction == 'n':
        return 's'
    if direction == 's':
        return 'n'
    if direction == 'e':
        return 'w'
    if direction == 'w':
        return 'e'

def mark_visited(curr_room, exits):
    visited[curr_room] = {}
    for direction in exits:
        #print(direction)
        visited[curr_room][direction] = '?'
        #print(visited)

def path_builder(curr_room):
    curr_room = player.current_room.id
    curr_exits = player.current_room.get_exits()
    # track the prev room
    prev_room = None       
    # build a stack 
    s = Stack()
    # add starting room to the stack
    #print(player.current_room)
    s.push([None, curr_room, prev_room, curr_exits])

    while len(visited) < len(room_graph):
        path = s.pop()
        #print(path)
        # destructure my path
        direction = path[0]
        curr_room = path[1]
        prev_room = path[2]
        curr_exits = path[3]
        
        # if cur room not in visited add it
        #print(curr_room)
        if curr_room not in visited:
            mark_visited(curr_room, curr_exits)

        # check to see if I have moved if I have set the prev room to the reverse direction
        if direction is not None:
            visited[curr_room][reverse(direction)] = prev_room

        # check to see if there is a room that I just left
        #print(prev_room)
        if prev_room is not None:
            visited[prev_room][direction] = curr_room
            

        # loop the room I am in to see if there is another path
        for d in visited[curr_room].keys():
            
            if visited[curr_room][d] == '?':
                # push the path im on
                s.push(path)
                # hold the room im in
                prev_room = player.current_room.id
                # move my player
                player.travel(d)
                traversal_path.append(d)
                #push my moved path
                s.push([d, player.current_room.id, prev_room, player.current_room.get_exits()])
                # break the loop
                break
        # travel backwards
        if curr_room == player.current_room.id:
            player.travel(reverse(direction))
            traversal_path.append(reverse(direction))


        
        
        
path_builder(player.current_room.id)
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
