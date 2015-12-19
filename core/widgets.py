import core

key = core.Inputhandler


class Widget(object):
    def_height = 23

    def __init__(self, x, y, width, height, command, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.command = command
        self.text = text
        self.frame = core.p.Rect((self.x, self.y), (self.width, self.height))
        self.img_text = core.Var.font_tiny.render(text, True, core.Var.BLACK)
        self.frame_text = self.img_text.get_rect()
        self.frame_text.right = self.x - self.width + self.frame_text.width
        self.frame_text.centery = self.frame.centery
        self.mouse_pressed_on_this = False

    def render(self, s):
        raise NotImplementedError

    def check_click(self):
        raise NotImplementedError

    def check_for_press(self):
        if key.mouse_buttons_pressed[0] and self.frame.collidepoint(key.x_mouse, key.y_mouse):
            self.mouse_pressed_on_this = True

    def check_for_release(self):
        if key.mouse_buttons_released[0]:
            self.mouse_pressed_on_this = False


class Button(Widget):
    width = 160
    height = 32

    @staticmethod
    def load_resources():
        Button.width = core.dpp(160)
        Button.height = core.dpp(32)

    def __init__(self, text, x, y, command, big=True, disabled=False):
        Widget.__init__(self, x, y, Button.width, Button.height - core.dpp(2), command, text)
        if big:
            self.img_text = core.Var.font_button.render(text, True, core.Var.BLACK)
        else:
            self.img_text = core.Var.font_tiny.render(text, True, core.Var.BLACK)
        self.frame_text = self.img_text.get_rect()
        self.frame_text.center = self.frame.center
        self.disabled = disabled
        self.__color_main = core.Var.THEME_DEFAULT

    def render(self, s):
        core.p.draw.rect(s, self.__color_main, self.frame)
        s.blit(self.img_text, self.frame_text)

    def check_click(self):
        self.check_for_press()
        if self.disabled:
            self.__color_main = core.Var.THEME_LIGHT
        elif self.frame.collidepoint(key.x_mouse, key.y_mouse):
            if not key.mouse_buttons_down[0]:
                self.__color_main = core.Var.THEME_HOVER
            else:
                self.__color_main = core.Var.THEME_DOWN
        else:
            self.__color_main = core.Var.THEME_DEFAULT
        if key.mouse_buttons_released[
            0] and self.mouse_pressed_on_this and not self.disabled and self.frame.collidepoint(key.x_mouse,
                                                                                                key.y_mouse):
            self.command()
        self.check_for_release()


class Checkbox(Widget):
    def __init__(self, x, y, command, text=""):
        Widget.__init__(self, x, y, core.dpp(Widget.def_height), core.dpp(Widget.def_height), command, text)
        self.ticked = False
        self.frame_text.left -= core.dpp(150 - Widget.def_height)
        self.__line_thickness = round(self.width / 9)
        self.__check_pointlist = [(self.x + self.width - self.width / 7, self.y + self.height / 8),
                                  (self.x + self.width / 4, self.y + self.height - self.height / 9),
                                  (self.x + self.width / 9, self.y + self.height / 2.5)]
        self.__color_main = core.Var.THEME_DEFAULT

    def render(self, s):
        core.screen_surface.blit(self.img_text, self.frame_text)
        core.p.draw.rect(s, self.__color_main, self.frame)
        if self.ticked:
            core.p.draw.lines(s, core.Var.THEME_LIGHT, False, self.__check_pointlist, self.__line_thickness)

    def check_click(self):
        self.check_for_press()
        if self.frame.collidepoint(key.x_mouse, key.y_mouse):
            self.__color_main = core.Var.THEME_HOVER
            if key.mouse_buttons_down[0]:
                self.__color_main = core.Var.THEME_DOWN
            else:
                self.__color_main = core.Var.THEME_HOVER
            if key.mouse_buttons_released[0] and self.mouse_pressed_on_this:
                self.ticked = not self.ticked
                self.command(self.ticked)
        else:
            self.__color_main = core.Var.THEME_DEFAULT
        self.check_for_release()


class Cyclebutton(Widget):
    def __init__(self, x, y, width, command, items, text=""):
        if width < core.dpp(45):
            width = core.dpp(45)
        Widget.__init__(self, x, y, width, core.dpp(Widget.def_height), command, text)
        self.items = items
        self.selected_item = 0
        self.__frame_left = core.p.Rect((self.x, self.y), (core.dpp(Widget.def_height), self.height))
        self.__frame_right = core.p.Rect((self.frame.right - core.dpp(Widget.def_height), self.y),
                                         (core.dpp(Widget.def_height) + 1, self.height))
        self.__frame_mid = core.p.Rect(self.__frame_left.topright, (
            self.frame.width - self.__frame_left.width - self.__frame_right.width, self.height))
        self.__img_text_selected = core.Var.font_tiny.render(self.items[self.selected_item], True, core.Var.BLACK)
        self.__frame_text_selected = self.__img_text_selected.get_rect()
        self.__frame_text_selected.center = self.frame.center
        self.__arrow_size = core.dpp(5.3)  # bigger the number, smaller the arrow
        self.__left_arrow = [(self.__frame_left.left + self.__arrow_size * 1.1, self.__frame_left.centery),
                             (self.__frame_left.right - self.__arrow_size, self.__frame_left.top + self.__arrow_size),
                             (
                                 self.__frame_left.right - self.__arrow_size,
                                 self.__frame_left.bottom - self.__arrow_size)]
        self.__right_arrow = [(self.__frame_right.right - self.__arrow_size * 1.1, self.__frame_right.centery),
                              (self.__frame_right.left + self.__arrow_size, self.__frame_right.top + self.__arrow_size),
                              (self.__frame_right.left + self.__arrow_size,
                               self.__frame_right.bottom - self.__arrow_size)]

    def set_item(self, id_item):
        self.selected_item = id_item
        self.__img_text_selected = core.Var.font_tiny.render(self.items[id_item], True, core.Var.BLACK)
        self.__frame_text_selected = self.__img_text_selected.get_rect()
        self.__frame_text_selected.center = self.frame.center

    def render(self, s):
        if self.__frame_mid.collidepoint(key.x_mouse, key.y_mouse):
            core.p.draw.rect(s, core.Var.THEME_HOVER, self.__frame_mid)
        else:
            core.p.draw.rect(s, core.Var.THEME_DEFAULT, self.__frame_mid)
        if self.__frame_left.collidepoint(key.x_mouse, key.y_mouse):
            core.p.draw.rect(s, core.Var.THEME_HOVER, self.__frame_left)
        else:
            core.p.draw.rect(s, core.Var.THEME_DOWN, self.__frame_left)
        if self.__frame_right.collidepoint(key.x_mouse, key.y_mouse):
            core.p.draw.rect(s, core.Var.THEME_HOVER, self.__frame_right)
        else:
            core.p.draw.rect(s, core.Var.THEME_DOWN, self.__frame_right)
        core.p.draw.polygon(s, core.Var.THEME_LIGHT, self.__left_arrow)
        core.p.draw.polygon(s, core.Var.THEME_LIGHT, self.__right_arrow)
        s.blit(self.img_text, self.frame_text)
        s.blit(self.__img_text_selected, self.__frame_text_selected)

    def check_click(self):
        self.check_for_press()
        if key.mouse_buttons_released[0] and self.mouse_pressed_on_this:
            if self.__frame_left.collidepoint(key.x_mouse, key.y_mouse):
                item_id = self.selected_item - 1
                if item_id < 0:
                    item_id = len(self.items) - 1
                self.set_item(item_id)
                self.command(item_id)
            elif self.__frame_right.collidepoint(key.x_mouse, key.y_mouse):
                item_id = self.selected_item + 1
                if item_id >= len(self.items):
                    item_id = 0
                self.set_item(item_id)
                self.command(item_id)
        self.check_for_release()


class Slider(Widget):
    def __init__(self, x, y, width, command, text=""):
        Widget.__init__(self, x, y, width - core.dpp(40), core.dpp(Widget.def_height), command, text)
        self.frame_text.left -= core.dpp(40)
        self.__circle_radius = core.dppr(8)
        self.__line_width = core.dppr(5)
        self.__anotherpoint = (0, 0)
        self.value = 0
        self.__color_hover = core.Var.THEME_DEFAULT
        self.__change_value = False
        self.__img_value = core.Var.font_tiny.render(": {:3d}".format(self.value), True, core.Var.BLACK)
        self.__frame_value = self.__img_value.get_rect()
        self.__frame_value_back = core.p.Rect((0, 0), (width - self.width - core.dpp(13), self.height - core.dpp(4)))
        self.__frame_value_back.midleft = self.frame.midright
        self.__frame_value_back.left += core.dpp(13)
        self.__frame1 = core.p.Rect((self.x-self.__circle_radius*2, self.y), (self.width+self.__circle_radius*4,
                                                                              self.height))

    def render(self, s):
        core.p.draw.rect(s, core.Var.THEME_LIGHT, self.__frame_value_back)
        s.blit(self.img_text, self.frame_text)
        s.blit(self.__img_value, self.__frame_value)
        core.p.draw.line(s, core.Var.THEME_DOWN, self.frame.midleft, self.frame.midright, self.__line_width)
        core.p.draw.line(s, core.Var.THEME_LIGHT, self.frame.midleft, self.__anotherpoint, self.__line_width)
        core.p.draw.circle(s, self.__color_hover, self.__anotherpoint, self.__circle_radius)

    def check_for_press(self):
        if key.mouse_buttons_pressed[0] and self.__frame1.collidepoint(key.x_mouse, key.y_mouse):
            self.mouse_pressed_on_this = True

    def check_click(self):
        self.check_for_press()
        if (self.__anotherpoint[0] - key.x_mouse) ** 2 + (
                    self.__anotherpoint[1] - key.y_mouse) ** 2 < self.__circle_radius ** 2:
            self.__color_hover = core.Var.THEME_HOVER
            if key.mouse_buttons_pressed[0]:
                self.__change_value = True
        else:
            self.__color_hover = core.Var.THEME_DEFAULT
        if self.__change_value:
            self.set_value((key.x_mouse - self.x) / self.width * 100)
        if key.mouse_buttons_released[0] and self.__change_value and self.mouse_pressed_on_this:
            self.__change_value = False
            self.command(self.value)
        self.check_for_release()

    def set_value(self, v):
        if v < 0:
            v = 0
        elif v > 100:
            v = 100
        self.value = round(v)
        self.__img_value = core.Var.font_tiny.render(str(self.value), True, core.Var.BLACK)
        self.__frame_value = self.__img_value.get_rect()
        self.__frame_value.midright = self.frame.midright
        self.__frame_value.left += core.dpp(39)
        self.__anotherpoint = (round(self.x + v / 100 * self.width), round(self.frame.centery))


class Keybind(Widget):
    def __init__(self, x, y, width, command, action, value, text=""):
        Widget.__init__(self, x, y, width, core.dpp(Widget.def_height), command, text)
        self.action = action
        self.value = value
        self.__color_main = core.Var.THEME_DEFAULT
        self.__change_value = False
        if value != -1:
            self.__value_text = core.p.key.name(value).upper()
        else:
            self.__value_text = " "
        self.__img_value = core.Var.font_tiny.render(self.__value_text, True, core.Var.BLACK)
        self.__frame_value = self.__img_value.get_rect()
        self.__frame_value.center = self.frame.center
        self.__c = 0

    def render(self, s):
        s.blit(self.img_text, self.frame_text)
        core.p.draw.rect(s, self.__color_main, self.frame)
        s.blit(self.__img_value, self.__frame_value)

    def check_click(self):
        self.check_for_press()

        if self.frame.collidepoint(key.x_mouse, key.y_mouse):
            if key.mouse_buttons_down[0]:
                self.__color_main = core.Var.THEME_DOWN
            else:
                self.__color_main = core.Var.THEME_HOVER
            if self.mouse_pressed_on_this and key.mouse_buttons_released[0]:
                self.__change_value = True
                self.__c = core.Var.counter
        else:
            self.__color_main = core.Var.THEME_DEFAULT

        if self.__change_value:
            self.__color_main = core.Var.THEME_LIGHT
            if key.escape_pressed or (True in key.mouse_buttons_pressed and self.__c != core.Var.counter):
                self.__change_value = False
            else:
                v = None
                for i in core.Inputhandler.all_events:
                    if i.type == core.p.KEYDOWN:
                        v = i.key
                if v is not None:
                    self.set_value(v)
                    self.command(self.action, self.value)
                    self.__change_value = False
        self.check_for_release()

    def set_value(self, v):
        if v != -1:
            self.value = v
            self.__value_text = core.p.key.name(v).upper()
            self.__img_value = core.Var.font_tiny.render(self.__value_text, True, core.Var.BLACK)
            self.__frame_value = self.__img_value.get_rect()
            self.__frame_value.center = self.frame.center
        else:
            self.value = v
            self.__value_text = " "
            self.__img_value = core.Var.font_tiny.render(self.__value_text, True, core.Var.BLACK)
            self.__frame_value = self.__img_value.get_rect()
            self.__frame_value.center = self.frame.center


class Label(Widget):
    def __init__(self, x, y, width, text, fontsize):
        Widget.__init__(self, x, y, width, core.dpp(fontsize), None, text)
        font = core.p.font.SysFont("Verdana", core.dppr(fontsize))
        self.img_text = font.render(text, True, core.Var.BLACK)
        self.frame_text.center = x, y

    def render(self, s):
        s.blit(self.img_text, self.frame_text)

    def check_click(self):
        pass


class Textfield(Widget):
    def __init__(self, x, y, width, command, text, maxlen):
        Widget.__init__(self, x, y, width, core.dpp(Widget.def_height), command, text)
        self.value = ""
        self.__img_value = core.Var.font_tiny.render(self.value, True, core.Var.BLACK)
        self.__frame_value = self.__img_value.get_rect()
        self.__frame_value.midleft = self.frame.midleft
        self.__color_main = core.Var.THEME_DEFAULT
        self.__blink_time = 0.8
        self.__previous_blink = core.time()
        self.__blink = False
        self.__change_value = False
        self.__c = 0
        self.maxlen = maxlen

    def render(self, s):
        s.blit(self.img_text, self.frame_text)
        core.p.draw.rect(s, self.__color_main, self.frame)
        s.blit(self.__img_value, self.__frame_value)
        if self.__blink:
            core.p.draw.line(s, core.Var.BLACK, self.__frame_value.topright, self.__frame_value.bottomright,
                             core.dppr(2))

    def check_click(self):
        self.check_for_press()
        t = core.time()

        if self.frame.collidepoint(key.x_mouse, key.y_mouse):
            if key.mouse_buttons_down[0]:
                self.__color_main = core.Var.THEME_DOWN
            else:
                self.__color_main = core.Var.THEME_HOVER
            if self.mouse_pressed_on_this and key.mouse_buttons_released[0]:
                self.__change_value = True
                self.__c = core.Var.counter
        else:
            if key.mouse_buttons_pressed[0]:
                self.__change_value = False
            self.__color_main = core.Var.THEME_DEFAULT
        if self.__change_value:
            if t - self.__previous_blink > self.__blink_time:
                self.__previous_blink = t
                self.__blink = not self.__blink
            for i in core.Inputhandler.all_events:
                if i.type == core.p.KEYDOWN:
                    if i.key == core.p.K_BACKSPACE:
                        self.value = self.value[:-1]
                    elif i.key == core.p.K_RETURN:
                        self.command()
                    elif i.key <= 127 and core.Var.font_tiny.size(self.value)[0] <= self.width*.93:
                        if core.p.key.get_mods() & core.p.KMOD_SHIFT:
                            self.value += chr(i.key).upper()
                        else:
                            self.value += chr(i.key)
            self.change_value()
        else:
            self.__blink = False
        self.check_for_release()

    def change_value(self):
        self.__img_value = core.Var.font_tiny.render(self.value, True, core.Var.BLACK)
        self.__frame_value = self.__img_value.get_rect()
        self.__frame_value.midleft = self.frame.midleft
        self.__frame_value.left = self.frame.left + core.dpp(3)


class WallofText(Widget):
    def __init__(self, x, y, width, height, text, fontsize=14):
        Widget.__init__(self, x, y, width, height, None, text)
        self.__textsurface = core.p.Surface((width, height), flags=core.p.SRCALPHA)
        font = core.p.font.SysFont("Verdana", core.dppr(fontsize))
        line_spacing = font.size("A")[1]+core.dpp(4)
        data = text.split("\\n")
        line = ""
        y = self.y
        for paragraph in data:
            wordlist = paragraph.split()
            for nr in range(len(wordlist)):
                if font.size(wordlist[nr]+line)[0] < self.width - font.size(wordlist[nr])[0]*3 and nr+1 < len(wordlist):
                    line += " "+wordlist[nr]
                else:
                    line += " "+wordlist[nr]
                    self.__textsurface.blit(font.render(line, True, core.Var.BLACK), (self.x, y))
                    y += line_spacing
                    line = ""
            y += line_spacing


    def render(self, s):
        s.blit(self.__textsurface, (self.x, self.y))

    def check_click(self):
        pass


class Message(object):
    def __init__(self, message):
        self.img_message = []
        self.frame_message = []
        self.message = message
        self.frame = None
        self.linesize = core.Var.font_tiny.get_linesize()
        self.linesize = core.Var.font_tiny.get_linesize() + core.dpp(2)
        longest_line = 0
        for i in self.message:
            img = core.Var.font_tiny.render(i, True, core.Var.BLACK)
            self.img_message.append(img)
            self.frame_message.append(img.get_rect())
            if img.get_width() > longest_line:
                longest_line = img.get_width()
        box_width = longest_line + core.dpp(90)
        box_height = len(self.message) * self.linesize + core.dpp(80)
        self.frame = core.p.Rect((core.Var.SCREEN_WIDTH - box_width) / 2, (core.Var.SCREEN_HEIGHT - box_height) / 2,
                                 box_width, box_height)
        for i in range(len(self.frame_message)):
            self.frame_message[i].x = self.frame.x + core.dpp(40)
            self.frame_message[i].y = self.frame.y + core.dpp(22) + i * self.linesize

    def render(self, s):
        raise NotImplementedError

    def update(self, delta):
        raise NotImplementedError


class MessageConfirm(Message):
    def __init__(self, message, buttonstext):
        Message.__init__(self, message)
        self.buttonstext = buttonstext

        self.ok_button = Button(self.buttonstext[0], self.frame.left + core.dpp(15),
                                self.frame.bottom - core.dpp(41), self.accepted, big=False)
        self.ok_button.frame.width = self.ok_button.frame_text.width + core.dpp(15)
        self.ok_button.frame_text.center = self.ok_button.frame.center
        self.cancel_button = Button(self.buttonstext[1], 0,
                                    self.frame.bottom - core.dpp(41), self.canceled, big=False)
        self.cancel_button.frame.width = self.cancel_button.frame_text.width + core.dpp(15)
        self.cancel_button.frame.x = self.frame.right - core.dpp(15) - self.cancel_button.frame.width
        self.cancel_button.frame_text.center = self.cancel_button.frame.center
        self.value = None

    def render(self, s):
        core.p.draw.rect(s, core.Var.THEME_BACKGROUND, self.frame)
        for i in range(len(self.img_message)):
            s.blit(self.img_message[i], self.frame_message[i])
        self.ok_button.render(s)
        self.cancel_button.render(s)

    def update(self, delta):
        self.ok_button.check_click()
        self.cancel_button.check_click()

    def accepted(self):
        self.value = True

    def canceled(self):
        self.value = False


class MessageInput(Message):
    def __init__(self, message):
        Message.__init__(self, message)
        self.ok_button = Button("Ok", self.frame.centerx,
                                self.frame.bottom - core.dpp(41), self.set_value, big=False)
        self.ok_button.frame.width = self.ok_button.frame_text.width + core.dpp(15)
        self.ok_button.frame.centerx = self.frame.centerx
        self.ok_button.frame_text.center = self.ok_button.frame.center
        self.textfield = Textfield(self.frame.left + core.dpp(30), self.frame.centery + core.dpp(5), core.dpp(150),
                                   self.set_value, "", 18)
        self.value = None

    def update(self, delta):
        self.ok_button.check_click()
        self.textfield.check_click()

    def render(self, s):
        core.p.draw.rect(s, core.Var.THEME_BACKGROUND, self.frame)
        for i in range(len(self.img_message)):
            s.blit(self.img_message[i], self.frame_message[i])
        self.ok_button.render(s)
        self.textfield.render(s)

    def set_value(self):
        if len(self.textfield.value) > 0:
            self.value = self.textfield.value
