#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame as p
import os
import sys
from math import sqrt
from random import randint
from time import time

# Kood pygame example failist, mis keelab windowsil High DPIga venituse.
if os.name != "nt" or sys.getwindowsversion()[0] < 6:
    pass
else:
    # Ensure that ctypes is installed. It is included with Python 2.5 and newer,
    # but Python 2.4 users must install ctypes manually.
    try:
        import ctypes
    except ImportError:
        print('install ctypes from http://sourceforge.net/projects/ctypes/files/ctypes')
        raise

    # Prevent stretching
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
# Example failist koodi l6pp

p.init()


class Var(object):
    # Core variables
    display_info = p.display.Info()
    ASPECT_RATIO = 16 / 9
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = round(SCREEN_WIDTH / ASPECT_RATIO)
    dpp = sqrt(SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2) / 1000
    dpp2 = sqrt(SCREEN_WIDTH ** 2 + SCREEN_HEIGHT ** 2) / 2203
    offset_x = 0
    offset_y = 0
    is_fullscreen = False
    current_screen = None
    current_game = [False, -1]
    survival_wave = 0
    game_saved = False
    game_loaded = False
    previous_screen = None
    new_screen = 1
    start_screen = True
    stop_screen = False
    aa_text = False
    previous_screen_surface = None
    exit = False
    show_fps = True
    uuid_gen = 1
    counter = 0
    fps_id = 4
    fps_current = fps_id
    fps = (30, 60, 90, 120, 0)
    language_id = 0
    languages = ("Eesti", "English", "Русский")
    resolution_id = 5
    resolutions = ((640, 360), (720, 405), (854, 480), (960, 540),
                   (1024, 576), (1280, 720), (1366, 768), (1600, 900), (1920, 1080),
                   (2048, 1152), (2560, 1440), (2880, 1620), (3200, 1800), (3840, 2160))
    clock = p.time.Clock()
    #        master,music,audio
    volume = [100, 100, 100]

    # Game data
    scoreboard_data = []
    level_boundries = (0, 0, 0, 0)
    level_background = None
    score = 0
    monsters_killed = 0
    bullets_shot = 0
    bullets_hit = 0

    # Resource Location Paths
    folder_img = "images"
    path_background = os.path.join(folder_img, "bck.png")
    path_zombie = os.path.join(folder_img, "zombie.png")
    path_hero = os.path.join(folder_img, "spritesheetHero.png")
    path_weapon = os.path.join(folder_img, "weapons.png")
    path_bloodsplash = os.path.join(folder_img, "bloodsplash.png")
    path_config = os.path.join("data", "config.pickle")
    path_survsave = os.path.join("data", "survivalsave.pickle")
    path_score = os.path.join("data", "scoreboard.pickle")
    path_zombiegore = os.path.join(folder_img, "zombiegore.png")
    path_flash = os.path.join(folder_img, "muzzleflash.png")
    path_grassybk = os.path.join(folder_img, "grassybackground.png")
    path_starwars = os.path.join(folder_img, "starwars.png")
    path_shell = os.path.join(folder_img, "shell.png")

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    LIGHT_GRAY = (180, 180, 180)
    GREEN_HEALTHBAR = (0, 200, 5)
    RED_HEALTHBAR = (200, 5, 2)
    YELLOW_BULLET = (255, 255, 0)
    BULLET_BAR_DARK = (55, 55, 45)
    BULLET_BAR_LIGHT = (200, 200, 45)
    COLOR_KEY = (255, 0, 255)
    THEME_DEFAULT = p.Color(34, 85, 63)  # Blueish
    default_hue = 154
    # THEME_DEFAULT = p.Color(0, 117, 6)  # Greenish
    # THEME_DEFAULT = p.Color(117, 0, 0)  # Redish
    THEME_DOWN = p.Color(0, 0, 0)
    THEME_LIGHT = p.Color(0, 0, 0)
    THEME_HOVER = p.Color(0, 0, 0)
    THEME_BACKGROUND = p.Color(0, 0, 0)

    # Strings
    str_mainmenu = (  # ("Jätka mängu", "Continue game", "Продолжить игру"),
        ("Lae mäng", "Load game", "Загрузить игру"),
        ("Uus mäng", "New game", "Новая игра"),
        ("Edetabel", "Scoreboard", "Табло"),
        ("Sätted", "Settings", "Настройки"),
        ("Abi", "Help", "Помогите"),
        ("Välju", "Exit", "Выход"))
    str_pausemenu = (("Jätka mängu", "Continue game", "Продолжить"),
                     ("Salvesta mäng", "Save game", "сохранить игру"),
                     ("Lae mäng", "Load game", "Загрузить игру"),
                     ("Peamenüü", "Main menu", "главное меню"),
                     ("Välju", "Exit", "Выход"))
    CAPTION = ("Zombi mäng HD 2.0", "Zombie game HD 2.0", "Зомби игры HD 2.0")
    str_back = ("Tagasi", "Back", "Назад")
    str_fullscreen = ("Täisekraan", "Full screen", "Полноэкранный")
    str_videoaudio = ("Mängu sätted", "Game settings", "варианты игры")
    str_controls = ("Nupud", "Controls", "управления")
    str_resolution = ("Resolutsioon", "Resolution", "Pазрешение")
    str_wave = ("Laine", "Wave", "Волна")
    str_language = ("Keel", "Language", "язык")
    str_keybinds = (("Liigu üles", "Move up", "вверх"), ("Liigu alla", "Move down", "вниз"),
                    ("Liigu vasakule", "Move left", "Двигай влево"),
                    ("Liigu paremale", "Move right", "Двигаться вправо"),
                    ("Lae relv", "Load weapon", "Нагрузка оружие"),
                    ("Eelmine relv", "Previous weapon", "Предыдущее оружие"),
                    ("Relv 1", "Weapon 1", "Оружие 1"), ("Relv 2", "Weapon 2", "Оружие 2"),
                    ("Relv 3", "Weapon 3", "Оружие 3"),
                    ("Relv 4", "Weapon 4", "Оружие 4"), ("Relv 5", "Weapon 5", "Оружие 5"),
                    ("Relv 6", "Weapon 6", "Оружие 6"), ("Relv 7", "Weapon 7", "Оружие 7"))
    str_fpslimit = (("Kaadrisageduse piir", "FPS limit", "FPS limit"), ("Piiramatu", "Unlimited", "безграничный"))
    str_are_you_sure = (("Jaa, olen", "Ei ole"), ("Yea, i am", "Not really"), ("я уверен", "Нет!"))
    str_exit_game_message = (
        ("Kas oled kindel, et soovid mängust lahkuda?", "Seda tehes kaotad sa salvestamata progressi."),
        ("Are you sure, that you want to exit to main menu?", "You will lose all unsaved progress."),
        ("Вы уверены, что, что вы хотите, чтобы выйти в главное меню?", "Вы потеряете все несохраненные прогресса."))
    str_exit_all_message = (("Kas mäng on liiga hirmus?", "Kui lahkud siis kaotad kogu", "salvestamata progressi."),
                            ("Is the game too spooky for you?", "If you do leave, then you'll",
                             "lose all unsaved progress."),
                            ("Является ли игра тоже жуткий для вас?", "Если вы оставить, то вы потеряете",
                             "все несохраненные прогресса."))
    str_are_you_sure_exit = (
        ("Väga kardan", "Tahan veel"), ("I am scared", "I want more"), ("мне страшно", "хочу больше"))
    str_save_message = (("Hoiatus!", "Salvestades kirjutad sa eelmise salvestuse üle.", "Kas oled kindel?"),
                        ("Warning!", "You will rewrite your old save.", "Are you sure?"),
                        ("Предупреждение!", "Вы переписать старый спасти.", "Вы уверены?"))
    str_scoreboard = (("Nr.", "Nimi", "Skoor", "Laine", "Laske", "Pihta", "Kille"),
                      ("No.", "Name", "Score", "Wave", "Shots", "Hits", "Monster kills"),
                      ("Нр.", "имя", "Гол", "Волна", "Выстрелов", "Пули попали", "Убийств"))
    str_gameover = (("Mäng läbi!", "Sul said elud otsa.", "Sisesta oma nimi", ""),
                    ("Game over!", "You ran out of health.", "Enter your name", ""),
                    ("Игра закончена", "Вы можете запустить из жизни.", "Введите ваше имя", ""))
    str_volume = (("Master", "Master", "Мастер"), ("Muusika", "Music", "Музыка"), ("Helid", "Sounds", "Звуки"))
    str_video = ("Video", "Video", "видео")
    str_sound = ("Heli", "Sound", "звук")
    str_game = ("Mäng", "Game", "Игра")
    str_color = ("Menüü värvus", "Menu color hue", "Меню оттенок цвета")
    str_showfps = ("Näita FPS", "Show FPS", "Показать FPS")
    str_wallofhelp = []

    # Fonts
    font_button = None
    font_title = None
    font_tiny = None
    font_ammo = None

    # Keys
    #             UP     DOWN  LEFT   RIGHT RELOAD PREW_W   WP1    WP2    WP3    WP4    WP5    WP6    WP7
    #             0       1     2       3       4     5      6      7       8     9      10     11    12
    key_binds = [p.K_w, p.K_s, p.K_a, p.K_d, p.K_r, p.K_q, p.K_1, p.K_2, p.K_3, p.K_4, p.K_5, p.K_6] #, p.K_7]

    # ObjData
    hero_max_health = 100
    hero_speed = None

    # Numbers
    bullet_timeout = 0.07
    bullet_line_thickness = None

    # Cheats
    infinite_ammo = False

    # Misc
    unit_vector = p.math.Vector2(1, 0)

    # Sounds
    p.mixer.music.load(os.path.join("sounds", "nemesis.ogg"))
    channel_weapona = p.mixer.Channel(0)
    channel_weaponr = p.mixer.Channel(3)
    channel_monster1 = p.mixer.Channel(1)
    channel_monster2 = p.mixer.Channel(2)
    channel_misc1 = p.mixer.Channel(4)
    channel_misc2 = p.mixer.Channel(5)
    sound_saber = [p.mixer.Sound(os.path.join("sounds", "Swing01.WAV")),
                   p.mixer.Sound(os.path.join("sounds", "Swing02.WAV"))]
    sound_guns = [[p.mixer.Sound(os.path.join("sounds", "glock18-2.wav"))],
                  [p.mixer.Sound(os.path.join("sounds", "m3-1.wav"))],
                  [p.mixer.Sound(os.path.join("sounds", "ak47-1.wav")),
                   p.mixer.Sound(os.path.join("sounds", "ak47-2.wav"))],
                  [p.mixer.Sound(os.path.join("sounds", "awp1.wav"))],
                  [p.mixer.Sound(os.path.join("sounds", "m249-1.wav")),
                   p.mixer.Sound(os.path.join("sounds", "m249-2.wav"))]]
    sound_reload = [p.mixer.Sound(os.path.join("sounds", "generic_reload.wav")),
                    p.mixer.Sound(os.path.join("sounds", "generic_shot_reload.wav")),
                    [p.mixer.Sound(os.path.join("sounds", "ak47_clipin.wav")),
                     p.mixer.Sound(os.path.join("sounds", "ak47_clipout.wav"))],
                    [p.mixer.Sound(os.path.join("sounds", "awp_clipin.wav")),
                     p.mixer.Sound(os.path.join("sounds", "awp_clipout.wav")),
                     p.mixer.Sound(os.path.join("sounds", "sg552_boltpull.wav"))],
                    p.mixer.Sound(os.path.join("sounds", "m249_reload.wav"))]
    sound_deploy = [p.mixer.Sound(os.path.join("sounds", "SaberOn.wav")),
                    p.mixer.Sound(os.path.join("sounds", "usp_slideback.wav")),
                    p.mixer.Sound(os.path.join("sounds", "m3_pump.wav")),
                    p.mixer.Sound(os.path.join("sounds", "ak47_boltpull.wav")),
                    p.mixer.Sound(os.path.join("sounds", "awp_deploy.wav")),
                    p.mixer.Sound(os.path.join("sounds", "m249_coverup.wav"))]
    sound_steps = [p.mixer.Sound(os.path.join("sounds", "pl_dirt1.wav")),
                   p.mixer.Sound(os.path.join("sounds", "pl_dirt2.wav"))]
    sound_hero_hit = [p.mixer.Sound(os.path.join("sounds", "bhit_flesh-1.wav")),
                      p.mixer.Sound(os.path.join("sounds", "bhit_flesh-2.wav")),
                      p.mixer.Sound(os.path.join("sounds", "bhit_flesh-3.wav"))]
    sound_zombie_die = [p.mixer.Sound(os.path.join("sounds", "zombie_die1.wav")),
                        p.mixer.Sound(os.path.join("sounds", "zombie_die2.wav")),
                        p.mixer.Sound(os.path.join("sounds", "zombie_die3.wav")),
                        p.mixer.Sound(os.path.join("sounds", "zombie_die4.wav")),
                        p.mixer.Sound(os.path.join("sounds", "zombie_die5.wav"))]
    sound_pick = p.mixer.Sound(os.path.join("sounds", "zoom.wav"))
    sound_steps[0].set_volume(0.34)
    sound_steps[1].set_volume(0.34)

    @staticmethod
    def set_volume():
        Var.channel_weaponr.set_volume((Var.volume[0] / 100) * (Var.volume[2] / 100))
        Var.channel_weapona.set_volume((Var.volume[0] / 100) * (Var.volume[2] / 100))
        Var.channel_monster1.set_volume((Var.volume[0] / 100) * (Var.volume[2] / 100))
        Var.channel_monster2.set_volume((Var.volume[0] / 100) * (Var.volume[2] / 100))
        Var.channel_misc1.set_volume((Var.volume[0] / 100) * (Var.volume[2] / 100))
        Var.channel_misc2.set_volume((Var.volume[0] / 100) * (Var.volume[2] / 100))
        p.mixer.music.set_volume((Var.volume[0] / 100) * (Var.volume[1] / 100))

    @staticmethod
    def init_dpp_dependent():
        Var.dpp = sqrt(Var.SCREEN_WIDTH ** 2 + Var.SCREEN_HEIGHT ** 2) / 1000
        Var.dpp2 = sqrt(Var.SCREEN_WIDTH ** 2 + Var.SCREEN_HEIGHT ** 2) / 2153
        try:
            if Var.language_id == 2:
                raise Exception
            Var.font_button = p.font.Font(os.path.join("data\\Dirty Ego\\Truetype", "DIRTYEGO.TTF"), round(30 * Var.dpp))
        except:
            Var.font_button = p.font.SysFont("Verdana", round(20 * Var.dpp))
        try:
            if Var.language_id == 2:
                raise Exception
            Var.font_title = p.font.Font(os.path.join("data\\Astonished\\Truetype", "ASTONISHED.TTF"), round(68 * Var.dpp))
        except:
            Var.font_title = p.font.SysFont("Verdana", round(40 * Var.dpp))
        Var.font_tiny = p.font.SysFont("Verdana", round(14 * Var.dpp))
        Var.font_ammo = p.font.SysFont("Verdana", round(22 * Var.dpp))
        Var.bullet_line_thickness = round(1.5 * Var.dpp)
        Var.hero_speed = 20 * Var.dpp

    @staticmethod
    def init_menu_colors():
        Var.THEME_DEFAULT = p.Color(34, 85, 63)
        if 288 > Var.default_hue > 180:
            lightness = 3
        else:
            lightness = 0
        Var.THEME_DEFAULT.hsla = (
            Var.default_hue, Var.THEME_DEFAULT.hsla[1], Var.THEME_DEFAULT.hsla[2] + 5 + lightness,
            Var.THEME_DEFAULT.hsla[3])
        Var.THEME_DOWN.hsla = (
            Var.THEME_DEFAULT.hsla[0], Var.THEME_DEFAULT.hsla[1], Var.THEME_DEFAULT.hsla[2] - 10 + lightness,
            Var.THEME_DEFAULT.hsla[3])
        Var.THEME_LIGHT.hsla = (
            Var.THEME_DEFAULT.hsla[0] + 1, Var.THEME_DEFAULT.hsla[1], Var.THEME_DEFAULT.hsla[2] + 20 + lightness,
            Var.THEME_DEFAULT.hsla[3])
        Var.THEME_HOVER.hsla = (
            Var.THEME_DEFAULT.hsla[0] - 1, Var.THEME_DEFAULT.hsla[1], Var.THEME_DEFAULT.hsla[2] + 9 + lightness,
            Var.THEME_DEFAULT.hsla[3])
        Var.THEME_BACKGROUND.hsla = (
            Var.THEME_DEFAULT.hsla[0] - 5, Var.THEME_DEFAULT.hsla[1] - 18, Var.THEME_DEFAULT.hsla[2] - 4 + lightness,
            Var.THEME_DEFAULT.hsla[3])

    @staticmethod
    def reset_score():
        Var.score = 0
        Var.monsters_killed = 0
        Var.bullets_shot = 0
        Var.bullets_hit = 0


