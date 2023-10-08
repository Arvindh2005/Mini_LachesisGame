import random
import pygame
import csv
import time
import math

pygame.init()
clock = pygame.time.Clock()
FPS = 60

# SCREEN
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("LACHESIS_DEFENDER")
icon = pygame.image.load("ALWAYSRR.ico")
pygame.display.set_icon(icon)
INITIAL_SCREEN_COLOUR = pygame.Color((40, 80, 120))
tiles = math.ceil(1000/2000) + 1
scroll = 0
# BACKGROUND PROPERTIES
BG = pygame.image.load("TITLE_PAGE.png").convert_alpha()
bg_speed = 2

# PARALLEL UNIVERSE OPERATION

parallel_universe_operator = 1

# LACHESIS PROPERTIES
lachesis_img = pygame.image.load("lachesis_pro1.png").convert_alpha()
lachesis_mask = pygame.mask.from_surface(lachesis_img)
lachesisX = 100
lachesisY = 100
lachesisXch = 0
lachesisYch = 0
lachesis_confirm = -1
lachesis_strength = 200

# MOUSE PROPERTIES
mouseX = 0
mouseY = 0

# GUN PROPERTIES


class Gun(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.gun_img = pygame.image.load("lachesisgun.png").convert_alpha()
        self.gunX = x
        self.gunY = y

    def draw(self):
        screen.blit(self.gun_img, (self.gunX, self.gunY))

# BULLET PROPERTIES


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_img = pygame.image.load("lachesisbullet.png").convert_alpha()
        self.bullet_mask = pygame.mask.from_surface(self.bullet_img)
        self.bulletX = x
        self.bulletY = y
        self.bulletXch = 5
        self.bullet_launch_code = -1
        self.bullet_launch_code2 = -1
        self.bullet_launch_code3 = -1
        self.result = False
        self.offset = (lachesisX - self.bulletX, lachesisY - self.bulletY)

    def draw(self, a):
        if a == 1:
            if self.bullet_launch_code == 1:
                screen.blit(self.bullet_img, (self.bulletX, self.bulletY))
                self.bulletX -= self.bulletXch
                self.offset = (lachesisX - self.bulletX, lachesisY - self.bulletY)
        if a == 2:
            if self.bullet_launch_code2 == 1:
                screen.blit(self.bullet_img, (self.bulletX, self.bulletY))
                self.bulletX -= self.bulletXch
                self.offset = (lachesisX - self.bulletX, lachesisY - self.bulletY)
        if a == 3:
            if self.bullet_launch_code3 == 1:
                screen.blit(self.bullet_img, (self.bulletX, self.bulletY))
                self.bulletX -= self.bulletXch
                self.offset = (lachesisX - self.bulletX, lachesisY - self.bulletY)

    def activator(self, a):
        if a == 1:
            if self.bullet_launch_code == 0:
                code_producer()
                self.bulletX = 758
                self.bullet_launch_code = 1
        if a == 2:
            if self.bullet_launch_code2 == 0:
                code_producer2()
                self.bulletX = 758
                self.bullet_launch_code2 = 1
        if a == 3:
            if self.bullet_launch_code3 == 0:
                code_producer3()
                self.bulletX = 758
                self.bullet_launch_code3 = 1

    def checker(self, x, result, a):
        global score
        if a == 1:
            if x <= 0 and (result == -1 or result == 0):
                self.bullet_launch_code = 0
                score += 1
            if result == 1:
                self.bullet_launch_code = -1
        if a == 2:
            if x <= 0 and (result == -1 or result == 0):
                self.bullet_launch_code2 = 0
                score += 1
            if result == 1:
                self.bullet_launch_code2 = -1

        if a == 3:
            if x <= 0 and (result == -1 or result == 0):
                self.bullet_launch_code3 = 0
                score += 1
            if result == 1:
                self.bullet_launch_code3 = -1

    def collision_detector(self, a):
        global lachesis_strength
        global collision_checker

        if a == 1:
            self.result = self.bullet_mask.overlap(lachesis_mask, self.offset)
            if self.result:
                self.bullet_launch_code = 0
                if self.bulletX < 758:
                    lachesis_strength -= score_degrader
                    collision_checker = True
                self.bulletX = 758
        if a == 2:
            self.result = self.bullet_mask.overlap(lachesis_mask, self.offset)
            if self.result:
                self.bullet_launch_code2 = 0
                if self.bulletX < 758:
                    lachesis_strength -= score_degrader
                    collision_checker = True
                self.bulletX = 758

        if a == 3:
            self.result = self.bullet_mask.overlap(lachesis_mask, self.offset)
            if self.result:
                self.bullet_launch_code3 = 0
                if self.bulletX < 758:
                    lachesis_strength -= score_degrader
                    collision_checker = True
                self.bulletX = 758

    def activity_decider(self):
        global pause
        if pause == 1:
            self.bulletXch = 0
        else:
            self.bulletXch = 10
            if score > 100:
                self.bulletXch = 10


collision_checker = False
bullet1 = Bullet(758, 40)
bullet2 = Bullet(758, 120)
bullet3 = Bullet(758, 200)
bullet4 = Bullet(758, 280)
bullet5 = Bullet(758, 360)
bullet6 = Bullet(758, 440)
bullet7 = Bullet(758, 520)
bullet8 = Bullet(758, 600)
whole_bullet = [bullet1, bullet2, bullet3, bullet4, bullet5, bullet6, bullet7, bullet8]

# SCORE DETECTOR
score = 0
FONT = pygame.font.Font("freesansbold.ttf", 25)
fontX = 300
fontY = 10
score_tracker = 0
score_degrader = 15


def score_font():
    if lachesis_confirm == 1:
        if pause == 0:
            text = FONT.render("Score : " + str(score), True, (0, 0, 0))
            screen.blit(text, (fontX, fontY))
        if pause == 1:
            text = FONT.render("Score : " + str(score), True, (0, 0, 0))
            screen.blit(text, (fontX, fontY))
    if lachesis_confirm == 0:
        text = FONT.render("Score : " + str(score), True, (0, 0, 0))
        screen.blit(text, (fontX, fontY))


def coin_font():
    text = FONT.render("Coins : " + str(coin_amount), True, (0, 0, 0))
    screen.blit(text, (700, 35))


# RABBIT PROPERTIES
RabbitX = 1100
RabbitY = 50
rabbit_threshold = 20


class Rabbit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        chr_list = []
        self.animation_list = []
        self.offset = ((lachesisX - RabbitX), (lachesisY - RabbitY))

        for img in range(1, 9):
            rabbit_img = pygame.image.load(f"rabbit/rabbit{img}.png").convert_alpha()
            chr_list.append(rabbit_img)

        self.animation_list.append(chr_list)
        self.rabbit_img = chr_list[self.frame_index]
        self.rabbit_mask = pygame.mask.from_surface(self.rabbit_img)
        self.rabbitX = x
        self.rabbitY = y

    def update_animation(self):
        animation_cooldown = 100
        self.rabbit_img = self.animation_list[0][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[0]):
            self.frame_index = 0

    def draw(self):
        screen.blit(self.rabbit_img, (RabbitX, RabbitY))
        self.offset = ((lachesisX - RabbitX), (lachesisY - RabbitY))

    def collision_checker(self):
        global lachesis_strength
        global RabbitX
        result = self.rabbit_mask.overlap(lachesis_mask, self.offset)
        if result:
            RabbitX = -500
            if lachesis_strength <= 180:
                lachesis_strength += 20
            else:
                lachesis_strength += 200 - lachesis_strength


# GRENADE PROPERTIES
grenade_activator = 0
grenade_degrader = 30


class Grenade(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.grenade_img = pygame.image.load("grenade.png").convert_alpha()
        self.grenadeX = 10000
        self.grenadeY = -1000000
        self.randomiser = 1
        self.grenadeYch = 4
        self.deactivator = 0
        self.Xvalue_get = 0
        self.Yvalue_get = 0
        self.grenade_mask = pygame.mask.from_surface(self.grenade_img)
        self.offset = (lachesisX - self.grenadeX, lachesisY - self.grenadeY)
        self.result = 0

    def runner(self):
        if self.randomiser == 0:
            self.grenadeX = random.choice([100, 200, 300])
            self.grenadeY = -100
            self.randomiser = 1

        if self.randomiser == 2:
            self.grenadeX = random.choice([10000, 20000, 30000])

    def deactivate(self):
        self.randomiser = 2
        self.deactivator = 1

    def activate(self):
        self.randomiser = 0
        self.deactivator = 0

    def draw(self):
        screen.blit(self.grenade_img, (self.grenadeX, self.grenadeY))
        self.grenadeY += self.grenadeYch

    def checker(self):
        if self.grenadeY >= 620 and self.deactivator == 0:
            self.randomiser = 0

    def collision_checker(self):
        global lachesis_strength
        global parallel_universe_operator
        self.offset = (lachesisX - self.grenadeX, lachesisY - self.grenadeY)
        self.result = self.grenade_mask.overlap(lachesis_mask, self.offset)
        if self.result:
            self.randomiser = 0
            self.Xvalue_get = self.grenadeX
            self.Yvalue_get = self.grenadeY
            explode_1.frame_index = 0
            lachesis_strength -= grenade_degrader
            if lachesis_strength >= 30 and not head1.access_on:
                parallel_universe_operator = 0


# EXPLOSION PROPERTIES
class Explosion:
    def __init__(self):
        chr_list = []
        self.animation_list = []
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        for img in range(1, 8):
            image = pygame.image.load(f"explode2/explode{img}.png").convert_alpha()
            chr_list.append(image)
        self.animation_list.append(chr_list)
        self.image = self.animation_list[0][self.frame_index]

    def draw(self, x, y):
        screen.blit(self.image, (x, y))

    def update_animation(self):
        global parallel_universe_operator
        animation_cooldown = 150
        self.image = self.animation_list[0][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            if self.frame_index < len(self.animation_list[0]):
                self.frame_index += 1
            if self.frame_index >= len(self.animation_list[0]):
                self.frame_index = 6
                parallel_universe_operator = 1
        if self.frame_index >= len(self.animation_list[0]):
            self.frame_index = 6


# WIND PROPERTIES
wind_maker = pygame.image.load("wind maker.png").convert_alpha()
wind_maker2 = pygame.image.load("wind maker1.png").convert_alpha()
wind_maker3 = pygame.image.load("wind_maker3.png").convert_alpha()
wind_maker4 = pygame.image.load("wind_maker4.png").convert_alpha()
gravity1 = pygame.image.load("gravity_maintain1.png").convert_alpha()
gravity2 = pygame.image.load("gravity_maintain2.png").convert_alpha()


class Wind:
    def __init__(self, x, y, z):
        self.wind_img = pygame.image.load(z).convert_alpha()
        self.windX = x
        self.windY = y
        self.wind_activator = 0

    def draw(self, x, y, z, d, dirn):
        if dirn == 1:
            self.windX = x
        if dirn == 2:
            self.windY = y
        if self.wind_activator == 1 and d != y:
            screen.blit(self.wind_img, (self.windX, self.windY))
            if z == 1:
                self.windY -= 4
            if z == 2:
                self.windY += 2
            if z == 3:
                self.windX += 4
            if z == 4:
                self.windX -= 4

    def checker(self, y, dirn):
        if self.wind_activator == 0:
            if dirn == 1:
                self.windY = y
            if dirn == 2:
                self.windX = y


# COIN PROPERTIES
coin_img = pygame.image.load("coin1.png").convert_alpha()
coin_mask = pygame.mask.from_surface(coin_img)
coinX = 1200
coinY = 200
coin_motion = 0
coin_amount = 0
coin_velocity = 6

coin_code = -1
coin_constant = 0
coin_no = 0
coin_list = []
great_data = 0
coin_pattern1 = 0
coin_pattern2 = 0
coin_pattern3 = 0
coin_pattern4 = 0
coin_pattern5 = 0
code_gen = 0

coin_details = open("coin_amt.txt", "r")
coin_amount = int(coin_details.read())
print(coin_amount)


def coin_code_generator():
    global great_data
    global coin_code
    global code_gen
    global coin_pattern1
    global coin_pattern2
    global coin_pattern3
    global coin_pattern4
    global coin_pattern5
    if code_gen == 0:
        coin_code = random.randint(1, 5)
        if coin_code == 1:
            coin_pattern1 = open("coin1.csv", "r")
            great_data = csv.reader(coin_pattern1)

        if coin_code == 2:
            coin_pattern2 = open("coin2.csv", "r")
            great_data = csv.reader(coin_pattern2)

        if coin_code == 3:
            coin_pattern3 = open("coin3.csv", "r")
            great_data = csv.reader(coin_pattern3)

        if coin_code == 4:
            coin_pattern4 = open("coin4.csv", "r")
            great_data = csv.reader(coin_pattern4)

        if coin_code == 5:
            coin_pattern5 = open("coin5.csv", "r")
            great_data = csv.reader(coin_pattern5)

        code_gen = 1


def coin_maker():
    global coin_no
    global coin_constant
    global coinX
    global coinY
    global coin_list

    coinX = 1200
    coinY = 200
    coin_no = 0
    if coin_constant == 0:
        for no in great_data:
            for j in no:
                if coin_no % 5 == 0 and coin_no > 0:
                    coinY += 65
                    coinX = 1200

                if j == "1":
                    x = [coinX, coinY]
                    coin_list.append(x)
                    coinX += 65

                elif j == "0":
                    coinX += 65

                coin_no += 1

        if coin_code == 1:
            coin_pattern1.close()
        if coin_code == 2:
            coin_pattern2.close()
        if coin_code == 3:
            coin_pattern3.close()
        if coin_code == 4:
            coin_pattern4.close()
        if coin_code == 5:
            coin_pattern5.close()

        coin_constant = 1


# HEADSTART, MAGNET, SHIELD PROPERTIES
headstart_ontime = 0
headstart_cooltime = 10
headstart_pause = 0
headstart_resume = 0
difference = 0

shield_ontime = 0
shield_cooltime = 10
difference1 = 0

magnet_ontime = 0
magnet_cooltime = 10
distance = 100
difference2 = 0


class Accessories:
    def __init__(self, img):
        self.access_img = pygame.image.load(img)
        self.accessX = -1200
        self.accessY = 100
        self.access_on = False
        self.offset = (lachesisX - self.accessX, lachesisY - self.accessY)
        self.accessmask = pygame.mask.from_surface(self.access_img)
        self.access_result = False

    def draw_access(self):
        screen.blit(self.access_img, (self.accessX, self.accessY))
        self.accessX -= 10

    def checker(self, thres):
        if score % thres == 0 and score > 10:
            self.accessX = 1200

    def collision_checker(self, types):
        global shield_ontime
        global headstart_ontime
        global magnet_ontime
        self.offset = (lachesisX - self.accessX, lachesisY - self.accessY)
        self.result = self.accessmask.overlap(lachesis_mask, self.offset)
        if self.result:
            self.accessX = -100
            self.access_on = True
            if types == 1:
                shield_ontime = time.time()
            if types == 2:
                headstart_ontime = time.time()
            if types == 3:
                magnet_ontime = time.time()


# PAUSE RESUME FEATURES
pause = 0
pause_button = pygame.image.load("resume.jpg").convert_alpha()
resume_button = pygame.image.load("pause.jpg").convert_alpha()
pause_button_active = 0
resume_button_active = 1


def pause_resume_button():
    if pause == 1:
        screen.blit(resume_button, (950, 653))
    if pause == 0:
        screen.blit(pause_button, (950, 653))
# GENERAL THINGS


power = pygame.image.load("power.png").convert_alpha()


def lachesislauncher(x, y):
    screen.blit(lachesis_img, (x, y))


def powerful():
    screen.blit(power, (lachesisX - 45, lachesisY - 10))


activation_code = -1
activation_code2 = -1
activation_code3 = -1
offset_list = []
result_list = []
approve = True
health_barX = 40
RETRY = -1


def code_producer():
    global activation_code
    activation_code = random.randint(0, 7)


def code_producer2():
    global activation_code2
    activation_code2 = random.randint(0, 7)


def code_producer3():
    global activation_code3
    activation_code3 = random.randint(0, 7)

# FINALISING EVERYTHING


gun1 = Gun(858, 40)
gun2 = Gun(858, 120)
gun3 = Gun(858, 200)
gun4 = Gun(858, 280)
gun5 = Gun(858, 360)
gun6 = Gun(858, 440)
gun7 = Gun(858, 520)
gun8 = Gun(858, 600)
gun_list = [gun1, gun2, gun3, gun4, gun5, gun6, gun7, gun8]
rabbit1 = Rabbit(RabbitX, RabbitY)
grenade1 = Grenade()
explode_1 = Explosion()
wind_up = Wind(lachesisX + 60, 600, "wind5.png")
wind_down = Wind(lachesisX + 60, 30, "wind7.png")
wind_posi = Wind(lachesisY + 30, 30, "wind3.png")
wind_nega = Wind(lachesisY + 30, 970, "wind4.png")
head1 = Accessories("headstart.png")
magnet1 = Accessories("magnet.png")
shield1 = Accessories("shield.png")

# SHOP PROPERTIES

shop_bg = pygame.image.load("SHOPICON.png")
headstart_lv1 = pygame.image.load("headstartlv1.png")
headstart_lv2 = pygame.image.load("headstartlv2.png")
headstart_lv3 = pygame.image.load("headstartlv3.png")
headstart_lv4 = pygame.image.load("headstartlv4.png")
headstart_lv5 = pygame.image.load("headstartlv5.png")

magnet_lv1 = pygame.image.load("magnetlv1.png")
magnet_lv2 = pygame.image.load("magnetlv2.png")
magnet_lv3 = pygame.image.load("magnetlv3.png")
magnet_lv4 = pygame.image.load("magnetlv4.png")
magnet_lv5 = pygame.image.load("magnetlv5.png")

shield_lv1 = pygame.image.load("shieldlv1.png")
shield_lv2 = pygame.image.load("shieldlv2.png")
shield_lv3 = pygame.image.load("shieldlv3.png")
shield_lv4 = pygame.image.load("shieldlv4.png")
shield_lv5 = pygame.image.load("shieldlv5.png")

update_lv2 = pygame.image.load("headstart lv1.png")
update_lv3 = pygame.image.load("headstart lv2.png")
update_lv4 = pygame.image.load("headstart lv3.png")
update_lv5 = pygame.image.load("headstart lv4.png")

shop_csv_data = open("shop_details.csv", "r")
shop_all = csv.reader(shop_csv_data)
shop_list = []

for i in shop_all:
    shop_list.append(i)

shop_csv_data.close()

print(shop_list)

headstart_level = shop_list[0][1]
magnet_level = shop_list[1][1]
shield_level = shop_list[2][1]

level2price = shop_list[0][2]
level3price = shop_list[0][3]
level4price = shop_list[0][4]
level5price = shop_list[0][5]

shop_activator = 0

headstartshopX = 100
headstartshopY = 134

magnetshopX = 375
magnetshopY = 134

shieldshopX = 650
shieldshopY = 134

headstartstatusX = 120
headstartstatusY = 300

magnetstatusX = 395
magnetstatusY = 300

shieldstatusX = 670
shieldstatusY = 300


def headstart_timemanager():
    global headstart_cooltime
    if headstart_level == "1":
        headstart_cooltime = 10
    if headstart_level == "2":
        headstart_cooltime = 15
    if headstart_level == "3":
        headstart_cooltime = 20
    if headstart_level == "4":
        headstart_cooltime = 25
    if headstart_level == "5":
        headstart_cooltime = 30


def magnet_timemanager():
    global magnet_cooltime
    if magnet_level == "1":
        magnet_cooltime = 10
    if magnet_level == "2":
        magnet_cooltime = 15
    if magnet_level == "3":
        magnet_cooltime = 20
    if magnet_level == "4":
        magnet_cooltime = 25
    if magnet_level == "5":
        magnet_cooltime = 30


def shield_timemanager():
    global shield_cooltime
    if shield_level == "1":
        shield_cooltime = 10
    if shield_level == "2":
        shield_cooltime = 15
    if shield_level == "3":
        shield_cooltime = 20
    if shield_level == "4":
        shield_cooltime = 25
    if shield_level == "5":
        shield_cooltime = 30


# RETRY SETTINGS
retry_button = pygame.image.load("retry.png").convert_alpha()
retryX = 220
retryY = 250

shop_button = pygame.image.load("shop_button.png").convert_alpha()
shopX = 560
shopY = 420

run = True

while run:
    clock.tick(FPS)
    screen.fill(INITIAL_SCREEN_COLOUR)
    screen.blit(BG, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_w:
                if pause == 0:
                    lachesisYch = -10
                    if lachesis_confirm == 1:
                        wind_up.wind_activator = 1

            if event.key == pygame.K_s:
                if pause == 0:
                    lachesisYch = 10
                    if lachesis_confirm == 1:
                        wind_down.wind_activator = 1

            if event.key == pygame.K_a:
                if pause == 0:
                    lachesisXch = -10
                    if lachesis_confirm == 1:
                        wind_nega.wind_activator = 1

            if event.key == pygame.K_d:
                if pause == 0:
                    lachesisXch = 10
                    if lachesis_confirm == 1:
                        wind_posi.wind_activator = 1

            if event.key == pygame.K_p:
                if pause == 0:
                    pause = 1
                    headstart_pause = time.time()
                    grenade1.grenadeYch = 0
                    lachesisYch = 0

            if event.key == pygame.K_r:
                if pause == 1:
                    pause = 0
                    headstart_resume = time.time()

                    grenade1.grenadeYch = 2
                    lachesisYch = 0
                    
            if event.key == pygame.K_SPACE:

                for i in range(0, 8):
                    if whole_bullet[i].bullet_launch_code == -1:
                        lachesis_strength = 200
                        whole_bullet[i].bullet_launch_code = 0
                        activation_code = 1

                    if whole_bullet[i].bullet_launch_code2 == -1:
                        lachesis_strength = 200
                        whole_bullet[i].bullet_launch_code2 = 0
                        activation_code2 = 2

                    if whole_bullet[i].bullet_launch_code3 == -1:
                        lachesis_strength = 200
                        whole_bullet[i].bullet_launch_code3 = 0
                        activation_code3 = 3

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_w:
                lachesisYch = 0
                if lachesis_confirm == 1:
                    wind_up.wind_activator = 0

            if event.key == pygame.K_s:
                lachesisYch = 0
                if lachesis_confirm == 1:
                    wind_down.wind_activator = 0

            if event.key == pygame.K_a:
                if pause == 0:
                    lachesisXch = 0
                    if lachesis_confirm == 1:
                        wind_nega.wind_activator = 0

            if event.key == pygame.K_d:
                if pause == 0:
                    lachesisXch = 0
                    if lachesis_confirm == 1:
                        wind_posi.wind_activator = 0

            if event.key == pygame.K_SPACE:
                if lachesis_confirm == 1:
                    score_degrader = 15
                    if not collision_checker:
                        lachesis_strength = 200

            if event.key == pygame.K_p:
                pause = 1
                rabbit_threshold = 1000
                lachesisYch = 0

            if event.key == pygame.K_r:
                pause = 0
                rabbit_threshold = 20
                lachesisYch = 0

        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos

        if event.type == pygame.MOUSEBUTTONUP:

            if 328 <= mouseX <= 486 and 422 <= mouseY <= 465:

                if lachesis_confirm == -1 and shop_activator != 1:
                    lachesis_confirm = 1

            if 560 <= mouseX <= 690 and 420 <= mouseY <= 466:

                if lachesis_confirm == -1:
                    shop_activator = 1
                    headstartshopX = 100
                    headstartstatusX = 120
                    magnetshopX = 375
                    magnetstatusX = 395
                    shieldshopX = 650
                    shieldstatusX = 670

            if shop_activator == 1:
                if 25 <= mouseX <= 106 and 10 <= mouseY <= 72:
                    if lachesis_confirm == -1:
                        BG = pygame.image.load("TITLE_PAGE.png")
                        headstartshopX = 10000
                        headstartstatusX = 10000
                        magnetshopX = 10000
                        magnetstatusX = 10000
                        shieldshopX = 10000
                        shieldstatusX = 10000
                        shop_activator = 0
                    if lachesis_confirm == 0:
                        BG = pygame.image.load("bigbg.png")
                        headstartshopX = 10000
                        headstartstatusX = 10000
                        magnetshopX = 10000
                        magnetstatusX = 10000
                        shieldshopX = 10000
                        shieldstatusX = 10000
                        shop_activator = 0

                if 120 <= mouseX <= 320 and 300 <= mouseY <= 376:

                    if headstart_level == "4":
                        if coin_amount > 5000:
                            headstart_level = "5"
                            coin_amount -= 5000

                    if headstart_level == "3":
                        if coin_amount > 4000:
                            headstart_level = "4"
                            coin_amount -= 4000

                    if headstart_level == "2":
                        if coin_amount > 3000:
                            headstart_level = "3"
                            coin_amount -= 3000

                    if headstart_level == "1":
                        if coin_amount > 2000:
                            headstart_level = "2"
                            coin_amount -= 2000

                if 395 <= mouseX <= 595 and 300 <= mouseY <= 376:

                    if magnet_level == "4":
                        if coin_amount > 5000:
                            magnet_level = "5"
                            coin_amount -= 5000

                    if magnet_level == "3":
                        if coin_amount > 4000:
                            magnet_level = "4"
                            coin_amount -= 4000

                    if magnet_level == "2":
                        if coin_amount > 3000:
                            magnet_level = "3"
                            coin_amount -= 3000

                    if magnet_level == "1":
                        if coin_amount > 2000:
                            magnet_level = "2"
                            coin_amount -= 2000

                if 670 <= mouseX <= 870 and 300 <= mouseY <= 376:

                    if shield_level == "4":
                        if coin_amount > 5000:
                            shield_level = "5"
                            coin_amount -= 5000

                    if shield_level == "3":
                        if coin_amount > 4000:
                            shield_level = "4"
                            coin_amount -= 4000

                    if shield_level == "2":
                        if coin_amount > 3000:
                            shield_level = "3"
                            coin_amount -= 3000

                    if shield_level == "1":
                        if coin_amount > 2000:
                            shield_level = "2"
                            coin_amount -= 2000

            if RETRY == 1:
                if 220 <= mouseX <= 320 and 250 <= mouseY <= 350 and shop_activator != 1:
                    lachesis_confirm = 1
                    lachesis_strength = 200
                    grenade_activator = 0
                    RETRY = 0
                    score = 0

                if 560 <= mouseX <= 692 and 420 <= mouseY <= 466:
                    shop_activator = 1
                    headstartshopX = 100
                    headstartstatusX = 120
                    magnetshopX = 375
                    magnetstatusX = 395
                    shieldshopX = 650
                    shieldstatusX = 670

            if lachesis_confirm == 1:
                if 950 <= mouseX <= 1000 and 653 <= mouseY <= 700:
                    if resume_button_active == 1:
                        pause = 1
                        resume_button_active = 0
                        pause_button_active = 1
                        lachesisYch = 0
                        grenade1.grenadeYch = 0
                        rabbit_threshold = 1000

                    elif pause_button_active == 1:
                        pause = 0
                        resume_button_active = 1
                        pause_button_active = 0
                        lachesisYch = 0
                        grenade1.grenadeYch = 2
                        rabbit_threshold = 20
    if lachesis_confirm == 1:

        BG = pygame.image.load("bigbg.png").convert()

        for i in range(0, tiles):
            screen.blit(BG, (i * 2000 + scroll, 0))
        scroll -= bg_speed

        if abs(scroll) > 2000:
            scroll = 0

        if head1.access_on:
            if pause == 0:
                if time.time() - headstart_ontime < headstart_cooltime + difference and score > 10:
                    powerful()
                    bg_speed = 50
                    grenade_degrader = 0
                    score_degrader = 0

                if time.time() - headstart_ontime > headstart_cooltime + difference and score > 10:
                    score_degrader = 15
                    grenade_degrader = 30
                    bg_speed = 2
                    head1.access_on = False
            if pause == 1:
                difference = time.time()
                powerful()
                bg_speed = 50
                grenade_degrader = 0
                score_degrader = 0
        else:
            difference = 0

        if shield1.access_on:
            if pause == 0:
                if time.time() - shield_ontime < shield_cooltime + difference1 and score > 10:
                    powerful()
                    grenade_degrader = 0
                    score_degrader = 0

                if time.time() - shield_ontime > shield_cooltime + difference1 and score > 10:
                    score_degrader = 15
                    grenade_degrader = 30
                    shield1.access_on = False
            if pause == 1:
                difference1 = time.time()
                powerful()
                bg_speed = 50
                grenade_degrader = 0
                score_degrader = 0
        else:
            difference1 = 0

        lachesislauncher(lachesisX, lachesisY)

        # WIND PROPERTIES

        screen.blit(wind_maker, (lachesisX, 670))
        screen.blit(wind_maker2, (lachesisX, 0))
        screen.blit(wind_maker3, (0, lachesisY))
        screen.blit(wind_maker4, (970, lachesisY))
        wind_up.draw(lachesisX + 60, 35, 1, lachesisY, 1)
        wind_up.checker(600, 1)
        wind_down.draw(lachesisX + 60, 570, 2, lachesisY, 1)
        wind_down.checker(30, 1)
        wind_posi.draw(800, lachesisY + 30, 3, lachesisX, 2)
        wind_posi.checker(30, 2)
        wind_nega.draw(35, lachesisY + 30, 4, lachesisX, 2)
        wind_nega.checker(970, 2)

        if wind_up.wind_activator == 0:
            screen.blit(gravity1, (lachesisX, 670))
        if wind_down.wind_activator == 0:
            screen.blit(gravity1, (lachesisX, 24))
        if wind_posi.wind_activator == 0:
            screen.blit(gravity2, (24, lachesisY))
        if wind_nega.wind_activator == 0:
            screen.blit(gravity2, (970, lachesisY))

        if parallel_universe_operator == 0:
            explode_1.draw(grenade1.Xvalue_get, grenade1.Yvalue_get + 20)
            explode_1.update_animation()

        score_font()

        for i in gun_list:
            i.draw()

        pause_resume_button()

        # RABBIT ACTIVATION

        if score % rabbit_threshold == 0:
            RabbitX = 1100
        rabbit1.update_animation()
        rabbit1.draw()
        rabbit1.collision_checker()

        # GRENADE ACTIVATION

        if score == 10:
            if grenade_activator == 0:
                grenade1.activate()
                grenade_activator = 1

        grenade1.draw()
        grenade1.checker()
        grenade1.runner()
        grenade1.collision_checker()

        head1.checker(100)
        head1.draw_access()
        head1.collision_checker(2)
        headstart_timemanager()

        magnet1.checker(126)
        magnet1.draw_access()
        magnet1.collision_checker(3)
        magnet_timemanager()

        shield1.draw_access()
        shield1.checker(50)
        shield1.collision_checker(1)
        shield_timemanager()

        if pause == 0:
            RabbitX -= 10

        if activation_code != -1:

            whole_bullet[activation_code].checker(whole_bullet[activation_code].bulletX, RETRY, 1)
            whole_bullet[activation_code].activator(1)
            whole_bullet[activation_code].draw(1)
            whole_bullet[activation_code].collision_detector(1)
            whole_bullet[activation_code].activity_decider()

        if activation_code2 != -1:

            whole_bullet[activation_code2].checker(whole_bullet[activation_code2].bulletX, RETRY, 2)
            whole_bullet[activation_code2].activator(2)
            whole_bullet[activation_code2].draw(2)
            whole_bullet[activation_code2].collision_detector(2)
            whole_bullet[activation_code2].activity_decider()

        if activation_code3 != -1:

            whole_bullet[activation_code3].checker(whole_bullet[activation_code3].bulletX, RETRY, 3)
            whole_bullet[activation_code3].activator(3)
            whole_bullet[activation_code3].draw(3)
            whole_bullet[activation_code3].collision_detector(3)
            whole_bullet[activation_code3].activity_decider()

        pygame.draw.rect(screen, (0, 0, 255), (health_barX, 10, 200, 10))
        pygame.draw.rect(screen, (255, 0, 0), (health_barX, 10, lachesis_strength, 10))

    lachesisY += lachesisYch
    lachesisX += lachesisXch

    if lachesisX <= 35:
        lachesisX = 35

    if lachesisX >= 640:
        lachesisX = 640

    if lachesisY <= 35:
        lachesisY = 35

    if lachesisY >= 570:
        lachesisY = 570

    if lachesis_strength <= 0:
        lachesis_confirm = 0
        score_degrader = 0
        grenade1.deactivate()
        collision_checker = False
        if RETRY == -1 or RETRY == 0:
            RETRY = 1

        for i in range(0, 8):
            whole_bullet[i].bullet_launch_code = -1
            whole_bullet[i].bullet_launch_code2 = -1
            whole_bullet[i].bullet_launch_code3 = -1
        if shop_activator == 0:
            screen.blit(retry_button, (retryX, retryY))
            screen.blit(shop_button, (shopX, shopY))

    if score % 30 == 0 and score > 5 and score_tracker != score:
        coin_motion = 1
        code_gen = 0
        coin_constant = 0
        coin_code_generator()
        coin_maker()
        score_tracker = score

    if coin_motion == 1:
        for i in coin_list:
            if score > 10 and RETRY != 1:
                screen.blit(coin_img, i)
            if pause == 0:
                i[0] -= coin_velocity
            offset = (lachesisX - i[0], lachesisY - i[1])
            result = coin_mask.overlap(lachesis_mask, offset)
            distance = math.sqrt(abs((math.pow((lachesisX - i[0]), 2) - math.pow((lachesisY - i[1]), 2))))
            if magnet1.access_on:
                if pause == 0:
                    if time.time() - magnet_ontime < magnet_cooltime + difference2 and score > 10:
                        if distance < 400:
                            coin_velocity = 30
                            i[1] = lachesisY
                else:
                    difference2 = time.time()

            else:
                coin_velocity = 6

            if result:
                i[0] = -50
                coin_amount += 1
            if i[0] < -1000:
                coin_list = []
                coin_motion = 0

    if shop_activator == 1:
        coin_font()
        BG = shop_bg
        if headstart_level == "1":
            screen.blit(headstart_lv1, (headstartshopX, headstartshopY))
            screen.blit(update_lv2, (headstartstatusX, headstartstatusY))
        if magnet_level == "1":
            screen.blit(magnet_lv1, (magnetshopX, magnetshopY))
            screen.blit(update_lv2, (magnetstatusX, magnetstatusY))
        if shield_level == "1":
            screen.blit(shield_lv1, (shieldshopX, shieldshopY))
            screen.blit(update_lv2, (shieldstatusX, shieldstatusY))

        if headstart_level == "2":
            screen.blit(headstart_lv2, (headstartshopX, headstartshopY))
            screen.blit(update_lv3, (headstartstatusX, headstartstatusY))
        if magnet_level == "2":
            screen.blit(magnet_lv2, (magnetshopX, magnetshopY))
            screen.blit(update_lv3, (magnetstatusX, magnetstatusY))
        if shield_level == "2":
            screen.blit(shield_lv2, (shieldshopX, shieldshopY))
            screen.blit(update_lv3, (shieldstatusX, shieldstatusY))

        if headstart_level == "3":
            screen.blit(headstart_lv3, (headstartshopX, headstartshopY))
            screen.blit(update_lv4, (headstartstatusX, headstartstatusY))

        if magnet_level == "3":
            screen.blit(magnet_lv3, (magnetshopX, magnetshopY))
            screen.blit(update_lv4, (magnetstatusX, magnetstatusY))

        if shield_level == "3":
            screen.blit(shield_lv3, (shieldshopX, shieldshopY))
            screen.blit(update_lv4, (shieldstatusX, shieldstatusY))

        if headstart_level == "4":
            screen.blit(headstart_lv4, (headstartshopX, headstartshopY))
            screen.blit(update_lv5, (headstartstatusX, headstartstatusY))

        if magnet_level == "4":
            screen.blit(magnet_lv4, (magnetshopX, magnetshopY))
            screen.blit(update_lv5, (magnetstatusX, magnetstatusY))

        if shield_level == "4":
            screen.blit(shield_lv4, (shieldshopX, shieldshopY))
            screen.blit(update_lv5, (shieldstatusX, shieldstatusY))

        if headstart_level == "5":
            screen.blit(headstart_lv5, (headstartshopX, headstartshopY))

        if magnet_level == "5":
            screen.blit(magnet_lv5, (magnetshopX, magnetshopY))

        if shield_level == "5":
            screen.blit(shield_lv5, (shieldshopX, shieldshopY))

    pygame.display.update()

pygame.quit()

coin_file = open("coin_amt.txt", "w")
coin_file.write(str(coin_amount))
coin_file.close()

commodity_list = [["headstart", headstart_level, "2000", "3000", "4000", "5000", "6000"],
                  ["magnet", magnet_level, "2000", "3000", "4000", "5000", "6000"],
                  ["shield", shield_level, "2000", "3000", "4000", "5000", "6000"]]

final_detail = open("shop_details.csv", "w", newline='')
detail_writer = csv.writer(final_detail)
detail_writer.writerows(commodity_list)
final_detail.close()
