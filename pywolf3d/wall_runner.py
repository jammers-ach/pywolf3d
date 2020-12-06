'''tools to optimise a level'''

class LevelOptimiser():

    def __init__(self, level, wall_lists, floor_lists, door_lists):
        self.level = level
        self.wall_lists = wall_lists
        self.floor_lists = floor_lists
        self.door_lists = door_lists

    def optimise(self):
        self._cull_walls()

        return self.level

    @property
    def w(self):
        return len(self.level)

    @property
    def h(self):
        return len(self.level[0])

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
if __name__ == '__main__':
    pass
