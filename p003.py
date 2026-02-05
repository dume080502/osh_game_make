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

# 현재 어떤 맵에 있는지 나타내는 변수 (0이 시작 지점)
current_map_x = 0

class Player:
    def __init__(self):
        self.width, self.height = 40, 40
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = 7
        self.walk_count = 0

    def move(self, keys):
        global current_map_x
        dx, dy = 0, 0
        moving = False
        
        if keys[pygame.K_w]: dy -= 1; moving = True
        if keys[pygame.K_s]: dy += 1; moving = True
        if keys[pygame.K_a]: dx -= 1; moving = True
        if keys[pygame.K_d]: dx += 1; moving = True

        # 속도 보정
        actual_speed = self.speed * 0.7071 if dx != 0 and dy != 0 else self.speed
        self.x += dx * actual_speed
        self.y += dy * actual_speed

        # 애니메이션 카운트
        if moving: self.walk_count += 0.2
        else: self.walk_count = 0

        # --- 맵 전환 로직 ---
        # 왼쪽 끝으로 나갔을 때
        if self.x < -self.width:
            current_map_x -= 1     # 맵 번호 감소
            self.x = WIDTH - 10    # 캐릭터를 오른쪽 끝으로 이동
        # 오른쪽 끝으로 나갔을 때
        elif self.x > WIDTH:
            current_map_x += 1     # 맵 번호 증가
            self.x = 10            # 캐릭터를 왼쪽 끝으로 이동

        # 위아래는 일단 화면 밖으로 못 나가게 고정
        self.y = max(0, min(HEIGHT - self.height, self.y))

    def draw(self, surface):
        leg_offset = math.sin(self.walk_count) * 8
        # 다리
        pygame.draw.rect(surface, PANTS, (self.x + 12, self.y + 25 + leg_offset, 6, 12))
        pygame.draw.rect(surface, PANTS, (self.x + 22, self.y + 25 - leg_offset, 6, 12))
        # 몸통
        pygame.draw.rect(surface, CLOTHES, (self.x + 10, self.y + 12, 20, 18))
        # 머리
        pygame.draw.circle(surface, SKIN, (int(self.x + 20), int(self.y + 10)), 9)
        # 팔
        pygame.draw.line(surface, SKIN, (self.x + 10, self.y + 15), (self.x + 5, self.y + 25 - leg_offset), 4)
        pygame.draw.line(surface, SKIN, (self.x + 30, self.y + 15), (self.x + 35, self.y + 25 + leg_offset), 4)

def draw_background(surface, map_id):
    # 기본 아스팔트
    surface.fill(GRAY)
    
    # 맵 번호(map_id)에 따라 배경 디자인을 살짝 다르게 표시
    # 1. 공통 요소 (인도)
    pygame.draw.rect(surface, BLACK, (0, 0, WIDTH, 100))
    pygame.draw.rect(surface, BLACK, (0, HEIGHT - 100, WIDTH, 100))

    # 2. 맵 별 차이점
    if map_id == 0: # 시작 지점: 횡단보도가 있음
        for y in range(120, HEIGHT - 120, 40):
            pygame.draw.rect(surface, WHITE, (WIDTH // 2 - 50, y, 100, 20))
    
    elif map_id < 0: # 왼쪽 맵들: 중앙선이 노란색 실선
        pygame.draw.rect(surface, YELLOW, (0, HEIGHT // 2 - 5, WIDTH, 10))
    
    elif map_id > 0: # 오른쪽 맵들: 중앙선이 흰색 점선
        for x in range(0, WIDTH, 60):
            pygame.draw.rect(surface, WHITE, (x, HEIGHT // 2 - 5, 30, 5))

    # 화면 구석에 현재 맵 번호 표시 (디버그용)
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

    # 현재 맵 번호에 맞는 배경 그리기
    draw_background(screen, current_map_x)
    player.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()