import pygame
import random as rand
import time
from dict import *

# display res and clock speed
x_res, y_res = 1000, 600
clk = 10
noEnemy = 1

RGB_MODE = False


# owocek :D
class FoodColor:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue


class AngySzpider:
    def __init__(ble, posx, posy, r, g, b):
        ble.x = posx
        ble.y = posy
        ble.r = r
        ble.g = g
        ble.b = b


# initialization of screen parameters
def init(res_x, res_y):
    pygame.init()
    display = pygame.display.set_mode((res_x, res_y))
    pygame.display.update()
    running = True

    pygame.display.set_caption('Danger Noodle 2')

    return display, running


# checks snake head position relative to its food
def check_food(sx, sy, fx, fy, lgth, scr, isfit):
    if sx == fx and sy == fy:
        fx, fy = rand_pos()
        if not isfit:
            lgth += 1
            scr += 10 * clk // 5
        else:
            if lgth > 3:
                lgth -= 1
                snake_List.pop(lgth)
            scr -= 5 * clk // 5
        if RGB_MODE:
            scr += 69
        if not RGB_MODE:
            colors["snake_body"] = (rand.randint(0, 255), rand.randint(0, 255), rand.randint(0, 255))
    return fx, fy, lgth, scr


# updates the position of the snake
def pos_update(snake_x, snake_y, _x, _y):
    snake_x += _x
    snake_y += _y
    return snake_x, snake_y


# checks which direction the snake has to move
def keypress(key, curr_x, curr_y):
    _x = curr_x
    _y = curr_y
    global clk, RGB_MODE, noEnemy

    if key.key == pygame.K_LEFT and _x != dn_var["mv_tick"]:
        _x = -dn_var["mv_tick"]
        _y = 0
    elif key.key == pygame.K_RIGHT and _x != -dn_var["mv_tick"]:
        _x = dn_var["mv_tick"]
        _y = 0
    elif key.key == pygame.K_UP and _y != dn_var["mv_tick"]:
        _y = -dn_var["mv_tick"]
        _x = 0
    elif key.key == pygame.K_DOWN and _y != -dn_var["mv_tick"]:
        _y = dn_var["mv_tick"]
        _x = 0
    elif key.key == pygame.K_q:
        if colors["background"] == (255, 255, 255):
            colors["background"] = (0, 0, 0)
        else:
            colors["background"] = (255, 255, 255)
    elif key.key == pygame.K_p:
        if RGB_MODE:
            RGB_MODE = False
            colors["background"] = (0, 0, 0)
        else:
            RGB_MODE = True
    elif key.key == pygame.K_KP_PLUS and clk < 25:
        if clk == 1:
            clk = 5
        else:
            clk += 5
    elif key.key == pygame.K_KP_MINUS and clk > 0:
        if clk - 5 < 5:
            clk = 1
        else:
            clk -= 5
    elif key.key == pygame.K_KP_MINUS and clk > 0:
        if clk - 5 < 5:
            clk = 1
        else:
            clk -= 5
    elif key.key == pygame.K_z:
        if 0 <= noEnemy < 2:
            noEnemy += 1
    elif key.key == pygame.K_c:
        if 2 >= noEnemy > 0:
            noEnemy -= 1
    return _x, _y


# creates random starting direction
def rand_start():
    start_x, start_y = 0, 0
    i = rand.randint(0, 1)
    j = rand.randint(0, 1)

    if i == 1:

        if j == 1:
            start_x = dn_var["mv_tick"]
        else:
            start_x = -dn_var["mv_tick"]
    else:

        if j == 1:
            start_y = dn_var["mv_tick"]
        else:
            start_y = -dn_var["mv_tick"]

    return start_x, start_y


# determines random food position
def rand_pos():
    rx = round(rand.randrange(0, x_res - dn_var["width"]) / dn_var["fd_side"]) * dn_var["fd_side"]
    ry = round(rand.randrange(0, y_res - dn_var["height"]) / dn_var["fd_side"]) * dn_var["fd_side"]
    return rx, ry


