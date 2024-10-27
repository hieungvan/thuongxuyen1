import pygame
import random
import time

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Xe Tải Chạy Đường Đồi Núi")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tải hình ảnh cho xe tải và núi
truck_image = pygame.image.load("buoi7/chim1.jpg")  # Tải hình ảnh xe tải
mountain_image = pygame.image.load("mountain.png")  # Tải hình ảnh núi

# Thông số xe tải
truck_pos = [100, 300]
truck_speed = 5

# Thông số núi
mountains = [(random.randint(200, 600), random.randint(100, 400))
             for _ in range(3)]

# Thời gian
start_time = time.time()
game_over = False

# Hàm kiểm tra va chạm


def check_collision(truck_rect, mountains):
    for mountain in mountains:
        if truck_rect.colliderect(pygame.Rect(mountain[0], mountain[1], mountain_image.get_width(), mountain_image.get_height())):
            return True
    return False


# Vòng lặp chính của game
running = True
while running:
    screen.fill(WHITE)

    # Vẽ núi
    for mountain in mountains:
        screen.blit(mountain_image, mountain)

    # Vẽ xe tải
    screen.blit(truck_image, truck_pos)

    # Hiển thị thời gian
    elapsed_time = time.time() - start_time
    time_remaining = 60 - elapsed_time
    font = pygame.font.Font(None, 36)
    text = font.render(f'Time: {int(time_remaining)}', True, BLACK)
    screen.blit(text, (10, 10))

    # Kiểm tra kết thúc game
    if time_remaining <= 0:
        game_over = True
    if check_collision(pygame.Rect(truck_pos[0], truck_pos[1], truck_image.get_width(), truck_image.get_height()), mountains):
        game_over = True

    if game_over:
        game_over_text = font.render('Game Over!', True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2))
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            truck_pos[0] -= truck_speed
        if keys[pygame.K_RIGHT]:
            truck_pos[0] += truck_speed
        if keys[pygame.K_UP]:
            truck_pos[1] -= truck_speed
        if keys[pygame.K_DOWN]:
            truck_pos[1] += truck_speed

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
