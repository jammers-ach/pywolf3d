import json
import logging

from ursina import Entity, scene, color, Grid, Plane, load_texture, curve, invoke, Mesh, load_model, Vec3, MeshCollider

from wall_runner import LevelOptimiser
from sprites import SolidSprite

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

cube = (
    #x y z
    (0,0,0), #0
    (0,0,1), #1
    (0,1,0), #2
    (0,1,1), #3
    (1,0,0), #4
    (1,0,1), #5
    (1,1,0), #6
    (1,1,1), #7
)
quadverts = {
    'w': [cube[x] for x in (6 ,2 ,0, 4, 6, 0)], # 0 2 6 4
    'e': [cube[x] for x in (3 ,7 ,5, 1, 3, 5)], # 1 3 7 5
    'n': [cube[x] for x in (7 ,6 ,4, 5, 7, 4)], # 4 5 6 7
    's': [cube[x] for x in (2, 3, 1, 0, 2, 1)], # 0 1 2 3
}

class LevelMesh():
    def wall_file_name(self, val, northsouth=False):
        '''returns the filename for a wall code'''
        wall_code = (val-1)*2
        if northsouth:
            wall_code += 1
        fname = f'wall{wall_code:04d}'
        return fname

    def __init__(self, floor_pane, wall_codes, door_codes, floor_codes):
        lo = LevelOptimiser(floor_pane,
                            wall_codes,
                            floor_codes,
                            door_codes)
        level = lo.optimise()
        door_side_txt = load_texture("wall0100", path="wolfdata/extracted/")

        self.quad = load_model('quad')
        self.mesh_entities = {}
        dark = color.light_gray
        light = color.white
        faces = 0

        for z, row in enumerate(level):
            h = len(row)
            assert h == lo.h, f"row {z} is wrong length {lo.h} {h}"
            for x, val in enumerate(row):
                if val in wall_codes:
                    if val not in self.mesh_entities:
                        self.mesh_entities[val] = Entity(model=Mesh(),
                                                         collision=True,
                                                         collider='mesh',
                                                         texture=load_texture(self.wall_file_name(val), path="wolfdata/extracted/")
                     )
                    model = self.mesh_entities[val].model
                    for face in lo.external_walls(z,x):
                        texture_file = self.wall_file_name(val, northsouth=face=='n' or face =='s')
                        txt = load_texture(texture_file, path="wolfdata/extracted/")
                        model.vertices.extend(self.vertices(face, x, 0, z)) # add quad vertices, but offset.

                        if face == 'e' or face == 'w':
                            model.colors.extend((dark,) * len(self.quad.vertices)) # add vertex colors.
                        else:
                            model.colors.extend((light,) * len(self.quad.vertices)) # add vertex colors.

                        faces +=1

                if val in door_codes:
                    if val not in self.mesh_entities:
                        self.mesh_entities[val] = Entity(model=Mesh(),
                                                        collision=True,
                                                        collider='mesh',
                                                        texture=door_side_txt)
                    model = self.mesh_entities[val].model

                    face = "ew" if val %2 else "ns"
                    if face == "ew":
                        model.vertices.extend(self.vertices("n", x-1, 0, z))
                        model.colors.extend((light,) * len(self.quad.vertices)) # add vertex colors.
                        model.vertices.extend(self.vertices("s", x+1, 0, z))
                        model.colors.extend((light,) * len(self.quad.vertices)) # add vertex colors.
                        faces +=2
                    if face == "ns":
                        model.vertices.extend(self.vertices("e", x, 0, z-1))
                        model.colors.extend((dark,) * len(self.quad.vertices)) # add vertex colors.
                        model.vertices.extend(self.vertices("w", x, 0, z+1))
                        model.colors.extend((dark,) * len(self.quad.vertices)) # add vertex colors.
                        faces +=2


        for k,v in self.mesh_entities.items():
            v.model.uvs = (self.quad.uvs) * (lo.w * lo.h)
            v.model.generate() # call to create the mesh
            v.collider = MeshCollider(v, mesh=v.model, center=Vec3(0,0,0))      # add MeshCollider with custom shape and center.

        meshes = len(self.mesh_entities.items())
        print(f"made {meshes} wall meshes")
        print(f"made {faces} faces")


    def vertices(self, facing, x, y, z):
        vertices = [Vec3(x,y,z)+v for v in quadverts[facing]]
        return vertices



