import pygame
import math

# 초기화
pygame.init()
WIDTH, HEIGHT = 1280, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie City - Directional Character")

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
        self.direction = 0  # 방향 (라디안 단위)
        
    def move(self, keys):
        global current_map_x
        dx, dy = 0, 0
        moving = False
        
        if keys[pygame.K_w]: dy -= 1; moving = True
        if keys[pygame.K_s]: dy += 1; moving = True
        if keys[pygame.K_a]: dx -= 1; moving = True
        if keys[pygame.K_d]: dx += 1; moving = True
        
        # 이동 중일 때만 방향 업데이트
        if moving and (dx != 0 or dy != 0):
            # 방향 계산 (atan2 사용)
            self.direction = math.atan2(dy, dx)
        
        # 속도 보정
        actual_speed = self.speed * 0.7071 if dx != 0 and dy != 0 else self.speed
        self.x += dx * actual_speed
        self.y += dy * actual_speed
        
        # 애니메이션 카운트
        if moving: 
            self.walk_count += 0.2
        else: 
            self.walk_count = 0
        
        # --- 맵 전환 로직 (0~10번 맵으로 제한) ---
        # 왼쪽 끝으로 나갔을 때
        if self.x < -self.width:
            if current_map_x > 0:  # 0번 맵보다 왼쪽으로 못 가게
                current_map_x -= 1
                self.x = WIDTH - 10
            else:
                self.x = 0  # 벽에 막힘
        
        # 오른쪽 끝으로 나갔을 때
        elif self.x > WIDTH:
            if current_map_x < 10:  # 10번 맵보다 오른쪽으로 못 가게
                current_map_x += 1
                self.x = 10
            else:
                self.x = WIDTH - self.width  # 벽에 막힘
        
        # 위아래는 화면 밖으로 못 나가게 고정
        self.y = max(0, min(HEIGHT - self.height, self.y))
    
    def draw(self, surface):
        leg_offset = math.sin(self.walk_count) * 8
        
        # 중심점
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        
        # 방향에 따른 각도 (도 단위로 변환)
        angle_deg = math.degrees(self.direction)
        
        # 캐릭터의 로컬 좌표들을 방향에 맞게 회전
        # 기본 포즈는 오른쪽(0도)을 향함
        
        # 다리 위치 (로컬 좌표)
        leg1_local = [-8, 5 + leg_offset]
        leg2_local = [-8, 5 - leg_offset]
        
        # 몸통 중심점
        body_local = [-10, -8]
        
        # 머리 위치
        head_local = [-10, -20]
        
        # 팔 위치
        arm1_start_local = [-10, -5]
        arm1_end_local = [-15, 5 - leg_offset]
        arm2_start_local = [-10, -5]
        arm2_end_local = [-15, 5 + leg_offset]
        
        # 회전 함수
        def rotate_point(x, y, angle_rad):
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)
            rotated_x = x * cos_a - y * sin_a
            rotated_y = x * sin_a + y * cos_a
            return rotated_x, rotated_y
        
        # 모든 점들을 회전
        leg1_rot = rotate_point(leg1_local[0], leg1_local[1], self.direction)
        leg2_rot = rotate_point(leg2_local[0], leg2_local[1], self.direction)
        body_rot = rotate_point(body_local[0], body_local[1], self.direction)
        head_rot = rotate_point(head_local[0], head_local[1], self.direction)
        arm1_start_rot = rotate_point(arm1_start_local[0], arm1_start_local[1], self.direction)
        arm1_end_rot = rotate_point(arm1_end_local[0], arm1_end_local[1], self.direction)
        arm2_start_rot = rotate_point(arm2_start_local[0], arm2_start_local[1], self.direction)
        arm2_end_rot = rotate_point(arm2_end_local[0], arm2_end_local[1], self.direction)
        
        # 회전된 좌표를 화면 좌표로 변환
        leg1_x = center_x + leg1_rot[0]
        leg1_y = center_y + leg1_rot[1]
        leg2_x = center_x + leg2_rot[0]
        leg2_y = center_y + leg2_rot[1]
        body_x = center_x + body_rot[0]
        body_y = center_y + body_rot[1]
        head_x = center_x + head_rot[0]
        head_y = center_y + head_rot[1]
        
        # 다리 그리기
        pygame.draw.circle(surface, PANTS, (int(leg1_x), int(leg1_y)), 5)
        pygame.draw.circle(surface, PANTS, (int(leg2_x), int(leg2_y)), 5)
        
        # 몸통 그리기 (회전된 사각형)
        body_width = 20
        body_height = 18
        
        # 몸통의 4개 코너 계산
        body_corners = [
            (-body_width/2, -body_height/2),
            (body_width/2, -body_height/2),
            (body_width/2, body_height/2),
            (-body_width/2, body_height/2)
        ]
        
        rotated_corners = []
        for corner in body_corners:
            rotated = rotate_point(corner[0] + body_local[0], corner[1] + body_local[1], self.direction)
            rotated_corners.append((center_x + rotated[0], center_y + rotated[1]))
        
        pygame.draw.polygon(surface, CLOTHES, rotated_corners)
        
        # 머리 그리기
        pygame.draw.circle(surface, SKIN, (int(head_x), int(head_y)), 9)
        
        # 팔 그리기
        arm1_start_x = center_x + arm1_start_rot[0]
        arm1_start_y = center_y + arm1_start_rot[1]
        arm1_end_x = center_x + arm1_end_rot[0]
        arm1_end_y = center_y + arm1_end_rot[1]
        arm2_start_x = center_x + arm2_start_rot[0]
        arm2_start_y = center_y + arm2_start_rot[1]
        arm2_end_x = center_x + arm2_end_rot[0]
        arm2_end_y = center_y + arm2_end_rot[1]
        
        pygame.draw.line(surface, SKIN, 
                        (arm1_start_x, arm1_start_y), 
                        (arm1_end_x, arm1_end_y), 4)
        pygame.draw.line(surface, SKIN, 
                        (arm2_start_x, arm2_start_y), 
                        (arm2_end_x, arm2_end_y), 4)
        
        # 눈 그리기 (방향 표시)
        eye_offset = 4
        eye_local = rotate_point(-10 + eye_offset, -20, self.direction)
        eye_x = center_x + eye_local[0]
        eye_y = center_y + eye_local[1]
        pygame.draw.circle(surface, BLACK, (int(eye_x), int(eye_y)), 2)

