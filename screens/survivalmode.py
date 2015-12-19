#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint
from time import time
import core
import core.monster
import core.player
import core.uielements as ui
import core.widgets


class Survivalmode(core.Screen):
    def __init__(self):
        core.Screen.__init__(self, 0)
        self.wave_cooldown = 4
        self.next_wave_started = True
        self.wave = False
        self.end_wave = True
        self.n_spawn_this_wave = 0
        self.time_wave_end = 0
        self.n_spawn_zombies = 0
        self.max_zombies = 0
        self.end_message = None

    def on_start(self):
        self.next_wave_started = True
        self.wave = False
        self.end_wave = True
        core.monster.Monster.load_resources()
        core.player.Hero.load_resources()
        weapon_imgs = core.load_spritesheet_alpha(core.Var.path_weapon, 96, 4, 3)
        core.player.Hero.img_weapons = weapon_imgs[0:4]
        core.player.Hero.img_weapons.append(weapon_imgs[9])
        core.Item.img_weaponground = weapon_imgs[4:8]
        core.Item.img_weaponground.insert(0, weapon_imgs[8])
        core.Item.img_weaponground.append(weapon_imgs[10])
        core.Var.level_boundries = (0, round(core.Var.SCREEN_WIDTH*1.5), 0, round(core.Var.SCREEN_HEIGHT*1.5))
        core.Var.level_background = core.p.Surface((core.Var.level_boundries[1] - core.Var.level_boundries[0],
                                                    core.Var.level_boundries[3] - core.Var.level_boundries[2]))
        core.Var.level_background.fill(core.Var.BLACK)
        tile = core.load_image(core.Var.path_grassybk)
        tile_x = tile.get_width()
        tile_y = tile.get_height()
        for x in range(core.Var.level_background.get_width()//tile_x+1):
            for y in range(core.Var.level_background.get_height()//tile_y+1):
                core.Var.level_background.blit(tile, (x*tile_x, y*tile_y))
        core.Var.level_background.convert()
        core.Gameobj.reset()
        if not core.Var.game_loaded:
            core.Var.reset_score()
            core.Gameobj.reset_hero()
            core.Gameobj.hero = core.player.Hero(0, 0, core.Var.hero_max_health, core.Var.hero_speed)
            core.Gameobj.hero.x = core.Var.level_boundries[1] / 2
            core.Gameobj.hero.y = core.Var.level_boundries[3] / 2
            core.Var.survival_wave = 1
        else:
            core.Var.game_loaded = False
        self.time_wave_end = time()

    def render(self, s):
        s.blit(core.Var.level_background, (-core.Var.offset_x, -core.Var.offset_y))
        # DRAW BULLETS
        for i in core.Gameobj.bullets:
            if time() - i[4] > core.Var.bullet_timeout:
                core.Gameobj.bullets.remove(i)
                continue
            core.p.draw.line(s, core.Var.YELLOW_BULLET, (i[0], i[1]), (i[2], i[3]), core.Var.bullet_line_thickness)
        # DRAW ITEMS
        for i in core.Gameobj.items:
            i.render(s)
        # DRAW PARTICLES
        for i in core.Gameobj.particles_below:
            i.render(s)
        # DRAW MONSTERS
        for i in core.Gameobj.monsters:
            i.render(s)
        # DRAW HERO
        core.Gameobj.hero.render(s)
        # DRAW PARTICLES
        for i in core.Gameobj.particles_over:
            i.render(s)

        # DRAW HUD
        if self.next_wave_started:  # TODO
            img_text_wave = core.Var.font_title.render(
                core.Var.str_wave[core.Var.language_id] + " " + str(core.Var.survival_wave), True, core.Var.WHITE)
            frame_text_wave = img_text_wave.get_rect()
            frame_text_wave.center = (core.Var.SCREEN_WIDTH / 2, core.Var.SCREEN_HEIGHT / 2)
            s.blit(img_text_wave, frame_text_wave)
        ui.draw_healthbar(s, 25, core.udpp(core.Var.SCREEN_HEIGHT) - 42, 150, 24, core.Gameobj.hero.health,
                          core.Gameobj.hero.maxhealth)
        ui.draw_ammo(s, core.udpp(core.Var.SCREEN_WIDTH)-103, core.udpp(core.Var.SCREEN_HEIGHT) - 42,
                     core.Gameobj.guns[core.Gameobj.hero.current_gun].clip,
                     core.Gameobj.hero.ammo[
                         core.Gameobj.guns[core.Gameobj.hero.current_gun].bullet_type])
        ui.draw_score(s, core.Var.SCREEN_WIDTH/2-core.dpp(38), core.Var.SCREEN_HEIGHT-core.dpp(42))

        if self.end_message is not None:
            self.end_message.render(s)

    def update(self, delta):
        if core.Gameobj.hero.health == 0 and self.end_message is None:
            self.end_message = core.widgets.MessageInput(core.Var.str_gameover[core.Var.language_id])
            core.Gameobj.guns[core.Gameobj.hero.current_gun].reload_bool = False
        if self.end_message is None:
            current_time = time()
            # Do things when start the wave
            if self.next_wave_started and current_time - self.time_wave_end >= self.wave_cooldown:
                self.start_next_wave()
                self.next_wave_started = False
                self.wave = True
                self.end_wave = False
            # If there is need for more monsters, then spawn
            elif self.wave and len(core.Gameobj.monsters) < self.max_zombies and self.n_spawn_this_wave > 0:
                self.n_spawn_this_wave -= (self.max_zombies - len(core.Gameobj.monsters))
                Survivalmode.spawn_zombie(self.max_zombies - len(core.Gameobj.monsters))
            # Check if wave has ended
            elif not self.end_wave and len(core.Gameobj.monsters) == 0:
                core.Var.survival_wave += 1
                self.end_wave = True
                self.time_wave_end = time()
                self.next_wave_started = True
            if core.Var.counter % 2 == 0:
                core.Gameobj.check_collision_between_monsters()
            for i in core.Gameobj.monsters:
                i.update(delta)
            core.Gameobj.hero.update(delta)
            for i in core.Gameobj.items:
                i.check_collision(core.Gameobj.hero.x, core.Gameobj.hero.y, core.Gameobj.hero.size*2)
            for i in core.Gameobj.particles_below:
                i.update(delta)
            for i in core.Gameobj.particles_over:
                i.update(delta)
            core.offset()
        else:
            self.end_message.update(delta)
            if self.end_message.value is not None:
                core.Var.scoreboard_data.append([str(len(core.Var.scoreboard_data) + 1), self.end_message.value,
                                                 str(core.Var.score), str(core.Var.survival_wave),
                                                 str(core.Var.bullets_shot), str(core.Var.bullets_hit),
                                                 str(core.Var.monsters_killed)])
                templist = []
                for i in core.Var.scoreboard_data:
                    templist.append(int(i[2]))
                sortedlist = [x for y, x in sorted(zip(templist, core.Var.scoreboard_data))]
                core.Var.scoreboard_data = list(reversed(sortedlist))
                for i in range(len(core.Var.scoreboard_data)):
                    core.Var.scoreboard_data[i][0] = str(i+1)
                if len(core.Var.scoreboard_data) > 15:
                    core.Var.scoreboard_data.pop()
                core.Var.start_screen = True
                core.Var.stop_screen = True
                core.Var.new_screen = 5
                self.end_message = None

    def on_resume(self):
        core.Var.current_game = [True, 0]
        core.Var.fps_current = core.Var.fps_id
        core.Var.game_saved = False
        core.p.mixer.music.pause()

    def on_pause(self):
        pass

    def on_stop(self):
        core.p.mixer.music.unpause()

    @staticmethod
    def spawn_zombie(amount):
        for i in range(amount):
            spawn_location = randint(0, 3)
            a = randint(30, 400)
            if spawn_location == 0:
                x = core.Var.level_boundries[0] - a
                y = randint(core.Var.level_boundries[2] - a, core.Var.level_boundries[3] + a)
            elif spawn_location == 1:
                x = core.Var.level_boundries[1] + a
                y = randint(core.Var.level_boundries[2] - a, core.Var.level_boundries[3] + a)
            elif spawn_location == 2:
                x = randint(core.Var.level_boundries[0] - a, core.Var.level_boundries[1] + a)
                y = core.Var.level_boundries[2] - a
            elif spawn_location == 3:
                x = randint(core.Var.level_boundries[0] - a, core.Var.level_boundries[1] + a)
                y = core.Var.level_boundries[3] + a
            else:
                x, y = 0, 0
            core.Gameobj.monsters.append(core.monster.Zombie(x, y))

    def start_next_wave(self):
        self.n_spawn_zombies = round(11 * 1.4**core.Var.survival_wave)
        if core.Var.survival_wave < 7:
            self.max_zombies = round(10 * 1.3**core.Var.survival_wave)
        else:
            self.max_zombies = 55
        self.n_spawn_this_wave = self.n_spawn_zombies
