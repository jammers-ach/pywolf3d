'''
Created on 21 Aug 2014

http://www.pygame.org/wiki/SimpleOpenGL2dClasses?parent=CookBook

@author: jammers
'''


from OpenGL.GL import *

import os
from game_options import rendering_opts
import pygame

darken = lambda x,f: int(x*f)

def darken_surf(surface):
    '''Darkens a surface'''
    #Todo this is really ineffcient
    
    ix = surface.get_width()
    iy = surface.get_height()
    f = rendering_opts['darken_factor']
    for x in range(ix):
        for y in range(iy):
            r,b,g,a = surface.get_at((x,y))

            surface.set_at((x,y),(darken(r,f),darken(b,f),darken(g,f),a))
    

def load_texture(imageName,darken=True):
    """Load an image file as a 2D texture using pygame,
    returns two textures, the normal one and the darker one"""
    p = os.path.join(rendering_opts['tex_dir'],imageName)
    textureSurface = pygame.image.load(p)
    
    light_image = pygame.image.tostring(textureSurface, "RGBA", 1)
    
    ix = textureSurface.get_width()
    iy = textureSurface.get_height()
    
    ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, ID)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(
            GL_TEXTURE_2D, 0, 3, ix, iy, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, light_image
        )
    
    ID2=None
    if(darken):
        darken_surf(textureSurface)
        dark_image = pygame.image.tostring(textureSurface, "RGBA", 1)
        ID2 = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, ID2)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(
                GL_TEXTURE_2D, 0, 3, ix, iy, 0,
                GL_RGBA, GL_UNSIGNED_BYTE, dark_image
            )
    
    print "TEXTURE: loaded %s" % p
    return ID,ID2

def prep_texture(texture):
    '''Preps a texture for rendering'''
    glEnable(GL_TEXTURE_2D)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    
    glBindTexture(GL_TEXTURE_2D, texture)