# displays death message
def message(text, color, msg_x, msg_y):
    font_style = pygame.font.SysFont("arial.ttf", 40)
    msg = font_style.render(text, True, color)
    dis.blit(msg, [msg_x/2, msg_y/2])


# draw enemy
def spoder_draw(spoder, snake_x, snake_y, en_mv):
    if en_mv:
        spoder = spoder_move(spoder, snake_x, snake_y)
        en_mv = False
    else:
        en_mv = True
    pygame.draw.rect(dis, (spoder.r, spoder.g, spoder.b), [spoder.x, spoder.y,
                                                           en_var["fd_side"], en_var["fd_side"]])
    return en_mv


# move enemy
def spoder_move(spoder, snake_x, snake_y):
    if spoder.y - snake_y > 0:
        spoder.y -= dn_var["mv_tick"]
    elif spoder.y - snake_y < 0:
        spoder.y += dn_var["mv_tick"]
    elif spoder.x - snake_x > 0 and spoder.y - snake_y == 0:
        spoder.x -= dn_var["mv_tick"]
    elif spoder.x - snake_x < 0 and spoder.y - snake_y == 0:
        spoder.x += dn_var["mv_tick"]
    return spoder


# RGB
def draw_food(fd, fx, fy):
    global RGB_MODE

    if fd.red <= 255 and fd.blue == 0 and fd.green > 0:
        fd.red += 17
        fd.green -= 17
    elif fd.red > 0 and fd.blue <= 255 and fd.green == 0:
        fd.blue += 17
        fd.red -= 17
    elif fd.green <= 255 and fd.red == 0 and fd.blue > 0:
        fd.green += 17
        fd.blue -= 17

    if RGB_MODE:
        colors["snake_body"] = (fd.red, fd.green, fd.blue)
        colors["background"] = (fd.blue, fd.red, fd.green)
    pygame.draw.rect(dis, (fd.red, fd.blue, fd.green), [fx, fy, dn_var["fd_side"], dn_var["fd_side"]])


# RGB
def draw_fit_food(fd, fx, fy):
    global RGB_MODE

    if RGB_MODE:
        if fd.red <= 255 and fd.blue == 0 and fd.green > 0:
            fd.red += 17
            fd.green -= 17
        elif fd.red > 0 and fd.blue <= 255 and fd.green == 0:
            fd.blue += 17
            fd.red -= 17
        elif fd.green <= 255 and fd.red == 0 and fd.blue > 0:
            fd.green += 17
            fd.blue -= 17
    else:
        fd.red = 0
        fd.green = 0
        fd.blue = 255

    pygame.draw.rect(dis, (fd.red, fd.green, fd.blue), [fx, fy, (dn_var["fd_side"]), (dn_var["fd_side"])])


# checks the current position of the snake and determines whether the snake should die or not and displays msg
def check_boundaries(snake_x, snake_y, is_alive):
    no_end = True
    die = True

    if snake_x < 0 or snake_x > x_res-20 or snake_y < 0 or snake_y > y_res-20:
        dis.fill(colors["background"])
        disp_score(int(score))
        message("You crossed the boundaries, u lost.", colors["msg"], 100, y_res + 100)
        message("Press SPACE to replay or ESC to exit", colors["msg"], 100, y_res + 0)
        pygame.display.update()
        pause = True

        while pause:

            for died_Event in pygame.event.get():

                # if the user quits the program, close it (otherwise, he can't)
                if died_Event.type == pygame.QUIT:
                    pause = False
                    die = False
                    no_end = False

                # if the user pressed a key, check which one and react accordingly
                if died_Event.type == pygame.KEYDOWN:
                    if died_Event.key == pygame.K_ESCAPE:
                        pause = False
                        die = False
                        no_end = False
                        break

                    if died_Event.key == pygame.K_SPACE:
                        pause = False
                        die = False
                        no_end = True
                        break
    return no_end, die


