#Sprite - Information for game sprites and objects
from textures import load_texture,prep_texture
import os
from game_options import rendering_opts
from gameobjects.vector3 import *
from OpenGL.GL import *
from OpenGL.GLU import *

sprite_mapping = None

sprite_mapping = None

sprite_height = 1.0
sprite_width = 1.0

def load_sprites():
    global sprite_mapping
    #Just load in one texture for now while we are testing

    sprite_mapping = {}
    a = os.path.join(rendering_opts['sprite_dir'],'Sprite-227.png')

    sprite_mapping[1] = {'texture':load_texture(a,darken=False)[0]}

class MObject(object): 
    '''A map object'''

    def __init__(self,x,y,obj_type):
        self.x = x
        self.y = y

        if(sprite_mapping == None):
            load_sprites()

        self.obj_type = obj_type
        self.sprite = sprite_mapping[obj_type]
        
        w = sprite_width
        h = sprite_height
        #put us in the middle of the square facing n/s
        self.vertices = ((x,0,y+0.5),(x+w,0,y+0.5),(x+w,1,y+0.5),(x,1,y+0.5))

        self.t_index = [  (0.0, 0.0),
                 (w, 0.0),
                 (w, h),
                 (0.0, h), ]
    
    def render(self,camera_coords):
        '''In wolf3d sprites always faced the player
        we can't do that nicely here, so we have to render
        a texture that always faces the camera
        
        this will render the object so that it faces the camera coordinates'''


        prep_texture(self.sprite['texture'])
        glBegin(GL_QUADS)
        
        glNormal3dv( (0.0, +1.0, 0.0) )
        v1, v2, v3, v4 = self.vertices
        glTexCoord2fv(self.t_index[0])
        glVertex( v1 )
        glTexCoord2fv(self.t_index[1])
        glVertex( v2 )
        glTexCoord2fv(self.t_index[2])
        glVertex( v3 )
        glTexCoord2fv(self.t_index[3])
        glVertex( v4 ) 
        glEnd()

        
