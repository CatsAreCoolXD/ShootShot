#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

import pygame
import pygame.mixer as mixer
import numpy
import math
import random

pygame.init()
mixer.init()

explosionS = mixer.Sound("sfx/explosion.wav")
coinSo = mixer.Sound("sfx/coin.wav")
coinSo.set_volume(50)
failS = mixer.Sound("sfx/fail.wav")
musicS = mixer.Sound("sfx/music.wav")
musicS.set_volume(0.5)

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)


class Player:
    def __init__(self, pos: tuple, gravity: tuple, sprite: pygame.Surface, maxVel, minVel, maxVelY):
        self.pos = pos
        self.velocity = (0, 0)
        self.gravity = gravity
        self.sprite = sprite
        self.maxVel = maxVel
        self.minVel = minVel
        self.maxVelY = maxVelY

    def addForce(self, force: tuple):
        self.velocity = numpy.add(self.velocity, force)

    def resetVelocity(self):
        self.velocity = (0, 0)

    def update(self):
        global scene, highscore, score, playerrect, failS
        self.velocity = numpy.add(self.velocity, (0, self.gravity / 10))
        if self.velocity[0] > self.maxVel:
            self.velocity[0] = self.maxVel
        elif self.velocity[0] < self.minVel:
            self.velocity[0] = self.minVel
        if self.velocity[1] > self.maxVelY:
            self.velocity[1] = self.maxVelY

        self.pos = numpy.subtract(self.pos, self.velocity)
        if self.pos[1] < -50:
            self.pos[1] += 770
        elif self.pos[1] > 770:
            scene = menu
            self.pos = (
            self.sprite.get_rect(center=(1280 / 2, 720 / 2))[0], self.sprite.get_rect(center=(1280 / 2, 720 / 2))[1])
            if highscore < score:
                highscore = score
            failS.play()
        if self.pos[0] < 0:
            self.pos[0] += 1330
        if self.pos[0] > 1280:
            self.pos[0] -= 1330

    def draw(self):
        global shotgun, paused, angle
        screen.blit(self.sprite, self.pos)
        if not paused:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - self.pos[0], mouse_y - self.pos[1]
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        rotshotgun = pygame.transform.rotate(shotgun, int(angle))
        screen.blit(rotshotgun, (self.pos[0] + 50, self.pos[1] + 50))


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 2)


player = pygame.image.load("other/player.png").convert_alpha()
player = pygame.transform.scale(player, (100, 100))
player = Player((590, 310), -9.81, player, 10, -10, 20)
background = pygame.transform.scale(pygame.image.load("other/background.png").convert_alpha(), (1280, 720))
background.set_alpha(99)
clock = pygame.time.Clock()
new_velocity = (0, 0)
game = 0
menu = 1
scene = menu
angle = 0
shotgun = pygame.image.load("other/shotgun.png").convert_alpha()
shotgun = pygame.transform.scale(shotgun, (83, 66))
pausemenu = pygame.image.load("other/pause.png").convert_alpha()
pygame.font.init()
font = pygame.font.Font("font/AlfaSlabOne-Regular.ttf", 150)
font2 = pygame.font.Font("font/PoorStory-Regular.ttf", 50)
font3 = pygame.font.SysFont("Arial", 350)
font4 = pygame.font.Font("font/Nunito-Black.ttf", 75)
titel = font.render("ShootShot", True, (0, 255, 0))
clicktext = font2.render("Click to start!", True, (0, 0, 0))
scoretext = font3.render("0", True, (0, 0, 0))
with open("other/highscore.txt", "r") as f:
    highscore = f.read()
    highscore.replace("\n", "")
highscore = int(highscore)
highscoretext = font4.render(f"Highscore: {highscore}", True, (0, 0, 0))
coins = []
for x in range(6):
    coins.append(pygame.transform.scale(pygame.image.load(f"coin/coin{x + 1}.png"), (50, 50)))
number = 0
particles = []
colors = [(255, 0, 0),
          (0, 0, 255),
          (255, 255, 0),
          (255, 0, 255),
          (0, 255, 255),
          (255, 125, 0),
          (125, 255, 0),
          (0, 255, 125),
          (0, 125, 255),
          (125, 0, 255)]
