import random
import sys

from pygame.locals import *

from config import *
from settings import *


def main():
    pygame.init()
    pygame.display.set_caption('Тетрис')
    show_text('Тетрис')

    while True:
        run_game()
        pause()
        show_text('Игра закончена')


def run_game():
    """Основной функционал игры"""
    global GOING_LEFT, LAST_SIDE_MOVE, GOING_RIGHT
    cup = get_cup()
    LAST_MOVE_DOWN = time.time()
    LAST_SIDE_MOVE = time.time()
    LAST_FALL = time.time()
    GOING_DOWN = False
    GOING_LEFT = False
    GOING_RIGHT = False
    POINTS = 0
    level, fall_speed = calc_speed(POINTS)
    falling_fig = get_new_fig()
    next_fig = get_new_fig()

    while True:
        if falling_fig == None:
            # Если нет падающих фигур - генерируем новую
            falling_fig = next_fig
            next_fig = get_new_fig()
            LAST_FALL = time.time()

            if not check_pos(cup, falling_fig):
                return  # Если на игровом поле нет свободного места - игра закончена
        quit_game()
        for event in pygame.event.get():
            if event.type == KEYUP:
                """События при отпускании кнопки"""
                if event.key == K_SPACE:
                    pause()
                    show_text('Пауза')
                    LAST_FALL = time.time()
                    LAST_MOVE_DOWN = time.time()
                    LAST_SIDE_MOVE = time.time()
                elif event.key == K_LEFT:
                    GOING_LEFT = False
                elif event.key == K_RIGHT:
                    GOING_RIGHT = False
                elif event.key == K_DOWN:
                    GOING_DOWN = False

            elif event.type == KEYDOWN:
                """Обработка событий нажатия на кнопку"""
                if event.key == K_LEFT and check_pos(cup, falling_fig, adj_x=-1):
                    falling_fig['x'] -= 1
                    GOING_LEFT = True
                    GOING_RIGHT = False
                    LAST_SIDE_MOVE = time.time()
                elif event.key == K_RIGHT and check_pos(cup, falling_fig, adj_x=1):
                    falling_fig['x'] += 1
                    GOING_RIGHT = True
                    GOING_LEFT = False
                    LAST_SIDE_MOVE = time.time()

                #Поворачиваем фигуру, если есть место
            elif event.key == K_UP:
                falling_fig['rotation'] = (falling_fig['rotation'] + 1) % len(FIGURES[falling_fig['shape']])
                if not check_pos(cup, falling_fig):
                    falling_fig['rotation'] = (falling_fig['rotation'] - 1) % len(FIGURES[falling_fig['shape']])

                """Ускорение падения фигуры вниз"""
            elif event.type == K_DOWN:
                GOING_DOWN = True
                if check_pos(cup, falling_fig, adj_y=1):
                    falling_fig['y'] += 1
                LAST_MOVE_DOWN = time.time()

                """Мгновенное падение фигуры вниз"""
            elif event.key == K_RETURN:
                GOING_DOWN = False
                GOING_LEFT = False
                GOING_RIGHT = False
                for i in range(1, CUP_HEIGHT):
                    if not check_pos(cup, falling_fig, adj_y=i):
                        break
                falling_fig['y'] += i - 1

        """Управление падением фигуры при удерживании клавиш"""
        if (GOING_LEFT or GOING_RIGHT) and time.time() - LAST_SIDE_MOVE > SIDE_FREQ:
            if GOING_LEFT and check_pos(cup, falling_fig, adj_x=-1):
                falling_fig['x'] -= 1
            elif GOING_RIGHT and check_pos(cup, falling_fig, adj_x=1):
                falling_fig['x'] += 1
            LAST_SIDE_MOVE = time.time()

        if GOING_DOWN and time.time() - LAST_MOVE_DOWN > DOWN_FREQ and check_pos(cup, falling_fig, adj_y=1):
            falling_fig['y'] +=1
            LAST_MOVE_DOWN = time.time()

        """Свободное падение фигуры"""
        if time.time() - LAST_FALL > fall_speed:
            if not check_pos(cup, falling_fig, adj_y=1):
                add_to_cup(cup, falling_fig)
                POINTS += clear_completed(cup)
                level, fall_speed = calc_speed(POINTS)
                falling_fig = None
            else:
                falling_fig['y'] += 1
                LAST_FALL = time.time()

        """Отрисовка окна игры со всеми надписями"""
        DISPLAY_SURF.fill(BG_COLOR)
        draw_title()
        game_cup(cup)
        draw_info(POINTS,level)
        draw_next_fig(next_fig)
        if falling_fig is not None:
            draw_fig(falling_fig)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def draw_next_fig(fig):
    """Превью следуещей фигуры"""
    next_surf = BASIC_FONT.render(f'Следующая:', True, TXT_COLOR)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (WINDOW_WIDTH - 150, 180)
    DISPLAY_SURF.blit(next_surf, next_rect)
    draw_fig(fig, pixel_x=WINDOW_WIDTH - 150, pixel_y=230)


