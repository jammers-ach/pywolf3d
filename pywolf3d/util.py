import math

def direction_to_target(a, b):
    '''how many degrees from north is a to b'''
    x1, y1, z1 = a
    x2, y2, z2 = b

    theta = math.atan2(z2-z1, x2-x1)
    angle = (90 - math.degrees(theta)) % 360
    return angle

def angle_to_dir(angle, shift=1, directions = 8):
    angle = (360 - angle)/360
    mod = (int(angle*directions) + shift) % directions
    return mod


if __name__ == '__main__':
    pos1 = [3.5,0,3.5]
    for x in [i/100 for i in range(-100, 101 )]:
        y = math.sqrt(1 - (x**2))
        pos2 = [pos1[0]+x, 0, pos1[3]+y]
        angle = direction_to_target(pos1, pos2)
        print(angle, angle_to_dir(angle), pos2)