class Gameobj(object):
    img_blood = []
    hero = None
    guns = []
    monsters = []
    bullets = []
    particles_below = []
    particles_over = []
    items = []

    @staticmethod
    def check_collision_between_monsters():
        l1 = list(range(len(Gameobj.monsters)))
        for m1 in l1[::-1]:
            direction_x = 0
            direction_y = 0
            # Checks collision with other monsters
            for m2 in l1:
                if Gameobj.monsters[m2].uuid != Gameobj.monsters[m1].uuid:
                    Gameobj.monsters[m1].collision_with_other = [False, 1, 1]
                    vect = p.math.Vector2(Gameobj.monsters[m2].x - Gameobj.monsters[m1].x,
                                          Gameobj.monsters[m2].y - Gameobj.monsters[m1].y)
                    if vect.length_squared() < (Gameobj.monsters[m1].size + Gameobj.monsters[m2].size) * 2:
                        direction_x += vect.x
                        direction_y += vect.y
            # Checks collision with hero
            vect = p.math.Vector2(Gameobj.hero.x - Gameobj.monsters[m1].x,
                                  Gameobj.hero.y - Gameobj.monsters[m1].y)
            if vect.length_squared() < (Gameobj.monsters[m1].size + Gameobj.hero.size - 3) / 1.04:
                direction_x += vect.x
                direction_y += vect.y
            vector = p.math.Vector2(direction_x, direction_y)
            if vector.x != 0 and vector.y != 0:
                vector = vector.normalize()
                Gameobj.monsters[m1].collision_with_other = [True, -vector.x, -vector.y]
            else:
                Gameobj.monsters[m1].collision_with_other = [False, 1, 1]

    @staticmethod
    def reset():
        Gameobj.img_blood = load_spritesheet(Var.path_bloodsplash, 48, 3, 2)
        # Guns
        #                          name,dmg,clip,spr,aut,spd,wgh,rldtime,pershot,range,bullettype, length,soundid
        Gameobj.guns = [Melee("Lightsaber", 144, True, .45, 0.9, dppr2(180), 6),
                        Gun("Glock 18", 32, 20, 6, True, 0.87, 1, 1850, 1, 0, 0, dppr2(40), 0),  # Handgun
                        Gun("Sawed off shotgun", 24, 8, 18, True, 1.37, 1.5, 3100, 7, dpp(250), 1, dppr2(60), 1),
                        # Shotgun
                        Gun("AK-47", 34, 30, 11, True, 0.145, 1.8, 2220, 1, 0, 2, dppr2(96), 2),  # Rifle
                        Gun("AWP", 252, 10, 2, False, 2.13, 2.5, 2850, 1, 0, 3, dppr2(96), 3),
                        Gun("M249", 24, 100, 9, True, 0.24, 2.35, 3500, 1, 0, 4, dppr2(96), 4)]  # Sniper
        Gameobj.monsters.clear()
        Gameobj.bullets.clear()
        Gameobj.particles_below.clear()
        Gameobj.particles_over.clear()
        Gameobj.items.clear()

    @staticmethod
    def reset_hero():
        Gameobj.hero = None

    @staticmethod
    def weapon_switch(prev_gun, new_gun):
        Gameobj.guns[prev_gun].reload_bool = False
        Gameobj.hero.prev_wep = prev_gun
        Var.channel_weaponr.stop()
        Var.channel_weaponr.play(Var.sound_deploy[new_gun])

    @staticmethod
    def particle_effect(img, amount, disappear, speed, x, y):
        for i in range(amount):
            # TODO maybe
            dis = dppr(25)
            rng = randint(0, len(img) - 1)
            if disappear:
                Gameobj.particles_over.append(
                    Particle((x, y, x + randint(-dis, dis), y + randint(-dis, dis)),
                             (randint(speed, dis + speed * 2) / 1000, 0), (randint(-15, 15), 0),
                             randint(750, 1400),
                             disappear,
                             img[rng]))
            else:
                Gameobj.particles_below.append(
                    Particle((x, y, x + randint(-dis, dis), y + randint(-dis, dis)),
                             (randint(speed, dis + speed * 2) / 1000, 0), (randint(-15, 15), 0),
                             randint(750, 1400),
                             disappear,
                             img[rng]))


