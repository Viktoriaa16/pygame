import pygame

clock = pygame.time.Clock()

# создаем параметры экрана, название игры и иконку игры
pygame.init()
screen = pygame.display.set_mode((917, 585))
pygame.display.set_caption("Pygame Run or Die")
icon = pygame.image.load('images/icon_witch1.ico')
pygame.display.set_icon(icon)

# подключение фона игры и персонажев
bg = pygame.image.load('images/les2.png')
# список движение влево и вправо
walk_left = [
    pygame.image.load('images/player_left/player_left1.png'),
    pygame.image.load('images/player_left/player_left2.png'),
    pygame.image.load('images/player_left/player_left3.png'),
    pygame.image.load('images/player_left/player_left4.png'),
]
walk_right = [
    pygame.image.load('images/player_right/player_right1.png'),
    pygame.image.load('images/player_right/player_right2.png'),
    pygame.image.load('images/player_right/player_right3.png'),
    pygame.image.load('images/player_right/player_right4.png'),
]

witch = pygame.image.load('images/witch.png')
witch_x = 800
witch_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 200
player_y = 430

is_jump = False
jump_count = 8

bg_sound = pygame.mixer.Sound('sounds/bg.mp3')
bg_sound.play()

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

label = pygame.font.Font('fonts/Roboto.ttf', 40)
lose_label = label.render('Вы проиграли!', False, (163, 10, 10))
restart_label = label.render('Играть заново', False, (0, 0, 0))
restart_label_rect = restart_label.get_rect(topleft=(300, 300))

bullets_left = 50
bullet = pygame.image.load('images/potion.png')
bullets = []

gameplay = True

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 917, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if witch_list_in_game:
            for (i, el) in enumerate(witch_list_in_game):
                screen.blit(witch, el)
                el.x -= 10

                if el.x < -10:
                    witch_list_in_game.pop(i)



                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -917:
            bg_x = 0


        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 1030:
                    bullets.pop(i)

                if witch_list_in_game:
                    for (index, witch_el) in enumerate(witch_list_in_game):
                        if el.colliderect(witch_el):
                            witch_list_in_game.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((48, 156, 123))
        screen.blit(lose_label,(300, 180))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 400
            witch_list_in_game.clear()
            bullets.clear()


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            witch_list_in_game.append(witch.get_rect(topleft=(800, 430)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1


    clock.tick(15)
