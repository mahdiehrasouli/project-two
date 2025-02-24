import pygame
import random

# تنظیمات اولیه
pygame.init()

# اندازه صفحه نمایش
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("بازی آجرشکن")

# رنگ‌ها
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# تنظیمات پد
paddle_width = 100
paddle_height = 15
paddle_speed = 10

# تنظیمات توپ
ball_width = 10
ball_speed_x = 3
ball_speed_y = -3

# تنظیمات آجرها
brick_width = 60
brick_height = 20

# تعداد مراحل
total_levels = 5
current_level = 1
total_balls = 3
current_balls = total_balls

# تابع رسم پد
def draw_paddle(x, y):
    pygame.draw.rect(screen, blue, [x, y, paddle_width, paddle_height])

# تابع رسم توپ
def draw_ball(x, y):
    pygame.draw.circle(screen, red, (x, y), ball_width)

# تابع رسم آجرها
def draw_bricks(bricks):
    for brick in bricks:
        pygame.draw.rect(screen, green, brick)

# تابع برای شروع مرحله جدید
def start_new_level():
    global ball_speed_x, ball_speed_y, brick_width, brick_height, current_balls
    # افزایش سرعت توپ
    ball_speed_x *= 1.1
    ball_speed_y *= 1.1
    # افزایش تعداد توپ‌ها
    current_balls += 1
    # افزایش تعداد آجرها
    brick_width = max(40, brick_width - 5)  # کوچکتر کردن آجرها در هر مرحله
    brick_height = max(15, brick_height - 3)  # کوچکتر کردن آجرها در هر مرحله

# تابع پیام باخت
def show_game_over():
    font = pygame.font.SysFont("Arial", 30)
    text = font.render("شما باختید. از اول شروع کنید!", True, (255, 0, 0))
    screen.blit(text, (screen_width // 3, screen_height // 2))
    pygame.display.update()
    pygame.time.wait(2000)

# تابع پیام برنده شدن
def show_you_win():
    font = pygame.font.SysFont("Arial", 30)
    text = font.render("شما برنده شدید!", True, (0, 255, 0))
    screen.blit(text, (screen_width // 3, screen_height // 2))
    pygame.display.update()
    pygame.time.wait(2000)

# تابع تنظیم آجرها برای هر مرحله
def setup_bricks():
    bricks = []
    rows = 5 + current_level  # افزایش تعداد ردیف‌ها در هر مرحله
    columns = 6 + current_level  # افزایش تعداد ستون‌ها در هر مرحله

    for i in range(rows):
        for j in range(columns):
            brick = pygame.Rect(j * (brick_width + 5) + 35, i * (brick_height + 5) + 30, brick_width, brick_height)
            bricks.append(brick)

    # تغییر تصادفی موقعیت آجرها
    random.shuffle(bricks)
    return bricks

# بازی
clock = pygame.time.Clock()
game_over = False
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - paddle_height - 10
ball_x = screen_width // 2
ball_y = paddle_y - ball_width

# ایجاد آجرها
bricks = setup_bricks()

# توابع توپ‌های متعدد
balls = [{'x': ball_x, 'y': ball_y, 'speed_x': ball_speed_x, 'speed_y': ball_speed_y}]

while not game_over:
    screen.fill(white)

    # بررسی رویدادهای بازی
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # حرکت پد
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_speed

    # حرکت توپ‌ها
    for ball in balls[:]:
        ball['x'] += ball['speed_x']
        ball['y'] += ball['speed_y']

        # برخورد توپ با دیوار
        if ball['x'] <= 0 or ball['x'] >= screen_width - ball_width:
            ball['speed_x'] = -ball['speed_x']
        if ball['y'] <= 0:
            ball['speed_y'] = -ball['speed_y']

        # برخورد توپ با پد
        if ball['y'] + ball_width >= paddle_y and paddle_x <= ball['x'] <= paddle_x + paddle_width:
            ball['speed_y'] = -ball['speed_y']

        # برخورد توپ با آجرها
        ball_rect = pygame.Rect(ball['x'] - ball_width, ball['y'] - ball_width, ball_width * 2, ball_width * 2)
        for brick in bricks[:]:
            if brick.colliderect(ball_rect):
                bricks.remove(brick)
                ball['speed_y'] = -ball['speed_y']
                break

    # بررسی باخت
    if len([ball for ball in balls if ball['y'] < screen_height]) == 0:
        current_balls -= 1
        if current_balls <= 0:
            show_game_over()
            balls = [{'x': ball_x, 'y': ball_y, 'speed_x': ball_speed_x, 'speed_y': ball_speed_y}]
            current_balls = total_balls
            bricks = setup_bricks()
            start_new_level()

    # بررسی پیروزی
    if len(bricks) == 0:
        if current_level == total_levels:
            show_you_win()
            game_over = True
        else:
            current_level += 1
            start_new_level()
            bricks = setup_bricks()

    # رسم المان‌ها
    draw_paddle(paddle_x, paddle_y)
    for ball in balls:
        draw_ball(ball['x'], ball['y'])
    draw_bricks(bricks)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
