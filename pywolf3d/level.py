import json
import logging

from ursina import Entity, scene, color, random


logger = logging.getLogger(__name__)

class Cube(Entity):
    def __init__(self, code,  position=(0,0,0)):
        green = code / 256
        red = 1 - green
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color.color(green, red, random.uniform(.9, 1.0)),
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

    # https://devinsmith.net/backups/xwolf/tiles.html
    # all valid values for walls
    wall_lists = range(0,63+1)
    floor_lists = range(106,143+1)
    door_lists = range(90, 101+1)
    start = (1,5,1)

    def __init__(self, levelfile=None):
        if levelfile:
            with open(levelfile) as f:
                data = json.load(f)
            self.level = data['level']

            self._cull_walls()

            for coord, code in data['object_list']:
                if code in [19, 20, 21, 22]:
                    self.start = (coord[1], 5, coord[0])


    def _cull_walls(self):
        '''takes in a level, culls all interal cubes
        cuts the number of cubes in a level to a minimum

        replaces the code for each wall with an -1 - internal wall code'''
        cull_list = []
        for i in range(self.w):
            for j in range(self.h):
                if self.level[i][j] in self.floor_lists:
                    continue
                if self.level[i][j] in self.wall_lists and \
                        (i == 0 or self.level[i-1][j] in self.wall_lists) and \
                        (i == self.w-1 or self.level[i+1][j] in self.wall_lists) and \
                        (j == 0 or self.level[i][j-1] in self.wall_lists) and \
                        (j == self.h-1 or self.level[i][j+1] in self.wall_lists):
                    cull_list.append((i,j))

        for i,j in cull_list:
            self.level[i][j] = -1

    @property
    def w(self):
        return len(self.level)

    @property
    def h(self):
        return len(self.level[0])

    @property
    def player_start(self):
        return self.start

    def load(self):
        logger.info("rendering cubes from map")
        for z, row in enumerate(self.level):
            h = len(row)
            assert h == self.h, f"row {z} is wrong length {self.h} {h}"
            for x, val in enumerate(row):
                if val == -1:
                    continue

                if val not in self.floor_lists \
                        and val not in self.door_lists:
                    cube = Cube(val, position=(x,1,z))
                else:
                    cube = Cube(255, position=(x,0,z))


                if val not in self.wall_lists and \
                        val not in self.floor_lists:
                    print(f"square {val} not in valid floor or wall lists")
