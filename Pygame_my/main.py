import pygame, random, sys
from database import get_best, cur, insert_result

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((960, 540))
pygame.display.set_caption("Последний монах")

icon = pygame.image.load('images/ico.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('images/back.png').convert_alpha()

first_bg = pygame.image.load('images/FirstBack.jpg').convert_alpha()

walk_right = [
    pygame.image.load('images/moove_right/r1.png').convert_alpha(),
    pygame.image.load('images/moove_right/r2.png').convert_alpha()
]
walk_left = [
    pygame.image.load('images/moove_left/l1.png').convert_alpha(),
    pygame.image.load('images/moove_left/l2.png').convert_alpha()
]

monstr = pygame.image.load('images/monstr.png').convert_alpha()
monstr_list_in_game = []

kolchan = pygame.image.load('images/kolch.png').convert_alpha()
kolchan_list_in_game = []

fat_monster_list = [
    pygame.image.load('images/fat_monster/rad1.png').convert_alpha(),
    pygame.image.load('images/fat_monster/rad2.png').convert_alpha()
]
fat_monster_list_in_game = []

rock = pygame.image.load('images/rock.png').convert_alpha()
rock_list_in_game = []

player_anim_count = 0
fat_monster_anim_count = 0
bg_x = 0

fat_monster_life = 10

player_speed = 20
player_x = 250
player_y = 430

is_jump = False #индикатор прыжка
jump_count = 10 #высота прыжка

bg_sound = pygame.mixer.Sound("sounds/chocolate.mp3")
bg_sound.play(-1)

shoot_sound = pygame.mixer.Sound("sounds/Shoot.mp3")

jump_sound = pygame.mixer.Sound("sounds/Jump.mp3")

kolchan_taken = pygame.mixer.Sound("sounds/kolch_take.mp3")

arrow_shot = pygame.mixer.Sound("sounds/arrow.mp3")

monstr_timer = pygame.USEREVENT + 1
pygame.time.set_timer(monstr_timer, 6000)

kolchan_timer = pygame.USEREVENT + 2
pygame.time.set_timer(kolchan_timer, 4000)

fat_monster_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fat_monster_timer, 30000)

score_timer = pygame.USEREVENT + 4
pygame.time.set_timer(score_timer, 1000)

label = pygame.font.Font("fonts/Oswald-VariableFont_wght.ttf", 40)
m_label = pygame.font.Font("fonts/Oswald-VariableFont_wght.ttf", 20)

lose_label = label.render("Вы проиграли!", False, (240, 240, 240))
restart_label = label.render("Начать заново!", False, (40, 240, 40))
restart_label_rect = restart_label.get_rect(topleft =(360, 300))

begin_label = label.render("PLAY", True, (40, 240, 40))
begin_label_rect = begin_label.get_rect(topleft =(200, 300))

name_saved_label = label.render("Имя выбрано, данные сохранены !", True, (200, 240, 40))
name_saved_label_rect = name_saved_label.get_rect(topleft=(200, 450))

gamers_top = get_best()
one_best_score = gamers_top[0][1]


bullet = pygame.image.load('images/patronR.png'). convert_alpha()
bullets = []
bullets_left = 5

gameplay = False
first_screen = True

G_USER_NAME = None
user_name = "Введите имя"

running = True

