import pygame
from pathlib import Path

from .player import Player
from .obstacle import Obstacle


WHITE = (255, 255, 255)
BROWN = (120, 80, 40)
DARK_GREEN = (30, 100, 30)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
GREEN = (50, 180, 80)
YELLOW = (220, 180, 40)


class GameEngine:

    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.ground_y = height - 40

        self.player = Player(80, self.ground_y)

        self.difficulties = {
            "Easy": {
                "speed": 4,
                "spawn_interval": 90
            },
            "Medium": {
                "speed": 6,
                "spawn_interval": 70
            },
            "Hard": {
                "speed": 8,
                "spawn_interval": 50
            }
        }

        self.current_difficulty = "Medium"

        self.speed = self.difficulties[
            self.current_difficulty
        ]["speed"]

        self.speed_increase_per_frame = 0.003
        self.max_speed = 12

        self.spawn_interval = self.difficulties[
            self.current_difficulty
        ]["spawn_interval"]

        self._spawn_timer = 0
        self.obstacles = []

        self.distance = 0
        self.score = 0

        self.font = pygame.font.SysFont(
            "Arial",
            30
        )

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

        self.difficulty_title_font = pygame.font.SysFont(
            "Arial",
            48,
            bold=True
        )

        self.difficulty_font = pygame.font.SysFont(
            "Arial",
            32,
            bold=True
        )

        self.difficulty_instruction_font = pygame.font.SysFont(
            "Arial",
            22
        )

        self.game_over = False
        self.final_score = 0
        self.selecting_difficulty = False

        self.jump_sound = None
        self.score_sound = None
        self.game_over_sound = None

        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()

            sound_directory = (
                Path(__file__).resolve().parent.parent
                / "assets"
                / "sounds"
            )

            self.jump_sound = pygame.mixer.Sound(
                str(sound_directory / "jump.wav")
            )

            self.score_sound = pygame.mixer.Sound(
                str(sound_directory / "score.wav")
            )

            self.game_over_sound = pygame.mixer.Sound(
                str(sound_directory / "game_over.wav")
            )

        except (pygame.error, FileNotFoundError, OSError):
            self.jump_sound = None
            self.score_sound = None
            self.game_over_sound = None

    def handle_event(self, event):

        if event.type != pygame.KEYDOWN:
            return None

        if self.game_over:

            if event.key in (
                pygame.K_r,
                pygame.K_RETURN
            ):
                self.selecting_difficulty = True
                return None

            if event.key in (
                pygame.K_q,
                pygame.K_ESCAPE
            ):
                return "quit"

            return None

        if self.selecting_difficulty:

            if event.key in (
                pygame.K_1,
                pygame.K_KP1
            ):
                self.start_new_game("Easy")
                return None

            if event.key in (
                pygame.K_2,
                pygame.K_KP2
            ):
                self.start_new_game("Medium")
                return None

            if event.key in (
                pygame.K_3,
                pygame.K_KP3
            ):
                self.start_new_game("Hard")
                return None

            if event.key == pygame.K_ESCAPE:
                self.selecting_difficulty = False
                return None

            return None

        if event.key in (
            pygame.K_SPACE,
            pygame.K_UP,
            pygame.K_w
        ):
            if self.player.jump():
                if self.jump_sound is not None:
                    self.jump_sound.play()

        return None

    def handle_input(self):
        pass

    def start_new_game(self, difficulty):

        self.current_difficulty = difficulty

        settings = self.difficulties[difficulty]

        self.speed = settings["speed"]
        self.spawn_interval = settings["spawn_interval"]

        self._spawn_timer = 0
        self.obstacles = []

        self.distance = 0
        self.score = 0
        self.final_score = 0

        self.player.x = 80
        self.player.y = self.ground_y - self.player.height
        self.player.vy = 0
        self.player.on_ground = True

        self.game_over = False
        self.selecting_difficulty = False

    def update(self):

        if self.selecting_difficulty:
            return

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

            if obstacle.rect().colliderect(
                self.player.rect()
            ):

                self.game_over = True
                self.final_score = self.score

                if self.game_over_sound is not None:
                    self.game_over_sound.play()

                return

        for obstacle in self.obstacles:

            if (
                not obstacle.scored
                and obstacle.x + obstacle.width < self.player.x
            ):

                obstacle.scored = True
                self.score += 1

                if self.score_sound is not None:
                    self.score_sound.play()

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

        difficulty_text = self.font.render(
            f"Difficulty: {self.current_difficulty}",
            True,
            BLACK
        )

        difficulty_rect = difficulty_text.get_rect(
            top=10,
            right=self.width - 10
        )

        screen.blit(
            difficulty_text,
            difficulty_rect
        )

        if self.selecting_difficulty:

            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 170)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            title_text = self.difficulty_title_font.render(
                "SELECT DIFFICULTY",
                True,
                WHITE
            )

            title_rect = title_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 - 120
                )
            )

            screen.blit(
                title_text,
                title_rect
            )

            easy_text = self.difficulty_font.render(
                "1 - EASY",
                True,
                GREEN
            )

            easy_rect = easy_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 - 50
                )
            )

            screen.blit(
                easy_text,
                easy_rect
            )

            medium_text = self.difficulty_font.render(
                "2 - MEDIUM",
                True,
                YELLOW
            )

            medium_rect = medium_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 + 10
                )
            )

            screen.blit(
                medium_text,
                medium_rect
            )

            hard_text = self.difficulty_font.render(
                "3 - HARD",
                True,
                RED
            )

            hard_rect = hard_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 + 70
                )
            )

            screen.blit(
                hard_text,
                hard_rect
            )

            instruction_text = (
                self.difficulty_instruction_font.render(
                    "Press 1, 2 or 3 to start | ESC to go back",
                    True,
                    WHITE
                )
            )

            instruction_rect = instruction_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 + 130
                )
            )

            screen.blit(
                instruction_text,
                instruction_rect
            )

            return

        if self.game_over:

            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 160)
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

            game_over_rect = game_over_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 - 100
                )
            )

            screen.blit(
                game_over_text,
                game_over_rect
            )

            final_score_text = self.game_over_score_font.render(
                f"Final Score: {self.final_score}",
                True,
                WHITE
            )

            final_score_rect = final_score_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 - 25
                )
            )

            screen.blit(
                final_score_text,
                final_score_rect
            )

            replay_text = self.game_over_instruction_font.render(
                "Press R or ENTER to play again",
                True,
                WHITE
            )

            replay_rect = replay_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 + 35
                )
            )

            screen.blit(
                replay_text,
                replay_rect
            )

            exit_text = self.game_over_instruction_font.render(
                "Press Q or ESC to exit",
                True,
                WHITE
            )

            exit_rect = exit_text.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2 + 75
                )
            )

            screen.blit(
                exit_text,
                exit_rect
            )