class Weapon(object):
    def __init__(self, name, damage, automatic, speed, weight, range_weapon, clip_size, bullet_type):
        self.name = name
        self.damage = damage
        self.automatic = automatic
        self.speed = speed
        self.weight = weight
        self.previous_shot = 0
        self.was_shot = False
        self.delta_shot = 0
        self.range = range_weapon
        self.clip_size = clip_size
        self.clip = clip_size
        self.bullet_type = bullet_type
        self.reload_bool = False

    def action(self):
        raise NotImplementedError


class Melee(Weapon):
    def __init__(self, name, damage, automatic, speed, weight, range_weapon, animation_len):
        Weapon.__init__(self, name, damage, automatic, speed * 1000, weight, range_weapon, -1, 0)
        self.attack = False
        self.attack_delta = -1
        self.animation_len = animation_len
        self.frame = 0
        self.lefthand = False
        self.monsters_hit = set()

    def action(self):
        if not self.attack:
            Var.channel_weapona.play(Var.sound_saber[self.lefthand])
            self.attack_delta = 0
            self.attack = True
            Gameobj.hero.hit_animation = True

    def can_hit(self, delta):
        if self.attack:
            if self.speed > self.attack_delta >= 0:
                self.attack_delta += delta
                self.frame = int(self.attack_delta / self.speed * self.animation_len)
                if self.speed * .72 > self.attack_delta > self.speed * .27:
                    center = p.math.Vector2(dpp(42), 0)
                    center.rotate_ip(-Gameobj.hero.angle)
                    tempx1 = center.x + Gameobj.hero.x
                    tempx2 = tempx1 + center.x * .7
                    tempy1 = center.y + Gameobj.hero.y
                    tempy2 = tempy1 + center.y * .7
                    for monster in Gameobj.monsters:
                        if monster.uuid not in self.monsters_hit:
                            length = dist(tempx1, tempy1, tempx2, tempy2, monster.x, monster.y)
                            if length < monster.size * 2.3:
                                self.monsters_hit.add(monster.uuid)
                                monster.get_damaged(self.damage)
            elif self.attack_delta >= self.speed:
                self.lefthand = not self.lefthand
                Gameobj.hero.hit_animation = False
                self.monsters_hit = set()
                self.attack = False
                self.attack_delta = -1
        else:
            self.frame = 0


