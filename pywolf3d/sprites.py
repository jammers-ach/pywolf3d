import logging

from pywolf3d import util
from ursina import Entity, scene, Plane, color, load_texture

logger = logging.getLogger(__name__)


class Sprite(Entity):
    def __init__(self, texture, position, parent=scene):
        x, y, z = position
        txt = load_texture(texture, path="wolfdata/extracted/")

        super().__init__(
            parent = scene,
            position = (x , y+0.5, z ),
            model = Plane((1,1)),
            texture = txt,
            rotation_x=-90,
            color = color.white,
            add_to_scene_entities=False,
        )

    @classmethod
    def texture_filename(cls, val):
        '''returns the filename for a wall code'''
        sprite_code = val - 21
        fname = f'sprite{sprite_code:04d}'
        return fname

    def face(self, target):
        ''' rotates this sprite so it faces target'''
        self.rotation_y = target.rotation_y


class SolidSprite(Sprite):
    pass

class FacingSprite(Entity):
    '''A sprite that faces away from the player
    i.e there are 8 different sides to it'''

    def __init__(self, position, parent=scene):
        x, y, z = position

        self.direction_textures = [load_texture(x, path="wolfdata/extracted/") for x in [
            "sprite0050", # towards you
            "sprite0051", # a little left
            "sprite0052", # facing left
            "sprite0053", # back left
            "sprite0054", # facing back
            "sprite0055", # back right
            "sprite0056", # facing right
            "sprite0057", # front right
        ]]

        super().__init__(
            parent = scene,
            position = (x , y+0.5, z ),
            model = Plane((1,1)),
            texture = self.direction_textures[0],
            rotation_x=-90,
            color = color.white,
            add_to_scene_entities=False,
        )

    def face(self, target):
        ''' rotates this sprite so it faces target'''
        self.rotation_y = target.rotation_y
        angle = util.direction_to_target(self.position, target.position)
        direction = util.angle_to_dir(angle)
        self.texture = self.direction_textures[direction]



