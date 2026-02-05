import pygame
import math

# 설정 상수 (상수는 따로 모으는 게 국룰입니다)
WIDTH, HEIGHT = 1280, 800
FPS = 60
SPEED = 7

# 색상 정의
COLORS = {
    "BG": (50, 50, 50),
    "ROAD": (30, 30, 30),
    "PLAYER_CLOTHES": (0, 100, 255),
    "SKIN": (255, 224, 189),
    "WHITE": (255, 255, 255)
}

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 40, 40)
        self.walk_count = 0
        self.speed = SPEED

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_s]: dy += 1
        if keys[pygame.K_a]: dx -= 1
        if keys[pygame.K_d]: dx += 1

        if dx != 0 or dy != 0:
            # 대각선 속도 보정 (math.hypot 활용)
            dist = math.hypot(dx, dy)
            self.rect.x += (dx / dist) * self.speed
            self.rect.y += (dy / dist) * self.speed
            self.walk_count += 0.2
        else:
            self.walk_count = 0

    def draw(self, surface):
        # 렌더링 로직은 기존과 유사하지만 self.rect를 기준으로 통일
        leg_offset = math.sin(self.walk_count) * 8
        p = self.rect
        # 몸통/머리/다리 그리기 (생략 - 기존 로직 유지 가능)
        pygame.draw.rect(surface, COLORS["PLAYER_CLOTHES"], (p.x + 10, p.y + 12, 20, 18))
        pygame.draw.circle(surface, COLORS["SKIN"], (p.centerx, p.y + 10), 9)

class MapManager:
    """맵의 전환과 렌더링을 책임지는 클래스"""
    def __init__(self):
        self.current_map_x = 0

    def update(self, player):
        # 맵 전환 경계 체크
        if player.rect.right < 0:
            self.current_map_x -= 1
            player.rect.left = WIDTH - 50
        elif player.rect.left > WIDTH:
            self.current_map_x += 1
            player.rect.right = 50
        
        # 상하 화면 이탈 방지
        player.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, surface):
        surface.fill(COLORS["BG"])
        # 여기서 map_id에 따른 맵 구성 요소를 그립니다.
        # 추후 타일맵 시스템으로 확장하기 용이합니다.

# --- 메인 실행 ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    player = Player()
    world = MapManager()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        player.handle_input()
        world.update(player) # 플레이어 위치에 따른 맵 상태 업데이트
        
        world.draw(screen)
        player.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()