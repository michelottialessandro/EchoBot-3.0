import pygame
import math

# Initialize Pygame
pygame.init()

# Set up colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Window dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Movement Simulation")

# Load and resize the robot image
original_robot_image = pygame.image.load("robot.png")
robot_size = (40, 40)  # New size (width, height)
robot_image = pygame.transform.scale(original_robot_image, robot_size)
robot_pos = [WIDTH // 2, HEIGHT // 2]
robot_speed = 5
robot_angle = 0  # Angle in degrees

# Obstacles definition
obstacles = [
    pygame.Rect(100, 100, 100, 20),
    pygame.Rect(300, 200, 20, 150),
    pygame.Rect(500, 100, 200, 20),
    pygame.Rect(200, 400, 150, 20)
]

def draw_window():
    WIN.fill(WHITE)
    draw_robot(WIN, robot_image, robot_pos, robot_angle)
    for obstacle in obstacles:
        pygame.draw.rect(WIN, RED, obstacle)
    pygame.display.update()

def draw_robot(surface, image, position, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=position).center)
    surface.blit(rotated_image, new_rect.topleft)

def move_robot(keys_pressed):
    global robot_angle
    
    # Rotate left or right
    if keys_pressed[pygame.K_LEFT]:
        robot_angle += 5
    if keys_pressed[pygame.K_RIGHT]:
        robot_angle -= 5
    
    # Move forward or backward
    if keys_pressed[pygame.K_UP]:
        robot_pos[1] += robot_speed * math.cos(math.degrees(robot_angle))
        robot_pos[0] -= robot_speed * math.sin(math.degrees(robot_angle))
    if keys_pressed[pygame.K_DOWN]:
        robot_pos[1] -= robot_speed * math.cos(math.degrees(robot_angle))
        robot_pos[0] += robot_speed * math.sin(math.degrees(robot_angle))

    # Boundary and collision detection
    robot_rect = pygame.Rect(robot_pos[0], robot_pos[1], robot_size[0], robot_size[1])
    for obstacle in obstacles:
        if robot_rect.colliderect(obstacle):
            # Move back if collides
            if keys_pressed[pygame.K_UP]:
                robot_pos[0] -= robot_speed * math.cos(math.degrees(robot_angle))
                robot_pos[1] += robot_speed * math.sin(math.degrees(robot_angle))
            if keys_pressed[pygame.K_DOWN]:
                robot_pos[0] += robot_speed * math.cos(math.degrees(robot_angle))
                robot_pos[1] -= robot_speed * math.sin(math.degrees(robot_angle))

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)  # Frames per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        move_robot(keys_pressed)
        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()
