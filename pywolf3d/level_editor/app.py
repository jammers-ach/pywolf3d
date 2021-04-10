import argparse
import json

from ursina import load_texture, Ursina, Entity, color, camera, Quad, mouse, time, window, invoke

Z_GRID = 0
Z_WALL = 2


def wall_file_name(val, northsouth=False):
    '''returns the filename for a wall code'''
    wall_code = (val-1)*2
    if northsouth:
        wall_code += 1
    fname = f'wall{wall_code:04d}'
    return fname

class Grid(Entity):
    fov_step = 20
    move_step = 10
    hold_step = 20

    def __init__(self, **kwargs):
        super().__init__()
        self.model=Quad(mode='line')
        self.color = color.red
        self.z = Z_GRID

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
        texture_file = wall_file_name(kwargs['wall_code'])
        txt = load_texture(texture_file, path="wolfdata/extracted/")
        self.texture = txt

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        if self.hovered:
            self.cursor.x = self.position.x
            self.cursor.y = self.position.y
            self.cursor.z = Z_GRID


    def input(self, key):
        # print(key)
        if key == 'left mouse down' and self.hovered:
            print("down", self.x, self.y)

def start_editor(level_data, path_to_game):
    w = len(level_data['level'])
    h = len(level_data['level'][0])
    app = Ursina()
    plane = Entity(model='quad', position=(w/2 - 0.5,h/2 - 0.5), color=color.azure, z=10, collider='box', scale=max(w,h)+2) # create an invisible plane for the mouse to collide with
    cursor = Grid()

    grid = []
    y = 0
    for row in level_data['level']:
        tile_row = []
        x = 0
        for wall_code in row:
            tile_row.append(Tile(model='quad', position=(x,y), cursor=cursor, wall_code=wall_code))
            x += 1
        grid.append(tile_row)
        y += 1

    camera.orthographic = True
    camera.fov = 5
    camera.position = (w/2,h/2)
    window.borderless = False

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