# draws entire snake
def draw_snake(wdt, hgh, noodle):
    for list_x in noodle:
        pygame.draw.rect(dis, colors["snake_body"], [list_x[0], list_x[1], wdt, hgh])


# checks for self collision
def check_self(snek_list, head, is_alive, enemy):
    die = True
    no_end = True
    pause = False

    for x_list in snek_list[:-1]:
        if x_list == head:
            pause = True
            dis.fill(colors["background"])
            disp_score(int(score))
            message("You ate yourself, you've lost!",
                    colors["msg"], 100, y_res + 100)
            message("Press SPACE to replay or any ESC to exit", colors["msg"], 100, y_res + 0)
            pygame.display.update()
        elif x_list[0] == enemy.x and x_list[1] == enemy.y or head[0] == enemy.x and head[1] == enemy.y:
            pause = True
            dis.fill(colors["background"])
            disp_score(int(score))
            message("You've been bitten by a spider!",
                    colors["msg"], 100, y_res + 0)
            message("Since to become spider-man u have to be human, u died.", colors["msg"], 100, y_res + 100)
            message("Press SPACE to replay or any ESC to exit", colors["msg"], 100, y_res + 200)
            pygame.display.update()

    while pause:
        for died_Event in pygame.event.get():

            # if the user quits the program, close it (otherwise, he can't)
            if died_Event.type == pygame.QUIT:
                pause = False
                die = False
                no_end = True

            # if the user pressed a key, check which one and react accordingly
            if died_Event.type == pygame.KEYDOWN:
                if died_Event.key == pygame.K_ESCAPE:
                    pause = False
                    die = True
                    no_end = False
                    break

                if died_Event.key == pygame.K_SPACE:
                    pause = False
                    die = False
                    no_end = True
                    break

    return no_end, die


# resets the game params in case of user incompetence and replay

def reset():
    s_list = []
    s_size = 3
    s_pos_x = x_res//2
    s_pos_y = y_res//2
    s_mov_x, s_mov_y = rand_start()
    en_x_1, en_y_1 = rand_start()
    en_x_2, en_y_2 = rand_start()
    f_x, f_y = rand_pos()
    f = FoodColor(255, 0, 0)
    scr = 0
    en_1 = AngySzpider(en_x_1, en_y_1, 125, 122, 0)
    en_2 = AngySzpider(en_x_2, en_y_2, 125, 122, 0)
    sn_pack = (s_pos_x, s_pos_y, s_mov_x, s_mov_y)
    return s_list, s_size, sn_pack, f_x, f_y, f, scr, en_1, en_2


# displays score
def disp_score(val):
    global noEnemy
    font_style = pygame.font.SysFont("arial.ttf", 50)
    value = font_style.render("Your Score: " + str(val), True, colors["score"])
    value1 = font_style.render("Your Speed: [" + str(clk) + " / 25]", True, colors["score"])
    value2 = font_style.render("Your Size: [" + str(snake_Size) + "]", True, colors["score"])
    value3 = font_style.render("No. Enemies: [" + str(noEnemy) + "]", True, colors["score"])
    dis.blit(value, [0, 0])
    dis.blit(value1, [0, 50])
    dis.blit(value2, [0, 100])
    dis.blit(value3, [0, 150])


# displays secret message
def disp_RGB():
    global RGB_MODE
    if RGB_MODE:
        font_style = pygame.font.SysFont("arial.ttf", 50)
        value = font_style.render("RGB IS ON TUDUDUDU TUDUDUDU", True, colors["snake_body"])
        dis.blit(value, [20, y_res-50])


