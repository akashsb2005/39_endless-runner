import pygame
from .player import Player
from .obstacle import Obstacle


WHITE = (255, 255, 255)
BROWN = (120, 80, 40)
DARK_GREEN = (30, 100, 30)
RED = (200, 0, 0)
BLACK = (0, 0, 0)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 40

        self.player = Player(80, self.ground_y)

        self.speed = 6
        self.speed_increase_per_frame = 0.003
        self.max_speed = 12

        self.spawn_interval = 70
        self._spawn_timer = 0
        self.obstacles = []

        self.distance = 0
        self.score = 0

        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont(
            "Arial",
            64,
            bold=True
        )
        self.game_over_score_font = pygame.font.SysFont(
            "Arial",
            36,
            bold=True
        )
        self.game_over_instruction_font = pygame.font.SysFont(
            "Arial",
            24
        )

        self.game_over = False
        self.final_score = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
        if event.key in (
            pygame.K_SPACE,
            pygame.K_UP,
            pygame.K_w
        ):
            self.player.jump()

        if self.game_over:
            if event.key in (
                pygame.K_SPACE,
                pygame.K_RETURN,
                pygame.K_ESCAPE
            ):
                return "quit"

            return None

        if event.key in (
            pygame.K_SPACE,
            pygame.K_UP,
            pygame.K_w
        ):
            self.player.jump()

        return None

    def handle_input(self):
        pass

    def update(self):
        if self.game_over:
            return

        self.speed = min(
            self.speed + self.speed_increase_per_frame,
            self.max_speed
        )

        self.player.update()

        self._spawn_timer += 1

        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0

            self.obstacles.append(
                Obstacle(
                    self.width,
                    self.ground_y,
                    self.speed
                )
            )

        for obstacle in self.obstacles:
            obstacle.move()
            obstacle.speed = self.speed

        for obstacle in self.obstacles:
            if obstacle.rect().colliderect(self.player.rect()):
                self.game_over = True
                self.final_score = self.score
                return

        for obstacle in self.obstacles:
            if (
                not obstacle.scored
                and obstacle.x + obstacle.width < self.player.x
            ):
                obstacle.scored = True
                self.score += 1

        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if not obstacle.off_screen()
        ]

        self.distance += self.speed

    def render(self, screen):
        pygame.draw.line(
            screen,
            BROWN,
            (0, self.ground_y),
            (self.width, self.ground_y),
            4
        )

        pygame.draw.rect(
            screen,
            WHITE,
            self.player.rect()
        )

        for obstacle in self.obstacles:
            pygame.draw.rect(
                screen,
                DARK_GREEN,
                obstacle.rect()
            )

        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            BLACK
        )

        screen.blit(
            score_text,
            (10, 10)
        )

        if self.game_over:
            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 140)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            game_over_text = self.game_over_font.render(
                "GAME OVER",
                True,
                RED
            )

            final_score_text = self.game_over_score_font.render(
                f"Final Score: {self.final_score}",
                True,
                WHITE
            )

            instruction_text = self.game_over_instruction_font.render(
                "Press SPACE, ENTER or ESC to exit",
                True,
                WHITE
            )

            game_over_rect = game_over_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 - 70
                )
            )

            final_score_rect = final_score_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2
                )
            )

            instruction_rect = instruction_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 + 60
                )
            )

            screen.blit(
                game_over_text,
                game_over_rect
            )

            screen.blit(
                final_score_text,
                final_score_rect
            )

            screen.blit(
                instruction_text,
                instruction_rect
            )