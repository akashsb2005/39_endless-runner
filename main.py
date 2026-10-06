import pygame
from game.game_engine import GameEngine


pygame.init()

WIDTH, HEIGHT = 800, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner - Pygame Version")

SKY = (200, 220, 240)

clock = pygame.time.Clock()
FPS = 60


def main():
    engine = GameEngine(WIDTH, HEIGHT)
    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if engine.game_over:
                    if event.key in (
                        pygame.K_SPACE,
                        pygame.K_RETURN,
                        pygame.K_ESCAPE
                    ):
                        running = False
                else:
                    engine.handle_event(event)

        SCREEN.fill(SKY)

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()