score = 0
score_buf = 0
while running:
    if first_screen:
        screen.blit(first_bg, (0, 0))
        lab_y = 100
        for index, gamer in enumerate(gamers_top):
            name, score_f = gamer
            s = f"{index + 1}.{name} - {score_f}"
            top_label = label.render(f"{s}", True, (200, 200, 250))
            screen.blit(top_label, (200, lab_y))
            lab_y+=50
            if index == 0:
                best_score = f"{name} - {score_f}"
        screen.blit(begin_label, begin_label_rect)
        pygame.draw.rect(first_bg, (40, 240, 40),(180, 302, 125, 60), 3)
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if user_name == "Введите имя":
                        user_name = event.unicode
                    else:
                        user_name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1] #срез всех символов кроме последнего
                elif event.key == pygame.K_RETURN:
                    if len(user_name)>2:
                        G_USER_NAME = user_name
                        print("Ok")


        name_label = label.render(user_name, True, (255, 102, 0))
        name_label_rect = name_label.get_rect(topleft=(200, 400))
        screen.blit(name_label, name_label_rect)
        if G_USER_NAME == user_name:
            screen.blit(name_saved_label, name_saved_label_rect)

        if begin_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            first_screen = False







    if gameplay:
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 960, 0))

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y)) #квадрат вокруг игрока

        arrows_count_label = m_label.render(f'Arrows: {bullets_left}', True, (10, 250, 10))
        screen.blit(arrows_count_label, (150, 20))

        score_label = m_label.render(f'Score: {score}', True, (250, 250, 250))
        screen.blit(score_label, (280, 20))

        best_score_label = m_label.render(f'Best score: {best_score}', True, (100, 100, 250))
        screen.blit(best_score_label, (380, 20))

        if monstr_list_in_game:
            for (i, el) in enumerate(monstr_list_in_game):
                screen.blit(monstr, el)
                el.x -= 10

                if el.x < -10:
                    monstr_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        if fat_monster_list_in_game:
            m_life_label = m_label.render(f'{fat_monster_life}', False, (250, 10, 10))
            for (i, el) in enumerate(fat_monster_list_in_game):
                screen.blit(fat_monster_list[fat_monster_anim_count], el)
                el.x -= 2
                screen.blit(m_life_label, (el.x+60, 330))

                if el.x < -70:
                    fat_monster_list_in_game.pop(i)
                if player_rect.colliderect(el):
                    gameplay = False

        if fat_monster_anim_count == 1: #определяет индекс картинки из списка картинок
            fat_monster_anim_count = 0
        else:
            fat_monster_anim_count+=1


        if kolchan_list_in_game:
            for (i, el) in enumerate(kolchan_list_in_game):
                screen.blit(kolchan, el)
                el.y += 10

                if el.y > 540:
                    kolchan_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    kolchan_list_in_game.pop(i)
                    kolchan_taken.play()
                    bullets_left+=5

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y)) #подбор картинки исходя от нажатой кнопки либо влево либо вправо
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 5: #движение игрока исходя от нажатий кнопок
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 900:
            player_x += player_speed


        if not is_jump: #блок кода для прыжка
            if keys[pygame.K_SPACE]: #проверка нажати ли клавиша пробелв
                is_jump = True
                jump_sound.play()
        else:
            if jump_count >= -10:
                if jump_count > 0:
                    player_y -= (jump_count ** 2)/2
                else:
                    player_y += (jump_count ** 2)/2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 10


        if player_anim_count == 1: #определяет индекс картинки из списка картинок
            player_anim_count = 0
        else:
            player_anim_count+=1

        bg_x -= 2 #отвечает за движение фона
        if bg_x == -960:
            bg_x = 0



        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x+=30

                if el.x > 960:
                    bullets.pop(i)

                if monstr_list_in_game and bullets:
                    for (index, flame_el) in enumerate(monstr_list_in_game):
                        if el.colliderect(flame_el):
                            monstr_list_in_game.pop(index)
                            score+=2
                            bullets.pop(i)
                            shoot_sound.play()

                if fat_monster_list_in_game and bullets:
                    for (index, fat_el) in enumerate(fat_monster_list_in_game):
                        if el.colliderect(fat_el):
                            if fat_monster_life == 1:
                                fat_monster_list_in_game.pop(index)
                                score+=10
                                fat_monster_life = 10
                            else:
                                fat_monster_life-=1
                            bullets.pop(i)
                            shoot_sound.play()
        score_buf = score

    elif not gameplay and not first_screen:
        screen.fill((1, 1, 1))
        screen.blit(lose_label, (360, 200))
        screen.blit(restart_label, restart_label_rect)
        if score_buf > one_best_score:
            text = f"Вы побили рекорд, ваш результат {score_buf}!"
        else:
            text = f"Рекорд не побит, ваш результат {score_buf}!"
        one_best_score_label = label.render(text, True, (240, 240, 240))
        screen.blit(one_best_score_label, (250, 400))
        score = 0

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            insert_result(user_name, score_buf)
            gameplay = True
            player_x = 250
            monstr_list_in_game.clear()
            fat_monster_list_in_game.clear()
            bullets.clear()
            bullets_left = 5
            kolchan_list_in_game.clear()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            insert_result(user_name, score_buf)
            score = 0
            running = False
            pygame.quit()
            sys.exit(0)
        if event.type == monstr_timer:
            monstr_list_in_game.append(monstr.get_rect(topleft =(965, 430)))

        if event.type == fat_monster_timer:
            fat_monster_list_in_game.append(fat_monster_list[fat_monster_anim_count].get_rect(topleft =(965, 370)))

        if event.type == kolchan_timer: #внесение в список колчана и его координат в случайном порядке по коррдинате х
            kolchan_list_in_game.append(kolchan.get_rect(topleft =(random.randint(50, 910), -50)))

        if event.type == score_timer:
            score+=1

        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_f and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft = (player_x + 56, player_y+13)))
            bullets_left-=1
            arrow_shot.play()

    clock.tick(15)