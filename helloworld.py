# import requests
# URL='http://naver.com'
# resp=requests.get(URL)
# print(resp.text)


# import sklearn


# import tensorflow



# for i in range(1,6):
#     print(i,end='\t')
# print()


# import pygame
# import numpy



import pygame
import os
import random
pygame.init()

screen_width=640
screen_height=480
screen=pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("by Cha")
clock=pygame.time.Clock()
rateFrame=30

#dir설정
# current_path=os.path.dirname(__file__)
# image_path=os.path.join(current_path, "images")
image_path=os.path.dirname(__file__)

#배경 이미지 설정
background=pygame.image.load(os.path.join(image_path, "background1.jpg"))

#스테이지 설정
stage=pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size=stage.get_rect().size
stage_height=stage_size[1]
stage_y_pos=(screen_height-stage_height)

#캐릭터 설정
character=pygame.image.load(os.path.join(image_path, "character.png"))
character_size=character.get_rect().size
character_width=character_size[0]
character_height=character_size[1]
character_x_pos=(screen_width-character_width)/2
character_y_pos=(screen_height-stage_height-character_height)
character_to_x=0
character_speed=3

#무기설정
weapon=pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size=weapon.get_rect().size
weapon_width=weapon_size[0]
weapon_speed=10
#무기는 한번에 여러발 발사 가능
weapons=[]

#공 만들기 (4개 크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]
#공 크기에 따른 최초 스피드
ball_speed_y=[-18,-15,-12,-9]   #index 0,1,2,3에 해당하는
#공 들
balls=[]
#최초 발생하는 큰 공 추가
balls.append({
    "pos_x":50, #공의 x좌표
    "pos_y":50, #공의 y좌표
    "img_idx":0,    #공의 img index
    "to_x":3,   #공의 x축 이동 방향
    "to_y":-6,  #공의 y축 이동 방향
    "init_spd_y":ball_speed_y[0]  #y 최초 속도  
})



running=True
while running:
    dt=clock. tick(rateFrame)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                character_to_x-=character_speed
            elif event.key==pygame.K_RIGHT:
                character_to_x+=character_speed
            elif event.key==pygame.K_SPACE:
                weapon_x_pos=character_x_pos+character_width/2-weapon_width/2   #캐릭터의 정중앙
                weapon_y_pos=character_y_pos    #캐릭터의 머리에서 발사
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                character_to_x=0

    character_x_pos+=character_to_x
    if character_x_pos<=0:
        character_x_pos=0
    elif character_x_pos>=(screen_width-character_width):
        character_x_pos=(screen_width-character_width) 

    #무기 위치 조정
    weapons=[ [w[0], w[1]-weapon_speed] for w in weapons ]
    #천장에 닿은 무기 없애기
    weapons=[ [w[0], w[1]] for w in weapons if w[1]>0]

    #공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_x_pos=ball_val["pos_x"]
        ball_y_pos=ball_val["pos_y"]
        ball_img_idx=ball_val["img_idx"]

        ball_size=ball_images[ball_img_idx].get_rect().size
        ball_width=ball_size[0]
        ball_height=ball_size[1]

        #가로벽에 닿았을 때 공 이동 위치 변경(튕겨 나오는 효과)
        if ball_x_pos<=0 or ball_x_pos>(screen_width-ball_width):
            ball_val["to_x"]=ball_val["to_x"]*(-1)
        #세로 위치
        #스테이지에 튕겨서 올라가는 처리
        if ball_y_pos>=(screen_height-stage_height-ball_height):
            ball_val["to_y"]=ball_val["init_spd_y"]
        else:   #그 외의 모든 경우는 속도를 증가
            ball_val["to_y"]+=0.5

        ball_val["pos_x"]+=ball_val["to_x"]
        ball_val["pos_y"]+=ball_val["to_y"]



    screen.blit(background, (0, 0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    # for idx, val in enumerate(balls):
    #     ball_x_pos=val["pos_x"]
    #     ball_y_pos=val["pos_y"]
    #     ball_img_idx=val["img_idx"]
    #     screen.blit(ball_images[ball_img_idx], (ball_x_pos, ball_y_pos))
    for val in balls:
        ball_x_pos=val["pos_x"]
        ball_y_pos=val["pos_y"]
        ball_img_idx=val["img_idx"]
        screen.blit(ball_images[ball_img_idx],(ball_x_pos,ball_y_pos))
    screen.blit(stage, (0, stage_y_pos))
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update()



pygame.time.delay(2000)
pygame.quit()