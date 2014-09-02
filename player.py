'''
Created on 22 Aug 2014

@author: jammers
'''
from gameobjects.matrix44 import Matrix44
from gameobjects.vector3 import Vector3

import pygame
from pygame.locals import *
from game_options import rendering_opts
from math import radians 


class Player(object):
    '''
    A player than can move around the map
    '''


    def __init__(self,game_map,x,y,direction=0.0):
        self.game_map = game_map #the game map we have
        self.x = float(x) + 0.5 #We start off in the middle of the square
        self.y = float(y) + 0.5 #We start off in the middle of the square
        self.facing = direction
        self.rotation_speed = radians(rendering_opts['rot_speed'])
        self.movement_speed = rendering_opts['movement_speed']
        
        self.camera_matrix = Matrix44()
        self.camera_matrix.translate = (self.x, rendering_opts['player_height'], self.y)
        
        self.rotation_direction = Vector3()
        self.movement_direction = Vector3() 
    

    def do_input(self,pressed):
        '''Takes the key input and handles updates the movement/rotation vectors'''
        self.rotation_direction.set(0.0, 0.0, 0.0)
        self.movement_direction.set(0.0, 0.0, 0.0)
        
        # Modify direction vectors for key presses
        if pressed[K_LEFT]:
            self.rotation_direction.y = +1.0
        elif pressed[K_RIGHT]:
            self.rotation_direction.y = -1.0
        if pressed[K_UP]:
            self.movement_direction.z = -1.0
        elif pressed[K_DOWN]:
            self.movement_direction.z = +1.0
    
    def update_vectors(self,time_passed_seconds):
        '''updates the position after a time has passed'''
        
        #Update roation vector
        rotation = self.rotation_direction * self.rotation_speed * time_passed_seconds
        rotation_matrix = Matrix44.xyz_rotation(*rotation)        
        self.camera_matrix *= rotation_matrix
        
        # Calcluate movment and add it to camera matrix translate
        heading = Vector3(self.camera_matrix.forward)
        movement = heading * self.movement_direction.z * self.movement_speed        
            
        #Find the x and y of how far forward we move
        movement_x = movement[0] * time_passed_seconds
        movement_y = movement[2] * time_passed_seconds
        
        #Move us in the aproropiate direction if we won't hit a wall
        if(movement_y != 0):
            wall_buffer= rendering_opts['wall_backoff'] if movement_y > 0 else -rendering_opts['wall_backoff']
            
            if(self.game_map.can_go(self.x,self.y + movement_y + wall_buffer )):
                self.camera_matrix[3,2] = self.y + movement_y
                self.y = self.y + movement_y

        
        if(movement_x != 0):
            wall_buffer= rendering_opts['wall_backoff'] if movement_x > 0 else -rendering_opts['wall_backoff']
            
            if(self.game_map.can_go(self.x + movement_x +wall_buffer,self.y )):
                self.camera_matrix[3,0] = self.x + movement_x
                self.x = self.x + movement_x

        if(movement_x != 0 or movement_y != 0):

            self.game_map.handle_pickups(self)