class Gun(Weapon):
    def __init__(self, name, damage, clip_size, spread, automatic, speed, weight, reload_time, per_shot, range_weapon,
                 bullet_type, length, sound):
        Weapon.__init__(self, name, damage, automatic, speed, weight, range_weapon, clip_size, bullet_type)
        self.spread = spread
        self.reload_time = reload_time
        self.reload_delta = 0
        self.per_shot = per_shot
        self.length = length
        self.sound = sound
        self.consecutive_shots = 0

    @staticmethod
    def extend_line(spread, amount):
        multiplier = amount / Gameobj.hero.vect_mouse.length()
        tempx = Gameobj.hero.vect_mouse.x * multiplier
        tempy = Gameobj.hero.vect_mouse.y * multiplier
        spread_vect = p.math.Vector2(tempx, tempy)
        spread_vect = spread_vect.rotate(spread)
        tempx, tempy = spread_vect.x, spread_vect.y
        return Gameobj.hero.x + tempx, Gameobj.hero.y + tempy

    def action(self):
        new_time = time()
        delta_time = new_time - self.previous_shot
        if self.clip == 0 and Inputhandler.mouse_buttons_pressed[0]:
            self.start_reload()
        elif self.clip == 0:
            self.was_shot = True
        elif not self.was_shot and not self.reload_bool and delta_time > self.speed and Var.channel_weaponr.get_sound() is None:
            Var.channel_weapona.play(Var.sound_guns[self.sound][randint(0, len(Var.sound_guns[self.sound]) - 1)])
            if self.sound == 3:
                Var.channel_weaponr.play(Var.sound_reload[3][2])
            self.previous_shot = new_time
            if not self.automatic:
                self.was_shot = True
            monsters_in_line = []
            Var.bullets_shot += 1
            self.consecutive_shots += 1
            hit = False
            center = p.math.Vector2(self.length, 0)
            accuracy = 1
            if self.sound == 2 and self.consecutive_shots < 8:
                accuracy -= .8**self.consecutive_shots
            for i in range(self.per_shot):
                monsters_in_line.clear()
                a = round(self.spread*accuracy)
                spread = randint(-a, a)
                if self.range == 0:
                    distance = Var.SCREEN_WIDTH * Var.ASPECT_RATIO
                else:
                    distance = self.range
                tempx, tempy = Gun.extend_line(spread, randint(round(distance-dpp(20)), round(distance+dpp(20))))
                for monster in Gameobj.monsters:
                    length = dist(Gameobj.hero.x, Gameobj.hero.y, tempx, tempy, monster.x, monster.y)
                    if length < monster.size and length is not False:
                        monsters_in_line.append(Gameobj.monsters.index(monster))
                monster_lengths = []
                damage_in_bullet = self.damage
                for n in monsters_in_line:
                    monster_lengths.append(Gameobj.monsters[n].vect_long.length_squared())
                monster_lengths = sorted(monster_lengths)
                closest_len = None
                for lengths in monster_lengths:
                    if damage_in_bullet < 1:
                        break
                    for monster_id in monsters_in_line:
                        closest_len = Gameobj.monsters[monster_id].vect_long.length_squared()
                        if closest_len == lengths:
                            closest_id = monster_id
                            break
                    hp = Gameobj.monsters[closest_id].health
                    Gameobj.monsters[closest_id].get_damaged(damage_in_bullet)
                    Gameobj.monsters[closest_id].kick_back(damage_in_bullet,
                                                           (Gameobj.hero.x, Gameobj.hero.y))
                    damage_in_bullet -= hp
                    hit = True
                if closest_len is not None and len(monsters_in_line) > 0 >= damage_in_bullet:
                    closest_len = sqrt(closest_len)
                    tempx, tempy = Gun.extend_line(spread, closest_len)
                center = p.math.Vector2(dpp(49.5), 0)
                center.rotate_ip(-Gameobj.hero.angle)
                Gameobj.bullets.append(
                    [Gameobj.hero.x + center.x - Var.offset_x, Gameobj.hero.y + center.y - Var.offset_y,
                     tempx - Var.offset_x, tempy - Var.offset_y, new_time])
            center_dir = p.math.Vector2(center.x, center.y)
            center_dir.rotate_ip(-53)
            nr5 = dppr(5)
            if self.sound == 1:
                shell_id = 1
            else:
                shell_id = 0
            Gameobj.particles_below.append(
                Particle((Gameobj.hero.x + center.x * .9, Gameobj.hero.y + center.y * .9,
                          Gameobj.hero.x + center_dir.x + randint(-nr5, nr5),
                          Gameobj.hero.y + center_dir.y + randint(-nr5, nr5)),
                         (randint(dppr(80), dppr(135)) / 1000, 0),
                         (-Gameobj.hero.angle, -Gameobj.hero.angle + randint(10, 38)), 750, False,
                         Gameobj.hero.img_shell[shell_id], False))
            if hit:
                Var.bullets_hit += 1
            if not Var.infinite_ammo:
                self.clip -= 1

    def start_reload(self):
        if not self.reload_bool and self.clip != self.clip_size and Gameobj.hero.ammo[self.bullet_type] != 0:
            self.reload_delta = 0
            self.reload_bool = True
            if self.sound in [0, 1]:
                Var.channel_weaponr.play(Var.sound_reload[self.sound])
                if self.sound == 1:
                    Var.channel_weaponr.queue(Var.sound_reload[1])
            elif self.sound == 4:
                Var.channel_weaponr.play(Var.sound_reload[4])
            else:
                Var.channel_weaponr.play(Var.sound_reload[self.sound][1])

    def reload(self, delta):
        self.delta_shot = 0.1 / (0.1 + self.previous_shot - time())
        if self.delta_shot > 1:
            self.delta_shot = 1
        elif self.delta_shot < 0:
            self.delta_shot = 0
        self.reload_delta += delta
        if self.reload_bool and self.reload_delta > self.reload_time:
            Var.channel_weaponr.stop()
            if self.sound not in [0, 1, 4]:
                Var.channel_weaponr.play(Var.sound_reload[self.sound][0])
                if self.sound == 2:
                    Var.channel_weaponr.queue(Var.sound_deploy[3])
            if Gameobj.hero.ammo[self.bullet_type] == -1:
                self.clip = self.clip_size
            else:
                Gameobj.hero.ammo[self.bullet_type] += -self.clip_size + self.clip
                if Gameobj.hero.ammo[self.bullet_type] < 0:
                    self.clip = self.clip_size + Gameobj.hero.ammo[self.bullet_type]
                    Gameobj.hero.ammo[self.bullet_type] = 0
                else:
                    self.clip = self.clip_size
            self.reload_bool = False


