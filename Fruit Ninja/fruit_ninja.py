import pygame, sys
import os
import random


player_lives = 4                                                #Số mạng trong game
score = 0                                                       #Điểm bắt đầu
fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']    #Các đối tượng trong game

# khởi tạo pygame và tạo cửa sổ
WIDTH = 800
HEIGHT = 500
FPS = 10                                                 # Đây là tần suất xuất hiện của các đối tượng mỗi 1 fps ứng với 1 khung hình/s
pygame.init()
pygame.display.set_caption('Fruit-Ninja Game')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))   # Kích cỡ khung cửa sổ chơi game 
clock = pygame.time.Clock()

# Phân màu sắc 
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

background = pygame.image.load('hinh-anh-xe-do-kieng-cuc-chat.jpg')                                  #Khung background của game
font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))    #Khung điểm
lives_icon = pygame.image.load('images/white_lives.png')                    #Hình ảnh hiển thị mạng (X)

# Cấu trúc tổng quát của game 
def generate_random_fruits(fruit):
    fruit_path = "images/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x' : random.randint(100,500),          #vị trí của trái cây trên tọa độ x
        'y' : 800,
        'speed_x': random.randint(-10,10),      #Quả chuyển động theo hướng x với vận tốc bao nhiêu. Điều khiển chuyển động theo đường chéo của trái cây
        'speed_y': random.randint(-80, -60),    # kiểm soát tốc độ của trái cây theo hướng y ( UP )
        'throw': False,                         #xác định xem tọa độ được tạo ra của các loại trái cây có nằm ngoài khung game hay không. Nếu ở ngoài thì sẽ bị bỏ đi
        't': 0,                                 #manages the
        'hit': False,
    }

    if random.random() >= 0.75:     #Trả về số dấu phẩy động ngẫu nhiên tiếp theo trong phạm vi [0.0, 1.0) để giữ lại trái cây bên trong khung trò chơi
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False

# Dữ liệu ngâu nhiên của trái cây
data = {}
for fruit in fruits:
    generate_random_fruits(fruit) #Duyệt từng đối tượng Fruit trong danh sách Fruits (chính là đối tượng tên ảnh trong thư mục img)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))

# Vẽ phông chữ trên màn hình
font_name = pygame.font.match_font('comic.ttf')
def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)

# Vị trí của hình ảnh hiện thị mạng
def draw_lives(display, x, y, lives, image) :
    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()       # lấy tọa độ (x, y) của các biểu tượng chữ thập (nằm ở phía trên cùng bên phải)
        img_rect.x = int(x + 35 * i)    # đặt biểu tượng chữ thập tiếp theo cách 35 pixel so với biểu tượng trước đó
        img_rect.y = y                  # số lượng pixel mà biểu tượng chữ thập nên được đặt từ đầu màn hình
        display.blit(img, img_rect)

# Hiển thị trò chơi trên màn hình và màn hình bắt đầu
def show_gameover_screen():
    gameDisplay.blit(background, (0,0))
    draw_text(gameDisplay, "FRUIT NINJA!", 90, WIDTH / 2, HEIGHT / 4)
    if not game_over :
        draw_text(gameDisplay,"Score : " + str(score), 50, WIDTH / 2, HEIGHT /2)

    draw_text(gameDisplay, "Press a key to begin!", 64, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Nhạc cho trò chơi 
pygame.mixer.init()
pygame.mixer.music.load("12234.mp3")
pygame.mixer.music.play(1000)

# Vòng lặp trò chơi
first_round = True
game_over = True        #kết thúc trò chơi - vòng lặp nếu nhiều hơn 3 lần Bom bị cắt
game_running = True     #được sử dụng để quản lý vòng lặp trò chơi
while game_running :
    if game_over :
        if first_round :
            show_gameover_screen()
            first_round = False
        game_over = False
        player_lives = 4
        draw_lives(gameDisplay, 655, 5, player_lives, 'images/red_lives.png')
        score = 0

    for event in pygame.event.get():
        # kiểm tra để đóng cửa sổ
        if event.type == pygame.QUIT:
            game_running = False

    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 655, 5, player_lives, 'images/red_lives.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']          #di chuyển trái cây theo tọa độ x
            value['y'] += value['speed_y']          #di chuyển trái cây theo tọa độ y
            value['speed_y'] += (1 * value['t'])    #tăng toạ độ của y
            value['t'] += 1                         #tăng tốc độ cho vòng tiếp theo


            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))    #Hình động của trái cây bên trong Khung
            else:
                generate_random_fruits(key)

            current_position = pygame.mouse.get_pos()   #lấy tọa độ hiện tại (x, y) tính bằng pixel của chuột

            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x']+60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y']+60:
                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 0:
                        hide_cross_lives(655, 15)
                    elif player_lives == 1:
                        hide_cross_lives(690, 15)
                    elif player_lives == 2:
                       hide_cross_lives(725, 15)
                    elif player_lives == 3:
                        hide_cross_lives(760, 15)
                    #nếu người dùng nhấp vào bom trong ba lần, thông báo GAME OVER sẽ được hiển thị và cửa sổ sẽ được đặt lại
                    if player_lives < 0 :
                        show_gameover_screen()
                        game_over = True

                    half_fruit_path = "images/explosion.png"
                else:
                    half_fruit_path = "images/" + "half_" + key + ".png"

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10
                if key != 'bomb' :
                    score += 1
                score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
                value['hit'] = True
        else:
            generate_random_fruits(key)

    pygame.display.update()
    clock.tick(FPS)      # giữ cho vòng lặp chạy ở tốc độ phù hợp (quản lý khung hình / giây )
                        
pygame.quit()