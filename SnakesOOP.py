import pygame
import random
from pygame.math import Vector2


class Snake():
    def __init__(self, a, b, c, color):
        self.body = [a, b, c]
        self.color = color
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, pygame.Color(self.color), block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class Food():
    def __init__(self):
        self.snake = Snake(Vector2(7, 10), Vector2(6, 10), Vector2(5, 10), 'blue')
        self.snake2 = Snake(Vector2(7, 5), Vector2(6, 5), Vector2(5, 5), 'purple')
        self.snack = pygame.image.load('mushroom.png').convert_alpha()
        self.randomize()

    def draw_food(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.snack, fruit_rect)

    def randomize(self):
        badspawn = True
        while badspawn:
            self.x = random.randint(0, cell_number - 1)
            self.y = random.randint(0, cell_number - 1)
            self.pos = Vector2(self.x, self.y)
            badspawn = False
            for block in self.snake.body:
                for block2 in self.snake2.body:
                    if block[0] == self.x and block[1] == self.y or block2[0] == self.x and block2[1] == self.y:
                        badspawn = True
                        break
                    else:
                        badspawn = False


class Game():
    def __init__(self):
        self.snake = Snake(Vector2(7, 10), Vector2(6, 10), Vector2(5, 10), 'blue')
        self.snake2 = Snake(Vector2(7, 5), Vector2(6, 5), Vector2(5, 5), 'purple')
        self.snack = Food()
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('PoetsenOne-Regular.ttf', 25)
        self.running = True
        self.endgame = False

    def update(self):
        self.snake.move_snake()
        self.snake2.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grid()
        self.snack.draw_food()
        self.snake.draw_snake()
        self.snake2.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.snack.pos == self.snake.body[0]:
            self.snack.randomize()
            self.snake.add_block()
        if self.snack.pos == self.snake2.body[0]:
            self.snack.randomize()
            self.snake2.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        if not 0 <= self.snake2.body[0].x < cell_number or not 0 <= self.snake2.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0] or block == self.snake2.body[0]:
                self.game_over()
        for block in self.snake2.body[1:]:
            if block == self.snake2.body[0] or block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        main()

    def draw_grid(self):
        grid_color = (167, 209, 61)
        for i in range(cell_number):
            for j in range(cell_number):
                if (i + j) % 2 == 0:
                    grid_rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grid_color, grid_rect)

    def draw_score(self):
        score_text = 'Snake1: ' + str(len(self.snake.body) - 3)
        score_text2 = 'Snake2: ' + str(len(self.snake2.body) - 3)
        score_surface = self.game_font.render(score_text, True, (56, 74, 12))
        score_surface2 = self.game_font.render(score_text2, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 730)
        score_y = int(cell_size * cell_number - 40)
        score_x2 = int(cell_size * cell_number - 80)
        score_y2 = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        score_rect2 = score_surface.get_rect(center=(score_x2, score_y2))
        screen.blit(score_surface, score_rect)
        screen.blit(score_surface2, score_rect2)

    def message(self, message, x, y):
        self.text = self.game_font.render(message, True, (0, 200, 0))
        self.textRect = self.text.get_rect()
        self.textRect.center = (x, y)
        screen.blit(self.text, self.textRect)

    def game_loop(self):
        game = Game()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                if event.type == SCREEN_UPDATE:
                    game.update()
                if event.type == pygame.KEYDOWN:
                    # snake1
                    if event.key == pygame.K_UP:
                        if game.snake.direction.y != 1:
                            game.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN:
                        if game.snake.direction.y != -1:
                            game.snake.direction = Vector2(0, 1)
                    if event.key == pygame.K_RIGHT:
                        if game.snake.direction.x != -1:
                            game.snake.direction = Vector2(1, 0)
                    if event.key == pygame.K_LEFT:
                        if game.snake.direction.x != 1:
                            game.snake.direction = Vector2(-1, 0)
                    # snake2
                    if event.key == pygame.K_w:
                        if game.snake2.direction.y != 1:
                            game.snake2.direction = Vector2(0, -1)
                    if event.key == pygame.K_s:
                        if game.snake2.direction.y != -1:
                            game.snake2.direction = Vector2(0, 1)
                    if event.key == pygame.K_d:
                        if game.snake2.direction.x != -1:
                            game.snake2.direction = Vector2(1, 0)
                    if event.key == pygame.K_a:
                        if game.snake2.direction.x != 1:
                            game.snake2.direction = Vector2(-1, 0)

            screen.fill((175, 215, 70))
            game.draw_elements()
            pygame.display.update()
            self.clock.tick(60)


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption('Snakes')

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)


def main():
    Game().game_loop()


if __name__ == '__main__':
    main()
