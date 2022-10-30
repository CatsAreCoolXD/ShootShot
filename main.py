import pygame
import pygame.mixer as mixer
import numpy
import math
import random

pygame.init()
mixer.init()

explosionS = mixer.Sound("sfx/explosion.wav")
coinSo = mixer.Sound("sfx/coin.wav")
failS = mixer.Sound("sfx/fail.wav")
musicS = mixer.Sound("sfx/music.wav")

screen = pygame.display.set_mode((1280, 720))

class Player:
    def __init__(self, pos: tuple, gravity: tuple, sprite: pygame.Surface, maxVel, minVel, maxVelY):
        self.pos = pos
        self.velocity = (0,0)
        self.gravity = gravity
        self.sprite = sprite
        self.maxVel = maxVel
        self.minVel = minVel
        self.maxVelY = maxVelY

    def addForce(self, force: tuple):
        self.velocity = numpy.add(self.velocity, force)

    def resetVelocity(self):
        self.velocity = (0,0)

    def update(self):
        global scene, highscore, score, playerrect, failS
        self.velocity = numpy.add(self.velocity, (0, self.gravity/10))
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
            self.pos = (self.sprite.get_rect(center=(1280/2, 720/2))[0], self.sprite.get_rect(center=(1280/2, 720/2))[1])
            if highscore < score:
                highscore = score
            failS.play()
        if self.pos[0] < 0:
            self.pos[0] += 1330
        if self.pos[0] > 1280:
            self.pos[0] -= 1330


    def draw(self):
        global shotgun
        screen.blit(self.sprite, self.pos)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.pos[0], mouse_y - self.pos[1]
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        rotshotgun = pygame.transform.rotate(shotgun, int(angle))
        screen.blit(rotshotgun, (self.pos[0]+50, self.pos[1]+50))


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 10, 10))
player = pygame.image.load("other/player.png").convert_alpha()
player = pygame.transform.scale(player, (100, 100))
player = Player((590, 310), -9.81, player, 10, -10, 20)
clock = pygame.time.Clock()
new_velocity = (0,0)
game = 0
menu = 1
scene = menu
shotgun = pygame.image.load("other/shotgun.png").convert_alpha()
shotgun = pygame.transform.scale(shotgun, (83, 66))
pygame.font.init()
font = pygame.font.Font("font/AlfaSlabOne-Regular.ttf", 150)
font2 = pygame.font.Font("font/PoorStory-Regular.ttf", 50)
font3 = pygame.font.SysFont("Arial", 350)
font4 = pygame.font.Font("font/Nunito-Black.ttf", 75)
titel = font.render("ShootShot", True, (0, 255, 0))
clicktext = font2.render("Click to start!", True, (0,0,0))
scoretext = font3.render("0", True, (0,0,0))
with open("other/highscore.txt", "r") as f:
    highscore = f.read()
    highscore.replace("\n", "")
highscore = int(highscore)
highscoretext = font4.render(f"Highscore: {highscore}", True, (0,0,0))
coins = []
for x in range(6):
    coins.append(pygame.transform.scale(pygame.image.load(f"coin/coin{x+1}.png"), (50, 50)))
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
titlerect = titel.get_rect(center=(1280/2, 150))
scorerect = scoretext.get_rect(center=(1280/2, 720/2))
highscorerect = highscoretext.get_rect(center=(1280/2, 50))
number2 = 0
currentCoin = 0
coin = pygame.Rect(coinLocation[0], coinLocation[1], 50, 50)
score = 0
explode = False
number3 = 0
clickmousepos = ()
musicS.play(loops=100)
while r:
    clock.tick(45)
    screen.fill((255,255,255))
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if scene == game:
                new_velocity = numpy.subtract(player.pos, mousePos)*-1
                player.resetVelocity()
                player.addForce(new_velocity/10)
                explode = True
                clickmousepos = mousePos
                explosionS.play()
            else:
                scene = game
                score = 0
                new_velocity = numpy.subtract(player.pos, mousePos) * -1
                player.resetVelocity()
                player.addForce(new_velocity / 10)
                explosionS.play()
    screen.blit(scoretext, scorerect)
    player.draw()
    if scene == game:
        player.update()
        screen.blit(coins[currentCoin], coinLocation)
        number2 += 0.15
        currentCoin = math.ceil(number2)
        if currentCoin > 5:
            currentCoin = 0
            number2 = -1
        playerrect = pygame.Rect(player.pos[0], player.pos[1], 100, 100)
        if coin.colliderect(playerrect):
            score += 1
            scoretext = font3.render(str(score), True, (0, 0, 0))
            scoretext.set_alpha(75)
            coinLocation = (random.randint(50, 1230), random.randint(50, 670))
            coin = pygame.Rect(coinLocation[0], coinLocation[1], 50, 50)
            coinSo.play()
        if explode:
            number3 += 1
            pygame.draw.circle(screen, (255, 0, 0), clickmousepos, number3*6)
            pygame.draw.circle(screen, (0, 0, 0), clickmousepos, (number3*6-35))
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
        clickTextAddY = math.cos(number)*30
        screen.blit(clicktext, (525, 600-clickTextAddY))
        particles.append(Particle(random.randint(250, 1075), random.randint(100, 200), random.choice(colors)))
        for particle in particles:
            particle.draw()
        if len(particles) > 70:
            particles.pop(random.randint(0, len(particles)-1))
        screen.blit(highscoretext, highscorerect)

    pygame.display.flip()

with open("other/highscore.txt", "w") as f:
    f.write(str(highscore))
pygame.quit()