def draw_background(surface, map_id):
    # 기본 아스팔트
    surface.fill(GRAY)
    
    # 1. 공통 요소 (인도)
    pygame.draw.rect(surface, BLACK, (0, 0, WIDTH, 100))
    pygame.draw.rect(surface, BLACK, (0, HEIGHT - 100, WIDTH, 100))
    
    # 2. 맵 별 차이점
    if map_id == 0:  # 시작 지점: 횡단보도가 있음
        for y in range(120, HEIGHT - 120, 40):
            pygame.draw.rect(surface, WHITE, (WIDTH // 2 - 50, y, 100, 20))
    
    elif map_id < 5:  # 왼쪽 맵들 (1-4번): 중앙선이 노란색 실선
        pygame.draw.rect(surface, YELLOW, (0, HEIGHT // 2 - 5, WIDTH, 10))
    
    elif map_id >= 5:  # 오른쪽 맵들 (5-10번): 중앙선이 흰색 점선
        for x in range(0, WIDTH, 60):
            pygame.draw.rect(surface, WHITE, (x, HEIGHT // 2 - 5, 30, 5))
    
    # 화면 구석에 현재 맵 번호 표시
    font = pygame.font.SysFont("arial", 30)
    map_text = font.render(f"Map Sector: {map_id}/10", True, WHITE)
    surface.blit(map_text, (20, 120))
    
    # 맵 경계 안내
    if map_id == 0:
        border_text = font.render("← 경계", True, WHITE)
        surface.blit(border_text, (20, 160))
    elif map_id == 10:
        border_text = font.render("경계 →", True, WHITE)
        surface.blit(border_text, (WIDTH - 150, 160))

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