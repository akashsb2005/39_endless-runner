import pygame

from game.game_engine import GameEngine


pygame.init()

WIDTH = 800
HEIGHT = 400
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner")

clock = pygame.time.Clock()

game = GameEngine(WIDTH, HEIGHT)

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            continue

        result = game.handle_event(event)

        if result == "quit":
            running = False

    game.update()

    screen.fill((220, 240, 255))

    game.render(screen)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()