def draw_fig(fig, pixel_x=None, pixel_y=None):
    """Отрисовка фигуры"""
    fig_to_draw = FIGURES[fig['shape']][fig['rotation']]
    if pixel_x is None and pixel_y is None:
        pixel_x, pixel_y = convert_coordinates(fig['x'], fig['y'])

    for x in range(FIGURE_WIDTH):
        for y in range(FIGURE_HEIGHT):
            if fig_to_draw[y][x] != EMPTY
                draw_block(None, None, fig['color'], pixel_x + (x * BLOCK), pixel_y + (y * block))

                
def draw_info(points, level):
    """Отрисовка статистики"""
    points_surf = BASIC_FONT.render(f'Очки: {points}', True, TITLE_COLOR)
    points_rect = points_surf.get_rect()
    points_rect.topleft = (WINDOW_WIDTH - 550, 180)
    DISPLAY_SURF.blit(points_surf, points_rect)

    level_surf = BASIC_FONT.render(f'Уровень: {level}', True, TXT_COLOR)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (WINDOW_WIDTH - 580, 250)
    DISPLAY_SURF.blit(level_surf, level_rect)

    pause_surf = BASIC_FONT.render('Пауза: пробел', True, INFO_COLOR)
    pause_rect = pause_surf.get_rect()
    pause_rect.topleft = (WINDOW_WIDTH - 580, 420)
    DISPLAY_SURF.blit(pause_surf, pause_rect)

    esc_surf = BASIC_FONT.render('выход: esc', True, INFO_COLOR)
    esc_rect = pause_surf.get_rect()
    esc_rect.topleft = (WINDOW_WIDTH - 580, 450)
    DISPLAY_SURF.blit(esc_surf, esc_rect)

def game_cup(cup):
    """Отрисовка границ стакана и игрового поля"""
    pygame.draw.rect(DISPLAY_SURF, BORDER_COLOR,
                     (SIDE_MARGIN - 4, TOP_MARGIN - 4, (CUP_WIDTH * BLOCK) + 8, (CUP_HEIGHT * BLOCK) + 8), 5)
    pygame.draw.rect(DISPLAY_SURF, BG_COLOR, (SIDE_MARGIN, TOP_MARGIN, BLOCK * CUP_WIDTH, BLOCK * CUP_HEIGHT))
    for x in range(CUP_WIDTH):
        for y in range(CUP_HEIGHT):
            draw_block(x, y, cup[x][y])


def draw_block(block_x, block_y, color, pixel_x=None,  pixel_y=None):
    """Отрисовка квадратиков фигур"""
    COLORS = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30))
    if color == EMPTY:
        return
    if pixel_x == None and pixel_y == None:
        pixel_x, pixel_y = convert_coordinates(block_x, block_y)
        pygame.draw.rect(DISPLAY_SURF, COLORS[color], (pixel_x + 1, pixel_y + 1, BLOCK - 1, BLOCK - 1), 0, 3)
        pygame.draw.rect(DISPLAY_SURF, LIGHT_COLORS[color], (pixel_x + 1, pixel_y + 1, BLOCK - 4, BLOCK - 4), 0, 3)
        pygame.draw.circle(DISPLAY_SURF, COLORS[color], (pixel_x + BLOCK / 2, pixel_y + BLOCK / 2), 5)


