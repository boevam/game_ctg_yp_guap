import pygame

clock = pygame.time.Clock()  # для смены кадров
pygame.init()
screen = pygame.display.set_mode((1000, 750))  # размер экрана
pygame.display.set_caption('clean teeth game | ctg')  # название страницы
icon = pygame.image.load('images/teeth.png').convert_alpha()  # иконка
pygame.display.set_icon(icon)  # вывод иконки
bg = pygame.image.load('images/bgiv1000750.JPG').convert()
vrag = pygame.image.load('images/vrag.PNG').convert_alpha()
label = pygame.font.Font('fonts/ST-Brigantina-free.otf', 150)
lose_label = label.render(' Ты проиграл!', False, (103, 6, 38))
restart_label = label.render('Начать игру заново?', False, (103, 6, 38))
restart_label_kvadrat = restart_label.get_rect(topleft=(235, 450))
patron = pygame.image.load('images/patron.PNG').convert_alpha()
bullets = []
bullets_left = 3

# Шрифт для отображения счета и патронов
font = pygame.font.Font('fonts/ST-Brigantina-free.otf', 60)
small_font = pygame.font.Font('fonts/ST-Brigantina-free.otf', 40)
font2 = pygame.font.Font('fonts/ST-Brigantina-free.otf', 90)
small_font2 = pygame.font.Font('fonts/ST-Brigantina-free.otf', 70)

bgsound = pygame.mixer.Sound('sounds/bg_music.mp3')  # подкрепление музыки на фон
bgsound.play()

# фото анимации игрока вправо
walk_right = [
    pygame.image.load('images/player_right/pr1.PNG').convert_alpha(),
    pygame.image.load('images/player_right/pr2.PNG').convert_alpha(),
    pygame.image.load('images/player_right/pr3.PNG').convert_alpha(),
    pygame.image.load('images/player_right/pr4.PNG').convert_alpha()
]
# фото анимации игрока влево
walk_left = [
    pygame.image.load('images/player_left/pl1.PNG').convert_alpha(),
    pygame.image.load('images/player_left/pl2.PNG').convert_alpha(),
    pygame.image.load('images/player_left/pl3.PNG').convert_alpha(),
    pygame.image.load('images/player_left/pl4.PNG').convert_alpha()
]

vrag_timer = pygame.USEREVENT + 1
pygame.time.set_timer(vrag_timer, 5000)
vrag_list_in_game = []
player_anim_count = 0  # индекс начала фото анимации
bgx = 0  # координата начала изображения
player_speed = 15
player_x = 50  # координата начала игрока
player_y = 450
jump = False
jump_count = 13

# ДОБАВЛЕННЫЕ ПЕРЕМЕННЫЕ:
enemy_speed = 14  # начальная скорость врага
enemy_speed_increase_rate = 2  # на сколько увеличивать скорость каждые 5 врагов
enemies_spawned = 0  # счетчик созданных врагов
enemies_jumped = 0  # счетчик перепрыгнутых врагов
enemies_killed = 0  # счетчик убитых врагов

gameplay = True
running = True
while running:

    screen.blit(bg, (bgx, 0))  # вывод фона на экран
    screen.blit(bg, (bgx + 1000, 0))  # вывод цикличного фона

    if gameplay:

        player_kvadrat = walk_left[0].get_rect(topleft=(player_x, player_y))  # рамка для ограничения игрока и врага

        if vrag_list_in_game:
            # создание списка из врагов, находящихся на экране
            for (i, el) in enumerate(vrag_list_in_game):
                screen.blit(vrag, el)
                el.x -= enemy_speed

                # проверка перепрыгнутых врагов (враг ушел за левую границу)
                if el.x < -50:  # враг полностью скрылся
                    enemies_jumped += 1  # увеличиваем счетчик перепрыгнутых
                    vrag_list_in_game.pop(i)

                # если игрок соприкоснулся с врагом, завершение игры
                if player_kvadrat.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        # анимация влево или вправо
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        # ограничения по хождению игрока
        if keys[pygame.K_LEFT] and player_x > 10:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 350:
            player_x += player_speed

        # условие для прыжка 5 урок
        if not jump:
            if keys[pygame.K_UP]:
                jump = True
        else:
            if jump_count >= -13:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                jump = False
                jump_count = 13

        # обновление анимации по индексу фото
        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        # обнова экрана
        bgx -= 5
        if bgx == - 1000:
            bgx = 0

        # появление снаряда при нажатии
        if bullets:
            # перебор элементов и рисовка снарядов
            for (i, el) in enumerate(bullets):
                screen.blit(patron, (el.x, el.y))
                el.x += 4

                if el.x > 1000:
                    bullets.pop(i)

                if vrag_list_in_game:
                    for (index, vrag_el) in enumerate(vrag_list_in_game):
                        if el.colliderect(vrag_el):
                            vrag_list_in_game.pop(index)
                            enemies_killed += 1
                            bullets.pop(i)
                            break  # выходим из цикла после уничтожения снаряда

        # Отображение количества патронов
        bullets_text = font.render(f"Патроны: {bullets_left}", True, (103, 6, 38))
        screen.blit(bullets_text, (20, 10))

        #Отображение счета (перепрыгнутые и убитые враги)
        jumped_text = small_font.render(f"Перепрыгнуто: {enemies_jumped}", True, (103, 6, 38))
        killed_text = small_font.render(f"Убито: {enemies_killed}", True, (103, 6, 38))
        total_score = enemies_jumped + enemies_killed
        total_text = small_font.render(f"Всего очков: {total_score}", True, (103, 6, 38))

        screen.blit(jumped_text, (20, 70))
        screen.blit(killed_text, (20, 100))
        screen.blit(total_text, (20, 130))

    else:
        screen.fill((255, 189, 197))  # вывод фона при проигрыше
        screen.blit(lose_label, (300, 120))
        screen.blit(restart_label, restart_label_kvadrat)

        # отображение финального счета при проигрыше
        final_score_text = font2.render(f"Ваш счет: {enemies_jumped + enemies_killed}", True, (103, 6, 38))
        final_jumped_text = (small_font2.render(f"Перепрыгнуто: {enemies_jumped}", True, (103, 6, 38)))
        final_killed_text = small_font2.render(f"Убито: {enemies_killed}", True, (103, 6, 38))

        screen.blit(final_score_text, (380, 255))
        screen.blit(final_jumped_text, (380, 340))
        screen.blit(final_killed_text, (380, 390))

        # обновление игры при нажатии на кнопку
        mouse = pygame.mouse.get_pos()
        if restart_label_kvadrat.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            vrag_list_in_game.clear()
            bullets.clear()
            bullets_left = 3
            # сброс всех счетчиков при рестарте
            enemies_jumped = 0
            enemies_killed = 0
            enemies_spawned = 0
            enemy_speed = 14  # сброс скорости врага

    pygame.display.update()

    # кнопка выкл
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == vrag_timer:
            vrag_list_in_game.append(vrag.get_rect(topleft=(1002, 530)))
            enemies_spawned += 1 # увеличиваем счетчик созданных врагов

            # увеличение скорости врага каждые 5 созданных врагов
            if enemies_spawned % 5 == 0:
                enemy_speed += enemy_speed_increase_rate


        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left > 0:
            bullets.append(patron.get_rect(topleft=(player_x + 150, player_y + 100)))
            bullets_left -= 1

    clock.tick(15)