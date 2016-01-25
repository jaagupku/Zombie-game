#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
from time import time
import core


class Monster(object):
    @staticmethod
    def load_resources():
        Zombie.img.clear()
        Zombie.img_gore_particles.clear()
        Zombie.img_gore_particles = core.load_spritesheet_alpha(core.Var.path_zombiegore, 64, 3, 2)
        Zombie.img = core.load_spritesheet_alpha(core.Var.path_zombie, 128, 2, 2)
        Devil.img = core.load_image_alpha(core.Var.path_devil)
        Devil.img_gore_particles = core.load_spritesheet_alpha(core.Var.path_zombiegore, 64, 3, 2)
        Devil.img_fireball = core.load_image_alpha(core.Var.path_fireball)

    def __init__(self, x, y, name, maxhealth, speed, damage, image, attacktimer, mass, attack_range):
        self.x = x
        self.y = y
        self.name = name
        self.maxhealth = maxhealth
        self.speed = speed
        self.damage = damage
        self.image = image
        self.attacktimer = attacktimer
        self.mass = mass
        self.uuid = core.Var.uuid_gen
        core.Var.uuid_gen += 1
        self.health = self.maxhealth
        self.frame = self.image.get_rect()
        self.size = (self.image.get_width() / 2) ** 2
        self.vect = core.p.math.Vector2(core.Gameobj.hero.x - self.x, core.Gameobj.hero.y - self.y)
        self.vect_long = core.p.math.Vector2(core.Gameobj.hero.x - self.x, core.Gameobj.hero.y - self.y)
        self.time_attacked = 0
        self.attack_bool = False
        self.kickback = 0
        self.collision_with_other = [False, 1, 1]
        self.kick_direction = [0, 0]
        self.attack_range = (core.dpp(attack_range) + core.sqrt(self.size) + core.sqrt(core.Gameobj.hero.size)) ** 2

    def render(self, s):
        animation_max = 30
        modifier = 0
        if not self.attack_bool:
            something = time() - self.time_attacked
            attack_peak_time = self.attacktimer / 4
            if something <= attack_peak_time:
                modifier = something / attack_peak_time * animation_max
            elif something <= attack_peak_time * 2:
                modifier = animation_max - something / (attack_peak_time * 2) * animation_max
        self.vect.x = core.Gameobj.hero.x - self.x
        self.vect.y = core.Gameobj.hero.y - self.y
        angle = self.vect.angle_to(core.Var.unit_vector) + modifier
        rotated = core.p.transform.rotate(self.image, angle)
        center = core.p.math.Vector2(core.dpp(12), 0)
        center.rotate_ip(-angle)
        self.frame = rotated.get_rect()
        self.frame.center = round(self.x + center.x - core.Var.offset_x), round(self.y + center.y - core.Var.offset_y)
        s.blit(rotated, self.frame)

    def kick_back(self, kick, pos):
        self.kickback += core.dpp(kick) / self.mass * 100
        self.kick_direction[0] = self.x - pos[0]
        self.kick_direction[1] = self.y - pos[1]

    def attack(self):
        if not self.attack_bool and time() - self.time_attacked > self.attacktimer:
            self.attack_bool = True

    def move(self, delta):
        kick_vect = core.p.math.Vector2(0, 0)
        if self.kickback != 0:
            self.kickback *= 1 - delta / 100
            kick_vect.x = self.kick_direction[0]
            kick_vect.y = self.kick_direction[1]
            kick_vect.scale_to_length(self.kickback * delta / 1000)
            if self.kickback < 0.01:
                self.kickback = 0
                self.kick_direction = [0, 0]
        speed = self.speed * delta
        speed_x, speed_y = 0, 0
        self.vect.x = core.Gameobj.hero.x - self.x
        self.vect.y = core.Gameobj.hero.y - self.y
        len_squared = self.vect.length_squared()
        if len_squared >= speed ** 2:
            self.vect.scale_to_length(speed)
            if not self.collision_with_other[0]:
                speed_x, speed_y = self.vect.x + kick_vect.x, self.vect.y + kick_vect.y
            else:
                speed_x = (speed + kick_vect.x) * self.collision_with_other[1] / 2
                speed_y = (speed + kick_vect.y) * self.collision_with_other[2] / 2
        self.x += speed_x
        self.y += speed_y

    def destroy(self):
        raise NotImplementedError

    def start_attack(self, delta):
        raise NotImplementedError

    def get_damaged(self, dmg):
        raise NotImplementedError


