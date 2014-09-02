'''
Things that appear in the game
@author jammers
'''
from sprite import MObject


class ImmovableThing(MObject):
    '''a sprite you can't pass through, e.g. a chair'''
    pass
        

class PassableThing(MObject):
    '''A sprite you can pass through, e.g. a ceiling light'''
    pass


class PickupThing(MObject):
    '''A sprite that you pass through and pick up, e.g. a gun or powerup'''

    def picked_up(self,player):
        '''Returns true if the item was picked up,
        false if not'''
        print 'picked up'
        return True
