#!/usr/bin/env python
# -*- coding: utf-8 -*-
import core
import core.widgets
import core.readwrite


class Menu(core.Screen):
    menu_items = []
    img_background = None

    def __init__(self):
        core.Screen.__init__(self, 1)
        self.img_title = None
        self.frame_title = None
        self.menu_commands = (  # Menu.continue_game,
            self.load_game, self.new_game, self.score_board, self.settings,
            self.help, self.exit)

    def on_start(self):
        core.widgets.Button.load_resources()
        Menu.img_background = core.load_image(core.Var.path_background)
        self.img_title = core.Var.font_title.render(core.Var.CAPTION[core.Var.language_id].upper(), True,
                                                    core.Var.BLACK)
        self.frame_title = self.img_title.get_rect()
        self.frame_title.center = (core.Var.SCREEN_WIDTH / 3, core.dpp(130))
        Menu.menu_items.clear()
        for i in range(len(core.Var.str_mainmenu)):
            Menu.menu_items.append(core.widgets.Button(core.Var.str_mainmenu[i][core.Var.language_id],
                                                       core.Var.SCREEN_WIDTH / 3 - core.widgets.Button.width / 2,
                                                       core.dpp(220) + i * core.widgets.Button.height,
                                                       self.menu_commands[i]))
            # Menu.menu_items[0].disabled = not core.Var.current_game[0]

    def render(self, s):
        s.fill(core.Var.WHITE)
        s.blit(Menu.img_background, (0, 0))
        s.blit(self.img_title, self.frame_title)
        for i in self.menu_items:
            i.render(s)

    def update(self, delta):
        for i in self.menu_items:
            i.check_click()

    def on_resume(self):
        core.Var.fps_current = 1
        core.p.mixer.music.unpause()

    def on_pause(self):
        pass

    def on_stop(self):
        pass

    def new_game(self):
        core.Var.start_screen = True
        core.Var.new_screen = 0
        core.Var.current_game = [True, 0]
        Menu.menu_items[0].disabled = False

    # def continue_game():
    #    core.Var.new_screen = core.Var.current_game[1]

    def load_game(self):
        core.readwrite.load_game()

    def score_board(self):
        core.Var.start_screen = True
        core.Var.new_screen = 5

    def settings(self):
        core.Var.start_screen = True
        core.Var.new_screen = 2

    def help(self):
        core.Var.start_screen = True
        core.Var.new_screen = 6

    def exit(self):
        core.Var.new_screen = 4
        core.Var.start_screen = True


