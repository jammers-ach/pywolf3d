from OpenGL.GL import *
from OpenGL.GLU import *

from pywolf3d.math.util import linear_distance


class GLGameMapRender(object):

    def __init__(self, map):
        self.gmap = map
        self.display_list = None
        self.update_cube_walls()

    def render(self):
        if self.display_list is None:
            # Create a display list
            self.display_list = glGenLists(1)
            glNewList(self.display_list, GL_COMPILE)

            # Draw the cubes
            for cube in list(self.gmap.cubes.values()):
                cube.render()

            #draw the floor, draw the ceiling
            self.gmap.floor.render()
            self.gmap.ceiling.render()

            # End the display list
            glEndList()

        else:
            # Render the display list
            glCallList(self.display_list)

    def _sort_objects(self,player):
        '''Sorts all the objects by distance to the player so they are rendered int he right order'''
        posx = player.x
        posy = player.y

        self.sorted_objects = []

        for obj in self.gmap.object_list:
            distance = linear_distance((posx,posy),(obj.x,obj.y))
            self.sorted_objects.append((distance,obj))

        self.sorted_objects = sorted(self.sorted_objects,
                                     reverse=True,
                                     key=lambda x:x[0])

    def objects_render(self,player):
        '''Renders the object, which need a player so they can face the camera'''
        self._sort_objects(player)
        for dist,obj in self.sorted_objects:
            obj.render(player.camera_matrix.get_row_vec3(0))


    def update_cube_walls(self):
        '''Finds out which walls of each cube need to be rendered'''
        for y in range(self.gmap.h):
            for x in range(self.gmap.w):
                if((x,y) in self.gmap.cubes):
                    check = [(x,y+1),(x,y-1),(x+1,y),(x-1,y)]
                    rendered_normals = []
                    for i in range(len(check)):
                        if(check[i] not in self.gmap.cubes or self.gmap.cubes[check[i]] == 0 ):
                            rendered_normals.append(i)
                    rendered_normals.append(4)
                    self.gmap.cubes[(x,y)].rendered_normals = rendered_normals



