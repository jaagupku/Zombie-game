import core


def draw_healthbar(s, x, y, width, height, currenthp, maxhp):
    x, y = core.dpp(x), core.dpp(y)
    width = core.dpp(width)
    height = core.dpp(height)
    healthbar_green = [x, y, currenthp/maxhp*width, height]
    healthbar_red = [x, y, width, height]
    core.p.draw.rect(s, core.Var.RED_HEALTHBAR, healthbar_red)
    if currenthp != 0:
        core.p.draw.rect(s, core.Var.GREEN_HEALTHBAR, healthbar_green)
    core.p.draw.rect(s, core.Var.BLACK, healthbar_red, core.dppr(1))


def draw_ammo(s, x, y, in_clip, on_hero):
    x, y = core.dpp(x), core.dpp(y)
    x1 = x+core.dpp(48)
    y1 = y-core.dpp(95)
    width = core.dpp(20)
    height1 = core.dpp(85)
    if core.Gameobj.guns[core.Gameobj.hero.current_gun].reload_bool:
        height2 = round(height1 * core.Gameobj.guns[core.Gameobj.hero.current_gun].reload_delta/core.Gameobj.guns[core.Gameobj.hero.current_gun].reload_time)
    else:
        height2 = round(height1 * core.Gameobj.guns[core.Gameobj.hero.current_gun].clip/core.Gameobj.guns[core.Gameobj.hero.current_gun].clip_size)
    rect1 = core.p.Rect(x1, y1, width, height1)
    rect2 = core.p.Rect(x1, y1+height1-height2+core.dpp(1), width, height2-core.dpp(2))
    if in_clip == -1:
        text = "-"
    else:
        text = str(in_clip)
    text += "/"
    if on_hero == -1:
        text += "-"
    else:
        text += str(on_hero)
    img_text = core.Var.font_ammo.render(text, core.Var.aa_text, core.Var.YELLOW_BULLET)
    frame_text = img_text.get_rect()
    frame_text.midtop = (x+core.dpp(37)), y
    s.blit(img_text, frame_text)
    core.p.draw.rect(s, core.Var.BULLET_BAR_DARK, rect1)
    if height2 > 0:
        core.p.draw.rect(s, core.Var.BULLET_BAR_LIGHT, rect2)
    core.p.draw.rect(s, core.Var.BLACK, rect1, core.dppr(1))
    frame_wep = core.Item.img_weaponground[core.Gameobj.hero.current_gun].get_rect()
    frame_wep.topright = x-core.dpp(5), y-core.dpp(8)
    s.blit(core.Item.img_weaponground[core.Gameobj.hero.current_gun], frame_wep)


def draw_fps_counter(s, x, y, fps):
    x, y = core.dpp(x), core.dpp(y)
    core.p.draw.rect(s, core.Var.BLACK, [x, y, core.dpp(95), core.dpp(28)])
    img_text = core.Var.font_button.render("FPS: " + str(round(fps)), core.Var.aa_text, core.Var.WHITE)
    s.blit(img_text, (x, y))


def draw_score(s, x, y):
    img = core.Var.font_ammo.render(core.Var.str_scoreboard[core.Var.language_id][2]+": "+str(core.Var.score),
                                    core.Var.aa_text, core.Var.WHITE)
    s.blit(img, (x, y))
