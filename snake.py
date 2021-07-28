import json
import pygame as pg
import random
import json
import time
pg.init()

WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Snake')
FPS = pg.time.Clock()

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

with open ('saved_game.json') as f:
    saved = json.load(f)

wall = [[int(x), 100] for x in range(160, 640, 20)] + [[int(x), 440] for x in range(160, 640, 20)]
wall += [[160, int(y)] for y in range(120, 200, 20)] + [[620, int(y)] for y in range(120, 200, 20)]
wall += [[160, int(y)] for y in range(420, 340, -20)] + [[620, int(y)] for y in range(420, 340, -20)]

font = pg.font.Font('font.ttf', 90)
window = 'intro'

snake_points = [[int(i), 260] for i in range(120, 39, -20)]
speed = 10
score = 0
key = 'R'
eaten = False
class Snake(pg.sprite.Sprite):
    def move(self):
        global snake_points, key, window
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and key != 'R': key = 'L'
        elif keys[pg.K_RIGHT] and key != 'L': key = 'R'
        elif keys[pg.K_UP] and key != 'D': key = 'U'
        elif keys[pg.K_DOWN] and key != 'U': key = 'D'     
    
    def draw(self):
        global snake_points, key, speed, score, eaten, speed
        dx, dy = snake_points[-1][0], snake_points[-1][1]
        if key == 'L':
            for i in range(len(snake_points) - 1, 0, -1):
                snake_points[i][0] = snake_points[i - 1][0]
                snake_points[i][1] = snake_points[i - 1][1]
            snake_points[0][0] -= 20
        elif key == 'R':
            for i in range(len(snake_points) - 1, 0, -1):
                snake_points[i][0] = snake_points[i - 1][0]
                snake_points[i][1] = snake_points[i - 1][1]
            snake_points[0][0] += 20
        elif key == 'D':
            for i in range(len(snake_points) - 1, 0, -1):
                snake_points[i][0] = snake_points[i - 1][0]
                snake_points[i][1] = snake_points[i - 1][1]
            snake_points[0][1] += 20
        elif key == 'U':
            for i in range(len(snake_points) - 1, 0, -1):
                snake_points[i][0] = snake_points[i - 1][0]
                snake_points[i][1] = snake_points[i - 1][1]
            snake_points[0][1] -= 20
        
        if eaten:
            snake_points.append([dx, dy])
            score += 1
            if score % 5 == 0: speed += 2
            eaten = False

        for x in range(len(snake_points)):
            if x == 0: pg.draw.rect(screen, (80, 200, 120), (snake_points[x][0], snake_points[x][1], 20, 20))
            else: pg.draw.rect(screen, (173, 255, 47), (snake_points[x][0], snake_points[x][1], 20, 20))

fx, fy = 380, 320
class Food(pg.sprite.Sprite):
    def spawn(self):
        global snake_points, eaten, fx, fy
        pg.draw.rect(screen, RED, (fx, fy, 20, 20))
        if fx == snake_points[0][0] and fy == snake_points[0][1]:
            eaten = True
            while [fx, fy] in snake_points or [fx, fy] in wall:
                fx, fy = random.randrange(0, WIDTH, 20), random.randrange(0, HEIGHT - 40, 20)

jylan = Snake()
apple = Food()

