# Aleksandra Półtorak Projekt 2
import pygame
from pygame.math import *
import math

windowWidth = 1200  # szerokosc okna
windowHeight = 800  # wysokosc okna

FPS = 60
planetCenter = Vector2(int(windowWidth / 2), int(windowHeight / 2))
planetRadius = 90
planetMass = 800
planetAngularVelocity = 0

PLAYER_MIN_SPEED = -5
PLAYER_SPEED = 0.035
PLAYER_JUMP = 2.5

ORBITING_OBJECT_SPEED = 0.025

class Physics(object):
    G = -1
    characterMass = 1


class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('character.png').convert_alpha()

        # okreslenie wielkosci i masy bohatera
        self.width = 25
        self.halfWidth = self.width / 2
        self.height = 25
        self.halfHeight = self.height / 2
        self.size = (self.width, self.height)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.mass = Physics.characterMass

        self.angle = 0
        self.prevAngle = 0
        self.angularVelocity = 0
        self.radius = planetRadius + self.halfHeight
        self.radialVelocity = 0
        self.onGround = False
        self.direction = 'right'

        # okreslenie pozycji bohatera
        self.position = Vector2()
        self.position.x = planetCenter.x + self.radius * math.sin(self.angle)
        self.position.y = planetCenter.y - 20 + self.radius * -math.cos(self.angle)
        self.prevPosition = Vector2()
        self.nextPosition = Vector2()

        self.acceleration = Vector2(0, 0)
        # okreslenie predkosci poruszania sie bohatera
        self.velocity = Vector2(0, 0)
        self.nextVelocity = Vector2()

        # zmienna opisujaca czy gracz chce wykonac skok
        self.isGoingToJump = False

    def updateMovement(self, step):
        angle = self.angle
        self.prevAngle = angle
        # print("prevAngle ", math.degrees(self.prevAngle))
        position = self.position
        self.prevPosition = position
        # print("PREV position = ", self.prevPosition)

        dx = self.position.x - planetCenter.x
        dy = self.position.y - planetCenter.y

        r = math.sqrt(dx ** 2 + dy ** 2)
        g = Physics.G * self.mass * planetMass / r ** 2

        self.radialVelocity += g
        if (self.radialVelocity < PLAYER_MIN_SPEED):
            self.radialVelocity = PLAYER_MIN_SPEED
        self.radius += self.radialVelocity

        # print("radius ", self.radius)

        bottom = self.radius - self.halfHeight
        self.onGround = False

        if (bottom <= planetRadius):
            self.onGround = True
            self.radius = planetRadius + self.halfHeight
            self.radialVelocity = 0

        if self.onGround == True and self.direction == 'none':
            self.angularVelocity = 0
        self.angle += self.angularVelocity * planetRadius / self.radius
        # print("angle ", self.angle)
        # print("angle ", math.degrees(self.angle))
        if (math.degrees(self.angle) >= 360.0):
            self.angle = 0.0

        # self.position.x = planetCenter.x + self.radius * math.sin(self.angle)
        # self.position.y = planetCenter.y + self.radius * -math.cos(self.angle)
        newPosition = Vector2()
        newPosition.x = planetCenter.x + self.radius * math.sin(self.angle)
        newPosition.y = planetCenter.y + self.radius * -math.cos(self.angle)

        positionChange = newPosition - position
        # print("positionChange = ", positionChange)

        self.position.x += positionChange.x * step
        self.position.y += positionChange.y * step

    def moveLeft(self):
        self.direction = 'left'
        self.angularVelocity = -PLAYER_SPEED

    def moveRight(self):
        self.direction = 'right'
        self.angularVelocity = PLAYER_SPEED

    def jump(self):
        if self.onGround == True:
            self.radialVelocity = PLAYER_JUMP

    def stop(self):
        self.direction = 'none'

    def draw(self, gameDisplay):

        positionX = self.position.x - self.halfWidth
        positionY = self.position.y - self.halfHeight
        self.rect.x = positionX
        self.rect.y = self.position.y
        characterPosition = Vector2(positionX, positionY)

        gameDisplay.blit(self.image, characterPosition)


class OrbitingObject(object):
    def __init__(self):
        self.radius = 30
        self.color = (138, 146, 152)
        self.image = pygame.image.load('orbiting.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))

        self.position = Vector2()

        self.prevRadius = self.radius
        self.radialVelocity = 0
        self.angularVelocity = 0

        self.angle = 0

    def updateMovement(self):
        self.prevRadius = self.radius
        self.radialVelocity += Physics.G
        self.angularVelocity = -ORBITING_OBJECT_SPEED

        if (self.radialVelocity < PLAYER_MIN_SPEED):
            self.radialVelocity = PLAYER_MIN_SPEED
        self.radius += self.radialVelocity

        self.radius = planetRadius + 200
        self.angle += self.angularVelocity * planetRadius / self.radius
        # print("angle ", self.angle)

        self.position.x = planetCenter.x + self.radius * math.sin(self.angle)
        self.position.y = planetCenter.y + self.radius * -math.cos(self.angle)

    def draw(self, gameDisplay):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), int(self.radius), 1)
        gameDisplay.blit(self.image, self.position)


class Planet(object):
    def __init__(self):
        self.radius = planetRadius
        self.color = (138, 146, 152)
        self.image = pygame.image.load('planet2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))

        self.mass = planetMass
        self.center = planetCenter
        self.position = Vector2(planetCenter.x - self.radius, planetCenter.y - self.radius)

        self.angularVelocity = planetAngularVelocity

        print(self.position)

    def draw(self, gameDisplay):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), int(self.radius), 1)
        gameDisplay.blit(self.image, self.position)


class Game(object):
    def __init__(self):
        pygame.init()  # inicjalizacja PyGame
        # ustawienie wielkosci okna gry
        self.displayWidth = windowWidth
        self.displayHeight = windowHeight
        self.gameDisplay = pygame.display.set_mode((self.displayWidth, self.displayHeight))
        # ustawienie tytulu okna
        pygame.display.set_caption('Projekt 2 - Aleksandra Półtorak')

        self.bg_image = pygame.image.load('bg_img.jpg')
        self.gameDisplay.fill((0, 0, 0))

        # zegar
        self.clock = pygame.time.Clock()

        self.character = Character()  # utworzenie bohatera
        self.planet = Planet()
        self.orbitingObject = OrbitingObject()
        self.playingGame = True
        self.gameOver = False

        self.step = 0.0

    def gameLoop(self):

        while self.playingGame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playingGame = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.character.stop()
                if event.type == pygame.KEYDOWN:
                    # jesli gra sie nie skonczyla to reaguj na nacisniecie klawiszy
                    if self.gameOver == False:
                        if event.key == pygame.K_LEFT:
                            self.character.moveLeft()
                        if event.key == pygame.K_RIGHT:
                            self.character.moveRight()
                        if event.key == pygame.K_UP:
                            self.character.jump()

                    if event.key == pygame.K_ESCAPE:
                        self.playingGame = False

            self.gameDisplay.blit(self.bg_image, (0, 0))

            self.character.updateMovement(self.step)
            self.orbitingObject.updateMovement()
            self.orbitingObject.draw(self.gameDisplay)
            self.planet.draw(self.gameDisplay)
            self.character.draw(self.gameDisplay)
            pygame.display.update()
            self.step += 0.001
            self.clock.tick(FPS)


game = Game()
game.gameLoop()

pygame.quit()
quit()