r = True
scoretext.set_alpha(75)
scoretext = scoretext.convert_alpha()
coinLocation = (random.randint(50, 1230), random.randint(50, 670))
titlerect = titel.get_rect(center=(1280 / 2, 150))
scorerect = scoretext.get_rect(center=(1280 / 2, 720 / 2))
highscorerect = highscoretext.get_rect(center=(1280 / 2, 50))
number2 = 0
currentCoin = 0
coinrect = pygame.Rect(coinLocation[0], coinLocation[1], 50, 50)
score = 0
explode = False
number3 = 0
clickmousepos = ()
musicS.play(loops=100)
collectedCoin = False
paused = False
decrease = score/2
colorbackgrounds = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (192, 192, 192), (128, 128, 128), (128, 0, 0), (128, 128, 0), (0, 128, 0), (128, 0, 128), (0, 128, 128), (0, 0, 128), (255, 140, 0), (255, 165, 0), (255, 69, 0), (218, 112, 214), (238, 130, 238), (186, 85, 211), (153, 50, 204), (148, 0, 211), (138, 43, 226), (160, 82, 45), (165, 42, 42), (178, 34, 34), (220, 20, 60), (255, 0, 0), (255,105, 180), (255, 20, 147), (255,192, 203), (219,112, 147), (199,21, 133), (176,48, 96), (160,32, 240), (148,0,211), (139,0,139), ( 128,0, 128), (128,0,0), (255, 0, 255), (255,0,0), (220,20, 60), (255, 250, 205), (248, 248, 255), (245, 245, 245), (255, 255, 240), (240, 255, 240), (240, 248, 255), (240, 255, 255), (240, 255, 255), (255, 240, 245), (255, 248, 220), (255, 250, 205), (250, 250, 210), (210, 245, 255), (245, 222, 179), (255, 228, 196), (255, 235, 205), (245, 245, 220), (220, 220, 220), (188, 143, 143), (255,193, 193), (255, 182, 193), (255, 160, 122), (255, 140, 0), (255, 127, 80)]
random.shuffle(colorbackgrounds)
backgroundColor = random.choice(colorbackgrounds)
while r:
    clock.tick(45)
    screen.fill(backgroundColor)
    screen.blit(background, (0,0))
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False
        if event.type == pygame.FULLSCREEN:
            screen = pygame.display.set_mode((1920, 1080))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if scene == game:
                if not paused:
                    new_velocity = numpy.subtract(player.pos, mousePos) * -1
                    player.resetVelocity()
                    player.addForce(new_velocity / 10)
                    explode = True
                    clickmousepos = mousePos
                    explosionS.play()
                else:
                    if mousePos[0] > 290 and mousePos[0] < 1020:
                        if mousePos[1] > 410 and mousePos[1] < 640:
                            paused = False
            elif scene == menu:
                decrease = 0
                coinrect = pygame.Rect(coinLocation[0], coinLocation[1], 50 - decrease, 50 - decrease)
                coins = []
                for x in range(6):
                    coins.append(pygame.transform.scale(pygame.image.load(f"coin/coin{x + 1}.png"),
                                                        (50 - decrease, 50 - decrease)))
                scene = game
                score = 0
                new_velocity = numpy.subtract(player.pos, mousePos) * -1
                player.resetVelocity()
                player.addForce(new_velocity / 10)
                explosionS.play()
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if scene == game:
                if keys[pygame.K_ESCAPE]:
                    if not paused:
                        paused = True
                    else:
                        paused = False
    screen.blit(scoretext, scorerect)
    player.draw()
    if scene == game:
        screen.blit(coins[currentCoin], coinLocation)
        if not paused:
            player.update()
        else:
            screen.blit(pausemenu, (0,0))

        if not paused:
            number2 += 0.15
            currentCoin = math.ceil(number2)
            if currentCoin > 5:
                currentCoin = 0
                number2 = -1
        if collectedCoin:
            if score < 101:
                decrease = (score/2)-5
            else:
                decrease = 45
            backgroundColor = random.choice(colorbackgrounds)
            coinrect = pygame.Rect(coinLocation[0], coinLocation[1], 50 - decrease, 50 - decrease)
            coins = []
            for x in range(6):
                coins.append(pygame.transform.scale(pygame.image.load(f"coin/coin{x + 1}.png"), (50-decrease, 50-decrease)))
            collectedCoin = False
        playerrect = pygame.Rect(player.pos[0], player.pos[1], 100, 100)

        if coinrect.colliderect(playerrect):
            score += 1
            background.map_rgb((255, 0, 0))
            collectedCoin = True
            scoretext = font3.render(str(score), True, (0, 0, 0))
            scoretext.set_alpha(75)
            coinLocation = (random.randint(50, 1230), random.randint(50, 670))
            coinrect = pygame.Rect(coinLocation[0], coinLocation[1], 50 - (score / 2), 50 - (score / 2))
            coinSo.play()
        if explode:
            number3 += 1
            pygame.draw.circle(screen, (255, 0, 0), clickmousepos, number3 * 6)
            pygame.draw.circle(screen, (0, 0, 0), clickmousepos, (number3 * 6 - 35))
            if number3 >= 10:
                explode = False
        else:
            number3 = 0
    elif scene == menu:
        highscoretext = font4.render(f"Highscore: {highscore}", True, (0, 0, 0))
        scoretext = font3.render("0", True, (0, 0, 0))
        scoretext = scoretext.convert_alpha()
        scoretext.set_alpha(75)
        score = 0
        screen.blit(titel, titlerect)
        number += 0.1
        clickTextAddY = math.cos(number) * 30
        screen.blit(clicktext, (525, 600 - clickTextAddY))
        particles.append(Particle(random.randint(250, 1075), random.randint(100, 200), random.choice(colors)))
        for particle in particles:
            particle.draw()
        if len(particles) > 70:
            particles.pop(random.randint(0, len(particles) - 1))
        screen.blit(highscoretext, highscorerect)

    pygame.display.flip()

with open("other/highscore.txt", "w") as f:
    f.write(str(highscore))
pygame.quit()