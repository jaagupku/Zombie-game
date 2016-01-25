import core
import core.widgets
import core.readwrite


class Pausemenu(core.Screen):
    def __init__(self):
        core.Screen.__init__(self, 3)
        self.buttons = []
        self.message_ask = None
        self.message_exit = None
        self.message_save = None
        self.surf = None

    def on_start(self):
        self.buttons.clear()
        self.surf = core.p.Surface((core.Var.SCREEN_WIDTH, core.Var.SCREEN_HEIGHT))
        self.surf.fill(core.Var.BLACK)
        self.surf.set_alpha(150)
        commands = (self.continue_game, self.save_game, self.load_game, self.main_menu, self.exit)
        for i in range(len(core.Var.str_pausemenu)):
            self.buttons.append(core.widgets.Button(core.Var.str_pausemenu[i][core.Var.language_id],
                                                    self.surf.get_width() / 2 - core.widgets.Button.width / 2,
                                                    self.surf.get_height() / 2 + (
                                                    i - len(core.Var.str_pausemenu) // 2) * core.widgets.Button.height,
                                                    commands[i]))

    def render(self, s):
        s.blit(core.Var.previous_screen_surface, (0, 0))
        s.blit(self.surf, (0, 0))
        for button in self.buttons:
            button.render(s)
        if self.message_ask is not None:
            self.message_ask.render(s)
        elif self.message_exit is not None:
            self.message_exit.render(s)
        elif self.message_save is not None:
            self.message_save.render(s)

    def update(self, delta):
        if self.message_ask is None and self.message_exit is None and self.message_save is None:
            for button in self.buttons:
                button.check_click()
        elif self.message_ask is not None:
            self.message_ask.update(delta)
            if self.message_ask.value is not None:
                if self.message_ask.value:
                    core.Var.new_screen = 1
                    core.Var.current_game = [False, -1]
                self.message_ask = None
        elif self.message_save is not None:
            self.message_save.update(delta)
            if self.message_save.value is not None:
                if self.message_save.value:
                    core.readwrite.save_game()
                self.message_save = None
        else:
            self.message_exit.update(delta)
            if self.message_exit.value is not None:
                if self.message_exit.value:
                    core.readwrite.write_scores()
                    core.Var.exit = True
                self.message_exit = None

    def on_pause(self):
        self.message_ask = None
        self.message_exit = None

    def on_stop(self):
        pass

    def on_resume(self):
        core.Var.fps_current = 1

    def continue_game(self):
        core.Var.new_screen = core.Var.current_game[1]

    def save_game(self):
        self.message_save = core.widgets.MessageConfirm(core.Var.str_save_message[core.Var.language_id],
                                                        core.Var.str_are_you_sure[core.Var.language_id])

    def load_game(self):
        core.readwrite.load_game()

    def main_menu(self):
        self.message_ask = core.widgets.MessageConfirm(core.Var.str_exit_game_message[core.Var.language_id],
                                                       core.Var.str_are_you_sure[core.Var.language_id])

    def exit(self):
        self.message_exit = core.widgets.MessageConfirm(core.Var.str_exit_all_message[core.Var.language_id],
                                                        core.Var.str_are_you_sure_exit[core.Var.language_id])


class Quitmessage(core.Screen):
    def __init__(self):
        core.Screen.__init__(self, 4)
        self.message_ask = None
        self.surf = None

    def render(self, s):
        s.blit(core.Var.previous_screen_surface, (0, 0))
        s.blit(self.surf, (0, 0))
        self.message_ask.render(s)

    def on_start(self):
        self.surf = core.p.Surface((core.Var.SCREEN_WIDTH, core.Var.SCREEN_HEIGHT))
        self.surf.fill(core.Var.BLACK)
        self.surf.set_alpha(150)
        self.message_ask = core.widgets.MessageConfirm(core.Var.str_exit_all_message[core.Var.language_id],
                                                       core.Var.str_are_you_sure_exit[core.Var.language_id])

    def on_stop(self):
        pass

    def on_resume(self):
        core.Var.fps_current = 1

    def update(self, delta):
        self.message_ask.update(delta)
        if self.message_ask.value is not None:
            if self.message_ask.value:
                core.readwrite.write_scores()
                core.Var.exit = True
            else:
                core.Var.new_screen = core.Var.previous_screen

    def on_pause(self):
        self.message_ask.value = None
