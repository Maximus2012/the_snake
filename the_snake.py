from random import choice, randint

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
SPEED = 6

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов (яблоко, змейка)."""

    def __init__(
        self, position=[(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)],
        body_color=None
    ):
        """Инициализация объекта с позицией и цветом."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Метод для отрисовки объекта
        (переопределяется в дочерних классах).
        """
        pass


class Apple(GameObject):
    """Класс яблока, которое нужно есть змейке."""

    def __init__(
        self,
        position=(
            randint(0, GRID_WIDTH - 20) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 20) * GRID_SIZE,
        ),
        body_color=(255, 0, 0),
    ):
        """
        Инициализация яблока со случайной позицией и цветом.

        :param position: начальная позиция яблока.
        :param body_color: цвет яблока.
        """
        super().__init__(position, body_color)
        self.randomize_position()

    def randomize_position(self):
        """Метод для случайного изменения позиции яблока на игровом поле."""
        self.positions = (
            randint(0, GRID_WIDTH - 20) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 20) * GRID_SIZE,
        )

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.positions, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки, управляемой игроком."""

    def __init__(
        self,
        length=1,
        positions=[(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)],
        direction=choice([UP, DOWN, LEFT, RIGHT]),
        next_direction=None,
        body_color=(0, 255, 0),
        last=None,
    ):
        """
        Инициализация змейки с начальной позицией и направлением.

        :param length: начальная длина змейки.
        :param positions: список позиций сегментов змейки.
        :param direction: начальное направление движения змейки.
        :param next_direction: направление для следующего шага.
        :param body_color: цвет змейки.
        :param last: последняя позиция змейки.
        """
        super().__init__(body_color=body_color)
        self.positions = positions
        self.length = length
        self.direction = direction
        self.next_direction = next_direction
        self.last = last

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, position):
        """
        Перемещение змейки на один шаг вперед.

        :param position: позиция для нового сегмента головы змейки.
        """
        start_snake_lentgh = self.length
        self.positions.insert(0, position)
        end_snake_lentgh = self.length
        if end_snake_lentgh == start_snake_lentgh:
            self.positions.pop()

    def draw(self):
        """Отрисовка всех сегментов змейки."""
        for position in self.positions[:-1]:  # ???
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
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сброс положения и направления змейки."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """
    Обработка событий клавиатуры для управления змейкой.

    :param game_object: объект змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
                
                
def main():
    """Main func."""
    pygame.init()
    running = True
    apple = Apple(1)
    snake = Snake(
        1,
        [],
        (0, -1),
    )
    snake.reset()
    screen.fill(BOARD_BACKGROUND_COLOR)
    while running:
        clock.tick(SPEED)
        handle_keys(snake)
        snake_positions = (snake.positions[-1][0], snake.positions[-1][1])
        snake.move(
            (
        snake.positions[0][0] + snake.direction[0] * 20,
        snake.positions[0][1] + snake.direction[1] * 20,
            )
        )
        snake.update_direction()
        apple.draw()
        if snake.get_head_position() == snake.positions[-1] and snake.length > 3:
            print("Length 1")
            snake.length = 1
            snake_position_first = snake.positions[0]
            snake.positions.clear()
            snake.positions.append(snake_position_first)
            screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.get_head_position() in snake.positions[1:]:
            print("loose")
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        # Проверка на столкновение с яблоком
        if snake.get_head_position() == apple.positions:
            snake.length += 1
            snake.positions.append(apple.positions)
            snake.draw()
            apple.randomize_position()
            while apple.positions in snake.positions:
                apple.randomize_position()
        # Проверка на выход за границы экрана
        if snake.get_head_position()[0] <= 0:
            snake_position_x = snake.positions[0][0] + 640
            snake_position_y = snake.positions[0][1]
            snake.positions[0] = (snake_position_x, snake_position_y)
        if snake.get_head_position()[0] >= 640:
            snake_position_x = snake.positions[0][0] - 640
            snake_position_y = snake.positions[0][1]
            snake.positions[0] = (snake_position_x, snake_position_y)
        if snake.get_head_position()[1] <= 0:
            snake_position_x = snake.positions[0][0]
            snake_position_y = snake.positions[0][1] + 480
            snake.positions[0] = (snake_position_x, snake_position_y)
        if snake.get_head_position()[1] >= 480:
            snake_position_x = snake.positions[0][0]
            snake_position_y = snake.positions[0][1] - 480
            snake.positions[0] = (snake_position_x, snake_position_y)
        # Очистка и отрисовка
        snake.last = snake_positions
        snake.draw()

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