class Screen(object):
    def __init__(self, screen_id):
        self.id = screen_id

    def on_start(self):
        raise NotImplementedError

    def on_resume(self):
        raise NotImplementedError

    def render(self, s):
        raise NotImplementedError

    def update(self, delta):
        raise NotImplementedError

    def on_pause(self):
        raise NotImplementedError

    def on_stop(self):
        raise NotImplementedError

    def get_id(self):
        return self.id


class Inputhandler(object):
    x_mouse, y_mouse = 0, 0
    mouse_rel = (0, 0)
    scroll_wheel = [False, False]
    mouse_buttons_down = [False, False, False]
    mouse_buttons_released = [False, False, False]
    mouse_buttons_pressed = [False, False, False]
    #                 up     down   left   right
    move_buttons = [False, False, False, False]
    select_weapon = [False, False, False, False, False, False, False]
    reload_button = False
    prev_button_pressed = False
    escape_pressed = False
    all_events = []

    @staticmethod
    def reset_keys():
        Inputhandler.move_buttons = [False, False, False, False]
        Inputhandler.select_weapon = [False, False, False, False, False, False, False]
        Inputhandler.reload_button = False
        Inputhandler.escape_pressed = False

    @staticmethod
    def handle(event):
        Inputhandler.x_mouse, Inputhandler.y_mouse = p.mouse.get_pos()
        Inputhandler.mouse_rel = p.mouse.get_rel()
        if True in Inputhandler.mouse_buttons_released or True in Inputhandler.mouse_buttons_pressed:
            Inputhandler.mouse_buttons_released = [False, False, False]
            Inputhandler.mouse_buttons_pressed = [False, False, False]
        if True in Inputhandler.scroll_wheel:
            Inputhandler.scroll_wheel = [False, False]
        if Inputhandler.escape_pressed:
            if Var.current_game[0] and Var.current_screen not in [3, 4]:
                Var.new_screen = 3
                Var.start_screen = True
            elif Var.current_screen == 3:
                Var.new_screen = Var.current_game[1]
                Var.stop_screen = True
            Inputhandler.escape_pressed = False
        if Inputhandler.prev_button_pressed:
            Inputhandler.prev_button_pressed = False
        Inputhandler.all_events.clear()
        for e in event:
            Inputhandler.all_events.append(e)
            if e.type == p.MOUSEBUTTONDOWN:
                if e.button in [1, 2, 3]:
                    Inputhandler.mouse_buttons_down[e.button - 1] = True
                    Inputhandler.mouse_buttons_pressed[e.button - 1] = True
                elif e.button in [4, 5]:
                    Inputhandler.scroll_wheel[e.button - 4] = True
            elif e.type == p.MOUSEBUTTONUP:
                if e.button in [1, 2, 3]:
                    Inputhandler.mouse_buttons_down[e.button - 1] = False
                    Inputhandler.mouse_buttons_released[e.button - 1] = True
            elif e.type == p.KEYDOWN:
                if e.key in Var.key_binds[0:4]:
                    Inputhandler.move_buttons[Var.key_binds[0:4].index(e.key)] = True
                elif e.key == Var.key_binds[4]:
                    Inputhandler.reload_button = True
                elif e.key == Var.key_binds[5]:
                    Inputhandler.prev_button_pressed = True
                elif e.key in Var.key_binds[6:13]:
                    Inputhandler.select_weapon[Var.key_binds[6:13].index(e.key)] = True
                elif e.key == p.K_ESCAPE:
                    Inputhandler.escape_pressed = True
            elif e.type == p.KEYUP:
                if e.key in Var.key_binds[0:4]:
                    Inputhandler.move_buttons[Var.key_binds[0:4].index(e.key)] = False
                elif e.key == Var.key_binds[4]:
                    Inputhandler.reload_button = False
                elif e.key in Var.key_binds[6:13]:
                    Inputhandler.select_weapon[Var.key_binds[6:13].index(e.key)] = False
            elif e.type == p.QUIT:
                if Var.current_screen not in [3, 4]:
                    Var.new_screen = 4
                    Var.start_screen = True


