# строим игру 2048!
import pygame
import random

pygame.init()

# добавление музыки и самого окошка делаем 60 фпс потому что это самый оптимальный фпс для игры пайгейм а также 2048
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

background_music = pygame.mixer.music.load('soundtrack2048.mp3')  # Музыка в фоне
pygame.mixer.music.play(-1)  # -1 позволяет музыке воспроизводиться в цикле

music_on_image = pygame.transform.scale(pygame.image.load('MUSIC_ON.png'), (30, 30))
music_off_image = pygame.transform.scale(pygame.image.load('MUSIC_OFF.png'), (30, 30))
# Определение прямоугольников для размещения кнопок
music_button_rect = music_on_image.get_rect()

new_game_button_image = pygame.transform.scale(pygame.image.load('NEWGAME.png'), (170, 50))
new_game_button_rect = new_game_button_image.get_rect()
# Определение прямоугольников для размещения кнопок
music_button_rect = music_on_image.get_rect()

icon_image = pygame.transform.scale(pygame.image.load('icon.png'), (30, 30))
icon_rect = icon_image.get_rect()


#отслеживания состояний звука и музыки
sound_on = True
music_on = True


# библиотека цветов 2048 (цвета в основе оригинальной игры чтобы соблюдать эстетику и классику жанра)
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# инициализация многих перемен для игры
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high
show_instruction = False
icon_x = 350
icon_y = 450
icon_width, icon_height = icon_rect.size


# рисовать игра окончена и написать подробнее что нужно нажать чтобы перезагрузить игру
def draw_over():
    pygame.draw.rect(screen, (112, 97, 81), [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))

#рисование инструкции
def draw_instruction():
    # Рисуем бардюры коричневого цвета
    pygame.draw.rect(screen, (161, 102, 47), [50, 50, 300, 300], 0, 10)
    pygame.draw.rect(screen, (187, 173, 160), [55, 55, 290, 290], 0, 10)  # Бежевый цвет внутри иммитация книги

    # Текст "HOW TO PLAY:"
    how_to_play_text = pygame.font.Font('freesansbold.ttf', 20).render('HOW TO PLAY:', True, (86, 28, 36))
    screen.blit(how_to_play_text, (125, 70))

    # Текст инструкции
    instruction_text1 = pygame.font.Font('freesansbold.ttf', 15).render('Use your arrow keys to move the tiles.', True, (126, 99, 99))
    instruction_text2_part1 = pygame.font.Font('freesansbold.ttf', 15).render('Tiles with the same number merge into', True, (126, 99, 99))
    instruction_text2_part2 = pygame.font.Font('freesansbold.ttf', 15).render('one when they touch.', True, (126, 99, 99))
    instruction_text3 = pygame.font.Font('freesansbold.ttf', 15).render('Add them up to reach', True, (126, 99, 99))
    instruction_text4 = pygame.font.Font('freesansbold.ttf', 15).render('2048!', True, (250, 163, 0))
    instruction_text5 = pygame.font.Font('freesansbold.ttf', 15).render('Press Esc to close this window.', True, (109, 41, 50))

    #текст внутри бежевого цвета ровно по размерам
    screen.blit(instruction_text1, (60, 110))
    screen.blit(instruction_text2_part1, (60, 135))
    screen.blit(instruction_text2_part2, (60, 155))
    screen.blit(instruction_text3, (60, 180))
    screen.blit(instruction_text4, (217, 180))
    screen.blit(instruction_text5, (80, 320))

# направление и счетчик всего слияние блоков чтобы оно записывалось каждый раз а после в конце суммировалась
def take_turn(direc, board):
    merged = [[False for _ in range(4)] for _ in range(4)]
    total_score = 0  # Добавляем счетчик очков для этого хода
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        total_score += board[i - shift - 1][j]  # Увеличиваем счетчик очков
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True
    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        total_score += board[3 - i + shift][j]  # Увеличиваем счетчик очков
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True
    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    total_score += board[i][j - shift - 1]  # Увеличиваем счетчик очков
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True
    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        total_score += board[i][4 - j + shift]  # Увеличиваем счетчик очков
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board, total_score  # Возвращаем доску и счетчик очков




