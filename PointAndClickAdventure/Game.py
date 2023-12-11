import pygame
import random

from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption("Soul Render")
clock = pygame.time.Clock()
test_font = pygame.font.Font(None,50)
game_active = False

# Background Settings
sky_surface = pygame.image.load("Images\IMG_2620.jpg").convert_alpha()
ground_surface = pygame.image.load("Images\IMG_2622.jpg").convert_alpha()
background_surface = [pygame.image.load("Images\Background.png").convert_alpha(),
                      pygame.image.load("Images\Background2.png").convert_alpha(),
                      pygame.image.load("Images\Background3.png").convert_alpha(),
                      pygame.image.load("Images\Background4.png").convert_alpha()]
bg1 = random.randint(0, 3)
bg2 = random.randint(0, 3)
currentbg = 1
start_screen_background_surface = pygame.image.load("Images\pgkks5by.png")
start_screen_foreground_surface = pygame.image.load("Images\Start Screen.png")
start_screen_play_words_surface = pygame.image.load("Images\hg7iomdm2.png")
# Music
songs = [pygame.mixer.Sound("Images\Music\Soul Render Song 1.mp3"),
         pygame.mixer.Sound("Images\Music\Soul Render Song 2.mp3"),
         pygame.mixer.Sound("Images\Music\Soul Render Song 3.mp3"),
         pygame.mixer.Sound("Images\Music\Soul Render Song 4.mp3"),
         pygame.mixer.Sound("Images\Music\Soul Render Song 6.mp3")]
current_song = random.randint(0,4)
songs[current_song].play()
song_timer = pygame.USEREVENT + 1
pygame.time.set_timer(song_timer, int(songs[current_song].get_length()*1000))
# Game Score
text_surface = test_font.render("Number Of Souls:", True, "White")
text_rect = text_surface.get_rect(midleft = (355, 50))
current_score = 0
typable_score = str(current_score)
score_surface = test_font.render(typable_score, True, "White")
score_rect = score_surface.get_rect(midleft = (650, 50))

background_x_pos = 0

# Player Settings
player_x = 150
player_y = 480
player_walk_default = pygame.image.load("Images\Animations\Player Character\Player Default.png").convert_alpha()
player_walk_1 = pygame.image.load("Images\Animations\Player Character\Walk\Walk 1.png").convert_alpha()
player_walk_2 = pygame.image.load("Images\Animations\Player Character\Walk\Walk 2.png").convert_alpha()
player_walk_3 = pygame.image.load("Images\Animations\Player Character\Walk\Walk 3.png").convert_alpha()
player_fall = pygame.image.load("Images\Animations\Player Character\Walk\Walk 3.png").convert_alpha()
player_jump = pygame.image.load("Images\Animations\Player Character\Player Jump.png").convert_alpha()
player_walk_cycle = [player_walk_default,player_walk_1 , player_walk_2, player_walk_3]
player_death_cycle = [pygame.image.load("Images\Animations\Player Character\Player Death\Player Death 1.png").convert_alpha(),
                      pygame.image.load("Images\Animations\Player Character\Player Death\Player Death 2.png").convert_alpha(),
                      pygame.image.load("Images\Animations\Player Character\Player Death\Player Death 3.png").convert_alpha(),
                      pygame.image.load("Images\Animations\Player Character\Player Death\Player Death 4.png").convert_alpha(),
                      pygame.image.load("Images\Animations\Player Character\Player Death\Player Death 5.png").convert_alpha(),
                      pygame.image.load("Images\Animations\Player Character\Player Death\Player Death 6.png").convert_alpha(),
                      pygame.image.load("Images\Animations\Player Character\Player Death\Player Death 7.png").convert_alpha(),
                      pygame.image.load("Images\Animations\Player Character\Player Death\Player Death 8.png").convert_alpha(),
                      pygame.image.load("Images\Animations\Player Character\Player Death\Player Death 9.png").convert_alpha(),
                      pygame.image.load("Images\Animations\Player Character\Player Death\Player Death 10.png").convert_alpha(),]
player_attack_cycle = [pygame.image.load("Images\Animations\Player Character\Attack\Attack 1.png"),
                       pygame.image.load("Images\Animations\Player Character\Attack\Attack 2.png"),
                       pygame.image.load("Images\Animations\Player Character\Attack\Attack 3.png"),
                       pygame.image.load("Images\Animations\Player Character\Attack\Attack 4.png"),
                       pygame.image.load("Images\Animations\Player Character\Attack\Attack 5.png"),
                       pygame.image.load("Images\Animations\Player Character\Attack\Attack 6.png"),]
