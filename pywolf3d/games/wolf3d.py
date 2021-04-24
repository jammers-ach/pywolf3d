from ursina import load_texture, Texture

## Wall defs

class WallDef():
    def __init__(self, code, description, filename=None):
        self.code = code
        self.description = description

        if filename:
            self.filename = filename
        else:
            self.filename = self.generate_filename(code)

    @property
    def texture(self):
        return load_texture(self.filename, path="wolfdata/extracted/")

    @property
    def editor_texture(self):
        return self.texture

    @classmethod
    def generate_filename(cls, val, northsouth=False):
        '''returns the filename for a wall code'''
        wall_code = (val-1)*2
        if northsouth:
            wall_code += 1
        fname = f'wall{wall_code:04d}'
        return fname

class FloorDef(WallDef):
    def __init__(self, code, description, filename=None):
        self.code = code
        self.description = description

        self._texture = 'white_cube'

    @property
    def texture(self):
        return self._texture

class DoorDef(WallDef):
    def __init__(self, code, description, filename=None):
        super().__init__(code, description, filename)
        self.face = "ew" if code %2 else "ns"
        self.description += f" ({self.face})"

    @classmethod
    def generate_filename(cls, val, northsouth=False):
        '''returns the filename for a door code'''
        return 'wall0098'

    @property
    def editor_texture(self):
        if self.face == "ns":
            from PIL import Image
            txt = Texture(f"wolfdata/extracted/{self.filename}.png")
            txt.apply()
            txt._cached_image = txt._cached_image.transpose(Image.ROTATE_90)
            txt.apply()
            return txt
        else:
            return self.texture

_WALL_DEFS = [
    WallDef(1, "Grey stone"),
    WallDef(2, "Grey stone2"),
    WallDef(3, "Grey stone with swastika"),
    WallDef(4, "Grey stone with hitler"),
    WallDef(5, "Blue brick cell door"),
    WallDef(6, "Grey alcove with swastika"),
    WallDef(7, "blue brick cell door2"),
    WallDef(8, "blue brick 1"),
    WallDef(9, "blue brick 2"),
    WallDef(10, "Wood with eagle"),
    WallDef(11, "Wood with hitler"),
    WallDef(12, "wood"),
    WallDef(13, "elevator door"),
    WallDef(14, "metal with warning sign"),
    WallDef(15, "bare metal"),
    WallDef(16, "sky"),
    WallDef(17, "red brick"),
    WallDef(18, "red brick with swastika"),
    WallDef(19, "purple brick"),
    WallDef(20, "purple brick w/ eagle banner"),
    WallDef(21, "elevator side"),
    WallDef(22, "wood w/ iron cross"),
    WallDef(23, "Grey stone with slime"),
    WallDef(24, "purple brick w/ blood"),
    WallDef(25, "grey stone with slime 2"),
    WallDef(26, "grey stone2"),
    WallDef(27, "grey stone with warning"),
    WallDef(28, "brown stone"),
    WallDef(29, "brown stone w/ blood"),
    WallDef(30, "brown stone w/ blood 2"),
    WallDef(31, "brown stone w/ blood 3"),
    WallDef(32, "brown stone w/ blood 4"),
    WallDef(33, "stain glass hitler"),
    WallDef(34, "blue wall with skull"),
    WallDef(35, "grey bricks"),
    WallDef(36, "blue brick w/ swastika"),
    WallDef(37, "grey bricks with sewer"),
    WallDef(38, "misc red bricks"),
    WallDef(39, "grey bricks 2"),
    WallDef(40, "blue wall"),
    WallDef(41, "blue bricks with warning sign"),
    WallDef(42, "brown tiles"),
    WallDef(43, "grey bricks with map"),
    WallDef(44, "light brown bricks"),
    WallDef(45, "light brown bricks 2"),
    WallDef(46, "brown tiles 2"),
    WallDef(47, "brown tiles w swastika"),
    WallDef(48, "brown tiles w space"),
    WallDef(49, "grey bricks w hitler"),
    WallDef(50, "door"),
]

