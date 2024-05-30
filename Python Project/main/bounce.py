import pygame

pygame.init()

w = 1000
h = 800
screen = pygame.display.set_mode([w, h])

fps = 60
timer = pygame.time.Clock()

# game variables
wall_thickness = 10
gravity = 0.5
stop = 0.3
# track positions of mouse to get movement vector
mouse_trajectory = []


class Ball:
    def __init__(self, x_pos, y_pos, radius, image_path, mass, retention, y_speed, x_speed, id, friction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.image = pygame.transform.scale(pygame.image.load(image_path), (4 * radius, 4 * radius))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.mass = mass
        self.retention = retention
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.id = id
        self.selected = False
        self.friction = friction

    def draw(self):
        screen.blit(self.image, self.rect)

    def motion(self):
        if not self.selected:
            if self.y_pos < h - self.radius - (wall_thickness / 2):
                self.y_speed += gravity
            if (self.y_pos < self.radius + (wall_thickness/2) and self.y_speed < 0) or \
                    (self.y_pos > h - self.radius - (wall_thickness/2) and self.y_speed > 0):
                self.y_speed *= -1 * self.retention
                if abs(self.y_speed) < stop:
                    self.y_speed = 0
            if (self.x_pos < self.radius + (wall_thickness/2) and self.x_speed < 0) or \
                    (self.x_pos > w - self.radius - (wall_thickness/2) and self.x_speed > 0):
                self.x_speed *= -1 * self.retention
                if abs(self.x_speed) < stop:
                    self.x_speed = 0
            if self.y_speed == 0 and self.x_speed != 0:
                if self.x_speed > 0:
                    self.x_speed -= self.friction
                elif self.x_speed < 0:
                    self.x_speed += self.friction
        else:
            self.x_speed = x_push
            self.y_speed = y_push
        return self.y_speed

    def update_pos(self, mouse):
        if not self.selected:
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed
            self.rect.center = (self.x_pos, self.y_pos)
        else:
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]
            self.rect.center = (self.x_pos, self.y_pos)

    def check_select(self, pos):
        self.selected = False
        if self.rect.collidepoint(pos):
            self.selected = True
        return self.selected


def draw_walls():
    left = pygame.draw.line(screen, 'white', (0, 0), (0, h), wall_thickness)
    right = pygame.draw.line(screen, 'white', (w, 0), (w, h), wall_thickness)
    top = pygame.draw.line(screen, 'white', (0, 0), (w, 0), wall_thickness)
    bottom = pygame.draw.line(screen, 'white', (0, h), (w, h), wall_thickness)
    wall_list = [left, right, top, bottom]
    return wall_list


def calc_motion_vector():
    x_speed = 0
    y_speed = 0
    if len(mouse_trajectory) > 10:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)
    return x_speed, y_speed


ball1 = Ball(50, 50, 30, "poole.png", 100, .8, 0, 0, 1, 0.02)
ball2 = Ball(500, 50, 50, "poole.png", 300, .8, 0, 0, 2, 0.03)
ball3 = Ball(200, 50, 40, "poole.png", 200, .8, 0, 0, 3, 0.04)
ball4 = Ball(700, 50, 60, "poole.png", 500, .8, 0, 0, 4, .1)
balls = [ball1, ball2, ball3, ball4]

# main game loop
run = True
active_select = False
while run:
    timer.tick(fps)
    screen.fill('blue')
    mouse_coords = pygame.mouse.get_pos()
    mouse_trajectory.append(mouse_coords)
    if len(mouse_trajectory) > 20:
        mouse_trajectory.pop(0)
    x_push, y_push = calc_motion_vector()

    walls = draw_walls()
    for ball in balls:
        ball.draw()
        ball.update_pos(mouse_coords)
        ball.y_speed = ball.motion()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for ball in balls:
                    if ball.check_select(event.pos):
                        active_select = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_select = False
                for ball in balls:
                    ball.check_select((-1000, -1000))

    pygame.display.flip()

pygame.quit()
