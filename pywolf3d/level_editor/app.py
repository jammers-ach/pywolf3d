import argparse
import json

from ursina import load_texture, Ursina, Entity, color, camera, Quad, mouse, time, window, invoke, WindowPanel, \
    Text, InputField, Space, scene, Button, Draggable, Tooltip, Scrollable

from pywolf3d.games.wolf3d import WALL_DEFS, WallDef, OBJECT_DEFS

Z_GRID = 0
Z_WALL = 2


class LevelEditor():
    def __init__(self, fname, path_to_game):

        level_data = None
        self.fname = fname
        with open(fname) as f:
            level_data = json.load(f)

        w = len(level_data['level'])
        h = len(level_data['level'][0])

        self.cursor = Grid(self, parent=scene)

        self.grid = []
        y = 0
        for row in level_data['level']:
            tile_row = []
            x = 0
            for wall_code in row:
                tile_row.append(Tile(self, position=(x,y), cursor=self.cursor, wall_code=wall_code, parent=scene))

                x += 1
            self.grid.append(tile_row)
            y += 1

        camera.orthographic = True
        camera.fov = 5
        camera.position = (w/2,h/2)

        self.wall_holder = Inventory(cursor=self.cursor)
        self.wall_holder.add_script(Scrollable())

        for _,w in WALL_DEFS.items():
            self.wall_holder.append(w)

        self.object_holder = Inventory(cursor=self.cursor, visible=False)
        self.object_holder.add_script(Scrollable())

        for _,w in OBJECT_DEFS.items():
            self.object_holder.append(w)

        self.mode = "tile"


    def save(self):
        json_data = {"object_list": [],
                    "name": "test level",
                    "size": []}

        level = []
        for r in self.grid:
            row = []
            for col in r:
                row.append(col.wall_code)

            level.append(row)
        json_data["level"] = level

        with open(self.fname, 'w') as f:
            json.dump(json_data, f)
            print(f"written to {self.fname}")


class Inventory(Entity):
    def __init__(self, rows=2, cols=5, full_size=60, scrollable=True, **kwargs):
        super().__init__(
            parent = camera.ui,
            model = Quad(radius=.015),
            texture = 'white_cube',
            texture_scale = (rows,cols),
            scale = (.1 * rows, .1 * cols),
            origin = (-.5, .5),
            position = (-0.9,.5),
            color = color.color(0,0,.1,.9),
            )

        self.rows = rows
        self.cols = cols
        self.full_cols = full_size - cols

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.used_spots = []


    def find_free_spot(self):
        for y in range(self.cols+self.full_cols):
            for x in range(self.rows):
                if not (x,y) in self.used_spots:
                    self.used_spots.append((x,y))
                    return x, y
        raise Exception("No free spots")


    def append(self, wall_def, x=0, y=0):
        x, y = self.find_free_spot()
        print(x,y)
        def clicked():
            print(f"clicked {wall_def.description}")
            self.cursor.current_tile = wall_def.code

        icon = Button(
            parent = self,
            model = 'quad',
            texture = wall_def.editor_texture,
            color = color.white,
            scale_x = 1/self.texture_scale[0],
            scale_y = 1/self.texture_scale[1],
            origin = (-.5,.5),
            x = x * 1/self.texture_scale[0],
            y = -y * 1/self.texture_scale[1],
            z = -.5,
            on_click = clicked,
            )
        icon.tooltip = Tooltip(wall_def.description)
        icon.tooltip.background.color = color.color(0,0,0,.8)


    def item_clicked(self, item):
        self.selected.deselect()
        self.selected = item


class Grid(Entity):
    fov_step = 20
    move_step = 10
    hold_step = 20

    def __init__(self, editor, **kwargs):
        super().__init__()
        self.model=Quad(mode='line')
        self.color = color.red
        self.z = Z_GRID
        self.current_tile = 5
        self.editor = editor

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.position = mouse.world_point
        self.x = round(self.x, 0)
        self.y = round(self.y, 0)

    def input(self, key):
        # print(key)
        if key == "up arrow":
            camera.y += self.move_step * time.dt
        elif key == "down arrow":
            camera.y -= self.move_step * time.dt
        elif key == "left arrow":
            camera.x -= self.move_step * time.dt
        elif key == "right arrow":
            camera.x += self.move_step * time.dt

        elif key == "up arrow hold":
            camera.y += self.hold_step * time.dt
        elif key == "down arrow hold":
            camera.y -= self.hold_step * time.dt
        elif key == "left arrow hold":
            camera.x -= self.hold_step * time.dt
        elif key == "right arrow hold":
            camera.x += self.hold_step * time.dt

        elif key == "=" or key == "= hold":
            camera.fov -= self.fov_step * time.dt
        elif key == "-" or key == "- hold":
            camera.fov += self.fov_step * time.dt

        elif key == "s":
            self.editor.save()

        elif key == "o":
            self.editor.objects()


class Tile(Entity):
    def __init__(self, editor, **kwargs):
        super().__init__()
        self.model='quad'
        self.z = Z_WALL
        self.collider='box'
        self.editor = editor

        self.set_texture(kwargs['wall_code'])

        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_texture(self, wall_code):
        txt = WALL_DEFS[wall_code].texture
        self.wall_code = wall_code
        self.texture = txt


    def update(self):
        if self.hovered:
            self.cursor.x = self.position.x
            self.cursor.y = self.position.y
            self.cursor.z = Z_GRID


    def input(self, key):
        if key == 'left mouse down' and self.hovered and self.editor.mode == "tile":
            self.set_texture(self.cursor.current_tile)
            print("down", self.x, self.y, ' - ', self.wall_code)





def start_editor(fname, path_to_game):
    app = Ursina()
    editor = LevelEditor(fname, path_to_game)
    app.run()

def run():
    parser = argparse.ArgumentParser(description='Mapmaker for pywolf3d')
    parser.add_argument('level', help='path to level to load')
    parser.add_argument('--path', help='path to wolf3d datafiles (default ./wolfdata)',
                        default="./wolfdata/")
    args = parser.parse_args()

    start_editor(args.level, args.path)

if __name__ == '__main__':
    run()
