import logging
import math

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
            "sprite0050",
            "sprite0051",
            "sprite0052",
            "sprite0053",
            "sprite0054",
            "sprite0055",
            "sprite0056",
            "sprite0057",
        ]]

        self.direction_index = 0

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
        direction = direction_to_target(self, target)
        self.texture = self.direction_textures[direction]




def direction_to_target(a, b):
    '''how many degrees from north is a to b'''
    x1, y1, z1 = a.position
    x2, y2, z2 = b.position

    x = x2-x1
    z = z2-z1

    theta = math.atan(z/x)
    angle = (90 - math.degrees(theta)) % 360
    return int(angle / 360 * 8)
