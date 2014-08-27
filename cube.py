'''
Created on 21 Aug 2014

@author: jammers
'''
from gameobjects.vector3 import *
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

from os import listdir
from os.path import isfile, join

from textures import prep_texture
from game_options import rendering_opts

from wall_loader import load_walls


#if we're rendering colours
default_colour = (1,1,1)
black = (0,0,0)


darken_colour = lambda x:(x[0]* rendering_opts['darken_factor'],\
                          x[1]* rendering_opts['darken_factor'],\
                          x[2]* rendering_opts['darken_factor'])

wall_types = None
flat_types = None
default_texture=None

def load_textures():
    global wall_types
    global flat_types
    global default_texture
    
    wall_types,flat_types = load_walls()
    

class Cube(object):
    
    
    def __init__(self, position, wall_type,rendered_normals=[0,1,2,3]):
        
        self.position = position
        self.wall_type_code = wall_type
        self.rendered_normals = rendered_normals
        
        if(wall_types == None):
            load_textures()
            
        self.wall_type = wall_types[self.wall_type_code]
    
    num_faces = 5
    top_face = 4
    dark_faces = [0,1]
    light_faces = [2,3]
        
    vertices = [ (0.0, 0.0, 1.0),
                 (1.0, 0.0, 1.0),
                 (1.0, 1.0, 1.0),
                 (0.0, 1.0, 1.0),
                 (0.0, 0.0, 0.0),
                 (1.0, 0.0, 0.0),
                 (1.0, 1.0, 0.0),
                 (0.0, 1.0, 0.0) ]
    
    t_index = [  (0.0, 0.0),
                 (1.0, 0.0),
                 (1.0, 1.0),
                 (0.0, 1.0), ]
        
    normals = [ (0.0, 0.0, +1.0),  # front
                (0.0, 0.0, -1.0),  # back
                (+1.0, 0.0, 0.0),  # right
                (-1.0, 0.0, 0.0),  # left 
                (0.0, +1.0, 0.0),  # top
                (0.0, -1.0, 0.0) ] # bottom
    
    vertex_indices = [ (0, 1, 2, 3),  # front
                       (4, 5, 6, 7),  # back
                       (1, 5, 6, 2),  # right
                       (0, 4, 7, 3),  # left
                       (3, 2, 6, 7),  # top
                       (0, 1, 5, 4) ] # bottom    


    def render(self):
        if(rendering_opts['textures']):
            return self.render_texture()
        else:
            return self.render_color()
        
        
    def render_texture(self):

        #Load dark texture
        prep_texture(self.wall_type.texture1)
        vertices = [tuple(Vector3(v) + self.position) for v in self.vertices]
        
        glBegin(GL_QUADS)
    
        #Draw the 4 textured sides
        for face_no in self.light_faces:
            if(face_no != self.top_face and face_no in self.rendered_normals):
                glNormal3dv( self.normals[face_no] )
                
                v1, v2, v3, v4 = self.vertex_indices[face_no]
    
                glTexCoord2fv(self.t_index[0])
                glVertex( vertices[v1] )
                glTexCoord2fv(self.t_index[1])
                glVertex( vertices[v2] )
                glTexCoord2fv(self.t_index[2])
                glVertex( vertices[v3] )
                glTexCoord2fv(self.t_index[3])
                glVertex( vertices[v4] )            

        glEnd()
        
        #Now the dark faces
        prep_texture(self.wall_type.texture2)
        
        glBegin(GL_QUADS)
        for face_no in self.dark_faces:
            if(face_no != self.top_face and face_no in self.rendered_normals):
                glNormal3dv( self.normals[face_no] )
                
                v1, v2, v3, v4 = self.vertex_indices[face_no]
            
                glTexCoord2fv(self.t_index[0])
                glVertex( vertices[v1] )
                glTexCoord2fv(self.t_index[1])
                glVertex( vertices[v2] )
                glTexCoord2fv(self.t_index[2])
                glVertex( vertices[v3] )
                glTexCoord2fv(self.t_index[3])
                glVertex( vertices[v4] ) 
        glEnd()
        

        #if(self.top_face in self.rendered_normals):
        #    glColor( black )
        #    glBegin(GL_QUADS)
        #    glNormal3dv( self.normals[self.top_face] )
        #    v1, v2, v3, v4 = self.vertex_indices[self.top_face]
        #    glVertex( vertices[v1] )
        #    glVertex( vertices[v2] )
        #    glVertex( vertices[v3] )
        #    glVertex( vertices[v4] ) 
        #    glEnd()
        

    def render_color(self):                
        
        gl_col = colour_maps.get(self.wall_type,default_colour)

        glColor( gl_col )
    
        # Adjust all the vertices so that the cube is at self.position
        vertices = [tuple(Vector3(v) + self.position) for v in self.vertices]
            
        #Now the dark sdes
        glBegin(GL_QUADS)
    
        for face_no in self.light_faces:
            if(face_no != self.top_face and face_no in self.rendered_normals):
                glNormal3dv( self.normals[face_no] )
                
                v1, v2, v3, v4 = self.vertex_indices[face_no]
                        
                glVertex( vertices[v1] )
                glVertex( vertices[v2] )
                glVertex( vertices[v3] )
                glVertex( vertices[v4] )            
            
        glEnd()
        
        #now the light side
        gl_col = darken_colour(colour_maps.get(self.wall_type,default_colour))
        glColor( gl_col )
        
        glBegin(GL_QUADS)
        for face_no in self.dark_faces:
            if(face_no != self.top_face and face_no in self.rendered_normals):
                glNormal3dv( self.normals[face_no] )
                
                v1, v2, v3, v4 = self.vertex_indices[face_no]
                        
                glVertex( vertices[v1] )
                glVertex( vertices[v2] )
                glVertex( vertices[v3] )
                glVertex( vertices[v4] )            
            
        glEnd()
        
        
        if(self.top_face in self.rendered_normals):
            glColor( black )
            glBegin(GL_QUADS)
            glNormal3dv( self.normals[self.top_face] )
            v1, v2, v3, v4 = self.vertex_indices[self.top_face]
            glVertex( vertices[v1] )
            glVertex( vertices[v2] )
            glVertex( vertices[v3] )
            glVertex( vertices[v4] ) 
            glEnd()
        
        
        
        