class Zombie(Monster):
    img_gore_particles = []
    img = []

    def __init__(self, x, y):
        rng = randint(0, len(Zombie.img) - 1)
        Monster.__init__(self, x, y, "zombie_common", 100, core.dpp(55 / 1000), 8, Zombie.img[rng], 1, 10, 4.5)

    def get_damaged(self, dmg):
        if core.Var.channel_monster1.get_sound() is None:
            core.Var.channel_monster1.play(core.Var.sound_hero_hit[randint(0, 2)])
        elif core.Var.channel_monster2.get_sound() is None:
            core.Var.channel_monster2.play(core.Var.sound_hero_hit[randint(0, 2)])
        self.health -= dmg
        rng = core.dppr(10.3)
        x = self.x + randint(-rng, rng)
        y = self.y + randint(-rng, rng)
        core.Gameobj.particle_effect(core.Gameobj.img_blood, 3, True, core.dppr(35), x, y)

    def update(self, delta):
        if self.health < 1:
            self.destroy()
        self.vect_long.x = core.Gameobj.hero.x - self.x
        self.vect_long.y = core.Gameobj.hero.y - self.y
        len_squared_long = self.vect_long.length_squared()
        if len_squared_long < self.attack_range:
            self.start_attack(delta)
        else:
            self.attack_bool = False
        self.move(delta)
        self.attack()

    def start_attack(self, delta):
        if self.attack_bool:
            self.time_attacked = time()
            core.Gameobj.hero.get_damage(self.damage)
            self.attack_bool = False

    def destroy(self):
        if core.Var.channel_monster1.get_sound() is None:
            core.Var.channel_monster1.play(core.Var.sound_zombie_die[randint(0, 4)])
        else:
            core.Var.channel_monster2.play(core.Var.sound_zombie_die[randint(0, 4)])
        core.Var.monsters_killed += 1
        core.Gameobj.particle_effect(Zombie.img_gore_particles, 2 - self.health // 15, False, core.dppr(15), self.x,
                                     self.y)
        core.Var.score += self.maxhealth
        rng = randint(0, 6)
        if rng == 1:
            idgun = randint(2, 5)

            def action():
                if not core.Gameobj.hero.guns[idgun]:
                    core.Gameobj.hero.guns[idgun] = True
                clipsize = core.Gameobj.guns[idgun].clip_size
                core.Gameobj.hero.ammo[core.Gameobj.guns[idgun].bullet_type] += randint(clipsize // 2, clipsize * 2)
                core.Var.channel_misc2.play(core.Var.sound_pick)

            core.Gameobj.items.append(core.Item(self.x, self.y, core.Item.img_weaponground[idgun], action))
        core.Gameobj.monsters.remove(self)


class Devil(Monster):
    img_gore_particles = []
    img = None
    img_fireball = None

    def __init__(self, x, y):
        Monster.__init__(self, x, y, "devil", 265, core.dpp(34 / 1000), 24, Devil.img, 2.15, 30, 240)

    def get_damaged(self, dmg):
        if core.Var.channel_monster1.get_sound() is None:
            core.Var.channel_monster1.play(core.Var.sound_hero_hit[randint(0, 2)])
        elif core.Var.channel_monster2.get_sound() is None:
            core.Var.channel_monster2.play(core.Var.sound_hero_hit[randint(0, 2)])
        self.health -= dmg
        rng = core.dppr(10.3)
        x = self.x + randint(-rng, rng)
        y = self.y + randint(-rng, rng)
        core.Gameobj.particle_effect(core.Gameobj.img_blood, 3, True, core.dppr(35), x, y)

    def update(self, delta):
        if self.health < 1:
            self.destroy()
        self.vect_long.x = core.Gameobj.hero.x - self.x
        self.vect_long.y = core.Gameobj.hero.y - self.y
        len_squared_long = self.vect_long.length_squared()
        if len_squared_long < self.attack_range:
            self.start_attack(delta)
        else:
            self.attack_bool = False
        self.move(delta)
        self.attack()

    def start_attack(self, delta):
        if self.attack_bool:
            self.time_attacked = time()
            self.attack_bool = False
            if core.Var.channel_monster1.get_sound() is None:
                core.Var.channel_monster1.play(core.Var.sound_fireball)
            else:
                core.Var.channel_monster2.play(core.Var.sound_fireball)

            def command(*args):
                distance = (args[1] - core.Gameobj.hero.x) ** 2 + (args[2] - core.Gameobj.hero.y) ** 2
                if distance < core.dppr2(24) ** 2 + core.Gameobj.hero.size * 1.3:
                    core.Gameobj.hero.get_damage(self.damage)
                    core.Gameobj.particles_over.remove(args[0])
                elif args[3] < 1:
                    core.Gameobj.particles_over.remove(args[0])

            aim_adjustment = randint(350, 480)
            core.Gameobj.particles_over.append(
                    core.Particle((self.x, self.y,
                                   core.Gameobj.hero.x + (core.Gameobj.hero.vect_move.x / delta) * aim_adjustment,
                                   core.Gameobj.hero.y + (core.Gameobj.hero.vect_move.y / delta) * aim_adjustment),
                                  (400 / 1000, 333 / 1000), (0, 0),
                                  8000, False, self.img_fireball, True, command))

    def destroy(self):
        if core.Var.channel_monster1.get_sound() is None:
            core.Var.channel_monster1.play(core.Var.sound_zombie_die[randint(0, 4)])
        else:
            core.Var.channel_monster2.play(core.Var.sound_zombie_die[randint(0, 4)])
        core.Var.monsters_killed += 1
        core.Gameobj.particle_effect(Devil.img_gore_particles, 5 - self.health // 15, False, core.dppr(25), self.x,
                                     self.y)
        core.Var.score += self.maxhealth
        rng = randint(0, 2)
        if rng == 1:
            idgun = randint(2, 5)

            def action():
                if not core.Gameobj.hero.guns[idgun]:
                    core.Gameobj.hero.guns[idgun] = True
                clipsize = core.Gameobj.guns[idgun].clip_size
                core.Gameobj.hero.ammo[core.Gameobj.guns[idgun].bullet_type] += randint(clipsize, clipsize * 3)
                core.Var.channel_misc2.play(core.Var.sound_pick)

            core.Gameobj.items.append(core.Item(self.x, self.y, core.Item.img_weaponground[idgun], action))
        core.Gameobj.monsters.remove(self)
