import pygame as pg
import time
import random


class Item(pg.sprite.Sprite):
    def __init__(self, x, y, img, invx, invy, invimg, name):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hx = self.rect.x//100
        self.hy = self.rect.y//100
        self.invx = invx
        self.invy = invy
        self.invimg = invimg
        self.name = name
        self.power = 100

    def update(self):
        if self.hx < player.hx:
            if self.hx + 1 >= player.hx:
                if self.hy < player.hy:
                    if self.hy + 1 >= player.hy:
                        window.blit(self.image, (self.rect.x, self.rect.y))
                elif self.hy > player.hy:
                    if self.hy - 1 <= player.hy:
                        window.blit(self.image, (self.rect.x, self.rect.y))
                else:
                    window.blit(self.image, (self.rect.x, self.rect.y))

        elif self.hx > player.hx:
            if self.hx - 1 <= player.hx:
                if self.hy < player.hy:
                    if self.hy + 1 >= player.hy:
                        window.blit(self.image, (self.rect.x, self.rect.y))
                elif self.hy > player.hy:
                    if self.hy - 1 <= player.hy:
                        window.blit(self.image, (self.rect.x, self.rect.y))
                else:
                    window.blit(self.image, (self.rect.x, self.rect.y))

        else:
            if self.hy < player.hy:
                if self.hy + 1 >= player.hy:
                    window.blit(self.image, (self.rect.x, self.rect.y))
            elif self.hy > player.hy:
                if self.hy - 1 <= player.hy:
                    window.blit(self.image, (self.rect.x, self.rect.y))
            else:
                window.blit(self.image, (self.rect.x, self.rect.y))

        if pg.sprite.collide_rect(self, player):
            game_items.remove(self)
            player.grab(self)


class GameSprite(pg.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Object(GameSprite):
    def __init__(self, x, y, img, type):
        super().__init__(x, y, img)
        self.hx = self.rect.x//100
        self.hy = self.rect.y//100
        self.type = type
        self.level_pass = False

        if self.type == 0:
            self.tr = True
        elif self.type == 1:
            self.tr = False
        elif self.type == 2:
            self.tr = True
        elif self.type == 3:
            self.tr = False
            self.level_pass = False
        elif self.type == 4:
            self.tr = True
            self.level_pass = True

    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, x, y, img):
        super().__init__(x, y, img)
        self.i = []
        self.hx = self.rect.x//100
        self.hy = self.rect.y//100
        self.hp = 100
        self.stamina = 100
        self.stamina_regen_time = 0
        self.pick_time = 0
        self.pick = False
        self.picked_item = 0
        self.using_flash = False
        self.flash_cd = 0

    def update(self, near_walls):
        if self.pick:
            if time.time() - self.pick_time <= 5:
                grab_text = font.render('Picked up ' + self.picked_item.name, False, (255, 0, 0))
                window.blit(grab_text, (50, 820))
            else:
                self.pick = False
                self.picked_item = 0
                grab_text = font.render('', False, (255, 0, 0))
                window.blit(grab_text, (50, 820))

        for prp in near_walls:
            if prp.type == 2:
                pg.draw.rect(window, (0, 0, 0), (prp.rect.x+25, prp.rect.y+48, 50, 50))
                tip = font.render('F', True, (255, 0, 0))
                window.blit(tip, (prp.rect.x+45, prp.rect.y+60))

        self.hx = self.rect.x // 100
        self.hy = self.rect.y // 100
        keys = pg.key.get_pressed()

        if keys[pg.K_q] and flashlight in self.i and not self.using_flash and time.time() - self.flash_cd >= 1:
            self.using_flash = True
            self.flash_cd = time.time()
            pg.mixer.music.load('game_files/flashlight_onoff.mp3')
            pg.mixer.music.play()
        elif keys[pg.K_q] and flashlight in self.i and self.using_flash and time.time() - self.flash_cd >= 1:
            self.using_flash = False
            self.flash_cd = time.time()
            pg.mixer.music.load('game_files/flashlight_onoff.mp3')
            pg.mixer.music.play()

        if flashlight.power <= 0:
            self.using_flash = False

        if keys[pg.K_LSHIFT]:
            if self.stamina > 0:
                self.speed = 7
                self.stamina -= 1
                self.stamina_regen_time = time.time()
            else:
                self.speed = 5
                if time.time() - self.stamina_regen_time >= 3:
                    if self.stamina < 100:
                        self.stamina += 0.5
        else:
            self.speed = 5
            if time.time() - self.stamina_regen_time >= 3:
                if self.stamina < 100:
                    self.stamina += 0.5

        if keys[pg.K_w] and self.rect.y >= 0:
            self.image = pg.image.load('game_files/up.png')
            self.rect.y -= self.speed
            for wall in near_walls:
                if pg.sprite.collide_rect(self, wall) and wall.tr:
                    self.rect.y += self.speed
        if keys[pg.K_s] and self.rect.y <= WIN_HEIGHT - 50:
            self.image = pg.image.load('game_files/down.png')
            self.rect.y += self.speed
            for wall in near_walls:
                if pg.sprite.collide_rect(self, wall) and wall.tr:
                    self.rect.y -= self.speed
        if keys[pg.K_a] and self.rect.x >= 0:
            self.image = pg.image.load('game_files/left_right.png')
            self.rect.x -= self.speed
            for wall in near_walls:
                if pg.sprite.collide_rect(self, wall) and wall.tr:
                    self.rect.x += self.speed
        if keys[pg.K_d] and self.rect.x <= WIN_WIDTH - 25:
            self.image = pg.image.load('game_files/left_right.png')
            self.rect.x += self.speed
            for wall in near_walls:
                if pg.sprite.collide_rect(self, wall) and wall.tr:
                    self.rect.x -= self.speed

        if self.using_flash:
            flashlight.power -= 0.1

        self.draw()

    def grab(self, item):
        item.rect.x = self.rect.x
        item.rect.y = self.rect.y
        pg.mixer.music.load('game_files/pick_up.mp3')
        pg.mixer.music.play()
        self.pick_time = time.time()
        self.pick = True
        self.picked_item = item
        if item.name != 'Battery':
            self.i.append(item)
        else:
            flashlight.power = 100


