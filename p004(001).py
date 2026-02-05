import pygame
import math

# 설정 상수
WIDTH, HEIGHT = 1280, 800
FPS = 60
SPEED = 7

# 색상 정의 (상수는 대문자로!)
BLACK = (30, 30, 30)
GRAY = (50, 50, 50)
YELLOW = (200, 200, 0)
WHITE = (255, 255, 255)
SKIN = (255, 224, 189)
CLOTHES = (0, 100, 255) # 파란 셔츠
PANTS = (30, 30, 80) # 진한 회색 바지
HAT_COLOR = (139, 69, 19) # 갈색 모자
SHOES_COLOR = (100, 50, 0) # 갈색 신발

class Player:
    def __init__(self):
        self.width, self.height = 40, 40
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = SPEED
        self.walk_count = 0

        # 캐릭터 각 부분의 상대적 크기와 위치를 상수로 정의
        # 이렇게 하면 캐릭터의 전체 크기를 변경할 때 훨씬 유연합니다.
        self.body_width = 20
        self.body_height = 18
        self.head_radius = 9
        self.leg_width = 6
        self.leg_height = 12
        self.arm_thickness = 4
        self.hat_height = 8
        self.hat_brim_width = 28
        self.hat_brim_height = 4
        self.shoe_width = 8
        self.shoe_height = 5

    def move(self, keys):
        # 기존 이동 로직과 맵 전환 로직은 MapManager에서 처리하도록 분리하거나
        # 현재 코드에서는 편의상 유지합니다. (이전 피드백의 MapManager를 사용하는 것이 더 좋음)
        dx, dy = 0, 0
        moving = False
        
        if keys[pygame.K_w]: dy -= 1; moving = True
        if keys[pygame.K_s]: dy += 1; moving = True
        if keys[pygame.K_a]: dx -= 1; moving = True
        if keys[pygame.K_d]: dx += 1; moving = True

        if moving:
            # 대각선 속도 보정
            actual_speed = self.speed * 0.7071 if dx != 0 and dy != 0 else self.speed
            self.x += dx * actual_speed
            self.y += dy * actual_speed
            self.walk_count += 0.2
        else:
            self.walk_count = 0

        # 위아래 화면 밖으로 못 나가게 고정
        self.y = max(0, min(HEIGHT - self.height, self.y))

    def draw(self, surface):
        # 캐릭터의 '기준점'을 정의하여 모든 요소를 상대적으로 그립니다.
        # 여기서는 캐릭터의 중앙 하단을 기준으로 잡겠습니다.
        center_x = int(self.x + self.width / 2)
        bottom_y = int(self.y + self.height)

        # 걷는 애니메이션 오프셋
        leg_offset = math.sin(self.walk_count) * 8
        arm_offset = math.sin(self.walk_count + math.pi / 2) * 5 # 팔은 다리와 반대 위상

        # --- 다리 (새로운 위치 및 신발 추가) ---
        # 왼쪽 다리
        left_leg_rect = pygame.Rect(center_x - self.leg_width - 5, bottom_y - self.leg_height - self.shoe_height + leg_offset, self.leg_width, self.leg_height)
        pygame.draw.rect(surface, PANTS, left_leg_rect)
        # 왼쪽 신발
        pygame.draw.rect(surface, SHOES_COLOR, (left_leg_rect.x, left_leg_rect.bottom, self.shoe_width, self.shoe_height))

        # 오른쪽 다리
        right_leg_rect = pygame.Rect(center_x + 5, bottom_y - self.leg_height - self.shoe_height - leg_offset, self.leg_width, self.leg_height)
        pygame.draw.rect(surface, PANTS, right_leg_rect)
        # 오른쪽 신발
        pygame.draw.rect(surface, SHOES_COLOR, (right_leg_rect.x, right_leg_rect.bottom, self.shoe_width, self.shoe_height))


        # --- 몸통 ---
        body_rect = pygame.Rect(center_x - self.body_width / 2, bottom_y - self.leg_height - self.shoe_height - self.body_height, self.body_width, self.body_height)
        pygame.draw.rect(surface, CLOTHES, body_rect)

        # --- 팔 (새로운 위치) ---
        # 왼쪽 팔 (어깨에서 시작)
        left_arm_start = (body_rect.left, body_rect.top + 5)
        left_arm_end = (left_arm_start[0] - 5, left_arm_start[1] + 15 + arm_offset)
        pygame.draw.line(surface, SKIN, left_arm_start, left_arm_end, self.arm_thickness)
        
        # 오른쪽 팔 (어깨에서 시작)
        right_arm_start = (body_rect.right, body_rect.top + 5)
        right_arm_end = (right_arm_start[0] + 5, right_arm_start[1] + 15 - arm_offset)
        pygame.draw.line(surface, SKIN, right_arm_start, right_arm_end, self.arm_thickness)

        # --- 머리 ---
        head_center = (center_x, body_rect.top - self.head_radius)
        pygame.draw.circle(surface, SKIN, head_center, self.head_radius)

        # --- 모자 (새로운 추가) ---
        # 모자 상단
        hat_top_rect = pygame.Rect(head_center[0] - self.head_radius + 2, head_center[1] - self.head_radius - self.hat_height, self.head_radius * 2 - 4, self.hat_height)
        pygame.draw.rect(surface, HAT_COLOR, hat_top_rect)
        # 모자 챙
        hat_brim_rect = pygame.Rect(head_center[0] - self.hat_brim_width / 2, head_center[1] - self.head_radius - self.hat_brim_height / 2, self.hat_brim_width, self.hat_brim_height)
        pygame.draw.rect(surface, HAT_COLOR, hat_brim_rect)


