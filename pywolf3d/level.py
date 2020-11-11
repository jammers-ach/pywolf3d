from ursina import Entity, scene, color, random

class Cube(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color = color.lime,
        )

class LevelLoader():

    def load(self):
        for z in range(8):
            for x in range(8):
                cube = Cube(position=(x,0,z))