class Settings(core.Screen):
    def __init__(self):
        core.Screen.__init__(self, 2)
        self.widgets = set()
        self.widgets_game = set()
        self.widgets_controls = set()
        self.menu_button_x, self.menu_button_y = 15, 80
        self.subscreen_surface = None
        self.subscreen_frame = None
        self.settings_changed = False
        self.show_game = True
        self.show_controls = False

    def on_start(self):
        menu_x, menu_y = core.dpp(self.menu_button_x), core.dpp(self.menu_button_y)
        self.widgets = set()
        self.widgets_game = set()
        self.widgets_controls = set()
        self.show_game = True
        self.show_controls = False
        self.subscreen_surface = core.p.Surface(
                (core.Var.SCREEN_WIDTH - (menu_x + core.widgets.Button.width + core.dpp(20 + 15)),
                 core.Var.SCREEN_HEIGHT - core.dpp(15 * 2)))
        self.subscreen_surface.set_alpha(115)
        self.subscreen_surface.fill(core.Var.WHITE)
        self.subscreen_frame = self.subscreen_surface.get_rect()
        self.subscreen_frame.topleft = menu_x + core.widgets.Button.width + core.dpp(20), core.dpp(15)
        self.widgets.add(core.widgets.Button(core.Var.str_videoaudio[core.Var.language_id], menu_x,
                                             menu_y, self.show_video_settings))
        self.widgets.add(core.widgets.Button(core.Var.str_controls[core.Var.language_id], menu_x,
                                             menu_y + core.widgets.Button.height, self.show_control_settings))
        self.widgets.add(core.widgets.Button(core.Var.str_back[core.Var.language_id], menu_x,
                                             menu_y + core.widgets.Button.height * 2 + core.dpp(10), self.back))

        item_width = core.dpp(150)
        space_between_items = core.dpp(40)
        space_from_top = core.dpp(85)
        space_from_bottom = space_from_top / 5
        items_per_column = round(
                (self.subscreen_frame.height - space_from_top - space_from_bottom) / space_between_items)
        item_line_x = (
            self.subscreen_frame.left + item_width + core.dpp(20),
            self.subscreen_frame.left + item_width * 3 + core.dpp(44))
        item_line_y = (self.subscreen_frame.top + space_from_top,
                       self.subscreen_frame.top + space_from_top - items_per_column * space_between_items)

        # Add items to Game settings screen
        self.widgets_game.add(core.widgets.Label(item_line_x[len(self.widgets_game) // items_per_column],
                                                 item_line_y[len(self.widgets_game) // items_per_column] + len(
                                                         self.widgets_game) * space_between_items, item_width,
                                                 core.Var.str_video[core.Var.language_id], 16))
        resolutions = []
        for i in core.Var.resolutions:
            if i[0] > core.Var.display_info.current_w or i[1] > core.Var.display_info.current_h:
                continue
            str_res = str(i[0]) + "x" + str(i[1])
            resolutions.append(str_res)
        resolution_button = core.widgets.Cyclebutton(item_line_x[len(self.widgets_game) // items_per_column],
                                                     item_line_y[len(self.widgets_game) // items_per_column] + len(
                                                             self.widgets_game) * space_between_items, item_width,
                                                     self.select_resolution,
                                                     resolutions, core.Var.str_resolution[core.Var.language_id])
        resolution_button.set_item(core.Var.resolution_id)
        self.widgets_game.add(resolution_button)
        fpslimits = []
        for i in core.Var.fps:
            if i != 0:
                fpslimits.append(str(i))
            else:
                fpslimits.append(core.Var.str_fpslimit[1][core.Var.language_id])
        fpslimit_button = core.widgets.Cyclebutton(item_line_x[len(self.widgets_game) // items_per_column],
                                                   item_line_y[len(self.widgets_game) // items_per_column] + len(
                                                           self.widgets_game) * space_between_items, item_width,
                                                   self.select_fpslimit,
                                                   fpslimits, core.Var.str_fpslimit[0][core.Var.language_id])
        fpslimit_button.set_item(core.Var.fps_id)
        self.widgets_game.add(fpslimit_button)
        check_box_fullscreen = core.widgets.Checkbox(item_line_x[len(self.widgets_game) // items_per_column],
                                                     item_line_y[len(self.widgets_game) // items_per_column] + len(
                                                             self.widgets_game) * space_between_items,
                                                     self.change_fullscreen,
                                                     core.Var.str_fullscreen[core.Var.language_id])
        check_box_fullscreen.ticked = core.Var.is_fullscreen
        self.widgets_game.add(check_box_fullscreen)
        self.widgets_game.add(core.widgets.Label(item_line_x[len(self.widgets_game) // items_per_column],
                                                 item_line_y[len(self.widgets_game) // items_per_column] + len(
                                                         self.widgets_game) * space_between_items, item_width,
                                                 core.Var.str_game[core.Var.language_id], 16))
        language_button = core.widgets.Cyclebutton(item_line_x[len(self.widgets_game) // items_per_column],
                                                   item_line_y[len(self.widgets_game) // items_per_column] + len(
                                                           self.widgets_game) * space_between_items,
                                                   item_width, self.select_language, core.Var.languages,
                                                   core.Var.str_language[core.Var.language_id])
        language_button.set_item(core.Var.language_id)
        self.widgets_game.add(language_button)
        color_slider = core.widgets.Slider(item_line_x[len(self.widgets_game) // items_per_column],
                                           item_line_y[len(self.widgets_game) // items_per_column] + len(
                                                   self.widgets_game) * space_between_items,
                                           item_width, self.color_slider, core.Var.str_color[core.Var.language_id])
        color_slider.set_value(round(core.Var.default_hue / 3.6))
        self.widgets_game.add(color_slider)
        check_box_showfps = core.widgets.Checkbox(item_line_x[len(self.widgets_game) // items_per_column],
                                                  item_line_y[len(self.widgets_game) // items_per_column] + len(
                                                          self.widgets_game) * space_between_items,
                                                  self.change_showfps,
                                                  core.Var.str_showfps[core.Var.language_id])
        check_box_showfps.ticked = core.Var.show_fps
        self.widgets_game.add(check_box_showfps)
        self.widgets_game.add(core.widgets.Label(item_line_x[1],
                                                 item_line_y[0] + 0 * space_between_items, item_width,
                                                 core.Var.str_sound[core.Var.language_id], 16))
        master_slider = core.widgets.Slider(item_line_x[1],
                                            item_line_y[0] + 1 * space_between_items,
                                            item_width, self.master_slider,
                                            core.Var.str_volume[0][core.Var.language_id])
        master_slider.set_value(core.Var.volume[0])
        self.widgets_game.add(master_slider)
        music_slider = core.widgets.Slider(item_line_x[1],
                                           item_line_y[0] + 2 * space_between_items,
                                           item_width, self.music_slider, core.Var.str_volume[1][core.Var.language_id])
        music_slider.set_value(core.Var.volume[1])
        self.widgets_game.add(music_slider)
        sound_slider = core.widgets.Slider(item_line_x[1],
                                           item_line_y[0] + 3 * space_between_items,
                                           item_width, self.sound_slider, core.Var.str_volume[2][core.Var.language_id])
        sound_slider.set_value(core.Var.volume[2])
        self.widgets_game.add(sound_slider)

        self.widgets_game.add(
                core.widgets.Label(self.subscreen_frame.centerx, self.subscreen_frame.top + core.dpp(24), item_width,
                                   core.Var.str_videoaudio[core.Var.language_id], 24))

        # Add items to Controls screen
        for i in range(len(core.Var.key_binds)):
            self.widgets_controls.add(core.widgets.Keybind(item_line_x[len(self.widgets_controls) // items_per_column],
                                                           item_line_y[
                                                               len(self.widgets_controls) // items_per_column] + len(
                                                                   self.widgets_controls) * space_between_items,
                                                           item_width,
                                                           self.keybind, i, core.Var.key_binds[i],
                                                           core.Var.str_keybinds[i][core.Var.language_id]))
        self.widgets_controls.add(
                core.widgets.Label(self.subscreen_frame.centerx, self.subscreen_frame.top + core.dpp(24), item_width,
                                   core.Var.str_controls[core.Var.language_id], 24))

    def render(self, s):
        s.blit(Menu.img_background, (0, 0))
        s.blit(self.subscreen_surface, self.subscreen_frame)
        for widget in self.widgets:
            widget.render(s)
        if self.show_game:
            for widget in self.widgets_game:
                widget.render(s)
        elif self.show_controls:
            for widget in self.widgets_controls:
                widget.render(s)

    def update(self, delta):
        for widget in self.widgets:
            widget.check_click()
        if self.show_game:
            for widget in self.widgets_game:
                widget.check_click()
        elif self.show_controls:
            for widget in self.widgets_controls:
                widget.check_click()

    def on_resume(self):
        core.Var.fps_current = 1

    def on_pause(self):
        pass

    def on_stop(self):
        pass

    def back(self):
        core.Var.new_screen = 1
        if self.settings_changed:
            self.settings_changed = False
            core.readwrite.write_settings()
            core.Var.start_screen = True
            core.Var.stop_screen = True
            core.Var.current_game = [False, -1]
            core.Var.init_dpp_dependent()
            flag = (core.p.FULLSCREEN * core.Var.is_fullscreen) | core.p.HWSURFACE | core.p.DOUBLEBUF
            core.screen_surface = core.p.display.set_mode((core.Var.SCREEN_WIDTH, core.Var.SCREEN_HEIGHT), flag)

    def change_fullscreen(self, a):
        self.settings_changed = True
        core.Var.is_fullscreen = a

    def change_showfps(self, v):
        self.settings_changed = True
        core.Var.show_fps = v

    def master_slider(self, v):
        self.settings_changed = True
        core.Var.volume[0] = v
        core.Var.set_volume()

    def music_slider(self, v):
        self.settings_changed = True
        core.Var.volume[1] = v
        core.Var.set_volume()
        if v == 0:
            core.p.mixer.music.pause()
        else:
            core.p.mixer.music.unpause()

    def color_slider(self, v):
        if v >= 95:
            v = 94
        elif v <= 5:
            v = 6
        self.settings_changed = True
        core.Var.default_hue = v * 3.6
        core.Var.init_menu_colors()

    def sound_slider(self, v):
        self.settings_changed = True
        core.Var.volume[2] = v
        core.Var.set_volume()

    def keybind(self, action, key):
        self.settings_changed = True
        if key in core.Var.key_binds:
            core.Var.key_binds[core.Var.key_binds.index(key)] = -1
            for i in self.widgets_controls:
                if type(i) != core.widgets.Keybind:
                    continue
                if i.value == key and i.action != action:
                    i.set_value(-1)
        core.Inputhandler.reset_keys()
        core.Var.key_binds[action] = key

    def show_video_settings(self):
        self.show_game = True
        self.show_controls = False

    def show_control_settings(self):
        self.show_game = False
        self.show_controls = True

    def select_resolution(self, id_res):
        self.settings_changed = True
        core.Var.resolution_id = id_res
        core.Var.SCREEN_WIDTH = core.Var.resolutions[id_res][0]
        core.Var.SCREEN_HEIGHT = core.Var.resolutions[id_res][1]

    def select_language(self, id_lang):
        self.settings_changed = True
        core.Var.language_id = id_lang

    def select_fpslimit(self, id_fps):
        self.settings_changed = True
        core.Var.fps_id = id_fps


class Scoreboard(core.Screen):
    def __init__(self):
        core.Screen.__init__(self, 5)
        self.widgets = set()
        self.table_row_width = 0
        self.table_row_height = 0
        self.number_rows = 16
        self.columnlens = (0, 30, 170, 240, 300, 360, 405, 450)
        self.number_columns = len(self.columnlens)
        self.left = core.dpp(45)
        self.top = core.dpp(40)
        self.rows = []
        self.data = []

    def on_start(self):
        self.widgets = set()
        self.rows.clear()
        self.data.clear()
        self.left = core.dppr((800 - self.columnlens[-1]) / 2)
        self.top = core.dpp(40)
        self.table_row_width = core.dpp(self.columnlens[-1] + 1)
        self.table_row_height = round(core.Var.SCREEN_HEIGHT - 2 * self.top - core.widgets.Button.height)
        self.table_row_height /= self.number_rows
        self.table_row_height = round(self.table_row_height)
        menu_x, menu_y = core.Var.SCREEN_WIDTH / 2, core.Var.SCREEN_HEIGHT
        self.widgets.add(
                core.widgets.Button(core.Var.str_back[core.Var.language_id], menu_x - core.widgets.Button.width / 2,
                                    menu_y - core.widgets.Button.height - core.dpp(22), self.back))
        for i in range(self.number_rows):
            self.rows.append(core.p.Rect((self.left, self.top + i * self.table_row_height),
                                         (self.table_row_width, self.table_row_height)))
        data = [core.Var.str_scoreboard[core.Var.language_id]]
        for i in core.Var.scoreboard_data:
            data.append(i)
        item = []
        for i in data:
            for j in range(len(i)):
                item.clear()
                item.append(core.Var.font_tiny.render(i[j], True, core.Var.BLACK))
                item.append(item[0].get_rect())
                item[1].left = self.left + core.dppr(5 + self.columnlens[j])
                item[1].centery = self.rows[data.index(i)].centery
                self.data.append(item.copy())

    def render(self, s):
        s.blit(Menu.img_background, (0, 0))

        for row in self.rows:
            if row.collidepoint(core.Inputhandler.x_mouse, core.Inputhandler.y_mouse):
                color = core.Var.THEME_LIGHT
            else:
                color = core.Var.THEME_HOVER
            core.p.draw.rect(s, color, row)
            core.p.draw.line(s, core.Var.BLACK, (self.left, row.top),
                             (self.left + self.table_row_width, row.top), core.dppr(1.3))
        core.p.draw.line(s, core.Var.BLACK, (self.left, self.rows[-1].bottom),
                         (self.left + self.table_row_width, self.rows[-1].bottom), core.dppr(1.3))

        column = self.left
        core.p.draw.line(s, core.Var.BLACK, (column, self.top),
                         (column, self.top + self.number_rows * self.table_row_height), core.dppr(1.3))
        for i in range(self.number_columns):
            column = self.left + core.dppr(self.columnlens[i])
            core.p.draw.line(s, core.Var.BLACK, (column, self.top),
                             (column, self.top + self.number_rows * self.table_row_height), core.dppr(1.3))
        for i in range(len(self.data)):
            s.blit(self.data[i][0], self.data[i][1])

        for i in self.widgets:
            i.render(s)

    def update(self, delta):
        for i in self.widgets:
            i.check_click()

    def on_stop(self):
        pass

    def on_resume(self):
        core.Var.fps_current = 1

    def on_pause(self):
        pass

    def back(self):
        core.Var.new_screen = 1


class Help(core.Screen):
    def __init__(self):
        core.Screen.__init__(self, 6)
        self.widgets = []
        self.subscreen_surface = None
        self.subscreen_frame = None

    def on_start(self):
        self.widgets.clear()
        x, y = core.dpp(20), core.dpp(18)
        self.subscreen_surface = core.p.Surface(
                (core.Var.SCREEN_WIDTH - 2*x,
                 core.Var.SCREEN_HEIGHT - 2*y))
        self.subscreen_surface.set_alpha(115)
        self.subscreen_surface.fill(core.Var.WHITE)
        self.subscreen_frame = self.subscreen_surface.get_rect()
        self.subscreen_frame.topleft = x, y
        self.widgets.append(core.widgets.WallofText(x, 2*y, self.subscreen_frame.width, self.subscreen_frame.height,
                                                 core.Var.str_wallofhelp[core.Var.language_id]))
        self.widgets.append(core.widgets.Label(core.Var.SCREEN_WIDTH/2.05, x + core.dpp(10), core.dpp(150), core.Var.str_mainmenu[4][core.Var.language_id], 33))
        self.widgets.append(
                core.widgets.Button(core.Var.str_back[core.Var.language_id], core.Var.SCREEN_WIDTH/2 - core.widgets.Button.width / 2,
                                    core.Var.SCREEN_HEIGHT - core.widgets.Button.height - y - core.dpp(4), self.back))

    def render(self, s):
        s.blit(Menu.img_background, (0, 0))
        s.blit(self.subscreen_surface, self.subscreen_frame)
        for widget in self.widgets:
            widget.render(s)

    def update(self, delta):
        for widget in self.widgets:
            widget.check_click()

    def on_resume(self):
        pass

    def on_stop(self):
        pass

    def on_pause(self):
        pass

    def back(self):
        core.Var.new_screen = 1
