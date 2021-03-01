import pygame
import sys
import random
from winsound import Beep

import colors


class Game:
    def __init__(self):
        self.fps_controller = pygame.time.Clock()
        self.score = 0
        self.mouse_handlers = []

    def init_and_check_for_errors(self):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('Ok')

    def set_surface(self):
        self.play_surface = pygame.display.set_mode((width, height))

    def refresh_screen(self):
        pygame.display.flip()
        game.fps_controller.tick(23)

    def show_score(self, choice=1):
        s_font = pygame.font.Font(None, 24)
        s_surf = s_font.render(
            'Score: {0}'.format(self.score), True, colors.BLACK)
        s_rect = s_surf.get_rect()
        if choice == 1:
            s_rect.midtop = (80, 10)
        else:
            s_rect.midtop = (360, 120)
        self.play_surface.blit(s_surf, s_rect)

    def game_over(self):
        global game
        go_font = pygame.font.Font(None, 72)
        go_surf = go_font.render('Game over', True, colors.RED1)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        pygame.mixer.music.stop()
        screen.fill(colors.WHITE)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        for i, (text, click_handler) in enumerate((('RESTART', on_play), ('MENU', show_menu))):
            b = Button(330, 300 + (50 + 5) * i, 80, 50, text, click_handler, padding=5)
            game.mouse_handlers.append(b.handle_mouse_event)
            b.draw(screen)
        pygame.display.flip()
        Beep(208, 400)
        Beep(175, 400)
        Beep(130, 400)
        game = Game()
        while True:
            event_loop()


class Snake:
    def __init__(self, snake_color):
        self.snake_head_pos = [100, 50]  # [x, y]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = snake_color
        self.direction = "RIGHT"
        self.change_to = self.direction

    def validate_direction_and_change(self):
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(
            self, score, food_pos, screen_width, screen_height):
        self.snake_body.insert(0, list(self.snake_head_pos))
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            food_pos = [random.randrange(1, screen_width / 10) * 10,
                        random.randrange(1, screen_height / 10) * 10]
            # Beep(247, 100)
            score += 1
        else:
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface, surface_color):
        play_surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(
                play_surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def check_for_boundaries(self, game_over, screen_width, screen_height):
        if any((
                self.snake_head_pos[0] > screen_width - 10
                or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > screen_height - 10
                or self.snake_head_pos[1] < 0
        )):
            game_over()
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()


class Food:
    def __init__(self, food_color, screen_width, screen_height):
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width / 10) * 10,
                         random.randrange(1, screen_height / 10) * 10]

    def draw_food(self, play_surface):
        pygame.draw.rect(
            play_surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_x, self.food_size_y))


class TextObject:
    def __init__(self, x, y, text_func, color=colors.WHITE, font_name='Arial', font_size=20):
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bounds = self.get_surface(text_func())

    def draw(self, surface, centralized=False):
        text_surface, self.bounds = self.get_surface(self.text_func())
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2, self.pos[1])
        else:
            pos = self.pos
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass


class Button:
    def __init__(self, x, y, w, h, text, on_click=lambda x: None, padding=0):
        self.bounds = pygame.Rect(x, y, w, h)
        self.state = 'normal'
        self.on_click = on_click
        self.text = TextObject(x + padding, y + padding, lambda: text)

    @property
    def back_color(self):
        return dict(normal=colors.INDIANRED1,
                    hover=colors.INDIANRED2,
                    pressed=colors.INDIANRED3)[self.state]

    def draw(self, surface):
        pygame.draw.rect(surface, self.back_color, self.bounds)
        self.text.draw(surface)

    def handle_mouse_event(self, type, pos):
        if type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        if self.bounds.collidepoint(pos):
            if self.state != 'pressed':
                self.state = 'hover'
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        if self.bounds.collidepoint(pos):
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            self.on_click()
            self.state = 'hover'


def event_loop(change_to=False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if change_to:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
            if event.key == pygame.K_ESCAPE:
                pass
                # screen.fill(colors.GRAY)
                # pygame.display.flip()
                # while pygame.event.wait().key != pygame.K_ESCAPE:
                #     pass
                # screen.fill(colors.WHITE)
                # pygame.display.flip()
        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            for handler in game.mouse_handlers:
                handler(event.type, event.pos)
    return change_to


def start_game():
    music = pygame.mixer.music.load('background_music.mp3')
    pygame.mixer.music.play(-1, 0.0)
    while True:
        snake.change_to = event_loop(snake.change_to)

        snake.validate_direction_and_change()
        snake.change_head_position()
        game.score, food.food_pos = snake.snake_body_mechanism(
            game.score, food.food_pos, width, height)
        snake.draw_snake(game.play_surface, colors.WHITE)

        food.draw_food(game.play_surface)

        snake.check_for_boundaries(
            game.game_over, width, height)

        game.show_score()
        game.refresh_screen()


def on_play():
    start_game()


def on_quit():
    pygame.quit()
    sys.exit()


def show_menu():
    screen.fill(colors.WHITE)
    for i, (text, click_handler) in enumerate((('PLAY', on_play), ('QUIT', on_quit))):
        b = Button(20, 300 + (50 + 5) * i, 80, 50, text, click_handler, padding=5)
        game.mouse_handlers.append(b.handle_mouse_event)
        b.draw(screen)
    pygame.display.flip()
    while True:
        event_loop()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Snake Game')
    game = Game()
    snake = Snake(colors.GREEN)
    food = Food(colors.BROWN, width, height)

    game.init_and_check_for_errors()
    game.set_surface()

    show_menu()