# 맵 관리자는 이전 버전에서 가져와서 사용한다고 가정합니다.
# 현재 예제에서는 player.move 메서드에 맵 전환 로직이 포함되어 있습니다.
# 이 부분을 MapManager로 옮기는 것이 더 좋은 구조입니다.

class MapManager:
    """맵의 전환과 렌더링을 책임지는 클래스"""
    def __init__(self):
        self.current_map_x = 0

    def update(self, player):
        # 맵 전환 경계 체크 (player.x 사용)
        if player.x < -player.width: # 화면 왼쪽 끝을 완전히 벗어남
            self.current_map_x -= 1
            player.x = WIDTH - player.width - 10 # 캐릭터를 화면 오른쪽 끝 근처로 이동
        elif player.x > WIDTH: # 화면 오른쪽 끝을 완전히 벗어남
            self.current_map_x += 1
            player.x = 10 # 캐릭터를 화면 왼쪽 끝 근처로 이동
        
        # y축 경계는 player 클래스 내에서 처리하거나, 여기서 함께 처리할 수 있습니다.
        # 여기서는 player 클래스 내 처리를 따릅니다.

    def draw(self, surface):
        # 기본 아스팔트
        surface.fill(GRAY)
        
        # 맵 번호(map_id)에 따라 배경 디자인을 살짝 다르게 표시
        # 1. 공통 요소 (인도)
        pygame.draw.rect(surface, BLACK, (0, 0, WIDTH, 100))
        pygame.draw.rect(surface, BLACK, (0, HEIGHT - 100, WIDTH, 100))

        # 2. 맵 별 차이점
        if self.current_map_x == 0: # 시작 지점: 횡단보도가 있음
            for y in range(120, HEIGHT - 120, 40):
                pygame.draw.rect(surface, WHITE, (WIDTH // 2 - 50, y, 100, 20))
        
        elif self.current_map_x < 0: # 왼쪽 맵들: 중앙선이 노란색 실선
            pygame.draw.rect(surface, YELLOW, (0, HEIGHT // 2 - 5, WIDTH, 10))
        
        elif self.current_map_x > 0: # 오른쪽 맵들: 중앙선이 흰색 점선
            for x in range(0, WIDTH, 60):
                pygame.draw.rect(surface, WHITE, (x, HEIGHT // 2 - 5, 30, 5))

        # 화면 구석에 현재 맵 번호 표시 (디버그용)
        font = pygame.font.SysFont("arial", 30)
        map_text = font.render(f"Map Sector: {self.current_map_x}", True, WHITE)
        surface.blit(map_text, (20, 120))


# --- 메인 실행 ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Zombie City - Seamless Map Switch")
    clock = pygame.time.Clock()
    
    player = Player()
    world = MapManager() # MapManager 인스턴스 생성
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

        keys = pygame.key.get_pressed()
        player.move(keys)
        world.update(player) # MapManager가 플레이어 위치를 기반으로 맵 업데이트

        world.draw(screen) # MapManager가 배경을 그림
        player.draw(screen) # 플레이어 그림
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()