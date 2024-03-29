import argparse
import os
import pathlib

from ursina import Ursina

from pywolf3d.player import Wolf3dPlayer
from pywolf3d.level import LevelLoader

def extract(gamedir, target):
    from vswap.games import detect_game
    gamecls = detect_game(gamedir)
    game = gamecls(gamedir)
    game.load_all()
    game.output(target)

def get_game(path, level):
    if not os.path.isdir(path):
        print("{} is not a directory".format(path))
        return

    # look inside the path directory for some extracted files
    path = pathlib.Path(path)
    target = path / "extracted"

    if not level:
        level = path / "extracted" / "level0000.json"
    else:
        level = pathlib.Path(level)
        if not os.path.exists(level):
            raise Exception(f"{level} doesn't exist")


    if not os.path.isdir(target) or not os.path.exists(level):
        print("no extracted data, looking for original")
        extract(path, target)
        return level
    else:
        return level

def start_game(level_path):
    app = Ursina()
    level = LevelLoader(level_path)
    level.load()
    player = Wolf3dPlayer(position=level.player_start, level=level)
    app.run()


def run():
    parser = argparse.ArgumentParser(description='Wolf3d engine in ursina')
    parser.add_argument('--path', help='path to wolf3d datafiles (default ./wolfdata)', default="./wolfdata/")
    parser.add_argument('--level', help='path to level file (default first level)', default=None)
    args = parser.parse_args()

    first_level = get_game(pathlib.Path(args.path), args.level)
    if first_level:
        start_game(first_level)

if __name__ == '__main__':
    run()
