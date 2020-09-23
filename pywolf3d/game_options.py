'''
Created on 21 Aug 2014

@author: jammers
'''


rendering_opts = {
                  'textures':True, #Render with textures
                  'tex_dir':'textures/', #default_textures directory
                  'wall_dir':'walls/', #default subdirectory for walls
                  'sprite_dir':'sprites/',#default subdirectory for sprites
                  'perspective':True, #View in perspecitve mode or orthogonal
                  'rot_speed':90, #What speed to we rotate at
                  'player_height':0.6, #Player height
                  'movement_speed':5.0, #Movement speed default
                  'wall_backoff':0.3, #Of far from the wall we render so we don't see
                  'darken_factor':0.5, #How much do we darken the two surfaces by
                  'transparent_colour':(152,0,136),#rgb of that transparent colour
                  'fps':None, #How many FPS should we limit ourselves to?
                  'door_start_code':10,#When do wall codes and and door codes being?
                  }
