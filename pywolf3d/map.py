from pywolf3d.cube import Cube, Floor, Celing,Door
from pywolf3d.player import Player
from pywolf3d.things import ImmovableThing, PickupThing
from pywolf3d.game_options import rendering_opts

class GameMap(object):
    '''A single game level'''

    def __init__(self, wall_layout, object_list):
        '''
        :param wall_layout: array of codes for the level
        :param object_list: list of things in the level
        '''
        self.wall_layout = wall_layout

        self.w = len(wall_layout)
        self.h = len(wall_layout[1])

        self.cubes = {}

        self._generate_cubes()
        self.players = []

        #For now just 1 floor
        self.floor = Floor(self.w, self.h, 1)
        self.ceiling = Celing(self.w,self.h,2)

        self.object_list = object_list
        self._make_object_lists()

    def _make_object_lists(self):
        self.immovable_objs = {}
        self.pickups = {}

        for obj in self.object_list:
            if(isinstance(obj,ImmovableThing)):
                self.immovable_objs[(obj.x, obj.y)] = [obj]
            if(isinstance(obj,PickupThing)):
                self.pickups[(obj.x, obj.y)] = [obj]


    def add_player(self, start_x, start_y):
        '''add the player object at start_x, start_y'''
        p = Player(self,start_x,start_y)
        self.players.append(p)
        return p

    def can_go(self,x,y):
        '''Can an object go into square x,y?
            checks for walls/immovable objects
            '''
        if(x > self.w or x < 0 or y > self.h or y < 0):
            return False
        try:
            if(self.wall_layout[int(x)][int(y)] != 0):
                return False
        except IndexError:
            return False

        #Now look through the objects
        pos = (int(x),int(y))
        if(pos in self.immovable_objs and self.immovable_objs[pos] != []):
            return False

        return True

    def handle_pickups(self,player):
        '''picks up any objects the player might be standing on'''
        pos = (int(player.x),int(player.y))
        if(pos in self.pickups and self.pickups[pos] != []):
            for obj in self.pickups[pos]:
               if(obj.picked_up(player)):
                    self.pickups[pos].remove(obj)
                    self.object_list.remove(obj)
                    del obj

    def _generate_cubes(self):
        # generate all the cube objects for each
        # cell of the game
        for y in range(self.h):
            for x in range(self.w):
                wall_type = self.wall_layout[x][y]
                if(wall_type != 0 ):
                    position = (float(x), 0.0, float(y))
                    if(wall_type >= rendering_opts['door_start_code']):
                        cube = Door( position, wall_type - rendering_opts['door_start_code'])
                        self.cubes[(x,y)] = cube
                    else:
                        cube = Cube( position, wall_type )
                        self.cubes[(x,y)] = cube
