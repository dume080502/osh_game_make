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
        # 방향 상태 유지
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

        # --- 맵 전환 로직 (수정 및 삭제 없음) ---
        if self.x < -self.width:
            current_map_x -= 1
            self.x = WIDTH - 10
        elif self.x > WIDTH:
            current_map_x += 1
            self.x = 10

        self.y = max(0, min(HEIGHT - self.height, self.y))

    def draw(self, surface):
        leg_offset = math.sin(self.walk_count) * 8
        arm_offset = math.sin(self.walk_count + math.pi) * 8
        
        # --- 몸통 회전 연출용 변수 ---
        # 좌우 이동 중이면 몸통 폭을 줄여서 측면처럼 보이게 함
        is_side = self.facing_x != 0
        body_w = 14 if is_side else 20
        body_x = self.x + 10 + (3 if is_side else 0)
        
        head_cx = int(self.x + 20)
        head_cy = int(self.y + 10)

        # 1. 다리 (몸통 폭에 맞춰 간격 조정)
        leg_gap = 2 if is_side else 5
        pygame.draw.rect(surface, PANTS, (head_cx - leg_gap - 3, self.y + 25 + leg_offset, 6, 12))
        pygame.draw.rect(surface, PANTS, (head_cx + leg_gap - 3, self.y + 25 - leg_offset, 6, 12))
        
        # 2. 몸통
        pygame.draw.rect(surface, CLOTHES, (body_x, self.y + 12, body_w, 18))
        
        # 3. 팔 (측면일 때는 가고자 하는 방향의 팔만 강조하거나 위치 조정)
        if not is_side:
            pygame.draw.line(surface, SKIN, (self.x + 10, self.y + 15), (self.x + 5, self.y + 25 + arm_offset), 4)
            pygame.draw.line(surface, SKIN, (self.x + 30, self.y + 15), (self.x + 35, self.y + 25 - arm_offset), 4)
        else:
            # 측면일 때는 몸 중앙 근처에서 팔이 나옴
            pygame.draw.line(surface, SKIN, (head_cx, self.y + 15), (head_cx + (self.facing_x * 8), self.y + 25 + arm_offset), 4)

        # 4. 머리
        pygame.draw.circle(surface, SKIN, (head_cx, head_cy), 9)

        # 5. 눈 (시선 방향 및 뒷모습 처리)
        if self.facing_y >= 0:
            e_shift_x = self.facing_x * 4
            e_shift_y = self.facing_y * 2
            if not is_side: # 정면/대각선
                pygame.draw.circle(surface, EYE_COLOR, (head_cx - 3 + e_shift_x, head_cy + e_shift_y), 2)
                pygame.draw.circle(surface, EYE_COLOR, (head_cx + 3 + e_shift_x, head_cy + e_shift_y), 2)
            else: # 완전 측면
                pygame.draw.circle(surface, EYE_COLOR, (head_cx + e_shift_x, head_cy + e_shift_y), 2)

        # 6. 모자 (챙 방향 강조)
        brim_w = 18 if is_side else 24
        brim_x = head_cx - (brim_w // 2) + (self.facing_x * 4)
        pygame.draw.rect(surface, HAT_COLOR, (head_cx - 8, head_cy - 15, 16, 9))
        pygame.draw.rect(surface, HAT_COLOR, (brim_x, head_cy - 8, brim_w, 4))

def draw_background(surface, map_id):
    # (배경 로직 유지 - 생략 없이 그대로 사용하세요)
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

# 메인 루프 (기존 구조 유지)
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