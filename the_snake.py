from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
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
            "Метод draw должен быть переопределен в дочернем классе"
        )


class Apple(GameObject):
    """Класс для представления яблока в игре."""

    def __init__(self, position=(0, 0), body_color=APPLE_COLOR):
        """Инициализация яблока со случайной позицией."""
        position = self.get_random_position()
        super().__init__(position, body_color)

    def draw(self):
        """Метод для отрисовки яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Метод для обновления позиции яблока."""
        self.position = self.get_random_position()

    @staticmethod
    def get_random_position():
        """Метод для получения случайной позиции на игровом поле."""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )


class Snake(GameObject):
    """Класс для представления змейки в игре."""

    def __init__(
            self,
            positions=None,
            body_color=SNAKE_COLOR
    ):
        """Инициализация змейки."""
        if positions is None:
            positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        super().__init__(positions[0], body_color)
        self.positions = positions
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        """Метод для отрисовки змейки на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод для получения позиции головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод для движения змейки."""
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )

        if new_head in self.positions:
            self.reset()
        
        self.positions.insert(0, new_head)
        self.last = self.positions.pop()

    def reset(self):
        """Метод для сброса змейки в начальное состояние."""
        self.positions = [(GRID_SIZE * 5, GRID_SIZE * 5)]
        self.direction = RIGHT

    def update_direction(self):
        """Метод для обновления направления змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(snake):
    """Функция для обработки нажатий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры."""
    pygame.init()

    # Создаем экземпляр яблока со случайной позицией
    apple = Apple(None, APPLE_COLOR)

    # Создаем экземпляр змейки
    snake = Snake()

    while True:
        clock.tick(SPEED)

        # Обработка нажатий клавиш
        handle_keys(snake)

        # Обновление направления змейки
        snake.update_direction()

        # Движение змейки
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            apple.randomize_position()
            # Увеличиваем длину змейки, не удаляя последний сегмент
            snake.positions.append(snake.last)

        # Очистка экрана
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовка яблока
        apple.draw()

        # Отрисовка змейки
        snake.draw()

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
