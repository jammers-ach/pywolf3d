#Sprite - Information for game sprites and objects
from textures import load_translarent_texture,bind_texture
import os
from game_options import rendering_opts
from pywolf3d.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
import math
sprite_mapping = None

sprite_mapping = None

sprite_height = 1.0
sprite_width = 1.0



def load_sprites():
    global sprite_mapping
    #Just load in one texture for now while we are testing

    sprite_mapping = {}
    a = os.path.join(rendering_opts['sprite_dir'],'Sprite-251.png')
    b = os.path.join(rendering_opts['sprite_dir'],'Sprite-250.png')
    c = os.path.join(rendering_opts['sprite_dir'],'Sprite-205.png')


    sprite_mapping[1] = {'texture':load_translarent_texture(a)}
    sprite_mapping[2] = {'texture':load_translarent_texture(b)}
    sprite_mapping[3] = {'texture':load_translarent_texture(c)}




def remap_to_camera(camera_vector,verticies,pos):
    '''takes coordinates of 4 verticies, and the camera y angle and
    rotates the coordinates to face the camera'''
    #rotate
    i,j,k = camera_vector
    v = [(i*x,y,k*x) for x,y,z in verticies] #in each case x is the 'length', y doesn't change and z mirros x
    #It needs a diagram

    #translate
    v = [(x+pos[0]+0.5,y,z+pos[1]+0.5) for x,y,z in v]

    return v

class MObject(object):
    '''A map object'''

    def __init__(self,x,y,obj_type):
        self.x = x
        self.y = y

        if(sprite_mapping == None):
            load_sprites()

        self.obj_type = obj_type
        self.sprite = sprite_mapping[obj_type]

        #These aren't the verticies of the object, but the verticies of the coords
        #relative to a centre about which we rotate
        self.vertices = ((-0.5,0,0),(0.5,0,0),(0.5,1,0),(-0.5,1,0))

        self.t_index = [  (0.0, 0.0),
                 (sprite_height, 0.0),
                 (sprite_height, sprite_width),
                 (0.0, sprite_width), ]

    def render(self,camera_vector):
        '''In wolf3d sprites always faced the player
        we can't do that nicely here, so we have to render
        a texture that always faces the camera

        this will render the object so that it faces the camera coordinates'''

        bind_texture(self.sprite['texture'])
        glBegin(GL_QUADS)

        glNormal3dv( (0.0, +1.0, 0.0) )
        vertices = remap_to_camera(camera_vector,self.vertices,(self.x,self.y))
        v1, v2, v3, v4 = vertices
        glTexCoord2fv(self.t_index[0])
        glVertex( v1 )
        glTexCoord2fv(self.t_index[1])
        glVertex( v2 )
        glTexCoord2fv(self.t_index[2])
        glVertex( v3 )
        glTexCoord2fv(self.t_index[3])
        glVertex( v4 )
        glEnd()




