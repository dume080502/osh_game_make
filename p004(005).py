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
        
        head_cx = int(self.x + 20)
        head_cy = int(self.y + 10)
        is_side = self.facing_x != 0

        # 1. 다리 (기존 로직 유지)
        pygame.draw.rect(surface, PANTS, (self.x + 12, self.y + 25 + leg_offset, 6, 12))
        pygame.draw.rect(surface, PANTS, (self.x + 22, self.y + 25 - leg_offset, 6, 12))
        
        # 2. 몸통 (좌우 이동 시 아주 미세하게 폭 조절하여 측면 느낌만 부여)
        body_w = 18 if is_side else 20
        body_x = self.x + 11 if is_side else self.x + 10
        pygame.draw.rect(surface, CLOTHES, (body_x, self.y + 12, body_w, 18))
        
        # 3. 팔 (날개짓 교정: x축 오프셋을 시선 방향에 맞춤)
        if not is_side:
            # 정면/배면: 기존의 시원한 팔 동작 유지
            pygame.draw.line(surface, SKIN, (self.x + 10, self.y + 15), (self.x + 5, self.y + 25 + arm_offset), 4)
            pygame.draw.line(surface, SKIN, (self.x + 30, self.y + 15), (self.x + 35, self.y + 25 - arm_offset), 4)
        else:
            # 측면: 팔이 양옆으로 벌어지지 않고 진행 방향(facing_x) 앞뒤로 흔들림
            # 앞쪽 팔은 진행 방향으로, 뒤쪽 팔은 반대 방향으로 뻗음
            arm_swing_x = self.facing_x * 6 
            # 뒤쪽 팔 (먼저 그려서 몸 뒤로 보냄)
            pygame.draw.line(surface, SKIN, (head_cx, self.y + 15), (head_cx - arm_swing_x, self.y + 25 - arm_offset), 4)
            # 앞쪽 팔 (나중에 그려서 몸 앞으로 보냄)
            pygame.draw.line(surface, SKIN, (head_cx, self.y + 15), (head_cx + arm_swing_x, self.y + 25 + arm_offset), 4)

        # 4. 머리
        pygame.draw.circle(surface, SKIN, (head_cx, head_cy), 9)

        # 5. 눈 (시선 방향 반영)
        if self.facing_y >= 0:
            e_shift_x = self.facing_x * 4
            e_shift_y = self.facing_y * 2
            pygame.draw.circle(surface, EYE_COLOR, (head_cx - 3 + e_shift_x, head_cy + e_shift_y), 2)
            pygame.draw.circle(surface, EYE_COLOR, (head_cx + 3 + e_shift_x, head_cy + e_shift_y), 2)

        # 6. 모자 (챙 방향 반영)
        brim_x = head_cx - 12 + (self.facing_x * 4)
        pygame.draw.rect(surface, HAT_COLOR, (head_cx - 8, head_cy - 15, 16, 9))
        pygame.draw.rect(surface, HAT_COLOR, (brim_x, head_cy - 8, 24, 4))

def draw_background(surface, map_id):
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

# 메인 루프 (기존 구조 보존)
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
    clock.tick(FPS_VAL := 60)

pygame.quit()