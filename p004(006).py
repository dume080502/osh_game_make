import pygame
import math

# 초기화
pygame.init()
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie City - Seamless Map Switch")

# 색상
BLACK = (30, 30, 30)
GRAY = (50, 50, 50)
YELLOW = (200, 200, 0)
WHITE = (255, 255, 255)
SKIN = (255, 224, 189)
CLOTHES = (0, 100, 255)
PANTS = (30, 30, 80)
HAT_COLOR = (139, 69, 19)
EYE_COLOR = (0, 0, 0)

# 현재 어떤 맵에 있는지 나타내는 변수
current_map_x = 0

class Player:
    def __init__(self):
        self.width, self.height = 40, 40
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = 7
        self.walk_count = 0
        self.facing_x = 0
        self.facing_y = 1 

    def move(self, keys):
        global current_map_x
        dx, dy = 0, 0
        moving = False
        
        if keys[pygame.K_w]: dy -= 1; moving = True
        if keys[pygame.K_s]: dy += 1; moving = True
        if keys[pygame.K_a]: dx -= 1; moving = True
        if keys[pygame.K_d]: dx += 1; moving = True

        if moving:
            self.facing_x = dx
            self.facing_y = dy
            actual_speed = self.speed * 0.7071 if dx != 0 and dy != 0 else self.speed
            self.x += dx * actual_speed
            self.y += dy * actual_speed
            self.walk_count += 0.2
        else:
            self.walk_count = 0

        # --- 맵 전환 로직 (완전 보존) ---
        if self.x < -self.width:
            current_map_x -= 1
            self.x = WIDTH - 10
        elif self.x > WIDTH:
            current_map_x += 1
            self.x = 10

        self.y = max(0, min(HEIGHT - self.height, self.y))

    def draw(self, surface):
        # p004(002)의 역동적인 애니메이션 오프셋
        leg_offset = math.sin(self.walk_count) * 8
        arm_offset = math.sin(self.walk_count + math.pi) * 8 # p002의 그 느낌
        
        # 1. 다리 (p002 로직 그대로)
        pygame.draw.rect(surface, PANTS, (self.x + 12, self.y + 25 + leg_offset, 6, 12))
        pygame.draw.rect(surface, PANTS, (self.x + 22, self.y + 25 - leg_offset, 6, 12))
        
        # 2. 몸통 (p002 로직 그대로)
        pygame.draw.rect(surface, CLOTHES, (self.x + 10, self.y + 12, 20, 18))
        
        # 3. 팔 (p002의 그 시원한 날개짓 스타일 복구)
        pygame.draw.line(surface, SKIN, (self.x + 10, self.y + 15), (self.x + 5, self.y + 25 + arm_offset), 4)
        pygame.draw.line(surface, SKIN, (self.x + 30, self.y + 15), (self.x + 35, self.y + 25 - arm_offset), 4)

        # 4. 머리
        head_cx = int(self.x + 20)
        head_cy = int(self.y + 10)
        pygame.draw.circle(surface, SKIN, (head_cx, head_cy), 9)

        # 5. 눈 (시선 방향만 살짝 추가)
        if self.facing_y >= 0:
            e_shift_x = self.facing_x * 3
            e_shift_y = self.facing_y * 1
            pygame.draw.circle(surface, EYE_COLOR, (head_cx - 3 + e_shift_x, head_cy + e_shift_y), 2)
            pygame.draw.circle(surface, EYE_COLOR, (head_cx + 3 + e_shift_x, head_cy + e_shift_y), 2)

        # 6. 모자 (챙 방향만 시선에 맞춤)
        brim_x = head_cx - 12 + (self.facing_x * 3)
        pygame.draw.rect(surface, HAT_COLOR, (head_cx - 8, head_cy - 15, 16, 9))
        pygame.draw.rect(surface, HAT_COLOR, (brim_x, head_cy - 8, 24, 4))

def draw_background(surface, map_id):
    # 배경 로직 보존
    surface.fill(GRAY)
    pygame.draw.rect(surface, BLACK, (0, 0, WIDTH, 100))
    pygame.draw.rect(surface, BLACK, (0, HEIGHT - 100, WIDTH, 100))
    if map_id == 0:
        for y in range(120, HEIGHT - 120, 40):
            pygame.draw.rect(surface, WHITE, (WIDTH // 2 - 50, y, 100, 20))
    elif map_id < 0:
        pygame.draw.rect(surface, YELLOW, (0, HEIGHT // 2 - 5, WIDTH, 10))
    elif map_id > 0:
        for x in range(0, WIDTH, 60):
            pygame.draw.rect(surface, WHITE, (x, HEIGHT // 2 - 5, 30, 5))
    font = pygame.font.SysFont("arial", 30)
    map_text = font.render(f"Map Sector: {map_id}", True, WHITE)
    surface.blit(map_text, (20, 120))

# 메인 루프
player = Player()
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.move(keys)
    draw_background(screen, current_map_x)
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()