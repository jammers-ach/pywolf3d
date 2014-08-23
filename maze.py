'''
Simple maze generation algorithm by jammers
'''
import random

get_sides = lambda a: [(a[0],a[1]+1),(a[0],a[1]-1),(a[0]+1,a[1]),(a[0]-1,a[1])]
filter_sides = lambda a,w,h: [(x,y) for x,y in a if x>0 and y>0 and x<(w-1) and y<(w-1)]

def can_demolish(maze,a1,a2,w,h):
    '''Tells us if we can demolish a wall
    e.g.
    ###
    -#-
    ###
    
    ###
    ?O-   - returns false
    ###
    
    O##
    ?#-   - returns true
    ###
    '''
    
    sides = filter_sides(get_sides(a2),w,h)
    sides.remove(a1)
    print 'testing',a2,'from',a1,'on sides',sides
    for x,y in sides:
        if(maze[x][y] == 0):
            print 'no wall at',(x,y)
            return False
        
    return True
    
    
def generate_maze(w,h,start=(1,1)):
    '''Generates a maze'''
    maze = [[1 for i in range(w)] for j in range(h)]

    paths = [start]
    walls = filter_sides(get_sides(start),w,h)
    maze[start[0]][start[1]] = 0

    while(walls != []):
        index = random.randint(0,len(walls)-1)
        a = walls[index]

        #Find all the walls
        sides = [s for s in filter_sides(get_sides(a),w,h) ]
        
        #look at the sides, if there are more than one that's not a path we can't demolish
        c = 0
        for i in sides:
            if i in paths:
                c += 1
                
        if(c <=1):
            #Demolish wall and put the path in the seen path
            maze[a[0]][a[1]] = 0
            paths.append(a)
            walls.extend(sides)

        walls.remove(a)
    #Print the maze
    for r in maze:
        print r
                  
        
    return maze
    
if __name__=='__main__':
    generate_maze(10, 10)