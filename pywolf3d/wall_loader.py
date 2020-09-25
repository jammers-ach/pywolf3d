# Jammers 27/08/14
# Loads the wall config file into the game
from walls import WallType,FlatType,DoorType
import configparser

wall_config = 'defs/wall_def.cfg'

def parseWall(config,section_name):
    '''Given a config and a section_name it loads the texture and returns a wall class'''
    try:
        code = int(section_name.replace('Wall',''))
    except ValueError:
        print("ERROR: %s isn't a valid wall code" % (section_name))
        return


    #print code, config.items(section_name)
    d = config.get(section_name,'description')
    t1 = config.get(section_name,'texture1')
    t2 = config.get(section_name,'texture2')
    w = WallType(code,d,t1,t2)
    return w

def parseFlat(config,section_name):
    '''Loads a flat (wall/ceiling)'''
    try:
        code = int(section_name.replace('Flat',''))
    except ValueError:
        print("ERROR: %s isn't a valid wall code" % (section_name))
        return

    #print code, config.items(section_name)
    d = config.get(section_name,'description')
    t = config.get(section_name,'texture')
    w = FlatType(code,d,t)
    return w

def parseDoor(config,section_name):
    '''Loads a door'''
    try:
        code = int(section_name.replace('Door',''))
    except ValueError:
        print("ERROR: %s isn't a valid wall code" % (section_name))
        return

    #print code, config.items(section_name)
    d = config.get(section_name,'description')
    t = config.get(section_name,'texture')
    t2 = config.get(section_name,'sides')
    ns = config.getboolean(section_name,'northsouth')
    w = DoorType(code,d,t,t2,ns)
    return w



def load_walls():
    config = configparser.ConfigParser()
    config.read(wall_config)
    print(config)
    walls = {}
    flats = {}
    doors = {}

    #Go through each section, putting things into either walls or doors etc
    for i in config.sections():
        if(i.startswith('Wall')):
            w = parseWall(config,i)
            if(w!= None):
                if(w.code not in walls):
                    walls[w.code] = w
                    w.load_textures()
                else:
                    print('ERROR: %s already in config' % i)
        elif(i.startswith('Flat')):
            f = parseFlat(config,i)
            if(f != None):
                if(f.code not in flats):
                    flats[f.code] = f
                    f.load_textures()
                else:
                    print('ERROR: %s already in config' %i)
        elif(i.startswith('Door')):
            f = parseDoor(config,i)
            if(f != None):
                if(f.code not in doors):
                    doors[f.code] = f
                    f.load_textures()
                else:
                    print('ERROR: %s already in config' %i)

        else:
            print('ERROR: unown wall def %s' %i)

    return walls,flats,doors
