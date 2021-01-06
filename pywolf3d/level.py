import json
import logging

from ursina import Entity, scene, color, random, Grid, Plane, load_texture, curve

from wall_runner import LevelOptimiser

logger = logging.getLogger(__name__)


class Wall(Entity):
    def __init__(self, texture_file, position=(0,0,0),
                 facing='n'):
        txt = load_texture(texture_file, path="wolfdata/extracted/")
        x,y,z = position

        x_off = 0
        z_off = 0
        z_rot = 0

        if facing == 'w':
            z_off = -0.5
        elif facing == 'e':
            z_off = 0.5
            z_rot = 180

        elif facing == 'n':
            x_off = 0.5
            z_rot = 90
        elif facing == 's':
            x_off = -0.5
            z_rot = -90

        super().__init__(
            parent = scene,
            position = (x + x_off, y+0.5, z + z_off),
            model = Plane((1,1)),
            texture = txt,
            color = color.white,
            collision=True,
            collider='box',
            rotation_x=-90,
            rotation_z=z_rot,
            add_to_scene_entities=False,
        )


class Door(Entity):
    duration = 2

    def __init__(self,texture_file, parent=scene, position=(0,0,0),
                 facing='ns'):
        txt = load_texture(texture_file, path="wolfdata/extracted/")
        sidetxt = load_texture("wall0100", path="wolfdata/extracted/")
        x,y,z = position

        z_off = 0
        x_off = 0
        z_rot = 0

        self.facing = facing
        assert facing in ['ns', 'ew']
        if facing == 'ns':
            z_rot = 90
            z_off = 0.5
        elif facing == 'ew':
            z_rot = 180
            x_off = -0.5
        else:
            raise Exception(f"direction {facing} is not valid for a door")

        super().__init__(
        )

        self.door_x = x
        self.door_y = y+0.5
        self.door_z = z

        self.door1 = Entity(
            parent=self,
            position = (x, y+0.5, z),
            model = Plane((1,1)),
            texture = txt,
            color = color.white,
            collision=True,
            collider='box',
            rotation_x=-90,
            rotation_z=z_rot,
        )
        self.door2 = Entity(
            parent=self,
            position = (x, y+0.5, z),
            model = Plane((1,1)),
            texture = txt,
            color = color.white,
            collision=True,
            collider='box',
            rotation_x=-90,
            rotation_z=z_rot - 180,
        )

        self.door_side1 = Entity(
            parent=self,
            position = (x+x_off, y+0.5, z+z_off),
            model = Plane((1,1)),
            texture = sidetxt,
            color = color.white,
            collision=False,
            collider='box',
            rotation_x=-90,
            rotation_z=z_rot - 90,
        )

        self.door_side2 = Entity(
            parent=self,
            position = (x-x_off, y+0.5, z-z_off),
            model = Plane((1,1)),
            texture = sidetxt,
            color = color.white,
            collision=False,
            collider='box',
            rotation_x=-90,
            rotation_z=z_rot + 90,
        )

    def open(self):
        dz = -1 if self.facing == 'ns' else 0
        dx = -1 if self.facing == 'ew' else 0
        target = (self.door_x + dx, self.door_y, self.door_z + dz)
        self.door1.animate_position(target, self.duration, curve=curve.linear)
        self.door2.animate_position(target, self.duration, curve=curve.linear)

    def close(self):
        print("Closing door")
        target = (self.door_x, self.door_y, self.door_z)
        self.door1.animate_position(target, self.duration, curve=curve.linear)
        self.door2.animate_position(target, self.duration, curve=curve.linear)

class LevelLoader():
    level = [[33,33,33,33,33,33,33],
             [33,107,107,107,107,107,33],
             [33,33,107,107,107,33,33],
             [33,107,107,107,107,107,33],
             [33,107,107, 33,107,107,33],
             [33,107,107,107,107,107,33],
             [33,107,107,107,107,107,33],
             [33,107,107,107,107,107,33],
             [33,33,33,33,33,33,33]]
    start = (1,5,1)

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


    def wall_file_name(self, val, northsouth=False):
        '''returns the filename for a wall code'''
        wall_code = (val-1)*2
        if northsouth:
            wall_code += 1
        fname = f'wall{wall_code:04d}'
        return fname

    def door_file_name(self, val, northsouth=False):
        '''returns the filename for a door code'''
        return 'wall0098'

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

                if val in self.floor_lists:
                    continue
                if val in self.door_lists:
                    face = "ew" if val %2 else "ns"
                    Door(self.door_file_name(val), position=(x,0,z),
                         facing=face,
                         parent=walls)

                if val in self.wall_lists:
                    for face in lo.external_walls(z,x):
                        Wall(self.wall_file_name(val, northsouth=face=='n' or face =='s'), position=(x,0,z),
                            facing=face, )
                        total_cubes += 1


        print(f"made {total_cubes} walls")