class Particle(object):
    def __init__(self, pos, speed, angle, lifespan, fade, img, disappear=False):
        self.__x1 = pos[0]
        self.__y1 = pos[1]
        self.__x2 = pos[2]
        self.__y2 = pos[3]
        if self.__x1 == self.__x2:
            self.__x2 += 1
        self.lifespan = lifespan
        self.__timeleft = self.lifespan
        self.__vect = p.math.Vector2(self.__x2 - self.__x1, self.__y2 - self.__y1)
        self.__speed_step = (speed[1] - speed[0]) / self.lifespan
        self.__speed = speed[0]
        self.__angle_step = (angle[1] - angle[0]) / 100
        self.__angular_momentum = angle[0]
        self.__angle = randint(0, 360)
        self.__fade = fade
        self.__img = img
        if fade:
            self.__img.set_colorkey(Var.COLOR_KEY)
        self.__frame = self.__img.get_rect()
        self.__disappear = disappear
        self.rotated = p.transform.rotate(self.__img, self.__angle)

    def render(self, s):
        self.rotated = p.transform.rotate(self.__img, self.__angle)
        self.__frame = self.rotated.get_rect()
        self.__frame.center = self.__x1 - Var.offset_x, self.__y1 - Var.offset_y
        if self.__fade:
            if self.__timeleft < 1:
                Gameobj.particles_over.remove(self)
            alpha = (self.__timeleft / (self.lifespan / 2) - 1) * 254
            self.rotated.set_alpha(alpha)
        s.blit(self.rotated, self.__frame)

    def update(self, delta):
        self.__timeleft -= delta
        self.__angle += self.__angle_step * delta
        self.__speed += self.__speed_step * delta
        vect = p.math.Vector2(self.__vect.x, self.__vect.y)
        vect.scale_to_length(self.__speed * delta)
        self.__x1 += vect.x
        self.__y1 += vect.y
        if not self.__fade:
            if self.__timeleft < 1:
                if self.__disappear:
                    Gameobj.particles_over.remove(self)
                else:
                    self.__frame.center = self.__x1, self.__y1
                    Var.level_background.blit(self.rotated, self.__frame)
                    Gameobj.particles_below.remove(self)


