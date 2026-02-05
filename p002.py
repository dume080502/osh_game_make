import pygame
import math

# 초기화 및 설정
pygame.init()
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie City - Walking Human")

# 색상 설정
BLACK = (50, 50, 50)
DARK_GRAY = (30, 30, 30)
YELLOW = (200, 200, 0)
WHITE = (255, 255, 255)
SKIN = (255, 224, 189)
CLOTHES = (0, 100, 255)
PANTS = (30, 30, 80) # 바지 색상 (진청색)

PLAYER_SPEED = 6

class Player:
    def __init__(self):
        self.width, self.height = 40, 40
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.walk_count = 0 # 걷기 애니메이션을 위한 카운터

    def move(self, keys):
        dx, dy = 0, 0
        moving = False
        
        if keys[pygame.K_w]: dy -= 1; moving = True
        if keys[pygame.K_s]: dy += 1; moving = True
        if keys[pygame.K_a]: dx -= 1; moving = True
        if keys[pygame.K_d]: dx += 1; moving = True

        if dx != 0 and dy != 0:
            speed = PLAYER_SPEED * 0.7071
        else:
            speed = PLAYER_SPEED

        self.x += dx * speed
        self.y += dy * speed
        
        # 움직일 때만 애니메이션 카운터 증가
        if moving:
            self.walk_count += 0.2 
        else:
            self.walk_count = 0 # 멈추면 다리 모으기

        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(0, min(HEIGHT - self.height, self.y))
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        # 걷기 애니메이션 계산 (sin 함수를 이용해 부드럽게 앞뒤로 움직임)
        leg_offset = math.sin(self.walk_count) * 8

        # 1. 다리 그리기 (몸통보다 뒤에 그려야 하므로 먼저 그림)
        # 왼쪽 다리
        pygame.draw.rect(surface, PANTS, (self.x + 12, self.y + 25 + leg_offset, 6, 12))
        # 오른쪽 다리
        pygame.draw.rect(surface, PANTS, (self.x + 22, self.y + 25 - leg_offset, 6, 12))

        # 2. 몸통
        pygame.draw.rect(surface, CLOTHES, (self.x + 10, self.y + 12, 20, 18))
        
        # 3. 머리
        pygame.draw.circle(surface, SKIN, (int(self.x + 20), int(self.y + 10)), 9)
        
        # 4. 팔 (걷는 방향에 맞춰 살짝 흔들림)
        pygame.draw.line(surface, SKIN, (self.x + 10, self.y + 15), (self.x + 5, self.y + 25 - leg_offset), 4)
        pygame.draw.line(surface, SKIN, (self.x + 30, self.y + 15), (self.x + 35, self.y + 25 + leg_offset), 4)

# 배경 함수 (이전과 동일)
def draw_background(surface):
    surface.fill(BLACK)
    pygame.draw.rect(surface, DARK_GRAY, (0, 0, WIDTH, 100))
    pygame.draw.rect(surface, DARK_GRAY, (0, HEIGHT - 100, WIDTH, 100))
    for x in range(0, WIDTH, 60):
        pygame.draw.rect(surface, YELLOW, (x, HEIGHT // 2 - 5, 30, 10))
    for y in range(120, HEIGHT - 120, 40):
        pygame.draw.rect(surface, WHITE, (WIDTH // 4, y, 100, 20))

# 게임 루프
player = Player()
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)

    draw_background(screen)
    player.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()