# main xd
if __name__ == '__main__':

    # returns surface and sets the game running
    dis, is_running = init(x_res, y_res)
    clock = pygame.time.Clock()

    # declaration of starting movement direction (it is random cus yeah)
    mx, my = rand_start()

    # starting enemy spider params
    en_x, en_y = rand_pos()
    angy = AngySzpider(en_x, en_y, 125, 122, 0)
    en_x, en_y = rand_pos()
    angy2 = AngySzpider(en_x, en_y, 125, 122, 0)

    # starting position
    x = x_res//2
    y = y_res//2

    # starting food params
    food_x, food_y = rand_pos()
    fit_x, fit_y = rand_pos()
    food = FoodColor(255, 0, 0)
    fit = FoodColor(0, 0, 255)
    score = 0

    # starting snake params
    snake_List = []
    snake_Size = 3

    alive = True

    enemy_move = True
    enemy2_move = True

    # game loop
    while is_running:
        # get events
        for event in pygame.event.get():

            # if the user quits the program, close it (otherwise, he can't)
            if event.type == pygame.QUIT:
                is_running = False

            # if the user pressed a key, check which one and react accordingly
            if event.type == pygame.KEYDOWN:
                mx, my = keypress(event, mx, my)

        # if snake left the boundaries, die.
        is_running, alive = check_boundaries(x, y, is_running)

        if not is_running:
            break

        # if left the boundaries and the game is still running, reset
        if not alive:
            snake_List, snake_Size, snake_pack, food_x, food_y, food, score, angy, angy2 = reset()
            x = snake_pack[0]
            y = snake_pack[1]
            mx = snake_pack[2]
            my = snake_pack[3]

        # checks if the snake ate the food
        food_x, food_y, snake_Size, score = check_food(x, y, food_x, food_y, snake_Size, score, False)
        fit_x, fit_y, snake_Size, score = check_food(x, y, fit_x, fit_y, snake_Size, score, True)

        # clear screen and draw snake head and food and the enemy
        dis.fill(colors["background"])
        draw_food(food, food_x, food_y)
        draw_fit_food(fit, fit_x, fit_y)

        # update the snake position by change in x and y
        x, y = pos_update(x, y, mx, my)

        # update spoder position
        if noEnemy > 0:
            if angy.x == 2500 or angy.y == 2500:
                en_x, en_y = rand_pos()
                angy = AngySzpider(en_x, en_y, 125, 122, 0)
            enemy_move = spoder_draw(angy, x, y, enemy_move)

            if noEnemy == 2:
                if angy2.x == 2500 or angy2.y == 2500:
                    en_x, en_y = rand_pos()
                    angy2 = AngySzpider(en_x, en_y, 125, 122, 0)
                enemy2_move = spoder_draw(angy2, x, y, enemy2_move)
            else:
                angy2.x = 2500
                angy2.y = 2500
                enemy2_move = False
                enemy2_move = spoder_draw(angy2, x, y, enemy2_move)

        else:
            angy.x = 2500
            angy.y = 2500
            angy2.x = 2500
            angy2.y = 2500
            enemy_move = False
            enemy_move = spoder_draw(angy, x, y, enemy_move)
            enemy2_move = False
            enemy2_move = spoder_draw(angy2, x, y, enemy2_move)

        # movement of the snake
        snake_Head = [x, y]
        snake_List.append(snake_Head)
        if len(snake_List) > snake_Size:
            del snake_List[0]

        # checks self collision
        is_running, alive = check_self(snake_List, snake_Head, is_running, angy)

        # if self-collided and the game is still running, reset
        if not alive:
            snake_List, snake_Size, snake_pack, food_x, food_y, food, score, angy, angy2 = reset()
            x = snake_pack[0]
            y = snake_pack[1]
            mx = snake_pack[2]
            my = snake_pack[3]

        # checks self collision
        is_running, alive = check_self(snake_List, snake_Head, is_running, angy2)

        # if self-collided and the game is still running, reset
        if not alive:
            snake_List, snake_Size, snake_pack, food_x, food_y, food, score, angy, angy2 = reset()
            x = snake_pack[0]
            y = snake_pack[1]
            mx = snake_pack[2]
            my = snake_pack[3]

        # further draw
        draw_snake(dn_var["width"], dn_var["height"], snake_List)

        # display score and secrets and no. of enemies
        disp_score(int(score))
        disp_RGB()

        # update screen
        pygame.display.update()

        # increment clock
        clock.tick(clk)

    pygame.quit()
    quit()