class Item(object):
    img_weaponground = None

    def __init__(self, x, y, img, action):
        self.x = x
        self.y = y
        self.img = img
        self.action = action
        self.__frame = self.img.get_rect()
        self.size = (self.__frame.width / 2) ** 2
        self.__frame.center = self.x, self.y

    def check_collision(self, x, y, range):
        distance = (x - self.x) ** 2 + (y - self.y) ** 2
        if distance < self.size + range:
            self.action()
            Gameobj.items.remove(self)

    def render(self, s):
        self.__frame.center = self.x - Var.offset_x, self.y - Var.offset_y
        s.blit(self.img, self.__frame)


def load_image_alpha(path):
    img = p.image.load(path)
    img = p.transform.smoothscale(img, (dppr2(img.get_width()), dppr2(img.get_height())))
    img = img.convert_alpha()
    return img


def load_image(path):
    img = p.image.load(path)
    img = p.transform.smoothscale(img, (dppr2(img.get_width()), dppr2(img.get_height())))
    img = img.convert()
    return img


def load_spritesheet(path, size, x, y):
    sheet = p.image.load(path)
    imgs = []
    size = dppr2(size)
    for i in range(y):
        for j in range(x):
            sheet.set_clip(p.Rect(j * size, i * size, size, size))
            img = sheet.subsurface(sheet.get_clip())
            img.convert()
            img.set_colorkey(Var.COLOR_KEY)
            imgs.append(img)
    return imgs


