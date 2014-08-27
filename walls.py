#definitions of stuff to do with walls
from game_options import rendering_opts
import os
from textures import load_texture

load_wall = lambda a: load_texture(os.path.join(rendering_opts['wall_dir'],a),darken=False)[0]

class WallType(object):
    '''Gives us information about a wall, the texutres and a description'''

    def __init__(self,code,name,texture_1_path,texture_2_path,color=(0,0,0)):
        self.code = code
        self.name = name
        self.texture_1_path = texture_1_path
        self.texture_2_path = texture_2_path
        self.color = color

    def load_textures(self):
        '''Loads the textures from the walls'''

        self.texture1 = load_wall(self.texture_1_path)
        self.texture2 = load_wall(self.texture_2_path)


class FlatType(object):
    '''Gives us information about a flat (floor/ceiling)'''
    def __init__(self,code,name,texture,color=(0,0,0)):
        self.code = code
        self.name = name
        self.texture_path = texture
        self.color=color

    def load_textures(self):
        '''Loads the texture for this flat'''
        self.texture = load_wall(self.texture_path)


