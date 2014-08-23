from game_options import rendering_opts
#from maze import generate_maze
SCREEN_SIZE = (800, 600)

from math import radians 

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

from gameobjects.matrix44 import *
from gameobjects.vector3 import *
from cube import Cube
from map import GameMap

def resize(width, height):
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    if(rendering_opts['perspective']):
        gluPerspective(60.0, float(width)/height, .1, 1000.)
    else:
        glOrtho(-1,1,-1,1,-0.5,10);
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    
    glEnable(GL_DEPTH_TEST)
    
    glShadeModel(GL_FLAT)
    glClearColor(1.0, 1.0, 1.0, 0.0)

    glEnable(GL_COLOR_MATERIAL)
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)        
    glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))    
    

test_map = [[1,1,1,1],[0,0,0,0],[0,0,0,0],[0,1,0,0],[1,1,1,1]]    
#test_map = generate_maze(20,20)



def run():
    
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
    
    resize(*SCREEN_SIZE)
    init()
    
    clock = pygame.time.Clock()    
    
    glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))    
    glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    

    # This object renders the 'map'
    print test_map
    game_map = GameMap(test_map)        
    player = game_map.add_player(1, 2)


    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return                
            
        # Clear the screen, and z-buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                        
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.
        
        pressed = pygame.key.get_pressed()
        player.do_input(pressed)
        player.update_vectors(time_passed_seconds)
        
        # Upload the inverse camera matrix to OpenGL
        glLoadMatrixd(player.camera_matrix.get_inverse().to_opengl())
                
        # Light must be transformed as well
        glLight(GL_LIGHT0, GL_POSITION,  (0, 1.5, 1, 0)) 
                
        # Render the map
        game_map.render()
        
                
        # Show the screen
        pygame.display.flip()

run()