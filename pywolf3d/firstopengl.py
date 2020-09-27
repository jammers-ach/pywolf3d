from game_options import rendering_opts
SCREEN_SIZE = (800, 600)

from math import radians

from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

from pywolf3d.math import Matrix44
from pywolf3d.math import Vector3
from cube import Cube
from map import GameMap
#from sprite import MObject
from things import ImmovableThing, PassableThing, PickupThing

from pywolf3d.render.glmaprender import  GLGameMapRender


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

    #glEnable(GL_LIGHTING)
    #glEnable(GL_LIGHT0)
    #glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))
    glEnable (GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

    #glBlendFunc (GL_ONE, GL_ONE)

test_map  = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
             [1,0,0,0,1,0,0,3,3,3,3,3,3,3,3,3,3,3],
             [1,0,0,0,0,0,0,0,11,0,0,0,0,0,0,0,0,3],
             [1,0,0,0,1,0,0,0,3,0,0,0,0,0,0,0,0,3],
             [1,1,0,1,1,0,0,3,3,3,3,3,3,3,0,0,0,3],
             [1,1,0,1,1,0,0,1,1,1,1,1,1,4,0,0,4,1],
             [1,1,0,1,1,0,0,0,0,0,1,0,1,4,0,0,4,1],
             [1,1,10,1,1,0,0,1,1,0,0,0,0,0,0,0,0,1],
             [1,1,0,1,1,0,0,0,1,0,5,0,0,0,5,0,0,1],
             [1,1,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,1],
             [1,2,0,2,1,1,0,0,0,0,5,0,0,0,5,0,0,1],
             [6,0,0,0,6,1,0,0,1,0,0,0,0,0,0,0,0,1],
             [6,0,0,0,6,1,0,0,1,0,5,0,0,0,5,0,0,1],
             [6,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
             [6,6,6,6,6,1,1,1,1,1,1,1,1,1,1,1,1,1]]


FPS=rendering_opts['fps']

def run():

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)

    resize(*SCREEN_SIZE)
    init()

    clock = pygame.time.Clock()

    glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
    glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))


    # This object renders the 'map'
    #print test_map
    object_list = [ ImmovableThing(2,2,3),PassableThing(2,3,2),PickupThing(2,4,1),PickupThing(1,1,1)]
    game_map = GameMap(test_map,object_list)
    player = game_map.add_player(2, 3)

    maprender = GLGameMapRender(game_map)


    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYUP and event.key == K_ESCAPE:
                return

        # Clear the screen, and z-buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);


        if(FPS):
            time_passed = clock.tick(FPS)
        else:
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
        maprender.render()
        maprender.objects_render(player)

        # Show the screen
        pygame.display.flip()


if __name__ == '__main__':
    run()
