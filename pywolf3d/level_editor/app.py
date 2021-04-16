import argparse
import json

from ursina import load_texture, Ursina, Entity, color, camera, Quad, mouse, time, window, invoke, WindowPanel, \
    Text, InputField, Space, scene, Button, Draggable, Tooltip

from pywolf3d.games.wolf3d import WALL_DEFS, WallDef

Z_GRID = 0
Z_WALL = 2

class Inventory(Entity):
    def __init__(self, rows=5, cols=10, **kwargs):
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

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.used_spots = []


    def find_free_spot(self):
        for y in range(self.cols):
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
            texture = load_texture(wall_def.filename, path="wolfdata/extracted/"),
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

    def __init__(self, **kwargs):
        super().__init__()
        self.model=Quad(mode='line')
        self.color = color.red
        self.z = Z_GRID
        self.current_tile = 5
        # TODO enum me
        self.mode = "tile"

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


class Tile(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model='quad'
        self.z = Z_WALL
        self.collider='box'

        self.set_texture(kwargs['wall_code'])

        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_texture(self, wall_code):
        txt = WALL_DEFS[wall_code-1].texture
        self.wall_code = wall_code
        self.texture = txt


    def update(self):
        if self.hovered:
            self.cursor.x = self.position.x
            self.cursor.y = self.position.y
            self.cursor.z = Z_GRID


    def input(self, key):
        # print(key)
        if key == 'left mouse down' and self.hovered and self.cursor.mode == "tile":
            self.set_texture(self.cursor.current_tile)
            print("down", self.x, self.y, ' - ', self.wall_code)

def start_editor(level_data, path_to_game):
    w = len(level_data['level'])
    h = len(level_data['level'][0])
    app = Ursina()
    cursor = Grid(parent=scene)

    grid = []
    y = 0
    for row in level_data['level']:
        tile_row = []
        x = 0
        for wall_code in row:
            tile_row.append(Tile(position=(x,y), cursor=cursor, wall_code=wall_code, parent=scene))

            x += 1
        grid.append(tile_row)
        y += 1

    camera.orthographic = True
    camera.fov = 5
    camera.position = (w/2,h/2)

    wall_holder = Inventory(cursor=cursor)

    for w in WALL_DEFS:
        wall_holder.append(w)


    app.run()



def run():
    parser = argparse.ArgumentParser(description='Mapmaker for pywolf3d')
    parser.add_argument('level', help='path to level to load')
    parser.add_argument('--path', help='path to wolf3d datafiles (default ./wolfdata)',
                        default="./wolfdata/")
    args = parser.parse_args()

    with open(args.level) as f:
        print(f"Loading {args.level}")
        data = json.load(f)

    start_editor(data, args.path)

if __name__ == '__main__':
    run()
