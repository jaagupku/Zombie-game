#!/usr/bin/env python
# -*- coding: utf-8 -*-
import core


class Hero(object):
    img_hero_body = None
    img_hero_hands = None
    img_weapons = None
    img_flash = None
    img_saber = None
    img_shell = None
    # TODO MUZZLEFLASH

    def __init__(self, x, y, maxhp, speed):
        self.x = x
        self.y = y
        self.health = maxhp
        self.maxhealth = maxhp
        self.speed = speed / 100
        self.frame = Hero.img_hero_body.get_rect()
        self.size = (Hero.img_hero_body.get_width() / 2.5)**2
        self.sizenotsq = Hero.img_hero_body.get_width() / 2.5
        self.vect_move = core.p.math.Vector2(0, 0)
        self.vect_mouse = core.p.math.Vector2(core.Inputhandler.x_mouse - self.x, core.Inputhandler.y_mouse - self.y)
        self.current_gun = 1
        self.prev_wep = 0
        self.guns = [True, True, True, True, True, True, False]
        self.ammo = [-1, 33, 44, 44, 44]  # Handgun ammo, shotgun ammo, rifle ammo, sniper rifle, machine gun
        self.angle = 0
        self.hit_animation = False
        self.step = False
        self.moved_since_step = 0

    @staticmethod
    def load_resources():
        imglist = core.load_spritesheet_alpha(core.Var.path_hero, 128, 3, 1)
        Hero.img_hero_body = imglist[0]
        Hero.img_hero_hands = [imglist[1], imglist[2]]
        Hero.img_flash = core.load_image_alpha(core.Var.path_flash)
        sabersprites = core.load_spritesheet_alpha(core.Var.path_starwars, 256, 3, 5)[0:14]
        Hero.img_saber = [sabersprites[0], sabersprites[7], sabersprites[1:7], sabersprites[8:14]]
        Hero.img_shell = core.load_spritesheet_alpha(core.Var.path_shell, 16, 2, 1)

    def render(self, s):
        self.angle = self.vect_mouse.angle_to(core.Var.unit_vector)
        rotated_body = core.p.transform.rotate(self.img_hero_body, self.angle)
        center = core.p.math.Vector2(core.dpp(17), 0)
        center.rotate_ip(-self.angle)

        if self.current_gun == 0:
            if not self.hit_animation:

                rotated_weapon = core.p.transform.rotate(self.img_saber[core.Gameobj.guns[0].lefthand], self.angle)
            else:
                if core.Gameobj.guns[0].frame >= core.Gameobj.guns[0].animation_len:
                    core.Gameobj.guns[0].frame -= 1
                elif core.Gameobj.guns[0].frame < 0:
                    core.Gameobj.guns[0].frame = 0
                if core.Gameobj.guns[0].lefthand:
                    rotated_weapon = core.p.transform.rotate(self.img_saber[3][core.Gameobj.guns[0].frame], self.angle)
                else:
                    rotated_weapon = core.p.transform.rotate(self.img_saber[2][core.Gameobj.guns[0].frame], self.angle)
            center_w = core.p.math.Vector2(core.dpp(42), 0)
            center_w.rotate_ip(-self.angle)
        else:
            rotated_hands = core.p.transform.rotate(self.img_hero_hands[core.Gameobj.guns[self.current_gun].reload_bool],
                                                    self.angle)
            rotated_weapon = core.p.transform.rotate(self.img_weapons[self.current_gun-1], self.angle)
            center_w = core.p.math.Vector2(core.dpp(50-7*core.Gameobj.guns[self.current_gun].delta_shot), 0)
            center_w.rotate_ip(-self.angle)
            frame_hands = rotated_hands.get_rect()
            frame_hands.center = round(self.x+center.x-core.Var.offset_x), round(self.y+center.y-core.Var.offset_y)
            if core.Gameobj.guns[self.current_gun].delta_shot != 0:
                rotated_flash = core.p.transform.rotate(self.img_flash, self.angle)
                frame_flash = rotated_flash.get_rect()
                center_flh = core.p.math.Vector2(center_w.x, center_w.y)
                center_flh.scale_to_length(core.dpp(30)+core.Gameobj.guns[self.current_gun].length)
                frame_flash.center = round(self.x+center_flh.x-core.Var.offset_x), round(self.y+center_flh.y-core.Var.offset_y)
                s.blit(rotated_flash, frame_flash)
            s.blit(rotated_hands, frame_hands)

        self.frame = rotated_body.get_rect()
        self.frame.center = round(self.x-core.Var.offset_x), round(self.y-core.Var.offset_y)
        frame_weapon = rotated_weapon.get_rect()
        frame_weapon.center = round(self.x+center_w.x-core.Var.offset_x), round(self.y+center_w.y-core.Var.offset_y)
        s.blit(rotated_weapon, frame_weapon)
        s.blit(rotated_body, self.frame)

    def get_damage(self, dmg):
        self.health -= dmg
        core.Var.channel_misc2.play(core.Var.sound_hero_hit[core.randint(0, 2)])
        rng = core.dppr(10.3)
        x = self.x + core.randint(-rng, rng)
        y = self.y + core.randint(-rng, rng)
        core.Gameobj.particle_effect(core.Gameobj.img_blood, 5, True, core.dppr(35), x, y)
        if self.health < 0:
            self.health = 0

    def update(self, delta):
        self.move_hero(delta)
        if core.Inputhandler.mouse_buttons_down[0]:
            core.Gameobj.guns[self.current_gun].action()
        if core.Inputhandler.mouse_buttons_released[0]:
            core.Gameobj.guns[self.current_gun].was_shot = False
            core.Gameobj.guns[self.current_gun].consecutive_shots = 0
        if self.current_gun != 0:
            core.Gameobj.guns[self.current_gun].reload(delta)
            if core.Inputhandler.reload_button:
                core.Gameobj.guns[self.current_gun].start_reload()
        else:
            core.Gameobj.guns[0].can_hit(delta)
        prev_gun = self.current_gun
        if core.Inputhandler.prev_button_pressed:
            self.current_gun = self.prev_wep
            core.Gameobj.weapon_switch(prev_gun, self.current_gun)
        if True in core.Inputhandler.select_weapon and self.guns[core.Inputhandler.select_weapon.index(True)]:
            self.current_gun = core.Inputhandler.select_weapon.index(True)  # Relva valik keyboardiga
            if prev_gun != self.current_gun:
                core.Gameobj.weapon_switch(prev_gun, self.current_gun)
        elif core.Inputhandler.scroll_wheel[0]:  # Hiire rullikuga
            self.current_gun -= 1
            while True:
                if self.current_gun < 0:
                    self.current_gun = len(self.guns) - self.guns[::-1].index(True)-1
                    break
                elif not self.guns[self.current_gun]:
                    self.current_gun -= 1
                else:
                    break
            core.Gameobj.weapon_switch(prev_gun, self.current_gun)
        elif core.Inputhandler.scroll_wheel[1]:
            self.current_gun += 1
            while True:
                if self.current_gun >= len(self.guns):
                    self.current_gun = 0
                elif not self.guns[self.current_gun]:
                    self.current_gun += 1
                else:
                    break
            core.Gameobj.weapon_switch(prev_gun, self.current_gun)

    def move_hero(self, delta):
        move_x = self.x + core.Inputhandler.move_buttons[3] - core.Inputhandler.move_buttons[2]
        move_y = self.y + core.Inputhandler.move_buttons[1] - core.Inputhandler.move_buttons[0]
        self.vect_mouse.x = core.Inputhandler.x_mouse+core.Var.offset_x - self.x
        self.vect_mouse.y = core.Inputhandler.y_mouse+core.Var.offset_y - self.y
        self.vect_move.x = move_x - self.x
        self.vect_move.y = move_y - self.y
        speed = self.speed / core.Gameobj.guns[self.current_gun].weight * delta
        if self.vect_move.length_squared() != 0:
            self.vect_move.scale_to_length(speed)
            speed_x, speed_y = self.vect_move.x, self.vect_move.y
            new_x = self.x + speed_x
            new_y = self.y + speed_y
            if new_x < core.Var.level_boundries[0]+self.sizenotsq or new_x > core.Var.level_boundries[1]-self.sizenotsq:
                new_x = self.x
            if new_y < core.Var.level_boundries[2]+self.sizenotsq or new_y > core.Var.level_boundries[3]-self.sizenotsq:
                new_y = self.y
            self.moved_since_step += (self.x-new_x)**2 + (self.y-new_y)**2
            if core.Var.channel_misc1.get_sound() is None and self.moved_since_step > core.dpp(2.4)**2*delta:
                self.step = not self.step
                self.moved_since_step = 0
                core.Var.channel_misc1.play(core.Var.sound_steps[self.step])
            self.x = new_x
            self.y = new_y