player_index = 0
player_animation_ticks = 0
player_surface = player_walk_cycle[player_index]
player_rect = player_surface.get_rect(midbottom = (player_x,player_y))
player_attack_rect = player_surface.get_rect(midbottom = (player_x + 100, player_y))
player_gravity = 0
hit_time = 0
player_attacking = False
player_attack_tally = 0
player_dead = False
player_dead_tally = 0
total_kills = 0
tot_score_surface = test_font.render("Score " + str(total_kills), True, "White")
tot_score_rect = tot_score_surface.get_rect(midbottom = (555, 550))

def player_animation():
    global player_index, player_surface, settings
    if settings[player_gravity] == 0:
        if player_attacking == False:
            player_index += .1
            if player_index > 3:
                player_index = 0
            player_surface = player_walk_cycle[int(player_index)]
        if settings[player_gravity] > 0:
            player_surface = player_fall
            player_index = 0
        if settings[player_gravity] < 0:
            player_surface = player_jump
            player_index = 0


# Enemy Settings
enemy_speed = 2
    # Axer Settings
axer_default = pygame.image.load("Images\Animations\Axer\Axer.png").convert_alpha()
axer_walk_1 = pygame.image.load("Images\Animations\Axer\Axer Walked\Walk 1.png").convert_alpha()
axer_walk_2 = pygame.image.load("Images\Animations\Axer\Axer Walked\Walk 2.png").convert_alpha()
axer_walk_cycle = [axer_default, axer_walk_1]
axer_index = 0
axer_surface = axer_walk_cycle[axer_index]
    # Hammerer Settings
hammerer_default = pygame.image.load("Images\Animations\Hammerer\Hammerer.png").convert_alpha()
hammerer_walk_1 = pygame.image.load("Images\Animations\Hammerer\Hammerer Walk\Walk 1.png").convert_alpha()
hammerer_walk_2 = pygame.image.load("Images\Animations\Hammerer\Hammerer Walk\Walk 2.png").convert_alpha()
hammerer_walk_cycle = [hammerer_default, hammerer_walk_1, hammerer_walk_2]
hammerer_index = 0
hammerer_surface = hammerer_walk_cycle[hammerer_index]

    # Enemy List
enemy_rect_list = []

    # Enemy Movement
def enemy_movement(enemy_list):
    global axer_index, axer_surface, hammerer_index, hammerer_surface,settings
    if axer_index >= 1.9:
        axer_index = 1
        axer_surface = axer_walk_cycle[int(axer_index)]
        axer_index = 0
    else:
        axer_index += .05
        axer_surface = axer_walk_cycle[int(axer_index)]

    if hammerer_index >= 2.9:
        hammerer_index = 2
        hammerer_surface = hammerer_walk_cycle[int(hammerer_index)]
        hammerer_index = 0
    else:
        hammerer_index += .05
        hammerer_surface = hammerer_walk_cycle[int(hammerer_index)]

    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= settings[enemy_speed]
            if enemy_rect.bottom == 480:
                screen.blit(axer_surface, enemy_rect)
            else:
                screen.blit(hammerer_surface, enemy_rect)
            enemy_list = [enemy for enemy in enemy_list if enemy.x > -200]
            if settings[enemy_speed] < 25:
                for enemy in enemy_list:
                    if enemy.x < -200:
                        settings[enemy_speed] += 1



        return enemy_list
    else: return []
# Timer Settings
obstacle_timer = pygame.USEREVENT + 2
pygame.time.set_timer(obstacle_timer, 4800)

    # Enemy Collision
def collision(player, enemy_list):
    if enemy_list:
        for enemy_rect in enemy_list:
            if player.colliderect(enemy_rect) == True:
                return True

def att_collision(player, enemy_list):
    if enemy_list:
        for enemy_rect in enemy_list:
            if player.colliderect(enemy_rect) == True:
                return enemy_rect


settings = {
    current_score : 0,
    typable_score : str(current_score),
    player_x : 150,
    player_y : 480,
    player_gravity : 0,
    hit_time : 0,
    enemy_speed : 2,
    player_animation_ticks : 0
}


def Default_Settings(settings):
    settings[current_score] = 0
    settings[typable_score] = str(settings[current_score])
    settings[player_x] = 150
    settings[player_y] = 480
    settings[player_gravity] = 0
    settings[enemy_speed] = 2
    settings[hit_time] = 0
    settings[player_animation_ticks] = 0

#Default_Settings(settings)