_WALL_DEFS.extend([FloorDef(x, f"floor {x}") for x in range(106, 143+1)])
_WALL_DEFS.extend([DoorDef(90, f"door"),
                   DoorDef(91, f"door"),
                   DoorDef(92, f"door", filename="wall0104"),
                   DoorDef(93, f"door", filename="wall0104"),
                   DoorDef(94, f"door", filename="wall0104"),
                   DoorDef(95, f"door", filename="wall0104"),
                   DoorDef(96, f"door", filename="wall0104"),
                   DoorDef(97, f"door", filename="wall0104"),
                   DoorDef(98, f"door", filename="wall0104"),
                   DoorDef(99, f"door", filename="wall0104"),
                   DoorDef(100, f"Elevator door", filename="wall0102"),
                   DoorDef(101, f"Elevator door", filename="wall0102"),
                   ])

WALL_DEFS = {w.code: w for w in _WALL_DEFS}


## Objects

class ObjectDef():
    def __init__(self, code, description, filename=None):
        self.code = code
        self.description = description

        if filename:
            self.filename = filename
        else:
            self.filename = self.generate_filename(code)

    @property
    def texture(self):
        return load_texture(self.filename, path="wolfdata/extracted/")

    @property
    def editor_texture(self):
        return self.texture

    @classmethod
    def generate_filename(cls, val):
        '''returns the filename for a wall code'''
        sprite_code = val - 21
        fname = f'sprite{sprite_code:04d}'
        return fname


_OBJECT_DEFS = [
    ObjectDef(19, "player start (n)", filename="sprite0408"),
    ObjectDef(20, "player start (e)", filename="sprite0408"),
    ObjectDef(21, "player start (s)", filename="sprite0408"),
    ObjectDef(22, "player start (w)", filename="sprite0408"),
    ObjectDef(23, "water pool"),
    ObjectDef(24, "green barrel"),
    ObjectDef(25, "chairs"),
    ObjectDef(26, "green lamp"),
    ObjectDef(27, "chandelier"),
    ObjectDef(28, "hanging skeleton"),
    ObjectDef(29, "poridge"),
    ObjectDef(30, "stone column"),
    ObjectDef(31, "green plant"),
    ObjectDef(32, "skeleton"),
    ObjectDef(33, "sink"),
    ObjectDef(34, "fern"),
    ObjectDef(35, "empty vase"),
    ObjectDef(36, "table"),
    ObjectDef(37, "green light"),
    ObjectDef(38, "hanging pots"),
    ObjectDef(39, "suit of armour"),
    ObjectDef(40, "empty cage"),
    ObjectDef(41, "cage with skeleton"),
    ObjectDef(42, "bones"),
    ObjectDef(43, "gold key"),
    ObjectDef(44, "blue key"),
    ObjectDef(45, "bed"),
    ObjectDef(46, "basket"),
    ObjectDef(47, "chicken"),
    ObjectDef(48, "health pack"),
    ObjectDef(49, "clip"),
    ObjectDef(50, "machine gun"),
    ObjectDef(51, "chain gun"),
    ObjectDef(52, "treasure"),
    ObjectDef(53, "treasure"),
    ObjectDef(54, "treasure"),
    ObjectDef(55, "treasure"),
    ObjectDef(56, "extra life"),
    ObjectDef(57, "bones and blood"),
    ObjectDef(58, "wooden barrel"),
    ObjectDef(59, "well"),
    ObjectDef(60, "empty well"),
    ObjectDef(61, "blood"),
    ObjectDef(62, "flag"),
    ObjectDef(63, "ardwolf"),
    ObjectDef(64, "bones"),
    ObjectDef(65, "bones"),
    ObjectDef(66, "bones"),
    ObjectDef(67, "kitchen equipment"),
    ObjectDef(68, "boiler"),
    ObjectDef(69, "spears"),
    ObjectDef(70, "vines"),
    ObjectDef(71, "?"),
    ObjectDef(72, "?"),
    ObjectDef(73, "?"),
    ObjectDef(74, "?"),
]

OBJECT_DEFS = {w.code: w for w in _OBJECT_DEFS}
