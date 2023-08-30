import pygame
from random import randrange 
from time import sleep
pygame.init()
#初始化
frame=0
map_width=284
map_height=512
FPS=60
pipes=[[180,4]]
bird=[40,map_height//2-50]
gravity = 0.2
velocity = 0

gameScreen = pygame.display.set_mode((map_width,map_height))
clock=pygame.time.Clock()

bird_wing_up = bird_wing_up_copy = pygame.image.load("images/bird_wing_up.png")
bird_wing_down = bird_wing_down_copy = pygame.image.load("images/bird_wing_down.png")
background = pygame.image.load("images/background.png")
pipe_body = pygame.image.load("images/pipe_body.png")
pipe_end = pygame.image.load("images/pipe_end.png")
#定义函数
def draw_pipes():#管道
    global pipes
    for n in range( len(pipes) ):
        for m in range( pipes[n][1] ):
            gameScreen.blit( pipe_body , ( pipes[n][0] , m*32 ) )
        for m in range( pipes[n][1]+6 , 16 ):
            gameScreen.blit( pipe_body , ( pipes[n][0] , m*32 ) )
        gameScreen.blit( pipe_end , (pipes[n][0] , (pipes[n][1])*32 ) )
        gameScreen.blit( pipe_end , (pipes[n][0] , (pipes[n][1]+5)*32 ) )
        pipes[n][0] -= 1

def draw_bird(x,y):#鸟
    global frame
    if 0 <= frame <= 30:
            gameScreen.blit(bird_wing_up,(x,y))
            frame += 1
    elif 30 < frame <= 60 :
            gameScreen.blit(bird_wing_down,(x,y))
            frame += 1
            if frame == 60 : frame = 0
def reset():#重置环境
    global frame,map_width,map_height,FPS,pipes,bird,gravity,velocity
    frame = 0
    map_width = 284
    map_height = 512
    FPS = 60
    pipes.clear()
    bird.clear()
    pipes = [[180, 4]]
    bird = [40, map_height // 2 - 50]
    gravity = 0.2
    velocity = 0
def safe():#失败判断
    if bird[1]>map_height-35:
        print("hit floor")
        return False
    if bird[1]<0:
        print("hit celling")
        return False
    if pipes[0][0]-30 < bird[0] < pipes[0][0]+79:
        if bird[1]<(pipes[0][1]+1)*32 or bird[1]>(pipes[0][1]+4)*32:
            print("hit pipe")
            return False
    return True
def gameLoop():
    global velocity,bird_wing_down,bird_wing_up
    while True: 
        if len(pipes)<4:
            x = pipes[-1][0] + 200
            open_pos = randrange(1,9)
            pipes.append([x,open_pos])#添加其余管道
        if pipes[0][0]<-80:
            pipes.pop(0)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                bird[1] -= 40
                velocity = 0
            if event.type == pygame.QUIT:    #判断是否结束
                pygame.quit() 
                return 
        velocity += gravity
        bird[1] += velocity 
        bird_wing_down = pygame.transform.rotate(bird_wing_down_copy,-90*(velocity/15))#小鸟头朝下
        bird_wing_up = pygame.transform.rotate(bird_wing_up_copy,-90*(velocity/15))
        gameScreen.blit(background,(0,0))
        draw_pipes()
        draw_bird(bird[0],bird[1])
        pygame.display.update()
        if not safe():
            sleep(3)
            reset()
        clock.tick(FPS)
gameLoop()