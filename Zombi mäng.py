import core
import core.readwrite
import core.uielements
import screens

core.readwrite.load_settings()
# core.readwrite.write_scores()
core.readwrite.load_scores()
core.Var.set_volume()
core.Var.init_menu_colors()
screens_list = (screens.survivalmode.Survivalmode(), screens.menu.Menu(), screens.menu.Settings(),
                screens.escmenu.Pausemenu(), screens.escmenu.Quitmessage(), screens.menu.Scoreboard(),
                screens.menu.Help())
delta = 20
core.p.mixer.music.play(loops=-1)
# MAIN LOOP
while True:
    if core.Var.exit:
        break
    if core.Var.new_screen != core.Var.current_screen:
        core.Var.previous_screen = core.Var.current_screen
        if core.Var.counter != 0:
            core.Var.previous_screen_surface = core.p.Surface((core.Var.SCREEN_WIDTH, core.Var.SCREEN_HEIGHT))
            if core.Var.previous_screen != 4:
                screens_list[core.Var.previous_screen].render(core.Var.previous_screen_surface)
            screens_list[core.Var.previous_screen].on_pause()
        if core.Var.stop_screen:
            screens_list[core.Var.previous_screen].on_stop()
            core.Var.stop_screen = False
        if core.Var.start_screen:
            screens_list[core.Var.new_screen].on_start()
            core.Var.start_screen = False
        screens_list[core.Var.new_screen].on_resume()
        core.Var.current_screen = core.Var.new_screen

    event = core.p.event.get()
    core.Inputhandler.handle(event)
    screens_list[core.Var.current_screen].update(delta)
    screens_list[core.Var.current_screen].render(core.screen_surface)
    if core.Var.show_fps:
        core.uielements.draw_fps_counter(core.screen_surface, 5, 5, core.Var.clock.get_fps())
    core.p.display.flip()
    core.Var.counter += 1
    delta = core.Var.clock.tick(core.Var.fps[core.Var.fps_current])
    if delta < 1:
        delta = 1
    elif delta > 50:
        delta = 50

core.p.quit()
