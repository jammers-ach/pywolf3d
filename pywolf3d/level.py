import json
import logging

from ursina import Entity, scene, color, random, Grid, Plane, load_texture

from wall_runner import LevelOptimiser

logger = logging.getLogger(__name__)

class Cube(Entity):
    def __init__(self, code,  position=(0,0,0)):
        wall_code = code*2
        fname = f'wall{wall_code:04d}'
        txt = load_texture(fname, path="wolfdata/extracted/")
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = txt,
            color = color.white,
            collision=True,
            collider='box'
        )



class LevelLoader():
    level = [[33,107,107,107,107,107,33],
             [33,107,107,107,107,107,33],
             [33,107,107,107,107,107,33],
             [33,107,107,107,107,107,33],
             [33,107,107,107,107,107,33],
             [33,107,107,107,107,107,33],
             [33,107,107,107,107,107,33],
             [33,107,107,107,107,107,33],
             [33,33,33,33,33,33,33]]
    start = (0,5,0)

    # https://devinsmith.net/backups/xwolf/tiles.html
    # all valid values for walls, floors an doors
    wall_lists = range(0,63+1)
    floor_lists = range(106,143+1)
    door_lists = range(90, 101+1)

    def __init__(self, levelfile=None):
        if levelfile:
            with open(levelfile) as f:
                data = json.load(f)
            self.level = data['level']

            for coord, code in data['object_list']:
                if code in [19, 20, 21, 22]:
                    self.start = (coord[1], 5, coord[0])



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
        lo = LevelOptimiser(self.level,
                            self.wall_lists,
                            self.floor_lists,
                            self.door_lists)
        level = lo.optimise()
        total_cubes = 0


        Entity(model=Grid(self.w,self.h),
               position=(int(self.w/2), 0, int(self.h/2)),
               scale=max(self.w, self.h),
               color=color.color(0,0,0),
               collision=True,
               collider='box',
               rotation_x=90)

        for z, row in enumerate(level):
            h = len(row)
            assert h == self.h, f"row {z} is wrong length {self.h} {h}"
            for x, val in enumerate(row):
                if val == -1:
                    continue

                if val not in self.floor_lists \
                        and val not in self.door_lists:
                    Cube(val, position=(x,1,z))
                    total_cubes +=1


                if val not in self.wall_lists and \
                        val not in self.floor_lists:
                    print(f"square {val} not in valid floor or wall lists")
        print(f"made {total_cubes} walls")

