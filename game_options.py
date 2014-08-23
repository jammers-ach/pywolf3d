'''
Created on 21 Aug 2014

@author: jammers
'''


rendering_opts = {
                  'textures':True, #Render with textures
                  'tex_dir':'textures/', #default_textures directory
                  'wall_default':'Wall-000', #If there's no wall texture available what do we load
                  'floor_default':'Wall-000', #If there's no wall texture available what do we load
                  'perspective':True, #View in perspecitve mode or orthogonal
                  'rot_speed':90, #What speed to we rotate at
                  'player_height':0.6, #Player height
                  'movement_speed':5.0, #Movement speed default
                  'wall_backoff':0.3, #Of far from the wall we render so we don't see
                  'darken_factor':0.5, #How much do we darken the two surfaces by
                  }