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
            collision=True,
            collider='box'
        )


class LevelLoader():
    level = [[0,0,0,0,0,0,1],
             [1,0,0,0,0,0,1],
             [1,0,0,0,0,0,1],
             [1,0,0,0,0,0,1],
             [1,0,0,0,0,0,1],
             [1,0,0,0,0,0,1],
             [1,0,0,0,0,0,1],
             [1,0,0,0,0,0,1],
             [1,1,1,1,1,1,1]]

    @property
    def w(self):
        return len(self.level)

    @property
    def h(self):
        return len(self.level[0])

    def load(self):
        for z, row in enumerate(self.level):
            h = len(row)
            assert h == self.h, f"row {z} is wrong length {self.h} {h}"
            for x, val in enumerate(row):
                if val:
                    cube = Cube(position=(x,0,z))


        for x in range(self.w+2):
            for z in range(self.h+2):
                cube2 = Cube(position=(x-1,-1,z-1))