def convert_coordinates(x, y):
    """Конверция координат"""
    return (SIDE_MARGIN + (x * BLOCK)), (TOP_MARGIN + (y * BLOCK))


def draw_title():
    """Отрисовка названия"""
    title_surf = BIG_FONT.render('Тетрис', True, TITLE_COLOR)
    title_rect = title_surf.get_rect()
    title_rect.topleft = (WINDOW_WIDTH - 380, 30)
    DISPLAY_SURF.blit(title_surf, title_rect)


def clear_completed(cup):
    """Удаление заполненных рядов и сдвиг верхних рядов вниз"""
    removed_lines = 0
    y = CUP_HEIGHT -1
    while y >=0:
        if is_completed(cup, y):
            for push_down_y in range(y, 0, -1):
                for x in range(CUP_WIDTH):
                    cup[x][push_down_y] = cup[x][push_down_y -1]
            for x in range(CUP_WIDTH):
                cup[x][0] = EMPTY
            removed_lines += 1
        else:
            y -= 1
    return removed_lines


def is_completed(cup, y):
    """Проверка полностью заполненых рядов"""
    for x in range(CUP_WIDTH):
        if cup[x][y] == EMPTY:
            return False
    return True

def add_to_cup(cup, fig):
    """Добавление фигуры в стакан"""
    for x in range(FIGURE_WIDTH):
        for y in range(FIGURE_HEIGHT):
            if FIGURES[fig['shaoe']][fig['rotation']][y][x] != EMPTY:
                cup[x + fig['x']][y + fig['y']] = fig['color']


def quit_game():
    """Выход из игры"""
    for event in pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        pygame.event.post(event)


def in_cup(x, y):
    """Проверка нахождения фигуры в стакане"""
    return 0 <= x < CUP_WIDTH and y < CUP_HEIGHT


def check_pos(cup, fig, adj_x=0, adj_y=0):
    """Проверка того, находится ли фигура в границах стакана, не сталкиваясь с другими фигурами"""
    for x in range(FIGURE_WIDTH):
        for y in range(FIGURE_HEIGHT):
            above_cup = y + fig['y'] + adj_y < 0
            if above_cup or FIGURES[fig['shape']][fig['rotation']][y][x] == EMPTY:
                continue
            if not in_cup(x + fig['x'] + adj_x, y + fig['y'] + adj_y):
                return False
            if cup[x + fig['x'] + adj_x][y + fig['y'] + adj_y] != EMPTY:
                return False

    return True


def get_new_fig():
    """Возвращает новую фигуру со случайным цветом и углом поворота"""
    shape = random.choice(list(FIGURES.keys()))
    new_figure = {
        'shape': shape,
        'rotation': random.randint(0, len(FIGURES[shape]) + 1),
        'x': int(CUP_WIDTH / 2) - int(CUP_HEIGHT / 2),
        'y': -2,
        'color': random.randint(0, len(COLORS) - 1)
    }
    return new_figure


def calc_speed(points: int):
    """Вычисляем уровень"""
    level = int(points / 10) + 1
    fall_speed = 0.25 - (level * 0.02)
    return level, fall_speed


def show_text(text: str):
    """Отрисовка текста"""
    title_surf, title_rect = text_objects(text, BIG_FONT, TITLE_COLOR)
    title_rect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2))
    DISPLAY_SURF.blit(title_surf, title_rect)

    press_key_surf, press_key_rect = text_objects('Нажмите любую клавишу для продолжения', BASIC_FONT, TITLE_COLOR)
    press_key_rect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2) + 100)
    DISPLAY_SURF.blit(press_key_surf, press_key_rect)

    while check_keys() is None:
        pygame.display.update()
        FPS_CLOCK.tick()


def check_keys():
    quit_game()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def text_objects(text, font, color):
    """Создание объекта текста"""
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def get_cup():
    """Создание пустого стакана"""
    cup = list()
    for _ in range(CUP_WIDTH):
        cup.append([EMPTY] * CUP_HEIGHT)
    return cup


def pause():
    """Отрисовка экрана паузы"""
    pause = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    pause.fill((0, 0, 255, 127))
    DISPLAY_SURF.blit(pause, (0, 0))


if __name__ == '__main__':
    main()