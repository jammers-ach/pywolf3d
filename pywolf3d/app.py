from ursina import Ursina

from pywolf3d.player import Wolf3dPlayer
from pywolf3d.level import LevelLoader

def run():
    app = Ursina()
    level = LevelLoader()
    level.load()
    player = Wolf3dPlayer()
    app.run()

if __name__ == '__main__':
    run()
