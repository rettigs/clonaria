#!/usr/bin/env python

import sys, time, pygame
from entity import Entity
from model import Model
#from entityModel import EntityModel
#from entity import Entity
from util import Util
from world import World



def main():
    pygame.init()

    size = width, height = 640, 480
    speed = [2, 2]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    fakeplayer = pygame.image.load("resources/images/entity/player.png")
    fakeplayerrect = fakeplayer.get_rect()

    world = World("world1", (1000, 1000))
    world.generate()

    player = Entity("player", world.name, (world.width / 2, world.height / 2 + 1))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

    #    ballrect = ballrect.move(speed)
    #    if ballrect.left < 0 or ballrect.right > width:
    #        speed[0] = -speed[0]
    #    if ballrect.top < 0 or ballrect.bottom > height:
    #        speed[1] = -speed[1]

        screen.fill(black)
        screen.blit(fakeplayer, fakeplayerrect)
        pygame.display.flip()
        time.sleep(0.01)

    def display_box(screen, message):
        fontobject=pygame.font.SysFont('Arial', 18)
        if len(message) != 0:
            screen.blit(fontobject.render(message, 1, (255, 255, 255)),
                    ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
        pygame.display.flip()

if __name__ == '__main__':
    main()