# спавнить блоки рандомно, по логике 2048 должны спавнится 2 и 4 а больше них блоки не спавнятся поэтому наша главная цель взять только 2 рандомных числа и они появляются в каждом пустом ячейке колоны и строки
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# для рисование фона и рисования счетчика в самой окошке
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)

    # нарисовать очки
    score_text = font.render(f'Score: {score}', True, 'black')
    screen.blit(score_text, (10, 410))

    # нарисовать высшие очки
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(high_score_text, (10, 450))

    # добавить иконку музыки чтобы понимать куда кликать
    screen.blit(music_on_image if music_on else music_off_image, (350, 410))
    screen.blit(new_game_button_image, ((WIDTH - new_game_button_rect.width) // 2, HEIGHT - 100))
    screen.blit(icon_image, (350,450))
    pass


# рисование самих плиток для игры
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, (176, 161, 145), [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

# Функция для проверки возможности сделать ход в любом направлении без слияния
def can_move(board):
    for direc in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
        temp_board = [row[:] for row in board]
        temp_merged = [[False for _ in range(4)] for _ in range(4)]
        _, _ = take_turn(direc, temp_board)
        if temp_board != board:
            return True
    return False


# сам цикл игры
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction != '':
        temp_board = [row[:] for row in board_values]
        temp_score = 0
        temp_board, temp_score = take_turn(direction, temp_board)
        if temp_board != board_values:
            board_values = temp_board
            spawn_new = True
            score += temp_score
        direction = ''
        if not can_move(board_values):
            game_over = True

    if game_over:
        draw_over()
        if high_score > init_high:
            file = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    # Проверка для отображения инструкции
    if show_instruction:
        draw_instruction()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Получить координаты щелчка мыши
            mouse_pos = pygame.mouse.get_pos()

            if not show_instruction:  # если инструкция закрыта то можно нажимать на кнопку new game
                # Проверить, попадает ли щелчок в область кнопки "New Game"
                new_game_button_x, new_game_button_y = (WIDTH - new_game_button_rect.width) // 2, HEIGHT - 100
                new_game_button_width, new_game_button_height = new_game_button_rect.size
                if new_game_button_x <= mouse_pos[0] <= new_game_button_x + new_game_button_width \
                        and new_game_button_y <= mouse_pos[1] <= new_game_button_y + new_game_button_height:
                    # Если щелчок произошел в пределах кнопки "New Game", перезапустить игру
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False
            #координаты щелчка мыши
            mouse_pos = pygame.mouse.get_pos()
            #координаты и размеры изображения кнопки музыки
            music_button_x, music_button_y = 350, 410
            music_button_width, music_button_height = music_on_image.get_size()
            # Проверка попадание щелчка в область кнопки музыки
            if music_button_x <= mouse_pos[0] <= music_button_x + music_button_width \
                    and music_button_y <= mouse_pos[1] <= music_button_y + music_button_height:
                if music_on:
                    pygame.mixer.music.pause()
                    music_on = False
                    screen.blit(music_off_image, (music_button_x, music_button_y))
                else:
                    pygame.mixer.music.unpause()
                    music_on = True
                    screen.blit(music_on_image, (music_button_x, music_button_y))

        if show_instruction:  # Если инструкция открыта, игнорируем движения блоков
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                show_instruction = False  # Закрываем инструкцию по нажатию Esc
        else:  # Если инструкция закрыта, можем двигать блоки
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if icon_x <= mouse_pos[0] <= icon_x + icon_width and icon_y <= mouse_pos[1] <= icon_y + icon_height:
                    show_instruction = True

            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        direction = 'UP'
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        direction = 'DOWN'
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        direction = 'RIGHT'
                    elif event.key == pygame.K_RETURN and game_over:
                        # Перезапуск игры при нажатии Enter, когда игра окончена
                        board_values = [[0 for _ in range(4)] for _ in range(4)]
                        game_over = False
                        spawn_new = True
                        init_count = 0
                        direction = ''
                        score = 0
                    elif event.key == pygame.K_m:
                        # Включение/выключение музыки при нажатии 'm'
                        music_on = not music_on
                        if music_on:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                if event.key == pygame.K_ESCAPE:
                    show_instruction = False

    if score > high_score:
        high_score = score

    pygame.display.flip()

pygame.quit()