# Running The Game
while True:
    # Controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if not player_attacking:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player_attacking = True
            # Timer Event
            if event.type == obstacle_timer:
                if random.randint(0,2):
                    enemy_rect_list.append(axer_surface.get_rect(midbottom=(random.randint(1800, 2000), 480)))
                else:
                    enemy_rect_list.append(hammerer_surface.get_rect(midbottom=(random.randint(1800, 2000), 470)))

        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                Default_Settings(settings)
                axer_rect = axer_surface.get_rect(midbottom=(700, 480))
                player_rect: player_surface.get_rect(midbottom=(settings[player_x], settings[player_y]))
                total_kills = 0
                current_score = 0
        # Plays Music
        if event.type == song_timer:
            print(song_timer)
            songs[current_song].stop()
            current_song = random.randint(0,4)
            songs[current_song].play()
            pygame.time.set_timer(song_timer, int(songs[current_song].get_length() * 60000))

    # Movement Controls
    keys = pygame.key.get_pressed()
    if player_dead == False:
        if player_attacking == False:
            if keys[pygame.K_LEFT]:
                if settings[player_x] >= 50:
                    settings[player_x] -= 7
                    player_animation()
                else:
                    settings[player_x] = 50
            if keys[pygame.K_RIGHT]:
                settings[player_x] += 7
                player_animation()
            if keys[pygame.K_UP]:
                if settings[player_y] >= 480:
                    settings[player_gravity] = -20
            if keys[pygame.K_DOWN]:
                print("down")
    player_rect = player_surface.get_rect(midbottom=(settings[player_x], 555)) # Sets Player X Posistion
    #    if event.type == pygame.MOUSEMOTION:
    if game_active:# This will start the game loop
        # Draw all our Elements
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,490))
        screen.blit(background_surface[bg1],(background_x_pos,0))
        screen.blit(background_surface[bg2], (background_x_pos + 1299,0))
        if background_x_pos < -1299:
            background_x_pos = 0 # Looping the background
            bg1 = bg2
            bg2 = random.randint(0, 3)
        background_x_pos -= 3
        screen.blit(text_surface,text_rect)
        score_surface = test_font.render(settings[typable_score], True, "White")
        screen.blit(score_surface, score_rect)

        # Enemy Movement
        enemy_rect_list = enemy_movement(enemy_rect_list)


        # Player Movement
        settings[player_gravity] += 1
        settings[player_y] += settings[player_gravity]
        if settings[player_y] > 480:
            settings[player_y] = 480
            settings[player_gravity] = 0
        player_rect = player_surface.get_rect(midbottom=(settings[player_x], settings[player_y]))
        screen.blit(player_surface, player_rect)

        # Player Attack
        if player_attacking == True:
            player_attack_tally += .05
            player_surface = player_attack_cycle[int(player_attack_tally)]
            if player_attack_tally >= 5.6:
                player_attacking = False
                player_attack_tally = 0
                player_index = 0
                player_surface = player_walk_cycle[player_index]
                player_attack_rect = player_surface.get_rect(midbottom = (settings[player_x] + 100, settings[player_y]))
                if collision(player_attack_rect, enemy_rect_list):
                    enemy_rect_list.remove(att_collision(player_attack_rect, enemy_rect_list))
                    current_score += 1
                    settings[typable_score] = str(current_score)
                    total_kills += 1
                    settings[enemy_speed] = int(total_kills/2) + 2
        # Collisions
        if not player_attacking:
            if collision(player_rect, enemy_rect_list) == True:
                hit_time += 1
                if hit_time == 10:
                    current_score -= 1
                    settings[typable_score] = str(current_score)
                    hit_time = 0
                    if current_score <= 0:
                        player_dead = True

        if player_dead == True:
            player_dead_tally += .075
            player_surface = player_death_cycle[int(player_dead_tally)]
            if player_dead_tally >= 9.6:
                game_active = False
                enemy_rect_list.clear()
                player_dead = False
                player_dead_tally = 0
                player_index = 0
                player_surface = player_walk_cycle[player_index]

        mouse_position = pygame.mouse.get_pos()
        if player_rect.collidepoint(mouse_position):
            pygame.mouse.get_pressed()


    else:
        screen.blit(start_screen_background_surface, (0,0))
        screen.blit(start_screen_foreground_surface, (450,100))
        screen.blit(start_screen_play_words_surface, (300,10))
        tot_score_surface = test_font.render("Score " + str(total_kills), True, "White")
        screen.blit(tot_score_surface, tot_score_rect)

    # Update Everything
    pygame.display.update()
    clock.tick(60)