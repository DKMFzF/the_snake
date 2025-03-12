from random import randint
import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 10
SPEED_BOOST = 20  # Новая скорость при ускорении

direction_mapping = {
    (pygame.K_UP, DOWN): DOWN,
    (pygame.K_UP, UP): UP,
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_DOWN, UP): UP,
    (pygame.K_DOWN, DOWN): DOWN,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_LEFT, RIGHT): RIGHT,
    (pygame.K_LEFT, LEFT): LEFT,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, LEFT): LEFT,
    (pygame.K_RIGHT, RIGHT): RIGHT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        """Инициализация игрового объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        raise NotImplementedError(
            'Метод draw должен быть переопределен в дочернем классе'
        )

    def draw_cell(self, position, color):
        """Метод для отрисовки одной ячейки."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для представления яблока в игре."""

    def __init__(self, position=(0, 0), body_color=APPLE_COLOR):
        """Инициализация яблока со случайной позицией."""
        position = self.randomize_position()
        super().__init__(position, body_color)

    def draw(self):
        """Метод для отрисовки яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, snake_positions=None):
        """Метод для обновления позиции яблока."""
        if snake_positions is None:
            snake_positions = []

        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in snake_positions:
                return position


class Snake(GameObject):
    """Класс для представления змейки в игре."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация змейки."""
        super().__init__(body_color=body_color)
        self.reset()

    def draw(self):
        """Метод для отрисовки змейки"""
        for segment in self.positions:
            self.draw_cell(segment, self.body_color)

    def get_head_position(self):
        """Метод для получения позиции головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод для движения змейки."""
        x, y = self.get_head_position()  # Распаковываем координаты головы
        new_head = (
            (x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)

        self.last = self.positions.pop() if len(self.positions) > self.length \
            else None

    def reset(self):
        """Метод для сброса змейки в начальное состояние."""
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.direction = RIGHT
        self.last = None
        self.length = 1

    def update_direction(self, new_direction):
        """Метод для обновления направления змейки."""
        if new_direction:
            self.direction = new_direction


def handle_keys(snake):
    """Функция для обработки нажатий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            new_direction = direction_mapping.get((event.key, snake.direction))
            if new_direction:
                snake.update_direction(new_direction)


def handle_speed_boost():
    """Функция для обработки ускорения змейки."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        return SPEED_BOOST
    return SPEED


def main():
    """Основная функция игры."""
    pygame.init()
    snake = Snake()
    apple = Apple(APPLE_COLOR)
    while True:
        clock.tick(handle_speed_boost())

        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            apple.position = apple.randomize_position(snake.positions)
            snake.length += 1
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
