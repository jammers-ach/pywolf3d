import logging

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


class SolidSprite(Sprite):
    pass