i, stage, k = 1, 1, ''
def intro():
    global i, stage, k, window, font, score, key, snake_points, speed, fx, fy
    if i == 1: pg.draw.rect(screen, WHITE, pg.Rect(220, 200, 360, 60), 3)
    else: pg.draw.rect(screen, BLACK, pg.Rect(220, 200, 360, 60), 3)
    if i == 2: pg.draw.rect(screen, WHITE, pg.Rect(220, 280, 360, 60), 3)
    else: pg.draw.rect(screen, BLACK, pg.Rect(220, 280, 360, 60), 3)
    if i == 3: pg.draw.rect(screen, WHITE, pg.Rect(220, 360, 360, 60), 3)
    else: pg.draw.rect(screen, BLACK, pg.Rect(220, 360, 360, 60), 3)
    if i == 4: pg.draw.rect(screen, WHITE, pg.Rect(220, 440, 360, 60), 3)
    else: pg.draw.rect(screen, BLACK, pg.Rect(220, 440, 360, 60), 3)

    key = pg.key.get_pressed()
    if key[pg.K_RETURN]: k = 'ENTER'
    if key[pg.K_DOWN] and i != 4: i += 1
    if key[pg.K_UP] and i != 1: i -= 1
    time.sleep(0.1)

    screen.blit(font.render('PLAY', 0, WHITE), (350, 190))
    screen.blit(font.render(f'STAGE: {stage}', 0, WHITE), (310, 270))
    screen.blit(font.render('SAVED GAME', 0, WHITE), (270, 350))
    screen.blit(font.render('EXIT', 0, WHITE), (350, 430))

    font = pg.font.Font('font.ttf', 200)
    screen.blit(font.render('Snake', 0, BLACK), (254, 24))
    screen.blit(font.render('Snake', 0, WHITE), (250, 20))
    font = pg.font.Font('font.ttf', 90)
    

    if i == 1 and k == 'ENTER': window = 'game'
    elif i == 2 and k == 'ENTER':
        if stage == 1: stage = 2
        else: stage = 1
        k = ''
        time.sleep(0.2)
    elif i == 3 and k == 'ENTER':
        if saved != None:
            snake_points = saved['snake pos']
            fx, fy = saved['food pos'][0], saved['food pos'][1]
            speed = saved['speed']
            score = saved['score']
            stage = saved['stage']
            key = saved['key']
            window = 'game'
            window = 'game'
        k = ''
    elif i == 4 and k == 'ENTER': exit()

def crush_test():
    global snake_points, window
    if snake_points[0][0] < 0 or snake_points[0][0] >= WIDTH: window = 'game over'
    if snake_points[0][1] < 0 or snake_points[0][1] >= HEIGHT - 40: window = 'game over'
    if snake_points[0] in snake_points[1:]: window = 'game over'
    if stage == 2 and snake_points[0] in wall: window = 'game over'

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
    
    screen.blit(pg.image.load('bg.png'), (0, 0))

    keys = pg.key.get_pressed()
    if keys[pg.K_s]: k = 's'
    if k == 's' and (window == 'game' or window == ''):
        saving = {
                'snake pos' : snake_points,
                'food pos' : [fx, fy],
                'score' : score,
                'stage' : stage,
                'speed' : speed,
                'key' : key
            }
        with open ('saved_game.json', 'w') as out:
            json.dump(saving, out)
        window = ''
        screen.blit(font.render('Game saved', 0, WHITE), (260, 250))

    if window == 'intro': intro()

    elif window == 'game':
        pg.draw.rect(screen, BLACK, (0, HEIGHT - 40, WIDTH, 40))
        if stage == 2:
            for x in wall: pg.draw.rect(screen, BLACK, (x[0], x[1], 20, 20))

        jylan.draw()
        apple.spawn()
        jylan.move()

        font = pg.font.Font('font.ttf', 50)
        screen.blit(font.render(f'SCORE: {score}', 0, WHITE), (10, 560))
        screen.blit(font.render(f'STAGE: {stage}', 0, WHITE), (600, 560))
        font = pg.font.Font('font.ttf', 90)

        crush_test()

    elif window == 'game over':
        font = pg.font.Font('font.ttf', 200)
        screen.blit(font.render('Game Over', 0, BLACK), (144, 104))
        screen.blit(font.render('Game Over', 0, WHITE), (140, 100))
        font = pg.font.Font('font.ttf', 90)
        screen.blit(font.render(f'Your score: {score}', 0, WHITE), (250, 300))
        font = pg.font.Font('font.ttf', 40)
        screen.blit(font.render('Tap to SPACE to exit', 0, WHITE), (290, 550))
        font = pg.font.Font('font.ttf', 90)

        pg.draw.rect(screen, WHITE, (140, 280, 530, 7))

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]: exit()

    FPS.tick(speed)
    pg.display.update()