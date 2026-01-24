import pygame

# 초기화
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Game - Human Character")

# 색상 설정
BLACK = (0, 0, 0)
SKIN = (255, 224, 189)  # 살구색 (머리)
CLOTHES = (0, 100, 255) # 파란색 (몸통)
PLAYER_SPEED = 5

class Player:
    def __init__(self):
        # 캐릭터의 중심 위치 (Rect는 충돌 판정용으로 사용)
        self.width, self.height = 40, 40
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_s]: dy += 1
        if keys[pygame.K_a]: dx -= 1
        if keys[pygame.K_d]: dx += 1

        if dx != 0 and dy != 0:
            speed = PLAYER_SPEED * 0.7071
        else:
            speed = PLAYER_SPEED

        self.x += dx * speed
        self.y += dy * speed
        
        # 화면 밖 방지
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(0, min(HEIGHT - self.height, self.y))
        
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        # 1. 몸통 (가운데 사각형)
        body_rect = pygame.Rect(self.x + 10, self.y + 15, 20, 20)
        pygame.draw.rect(surface, CLOTHES, body_rect)

        # 2. 머리 (위쪽 원)
        head_pos = (int(self.x + 20), int(self.y + 10))
        pygame.draw.circle(surface, SKIN, head_pos, 8)

        # 3. 팔 (간단한 선 또는 작은 사각형)
        # 왼쪽 팔
        pygame.draw.line(surface, SKIN, (self.x + 10, self.y + 20), (self.x + 5, self.y + 30), 3)
        # 오른쪽 팔
        pygame.draw.line(surface, SKIN, (self.x + 30, self.y + 20), (self.x + 35, self.y + 30), 3)

# 게임 루프 실행부 (이전과 동일)
player = Player()
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)

    screen.fill(BLACK) 
    player.draw(screen) # 이제 사람 모양으로 그려짐
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()