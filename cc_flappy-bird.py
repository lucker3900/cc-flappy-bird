import pygame
from pygame.midi import frequency_to_midi

from pipe import Pipe
from bird import Bird

import random

# 游戏窗口设置
SCREEN_WIDTH = 780
SCREEN_HEIGHT = 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.mixer.init()  # 初始化音频系统

clock = pygame.time.Clock()
run = True
x = 0
y = 0
gd_x = 0
pipe_x = 200
pipe_speed = 4
pipe_distance = 150

pipes_top = []
pipes_btm = []

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
bg_img = pygame.image.load("img/bg.png")
bg_img = pygame.transform.scale(bg_img, (780, 600))
#bird1_img = pygame.image.load("img/bird1.png")
ground_img = pygame.image.load("img/ground.png")
pipe_btm_img = pygame.image.load("img/pipe.png")
restart_img = pygame.image.load("img/restart.png")
bg_music = pygame.mixer.Sound("sound/bgm.wav")
bg_music.set_volume(0.3)
bg_music.play(-1)  # 循环播放背景音乐

print(pipe_x)
#pipe_btm = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT/2 + pipe_distance/2, pipe_btm_img, False)

pipe_top_img = pygame.transform.flip(pipe_btm_img, False, True)
#旋转管子180度
#pipe_top = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT/2 - pipe_distance/2, pipe_top_img, True)

pipe_sprite = pygame.sprite.Group()

#pipe_sprite.add(pipe_btm)
#pipe_sprite.add(pipe_top)

bird_imgs = []
for i in range(1, 3):
    bird_imgs.append(pygame.image.load(f"img/bird{i}.png"))

#bird_sprite.add(bird_imgs)
bird = Bird(100, SCREEN_HEIGHT/2, bird_imgs)
bird.set_ground_height(SCREEN_HEIGHT - 100)  # 设置地面高度

bird_sprite = pygame.sprite.Group()
bird_sprite.add(bird)

pygame.display.set_caption("cc飞小鸟")
pygame.display.set_icon(bird_imgs[0])

#分数记录
game_score = 0

font = pygame.font.Font("微软正黑体.ttf", 30)

frequency = 1500
last_update = pygame.time.get_ticks() - frequency

game_over = False

while run:
    clock.tick(FPS)

    #游戏输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if game_over:
                    # 重置游戏
                    game_over = False
                    game_score = 0
                    bird.rect.center = (100, SCREEN_HEIGHT/2)
                    bird.down_speed = 0
                    pipe_sprite.empty()  # 清空所有管道
                else:
                    bird.jump(True)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not game_over:
                bird.jump(True)
            elif event.key == pygame.K_SPACE and game_over:
                # 重置游戏
                game_over = False
                game_score = 0
                bird.rect.center = (100, SCREEN_HEIGHT/2)
                bird.down_speed = 0
                pipe_sprite.empty()  # 清空所有管道
                last_update = pygame.time.get_ticks() - frequency  # 重置管道生成时间
                bg_music.play(-1)  # 重新播放背景音乐

    if (pygame.mouse.get_pressed()[0] or pygame.key.get_pressed()[pygame.K_UP]) and not game_over:
            bird.jump(False)

    #游戏结束
    if pygame.sprite.groupcollide(bird_sprite, pipe_sprite, False, False)\
       or bird.rect.bottom >= SCREEN_HEIGHT -100\
       or bird.rect.top <= 0:
        if not game_over:  # 只在第一次碰撞时停止音乐
            bg_music.stop()
        game_over = True

    #游戏更新
    if not game_over:
        bird_sprite.update()
        pipe_sprite.update()
        #碰撞判断
        now = pygame.time.get_ticks()


        if now - last_update > frequency:
            # 生成一个管子
            pipe_y = random.randint(-100, 100)
            pipe_btm = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT / 2 + pipe_distance/2 + pipe_y, pipe_btm_img, False)
            pipe_top = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT / 2 - pipe_distance/2 + pipe_y, pipe_top_img, True)
            #pipe_sprite = pygame.sprite.Group()

            pipe_sprite.add(pipe_btm)
            pipe_sprite.add(pipe_top)
            last_update = now

        pipes = pipe_sprite.sprites()
        if len(pipes) > 0:
            first_pipe = pipes[0]
            if bird.rect.left > first_pipe.rect.right and first_pipe.cross_pipe:
                print(f"第一根柱子坐标{first_pipe.rect.right}")
                game_score += 1
                first_pipe.cross_pipe = False

        # 游戏显示
        window.blit(bg_img, (0,0))
        #window.draw.rect(groun, (255, 0, 0), (900, SCREEN_HEIGHT - 100, 100, 100))
        gd_x -= 4
        if(gd_x <= -100):
            gd_x = 0
    else:
        bird.drop()

    window.blit(bg_img, (0, 0))
    bird_sprite.draw(window)
    pipe_sprite.draw(window)
    window.blit(ground_img, (gd_x, SCREEN_HEIGHT - 100))

    #显示分数
    cc_text = font.render("CC无聊纯娱乐", True, (0, 0, 255))
    window.blit(cc_text, (SCREEN_WIDTH / 2 - 100, 0))
    score_text = font.render(f"得分:{str(game_score)}", True, (0, 0, 255))
    window.blit(score_text, (SCREEN_WIDTH/2 - 50, 50))

    if game_over:
        # 获取重启按钮的矩形区域并设置中心点
        restart_rect = restart_img.get_rect()
        restart_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)  # 设置为屏幕中心
        window.blit(restart_img, restart_rect)  # 使用rect来定位

    pygame.display.update()

pygame.quit()