FPS = 30
clock = pg.time.Clock()
WIN_WIDTH = 1000
WIN_HEIGHT = 900
player = Player(150, 150, pg.image.load('game_files/up.png'))
pg.init()

font = pg.font.SysFont('Arial', 24)
font1 = pg.font.SysFont('Arial', 10)

game_items = list()

flashlight = Item(150, 550, pg.image.load('game_files/flashlight.png'), 0, 0,
                  pg.image.load('game_files/flashlight_model.png'), 'Flaslight')
game_items.append(flashlight)

bg = pg.image.load('game_files/background.png')

window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# pg.mixer.init()
# pg.mixer.music.load('ambient.mp3')
# pg.mixer.music.play()


def gameover():
    window.blit(pg.image.load('game_files/endgame.png'), (0, 0))
    pg.display.update()
    pg.mixer.music.load('game_files/wasted.mp3')
    pg.mixer.music.play()
    time.sleep(3)
    return False


def menu():
    window.blit(pg.image.load('game_files/menu.png'), (0, 0))
    do_menu = True
    while do_menu:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                do_menu = False
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            main(1)
            return 0
        pg.display.update()


def main(level_num):
    battery = 0
    near_walls = list()
    objects = list()
    doinventory = False
    game = True
    monstr_cd = time.time()
    hidetime = 0
    cd = 0
    hide = False
    if level_num == 1:
        level = level1()
    elif level_num == 2:
        level = level2()
    elif level_num == 3:
        level = level3()
        battery = Item(750, 150, pg.image.load('game_files/battery.png'), 0, 0, 0, 'Battery')
        game_items.append(battery)
    else:
        window.blit(pg.image.load('game_files/cont.png'), (0, 0))
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
            pg.display.update()
    level_map = level[0]
    player.rect.x = level[1][0]
    player.rect.y = level[1][1]
    key = Item(level[2][0], level[2][1], pg.image.load('game_files/key.png'), 0, 0,
               pg.image.load('game_files/key_model.png'), 'Key')
    game_items.append(key)

    for i in range(len(level_map)):
        for j in range(len(level_map[i])):
            if level_map[i][j] == '#':
                wall = Object(j * 100, i * 100, pg.image.load('game_files/wall.png'), 0)
                objects.append(wall)
            elif level_map[i][j] == 'bh':
                decal = Object(j * 100, i * 100, pg.image.load('game_files/bfhm.png'), 1)
                objects.append(decal)
            elif level_map[i][j] == 'bv':
                decal = Object(j * 100, i * 100, pg.image.load('game_files/bfvm.png'), 1)
                objects.append(decal)
            elif level_map[i][j] == 'btr':
                decal = Object(j * 100, i * 100, pg.image.load('game_files/bfrt.png'), 1)
                objects.append(decal)
            elif level_map[i][j] == 'bbr':
                decal = Object(j * 100, i * 100, pg.image.load('game_files/bfrb.png'), 1)
                objects.append(decal)
            elif level_map[i][j] == 'btl':
                decal = Object(j * 100, i * 100, pg.image.load('game_files/bflt.png'), 1)
                objects.append(decal)
            elif level_map[i][j] == 'bbl':
                decal = Object(j * 100, i * 100, pg.image.load('game_files/bflb.png'), 1)
                objects.append(decal)
            elif level_map[i][j] == 'bve':
                decal = Object(j * 100, i * 100, pg.image.load('game_files/bfve.png'), 1)
                objects.append(decal)
            elif level_map[i][j] == 'bhe':
                decal = Object(j * 100, i * 100, pg.image.load('game_files/bfhe.png'), 1)
                objects.append(decal)
            elif level_map[i][j] == 'bhs':
                decal = Object(j * 100, i * 100, pg.image.load('game_files/bfhs.png'), 1)
                objects.append(decal)
            elif level_map[i][j] == 'bvs':
                decal = Object(j * 100, i * 100, pg.image.load('game_files/bfvs.png'), 1)
                objects.append(decal)
            elif level_map[i][j] == 't':
                decal = Object(j * 100, i * 100, pg.image.load('game_files/table.png'), 1)
                objects.append(decal)
            elif level_map[i][j] == 'c':
                closet = Object(j * 100, i * 100, pg.image.load('game_files/closet.png'), 2)
                objects.append(closet)
            elif level_map[i][j] == 'd':
                door = Object(j * 100, i * 100, pg.image.load('game_files/door.png'), 3)
                objects.append(door)
            elif level_map[i][j] == 'dl':
                door = Object(j * 100, i * 100, pg.image.load('game_files/door.png'), 4)
                objects.append(door)
            elif level_map[i][j] == 'l1':
                pass
            elif level_map[i][j] == 'l2':
                pass
            elif level_map[i][j] == 'l3':
                pass

    pg.mixer.init()
    monstr = False
    while game:

        if player.hp <= 0:
            game = gameover()

        if 10 <= time.time() - monstr_cd <= 15:
            monstr = True
            hidetime = time.time()
            monstr_cd = -10
            pg.mixer.music.load('game_files/monstr.mp3')
            pg.mixer.music.play()

        if monstr:
            if time.time() - hidetime >= 5:
                pg.mixer.music.load('game_files/monstr_1.mp3')
                pg.mixer.music.play()
                window.blit(pg.image.load('game_files/monstr_1.png'), (0, 0))
                pg.display.update()
                time.sleep(2.5)
                game = gameover()

        window.blit(bg, (0, 0))
        window.blit(bg, (500, 0))
        window.blit(bg, (0, 500))
        window.blit(bg, (500, 500))
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_e:
                    doinventory = True
            elif event.type == pg.QUIT:
                game = False

        if hide:
            hide_cd = time.time()
            while hide:
                if time.time() - hide_cd >= 3:
                    pg.mixer.music.load('game_files/closet_monster.mp3')
                    pg.mixer.music.play()
                    player.hp -= 20
                    hide = False

                clock.tick(FPS)
                window.blit(pg.image.load('game_files/in_closet.png'), (0, 0))
                if time.time() - hidetime >= 5:
                    monstr = False
                    monstr_cd = time.time()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        hide = False
                        game = False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_f:
                            pg.mixer.music.load('game_files/closet_close.mp3')
                            pg.mixer.music.play()
                            hide = False
                            cd = time.time()
                pg.display.update()

        while doinventory:
            window.blit(pg.image.load('game_files/inventory.png'), (WIN_WIDTH // 2 - 218, WIN_HEIGHT // 2 - 224))
            for item in range(len(player.i)):
                if item <= 5:
                    player.i[item].invx = 18 + item * (59 + 8) + WIN_WIDTH // 2 - 218
                    player.i[item].invy = 17 + WIN_HEIGHT // 2 - 224
                elif 6 <= item <= 11:
                    player.i[item].invx = 18 + (item - 6) * (59 + 8) + WIN_WIDTH // 2 - 218
                    player.i[item].invy = 17 + 59 + 10 + WIN_HEIGHT // 2 - 224
                elif 12 <= item <= 17:
                    player.i[item].invx = 18 + (item - 12) * (59 + 8) + WIN_WIDTH // 2 - 218
                    player.i[item].invy = 17 + 2 * (59 + 10) + WIN_HEIGHT // 2 - 224
                elif 18 <= item <= 23:
                    player.i[item].invx = 18 + (item - 18) * (59 + 8) + WIN_WIDTH // 2 - 218
                    player.i[item].invy = 17 + 3 * (59 + 10) + WIN_HEIGHT // 2 - 224
                elif 24 <= item <= 29:
                    player.i[item].invx = 18 + (item - 24) * (59 + 8) + WIN_WIDTH // 2 - 218
                    player.i[item].invy = 17 + 4 * (59 + 10) + WIN_HEIGHT // 2 - 224
                elif 30 <= item <= 35:
                    player.i[item].invx = 18 + (item - 30) * (59 + 8) + WIN_WIDTH // 2 - 218
                    player.i[item].invy = 17 + 5 * (59 + 10) + WIN_HEIGHT // 2 - 224

                window.blit(player.i[item].invimg, (player.i[item].invx, player.i[item].invy))

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_e:
                        doinventory = False

            pg.display.update()

        for wall in objects:
            if player.using_flash:
                if wall.hy > player.hy:
                    if wall.hx > player.hx:
                        if player.hy + 2 >= wall.hy:
                            if player.hx + 2 >= wall.hx:
                                if wall not in near_walls:
                                    near_walls.append(wall)
                            else:
                                if wall in near_walls:
                                    near_walls.remove(wall)
                                    pass
                        else:
                            if wall in near_walls:
                                near_walls.remove(wall)
                                pass

                    elif wall.hx < player.hx:
                        if player.hy + 2 >= wall.hy:
                            if player.hx - 2 <= wall.hx:
                                if wall not in near_walls:
                                    near_walls.append(wall)
                            else:
                                if wall in near_walls:
                                    near_walls.remove(wall)
                                    pass
                        else:
                            if wall in near_walls:
                                near_walls.remove(wall)
                                pass

                    else:
                        if player.hy + 2 >= wall.hy:
                            if wall not in near_walls:
                                near_walls.append(wall)
                        else:
                            if wall in near_walls:
                                near_walls.remove(wall)
                                pass

                elif wall.hy < player.hy:
                    if wall.hx > player.hx:
                        if player.hy - 2 <= wall.hy:
                            if player.hx + 2 >= wall.hx:
                                if wall not in near_walls:
                                    near_walls.append(wall)
                            else:
                                if wall in near_walls:
                                    near_walls.remove(wall)
                                    pass
                        else:
                            if wall in near_walls:
                                near_walls.remove(wall)
                                pass

                    elif wall.hx < player.hx:
                        if player.hy - 2 <= wall.hy:
                            if player.hx - 2 <= wall.hx:
                                if wall not in near_walls:
                                    near_walls.append(wall)
                            else:
                                if wall in near_walls:
                                    near_walls.remove(wall)
                                    pass
                        else:
                            if wall in near_walls:
                                near_walls.remove(wall)
                                pass

                    else:
                        if player.hy - 2 <= wall.hy:
                            if wall not in near_walls:
                                near_walls.append(wall)
                        else:
                            if wall in near_walls:
                                near_walls.remove(wall)
                                pass

                else:
                    if wall.hx > player.hx:
                        if player.hx + 2 >= wall.hx:
                            if wall not in near_walls:
                                near_walls.append(wall)
                        else:
                            if wall in near_walls:
                                near_walls.remove(wall)
                                pass

                    elif wall.hx < player.hx:
                        if player.hx - 2 <= wall.hx:
                            if wall not in near_walls:
                                near_walls.append(wall)
                        else:
                            if wall in near_walls:
                                near_walls.remove(wall)
                                pass
            else:
                if player.hy - 1 == wall.hy or player.hy + 1 == wall.hy or player.hy == wall.hy:
                    if player.hx - 1 == wall.hx or player.hx + 1 == wall.hx or player.hx == wall.hx:
                        if wall not in near_walls:
                            near_walls.append(wall)
                    else:
                        if wall in near_walls:
                            near_walls.remove(wall)
                            pass
                else:
                    if wall in near_walls:
                        near_walls.remove(wall)
                        pass

        for object in near_walls:
            if object.type == 4:
                if key in player.i:
                    object.tr = False
                if pg.sprite.collide_rect(object, player):
                    if key in player.i:
                        player.i.remove(key)
                        game = main(level_num+1)

            elif object.type == 3:
                if pg.sprite.collide_rect(object, player):
                    object.image = pg.image.load('game_files/opened_door.png')
                    object.tr = False

        keys = pg.key.get_pressed()
        for wall in near_walls:
            if keys[pg.K_f] and time.time() - cd >= 0.5:
                if wall.type == 2:
                    pg.mixer.music.load('game_files/closet_open.mp3')
                    pg.mixer.music.play()
                    hide = True
            wall.update()

        player.update(near_walls)

        pg.draw.rect(window, (255, 0, 0), (0, 0, player.hp * 2, 10))
        hp_text = font1.render(str(round(player.hp)), True, (0, 255, 0))
        window.blit(hp_text, (0, 0))

        pg.draw.rect(window, (0, 0, 255), (0, 10, player.stamina * 2, 10))
        stamina_text = font1.render(str(round(player.stamina)), True, (255, 0, 0))
        window.blit(stamina_text, (0, 10))

        if flashlight in player.i:
            pg.draw.rect(window, (255, 255, 0), (0, 20, flashlight.power * 2, 10))
            power_text = font1.render(str(round(flashlight.power)), True, (0, 0, 255))
            window.blit(power_text, (0, 20))

        for it in game_items:
            it.update()

        pg.display.update()

    return False


# Редактор карт
# * - Пол
# # - Стена
# l1 - Лабораторное оборудование №1
# l2 - Лабораторное оборудование №2
# l3 - Лабораторное оборудование №3
# t - Стол
# bh, bv - Пол с кровью по середине
# bhe, bve - Конец кровавого следа слева
# bhs, bvs - Конец кровавого следа справа
# bbl, btl - Поворот следа крови налево
# bbr, btr - Поворот следа крови направо
# c - Шкафчик
# d - Дверь
# dl - Дверь на следующий уровень


def level1():
    lv1 = [['#', '#', '#',  '#',  '#',   '#',    '#', '#', '#', '#'],
           ['#', '*', '#', 'btr', 'bh', 'bhe',   '#', '*', '*', 'dl'],
           ['#', '*', '#', 'bbr', 'bh', 'btl',   '#', '*', '*', '#'],
           ['#', '*', '#',  '#',  '#',  'bv',    '#', '*', '*', '#'],
           ['#', 'bhs', 'bh', 'bh', 'bh', 'bbl', '*', '*', '*', '#'],
           ['#',  '*',  '#',  '#',  '#',   '#',  '#', '*', '*', '#'],
           ['#',  '*',  '*',  '*',  '*',   '*',  '#', '*', '*', '#'],
           ['#',  'c',  '*',  '*',  '*',   't',  '#', 'c', 'c', '#'],
           ['#',  '#',  '#',  '#',  '#',   '#',  '#', '#', '#', '#']]

    level = lv1
    pp = (150, 150)
    key_chance = random.randint(1, 3)
    if key_chance == 1:
        key = (550, 750)
    elif key_chance == 2:
        key = (550, 150)
    elif key_chance == 3:
        key = (750, 650)

    return level, pp, key


def level2():
    lv2 = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
           ['*', '*', '*', '*', '*', '*', '*', '*', '*', 'dl'],
           ['*', '*', '*', '*', '*', '*', '#', '*', '*', '#'],
           ['#', '*', '#', '#', '#', '#', '#', '*', '*', '#'],
           ['#', '*', '#', 't', '*', '*', 'd', '*', '*', '#'],
           ['#', '*', '#', '#', '#', '#', '#', '*', '*', '#'],
           ['#', '*', '*', '*', '*', '*', '#', '*', '*', '#'],
           ['#', '*', '*', '*', '*', 'c', '#', 'c', '*', '#'],
           ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

    level = lv2
    pp = (50, 150)
    key_chance = random.randint(0, 5)
    if key_chance == 1:
        key = (350, 450)
    else:
        x = random.randint(1, 4)
        y = random.randint(6, 7)
        key = (x*100+50, y*100+50)

    return level, pp, key


def level3():
    lv2 = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
           ['*', '*', '#', 't', '*', '*', '#', 't', '*', 'dl'],
           ['*', '*', '#', 'c', '*', '*', '#', '*', '*', '#'],
           ['#', '*', '#', '#', '#', 'd', '#', '#', 'd', '#'],
           ['#', '*', '*', '*', '*', '*', 'd', '*', '*', '#'],
           ['#', '*', '#', '#', '#', 'd', '#', '#', 'd', '#'],
           ['#', '*', '#', 'c', '*', '*', '#', 't', '*', '#'],
           ['#', 'c', '#', 't', '*', '*', '#', '*', '*', '#'],
           ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

    level = lv2
    pp = (50, 150)
    key_chance = random.randint(0, 2)
    if key_chance == 0:
        key = (350, 750)
    elif key_chance == 1:
        key = (350, 150)
    elif key_chance == 2:
        key = (750, 650)

    return level, pp, key


if __name__ == '__main__':
    menu()