class FlatSurface(object):
    '''
    A represetnation of the floor object
    '''

    height = 0.0

    def __init__(self,w,h,code,x=0,y=0):
        '''
        initilises the wall
        '''
        self.code = code
        if(flat_types == None):
            load_textures()
        self.flat_type = flat_types[code]
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        
        self.vertices = ((x,self.height,y),(x+w,self.height,y),(x+w,self.height,y+h),(x,self.height,y+h))
        self.t_index = [  (0.0, 0.0),
                 (w, 0.0),
                 (w, h),
                 (0.0, h), ]
    
    def render(self):
#         self.render_color()
        if(rendering_opts['textures']):
            return self.render_texture()
            #return self.render_color()
        else:
            return self.render_color()
        
        

        
        
    def render_texture(self):
        prep_texture(self.flat_type.texture)
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
    
    def render_color(self):
        
        gl_col = default_colour
        glColor( gl_col )
        glBegin(GL_QUADS)
        
        glNormal3dv( (0.0, +1.0, 0.0) )
        v1, v2, v3, v4 = self.vertices
        glVertex( v1 )
        glVertex( v2 )
        glVertex( v3 )
        glVertex( v4 )  
        glEnd()
        
        

class Floor(FlatSurface):
    '''
    A represetnation of the floor object
    '''
    pass


class Celing(FlatSurface):
    '''
    A represetnation of the floor object
    '''
    height = 1