def load_spritesheet_alpha(path, size, x, y):
    sheet = load_image_alpha(path)
    imgs = []
    size = dppr2(size)
    for i in range(y):
        for j in range(x):
            sheet.set_clip(p.Rect(j * size, i * size, size, size))
            img = sheet.subsurface(sheet.get_clip())
            img.convert_alpha()
            imgs.append(img)
    return imgs


def offset():
    keskx = Var.SCREEN_WIDTH / 2
    kesky = Var.SCREEN_HEIGHT / 2
    newoffset_x = Gameobj.hero.x - keskx
    newoffset_y = Gameobj.hero.y - kesky
    if newoffset_x < Var.level_boundries[0]:
        newoffset_x = Var.level_boundries[0]
    elif newoffset_x > Var.level_boundries[1] - Var.SCREEN_WIDTH:
        newoffset_x = Var.level_boundries[1] - Var.SCREEN_WIDTH
    if newoffset_y < Var.level_boundries[2]:
        newoffset_y = Var.level_boundries[2]
    elif newoffset_y > Var.level_boundries[3] - Var.SCREEN_HEIGHT:
        newoffset_y = Var.level_boundries[3] - Var.SCREEN_HEIGHT
    Var.offset_x = newoffset_x
    Var.offset_y = newoffset_y


def udpp(x):
    return x / Var.dpp


def dpp(x):
    return x * Var.dpp


def dppr2(x):
    return round(x * Var.dpp2)


def dppr(x):
    return round(dpp(x))


# J2rgmine funktsioon on leitud sealt
# http://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment
def dist(x1, y1, x2, y2, x3, y3):  # x3,y3 is the point
    px = x2 - x1
    py = y2 - y1
    something = px * px + py * py
    u = ((x3 - x1) * px + (y3 - y1) * py) / float(something)
    if u > 1:
        u = 1
    elif u < 0:
        u = 0
    x = x1 + u * px
    y = y1 + u * py
    dx = x - x3
    dy = y - y3
    distance = dx * dx + dy * dy
    return distance


p.display.set_caption(Var.CAPTION[Var.language_id])
screen_surface = None
