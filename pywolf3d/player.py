from ursina import *

class Wolf3dPlayer(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.speed = 5
        self.position = (1,5,1)
        self.height = 0.5

        self.camera_pivot = Entity(parent=self, y=self.height)
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)


        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)
        self.target_smoothing = 100
        self.smoothing = self.target_smoothing

        self.gravity = 1
        self.grounded = True
        self.jump_height = .5
        self.jump_duration = .5
        self.jumping = False
        self.air_time = 0


        for key, value in kwargs.items():
            setattr(self, key ,value)


    def update(self):
        rotate_sprites = False

        if application.development_mode:
            self.y -= held_keys['e']
            self.y += held_keys['q']

        if held_keys['a']:
            self.rotation_y -= 1
            rotate_sprites = True

        if held_keys['d']:
            self.rotation_y += 1
            rotate_sprites = True

        if held_keys['w'] or held_keys['s']:
            rotate_sprites = True


        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            ).normalized()

        origin = self.world_position + (self.up*.5)
        hit_info = raycast(origin , self.direction, ignore=[self,], distance=.5, debug=False)
        if not hit_info.hit:
            self.position += self.direction * self.speed * time.dt

        if rotate_sprites and self.level:
            for s in self.level.sprites:
                s.face(self)

        if self.gravity:
            # # gravity
            offset = (0,2,0)
            ray = boxcast(self.world_position + offset, self.down, ignore=(self,), thickness=.9)

            if ray.distance <= 2:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance-.05)
            self.air_time += time.dt * .25 * self.gravity


    def input(self, key):
        if key == 'space' and mouse.hovered_entity \
                and hasattr(mouse.hovered_entity.parent, 'open'):
            mouse.hovered_entity.parent.open()


    def jump(self):
        if not self.grounded:
            return

        self.grounded = False
        self.animate_y(self.y+self.jump_height, self.jump_duration, resolution=120, curve=curve.out_expo)
        invoke(self.start_fall, delay=self.jump_duration)


    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True