class Door(Entity):
    duration = 2
    hold_open = 5

    def __init__(self,texture_file, parent=scene, position=(0,0,0),
                 facing='ns'):
        txt = load_texture(texture_file, path="wolfdata/extracted/")
        x,y,z = position

        z_rot = 0
        self.door_x = x+0.5
        self.door_y = y+0.5
        self.door_z = z+0.5

        self.facing = facing
        assert facing in ['ns', 'ew']
        if facing == 'ns':
            z_rot = 90
        elif facing == 'ew':
            z_rot = 180
        else:
            raise Exception(f"direction {facing} is not valid for a door")

        super().__init__(
        )


        self.door1 = Entity(
            parent=self,
            position = (self.door_x, self.door_y, self.door_z),
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
            position = (self.door_x, self.door_y, self.door_z),
            model = Plane((1,1)),
            texture = txt,
            color = color.white,
            collision=True,
            collider='box',
            rotation_x=-90,
            rotation_z=z_rot - 180,
        )


    def open(self):
        dz = -1 if self.facing == 'ns' else 0
        dx = -1 if self.facing == 'ew' else 0
        target = (self.door_x + dx, self.door_y, self.door_z + dz)
        self.door1.animate_position(target, self.duration, curve=curve.linear)
        self.door2.animate_position(target, self.duration, curve=curve.linear)

        def close():
            self.close()
        invoke(close, delay=self.duration + self.hold_open)

    def close(self):
        print("Closing door")
        target = (self.door_x, self.door_y, self.door_z)
        self.door1.animate_position(target, self.duration, curve=curve.linear)
        self.door2.animate_position(target, self.duration, curve=curve.linear)

class LevelLoader():
    level = [[33,33,33,33,33,33,33],
             [33,107,107,107,107,107,33],
             [33,107,107,107,107,107,33],
             [33,107,107,107,107,107,33],
             [33,107,107, 33,107,107,33],
             [33,107,107,107,107,107,33],
             [33,107,107,107,107,107,33],
             [33,107,107,107,107,107,33],
             [33,33,33,33,33,33,33]]
    start = (3,5,3)
    object_list = []

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

            self.object_list = data['object_list']


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
        self.load_walls()
        self.load_objects()


    def load_walls(self):
        logger.info("rendering cubes from map")

        Entity(model=Grid(self.w,self.h),
               position=(int(self.w/2), 0, int(self.h/2)),
               scale=max(self.w, self.h),
               color=color.color(0,0,0),
               collision=True,
               collider='box',
               rotation_x=90)

        self.lvlmesh = LevelMesh(self.level,
                                 self.wall_lists,
                                 self.door_lists,
                                 self.floor_lists)


        for z, row in enumerate(self.level):
            h = len(row)
            assert h == self.h, f"row {z} is wrong length {self.h} {h}"
            for x, val in enumerate(row):
                # if val == -1:
                    # continue

                # if val in self.floor_lists:
                    # continue
                if val in self.door_lists:
                    face = "ew" if val %2 else "ns"
                    Door(self.door_file_name(val), position=(x,0,z),
                         facing=face)

                # if val in self.wall_lists:
                    # for face in lo.external_walls(z,x):
                        # Wall(self.wall_file_name(val, northsouth=face=='n' or face =='s'), position=(x,0,z),
                            # facing=face, )
                        # total_cubes += 1


        # print(f"made {total_cubes} walls")

    def load_objects(self):

        total_objects = 0

        self.sprites = []

        for coord, code in self.object_list:
            # see WL_GAME.C and WL_ACT1.C for details on ojbects
            if code in range(23, 74+1):
                txt = SolidSprite.texture_filename(code)
                y, x = coord
                self.sprites.append(SolidSprite(txt, position=(x+0.5,0,y+0.5)))
                total_objects += 1

        print(f"make {total_objects} objects")
