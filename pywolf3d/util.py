import math

# The direction of wolf3d objects in the order their sprites appwear
wolf3d_sprite_directions = [
    "s",     # towards you
    "sw",
    "w",     # facing left
    "nw",
    "n",     # facing away from you
    "ne",
    "e",     # facing right
    "se"
]

# the order in which 0-360 degrees maps to quadrants
real_quadrants = [
    "e",
    "ne",
    "n",
    "nw",
    "w",
    "sw",
    "s",
    "se"
]

quadrant_mapping = {real_quadrants.index(x): wolf3d_sprite_directions.index(x)
                    for x in real_quadrants}

def direction_to_target(a, b):
    '''how many degrees from north is a to b'''
    x1, y1, z1 = a
    x2, y2, z2 = b

    theta = math.atan2(x2-x1, z2-z1)
    angle = (90 - math.degrees(theta)) % 360
    return angle

def angle_to_dir(angle, shift=0, directions = 8):
    angle = (angle + shift)/360
    quadrant = int(angle*directions) % directions
    return int(quadrant)

if __name__ == '__main__':
    for i in range(0, 360, 10):
        print(i, angle_to_dir(i), quadrant_mapping[angle_to_dir(i)])
