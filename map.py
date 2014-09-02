'''
Created on 21 Aug 2014

@author: jammers
'''
from gameobjects.vector3 import *
from OpenGL.GL import *
from OpenGL.GLU import *
from cube import Cube,Floor, Celing
import pygame
from pygame.locals import *
from player import Player
from gameobjects.util import linear_distance
from things import ImmovableThing,PickupThing

get_sides = lambda x,y: [(x,y+1),(x,y-1),(x+1,y),(x-1,y)]

class GameMap(object):
    
    def __init__(self,wall_layout,object_list):
        

        self.wall_layout = wall_layout
        
        self.w = len(wall_layout)
        self.h = len(wall_layout[1])
        
        self.cubes = {}
        

        self.display_list = None
        self.generate_cubes()
        self.update_cube_walls()
        self.players = []
        
        #For now just 1 floor
        self.floor = Floor(self.w, self.h, 1)
        self.ceiling = Celing(self.w,self.h,2)
        
        self.object_list = object_list
        self._make_object_lists()


    def _make_object_lists(self):
        self.immovable_objs = {}
        self.pickups = {}

        for obj in self.object_list:
            if(isinstance(obj,ImmovableThing)):
                self.immovable_objs[(obj.x,obj.y)] = [obj]
            if(isinstance(obj,PickupThing)):
                self.pickups[(obj.x,obj.y)] = [obj]



    def add_player(self,start_x,start_y):
        p = Player(self,start_x,start_y)
        self.players.append(p)
        return p
    
    def can_go(self,x,y):
        '''Can an object go into square x,y?
            checks for walls/immovable objects
            '''
        if(x > self.w or x < 0 or y > self.h or y < 0):
            return False
        try:
            if(self.wall_layout[int(x)][int(y)] != 0):
                return False
        except IndexError,e:
            return False

        #Now look through the objects
        pos = (int(x),int(y))
        if(pos in self.immovable_objs and self.immovable_objs[pos] != []):
            return False

        return True

    def handle_pickups(self,player):
        '''picks up any objects the player might be standing on'''
        print 'pickups'
        pos = (int(player.x),int(player.y))
        if(pos in self.pickups and self.pickups[pos] != []):
            for obj in self.pickups[pos]:
               if(obj.picked_up(player)):
                    self.pickups[pos].remove(obj)
                    self.object_list.remove(obj)
                    del obj
        
    def generate_cubes(self):
        '''generates all the cubes'''
        #Go throught he wall definitation and create cubes for all the no 0
        for y in range(self.h):            
            for x in range(self.w):
                
                try:
                    wall_type = self.wall_layout[x][y]
                    if(wall_type != 0):
                        
                        position = (float(x), 0.0, float(y))
                        cube = Cube( position, wall_type )
                        self.cubes[(x,y)] = cube            
                except IndexError,e:
                    #TODO log me nicely
                    pass

    
    def update_cube_walls(self):
        '''Finds out which walls of each cube need to be rendered'''
        for y in range(self.h):            
            for x in range(self.w):
                if((x,y) in self.cubes):
                    check = [(x,y+1),(x,y-1),(x+1,y),(x-1,y)]
                    rendered_normals = []
                    for i in xrange(len(check)):
                        if(check[i] not in self.cubes or self.cubes[check[i]] == 0 ):
                            rendered_normals.append(i)
                    rendered_normals.append(4)
                    self.cubes[(x,y)].rendered_normals = rendered_normals
 
  


    def _sort_objects(self,player):
        '''Sorts all the objects by distance to the player so they are rendered int he right order'''
        posx = player.x
        posy = player.y

        self.sorted_objects = []

        for obj in self.object_list:
            distance = linear_distance((posx,posy),(obj.x,obj.y)) 
            self.sorted_objects.append((distance,obj))

        self.sorted_objects = sorted(self.sorted_objects,reverse=True)

    def objects_render(self,player):
        '''Renders the object, which need a player so they can face the camera'''
        self._sort_objects(player)
        for dist,obj in self.sorted_objects:
            obj.render(player.camera_matrix.get_row_vec3(0))


    def render(self):
                
        if self.display_list is None:
            
            # Create a display list
            self.display_list = glGenLists(1)                
            glNewList(self.display_list, GL_COMPILE)
            
            # Draw the cubes
            for cube in self.cubes.values():
                cube.render()
                
            #draw the floor, draw the ceiling
            self.floor.render()
            self.ceiling.render()
                           
            # End the display list
            glEndList()
            
        else:
            
            # Render the display list            
            glCallList(self.display_list)
