import pickle
import core
import core.player


# noinspection PyBroadException
def load_settings():
    data = load_file(core.Var.path_config)
    if data is not None:
        try:
            core.Var.ASPECT_RATIO = data["aspect_ratio"]
            core.Var.SCREEN_WIDTH = data["screen_width"]
            core.Var.SCREEN_HEIGHT = data["screen_height"]
            core.Var.resolution_id = data["resolution"]
            core.Var.is_fullscreen = data["fullscreen"]
            core.Var.language_id = data["language"]
            core.Var.fps_id = data["fps_limit"]
            core.Var.key_binds = data["key_binds"]
            core.Var.volume = data["volume"]
            core.Var.default_hue = data["color_hue"]
            core.Var.show_fps = data["showfps"]
        except:
            print("Failed to read some values.")
    else:
        print("No config file found, loaded default settings.")
    load_help_data()
    flag = (core.p.FULLSCREEN * core.Var.is_fullscreen) | core.p.HWSURFACE | core.p.DOUBLEBUF
    if core.Var.SCREEN_WIDTH > core.Var.display_info.current_w or core.Var.SCREEN_HEIGHT > core.Var.display_info.current_h:
        for i in core.Var.resolutions[:-1]:
            if i[0] <= core.Var.display_info.current_w and i[1] <= core.Var.display_info.current_h:
                core.Var.resolution_id = core.Var.resolutions.index(i)
                core.Var.SCREEN_WIDTH = i[0]
                core.Var.SCREEN_HEIGHT = i[1]
    core.Var.init_dpp_dependent()
    core.screen_surface = core.p.display.set_mode((core.Var.SCREEN_WIDTH, core.Var.SCREEN_HEIGHT), flag)


# noinspection PyBroadException
def write_settings():
    try:
        data = dict()
        data["aspect_ratio"] = core.Var.ASPECT_RATIO
        data["screen_width"] = core.Var.SCREEN_WIDTH
        data["screen_height"] = core.Var.SCREEN_HEIGHT
        data["fullscreen"] = core.Var.is_fullscreen
        data["resolution"] = core.Var.resolution_id
        data["language"] = core.Var.language_id
        data["fps_limit"] = core.Var.fps_id
        data["key_binds"] = core.Var.key_binds
        data["volume"] = core.Var.volume
        data["color_hue"] = core.Var.default_hue
        data["showfps"] = core.Var.show_fps
        write_file(core.Var.path_config, data)
    except:
        print("Failed to write settings to a file.")


# noinspection PyBroadException
def load_game():
    data = load_file(core.Var.path_survsave)
    save = []
    if data is not None:
        try:
            gameid = data["game_id"]
            if gameid == 0:
                core.Var.new_screen = gameid
                core.Var.start_screen = True
                core.Var.survival_wave = data["wave"]
                core.player.Hero.load_resources()
                core.Gameobj.hero = core.player.Hero(0, 0, core.Var.hero_max_health, core.Var.hero_speed)
                core.Gameobj.hero.x = core.Var.SCREEN_WIDTH / 2
                core.Gameobj.hero.y = core.Var.SCREEN_HEIGHT / 2
                core.Gameobj.hero.health = data["hero_health"]
                core.Gameobj.hero.guns = data["hero_weapons"]
                core.Gameobj.hero.ammo = data["hero_ammo"]
                score = data["score"]
                core.Var.score = score[0]
                core.Var.monsters_killed = score[1]
                core.Var.bullets_shot = score[2]
                core.Var.bullets_hit = score[3]
                core.Var.game_loaded = True
        except:
            print("Failed to read some values.")
    else:
        print("No savefile found.")
    if len(save):
        return [-1]
    else:
        return save


# noinspection PyBroadException
def save_game():
    try:
        data = dict()
        data["game_id"] = core.Var.current_game[1]
        if core.Var.current_game[1] == 0:
            data["wave"] = core.Var.survival_wave
        data["hero_health"] = core.Gameobj.hero.health
        data["hero_weapons"] = core.Gameobj.hero.guns
        data["hero_ammo"] = core.Gameobj.hero.ammo
        score = [core.Var.score, core.Var.monsters_killed, core.Var.bullets_shot, core.Var.bullets_hit]
        data["score"] = score
        if core.Var.current_game[1] == 0:
            path = core.Var.path_survsave
        else:
            path = None
        write_file(path, data)
        core.Var.game_saved = True
    except:
        print("Failed to save a game.")


def load_scores():
    data = load_file(core.Var.path_score)
    if data is not None:
        core.Var.scoreboard_data = eval(data)


def write_scores():
    write_file(core.Var.path_score, repr(core.Var.scoreboard_data))


def load_help_data():
    for language in ["ee", "en", "ru"]:
        file = open(core.os.path.join("data\\help", language+"_help.txt"), encoding="utf-8-sig")
        data = ""
        for line in file:
            data += line+"\\n"
        core.Var.str_wallofhelp.append(data)


# noinspection PyBroadException
def load_file(path):
    try:
        data = pickle.load(open(path, "rb"))
    except:
        print("Failed to read a file.")
        data = None
    return data


# noinspection PyBroadException
def write_file(path, data):
    try:
        pickle.dump(data, open(path, "wb+"))
    except:
        print("Error writing data to file.")
