import pygame
import sys
from pygame.locals import *
import random
import time
import csv

# Kích thước cửa sổ
WINDOWWIDTH = 800
WINDOWHEIGHT = 500
pygame.init()
w = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tải ảnh nền
BG = pygame.image.load('buoi7/bg2.jpg')
BG = pygame.transform.scale(BG, (WINDOWWIDTH, WINDOWHEIGHT))

# Tải ảnh các quả
tao = pygame.image.load('buoi7/tao.jpg')
tao = pygame.transform.scale(tao, (40, 50))
cam = pygame.image.load('buoi7/cam.jpg')
cam = pygame.transform.scale(cam, (40, 50))
xoai = pygame.image.load("buoi7/xoai.jpg")
xoai = pygame.transform.scale(xoai, (40, 50))
bom = pygame.image.load('buoi7/bom.webp')
bom = pygame.transform.scale(bom, (40, 50))
dua = pygame.image.load('buoi7/dua.webp')
dua = pygame.transform.scale(dua, (40, 50))
lemon = pygame.image.load('buoi7/chanh.webp')
lemon = pygame.transform.scale(lemon, (40, 50))

FPS = 60
fpsClock = pygame.time.Clock()

# Giao diện chính


def main_menu():
    while True:
        w.blit(BG, (0, 0))
        font = pygame.font.SysFont('Arial', 60)

        # Vẽ các nút
        start_text = font.render('BAT DAU', True, WHITE)
        score_text = font.render('XEM DIEM SO', True, WHITE)
        exit_text = font.render('Exit', True, WHITE)

        w.blit(start_text, (WINDOWWIDTH // 2 - 80, WINDOWHEIGHT // 2 - 60))
        w.blit(score_text, (WINDOWWIDTH // 2 - 120, WINDOWHEIGHT // 2))
        w.blit(exit_text, (WINDOWWIDTH // 2 - 50, WINDOWHEIGHT // 2 + 60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Kiểm tra vị trí nhấp chuột
                if WINDOWWIDTH // 2 - 80 < mouse_x < WINDOWWIDTH // 2 + 80 and WINDOWHEIGHT // 2 - 60 < mouse_y < WINDOWHEIGHT // 2 - 10:
                    game_loop()  # Bắt đầu game
                elif WINDOWWIDTH // 2 - 120 < mouse_x < WINDOWWIDTH // 2 + 120 and WINDOWHEIGHT // 2 < mouse_y < WINDOWHEIGHT // 2 + 50:
                    show_scores()  # Hiển thị điểm số
                elif WINDOWWIDTH // 2 - 50 < mouse_x < WINDOWWIDTH // 2 + 50 and WINDOWHEIGHT // 2 + 60 < mouse_y < WINDOWHEIGHT // 2 + 110:
                    pygame.quit()
                    sys.exit()

# Chạy game


def game_loop():
    global diem, mang, toc_do, level_up_time, paused
    ytao = 0
    ycam = 0
    yxoai = 0
    ybom = 0
    ydua = 0
    ylemon = 0
    x_tao = random.randint(0, WINDOWWIDTH - 50)
    x_cam = random.randint(0, WINDOWWIDTH - 50)
    x_xoai = random.randint(0, WINDOWWIDTH - 50)
    x_bom = random.randint(0, WINDOWWIDTH - 50)
    x_dua = random.randint(0, WINDOWWIDTH - 50)
    x_lemon = random.randint(0, WINDOWWIDTH - 50)

    diem = 0
    toc_do = 1
    mang = 3
    paused = False
    level_up_time = 0

    # Khởi tạo font
    font = pygame.font.SysFont('Arial', 30)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Nhấn phím P để tạm dừng
                    paused = not paused

            if not paused and event.type == pygame.MOUSEBUTTONDOWN:
                # Kiểm tra va chạm với các quả
                if x_tao < event.pos[0] < x_tao + 50 and ytao < event.pos[1] < ytao + 50:
                    diem += 5
                    ytao = 0
                    x_tao = random.randint(0, WINDOWWIDTH - 50)

                elif x_cam < event.pos[0] < x_cam + 50 and ycam < event.pos[1] < ycam + 50:
                    diem += 5
                    ycam = 0
                    x_cam = random.randint(0, WINDOWWIDTH - 50)

                elif x_xoai < event.pos[0] < x_xoai + 50 and yxoai < event.pos[1] < yxoai + 50:
                    diem += 5
                    yxoai = 0
                    x_xoai = random.randint(0, WINDOWWIDTH - 50)

                if diem >= 50:  # Quả bom xuất hiện từ level 1
                    if x_bom < event.pos[0] < x_bom + 50 and ybom < event.pos[1] < ybom + 50:
                        mang -= 1
                        ybom = 0
                        x_bom = random.randint(0, WINDOWWIDTH - 50)

                if diem >= 80 and level_up_time == 0:
                    level_up_time = time.time()
                    diem = 80

                    if x_dua < event.pos[0] < x_dua + 50 and ydua < event.pos[1] < ydua + 50:
                        diem += 10
                        ydua = 0
                        x_dua = random.randint(0, WINDOWWIDTH - 50)

                    if x_lemon < event.pos[0] < x_lemon + 50 and ylemon < event.pos[1] < ylemon + 50:
                        diem += 10
                        ylemon = 0
                        x_lemon = random.randint(0, WINDOWWIDTH - 50)

        if not paused:
            # Vẽ nền và các quả
            w.blit(BG, (0, 0))
            w.blit(tao, (x_tao, ytao))
            w.blit(cam, (x_cam, ycam))
            w.blit(xoai, (x_xoai, yxoai))

            # Quả bom
            if diem >= 50:
                w.blit(bom, (x_bom, ybom))

            if diem >= 80:
                w.blit(dua, (x_dua, ydua))
                w.blit(lemon, (x_lemon, ylemon))

            toc_do = tang_toc_do(diem, toc_do)

            # Cập nhật vị trí rơi của các quả
            ytao += toc_do
            ycam += toc_do
            yxoai += toc_do
            if diem >= 50:
                ybom += toc_do
            if diem >= 80:
                ydua += toc_do
                ylemon += toc_do

            # Cập nhật vị trí ngang với quỹ đạo lung tung
            # Tốc độ ngẫu nhiên theo chiều ngang
            x_tao += random.uniform(-1, 1)
            x_cam += random.uniform(-1, 1)
            x_xoai += random.uniform(-1, 1)
            x_bom += random.uniform(-1, 1)
            x_dua += random.uniform(-1, 1)
            x_lemon += random.uniform(-1, 1)

            # Khi quả ra khỏi màn hình
            if ytao > WINDOWHEIGHT:
                ytao = 0
                x_tao = random.randint(0, WINDOWWIDTH - 50)
                diem -= 5

            if ycam > WINDOWHEIGHT:
                ycam = 0
                x_cam = random.randint(0, WINDOWWIDTH - 50)
                diem -= 5

            if yxoai > WINDOWHEIGHT:
                yxoai = 0
                x_xoai = random.randint(0, WINDOWWIDTH - 50)
                diem -= 5

            if ybom > WINDOWHEIGHT:
                ybom = 0

            if ydua > WINDOWHEIGHT:
                ydua = 0

            if ylemon > WINDOWHEIGHT:
                ylemon = 0

            # Hiển thị điểm và số mạng còn lại
            text_diem = font.render('SCORE: {}'.format(diem), True, WHITE)
            text_mang = font.render('LIVE: {}'.format(mang), True, WHITE)

            w.blit(text_diem, (50, 50))
            w.blit(text_mang, (50, 80))

            # Kiểm tra kết thúc game khi hết mạng
            if mang <= 0:
                game_over()

            # Hiển thị giao diện New Level khi đạt 50 điểm
            time1 = time.time()
            if level_up_time > 0 and time1 - level_up_time < 5:  # Hiển thị "LEVEL UP" trong 5 giây
                font_level_up = pygame.font.SysFont('Arial', 60)
                text_level_up = font_level_up.render(
                    'LEVEL UP', True, (255, 255, 0))
                w.blit(text_level_up, (WINDOWWIDTH //
                       2 - 150, WINDOWHEIGHT // 2 - 30))
            elif level_up_time > 0 and time1 - level_up_time >= 5:
                level_up_time = 0  # Reset thời gian hiển thị "LEVEL UP"

        pygame.display.update()
        fpsClock.tick(FPS)


def show_scores():
    scores = []
    # Đọc điểm từ file CSV
    with open('scores.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            scores.append(row)

    while True:
        w.fill(BLACK)
        font = pygame.font.SysFont('Arial', 40)

        # Hiển thị điểm
        for i, score in enumerate(scores):
            text = font.render(f'{i + 1}. ĐIEM: {score[0]}', True, WHITE)
            w.blit(text, (WINDOWWIDTH // 2 - 100, 50 + i * 30))

        text_exit = font.render('NHAM ESC DE QUAY LAI', True, WHITE)
        w.blit(text_exit, (WINDOWWIDTH // 2 - 150, 50 + len(scores) * 30))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return  # Quay lại giao diện chính


def game_over():
    font_over = pygame.font.SysFont('Arial', 60)
    text_over = font_over.render('GAME OVER', True, (255, 0, 0))
    w.blit(text_over, (WINDOWWIDTH // 2 - 150, WINDOWHEIGHT // 2 - 30))
    pygame.display.update()
    time.sleep(3)

    # Lưu điểm vào file CSV
    with open('scores.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([diem])

    # Quay về giao diện chính
    main_menu()  # Gọi lại hàm main_menu để trở về màn hình chính


def tang_toc_do(diem, toc_do):
    if diem >= 20:
        toc_do = 1 + (diem - 20) * 0.02  # Giảm tốc độ tăng
    if diem % 100 == 0 and diem != 0:
        toc_do += 0.1  # Tăng nhẹ tốc độ
    return toc_do


# Gọi hàm để hiển thị giao diện bắt đầu
main_menu()
