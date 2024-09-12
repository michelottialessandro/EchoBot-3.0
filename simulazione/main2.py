import pygame
import math
import random
import os



pygame.init()
obstacles=[]

# Set up colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Window dimensions
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robot Movement Simulation")

# Robot parameters
robot_speed = 5
robot_angle = 0  # Angle in degrees

# Load robot image
original_robot_image = pygame.image.load("robot.png")
#robot_size = robot_image.get_rect().size

robot_size=(40,40)
robot_image = pygame.transform.scale(original_robot_image, robot_size)
robot_pos = [20, 20]

def create_obstacles():
    MAX_WIDTH= 100
    MAX_HEIGHT=100
    MIN_WIDTH=20
    MIN_HEIGHT=20
    for i in range(random.randint(12,16)):
        width=random.randint(MIN_WIDTH,MAX_WIDTH)
        height=random.randint(MIN_HEIGHT,MAX_HEIGHT)
        left=random.randint(20,WIDTH-20)
        top=random.randint(20,HEIGHT-20)
        obstacles.append(pygame.Rect(float(left),float(top),float(width),float(height)))

create_obstacles() 

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
    if keys_pressed[pygame.K_a]:
        robot_angle += 1
    if keys_pressed[pygame.K_d]:
        robot_angle -= 1   

    if keys_pressed[pygame.K_LEFT]:
        robot_pos[0] -= robot_speed 
        #robot_pos[1] += robot_speed * math.sin(robot_angle)

    if keys_pressed[pygame.K_RIGHT]:
        robot_pos[0] += robot_speed 
        #robot_pos[1] += robot_speed * math.sin(robot_angle)

    # Move forward or backward
    if keys_pressed[pygame.K_DOWN]:
        print(robot_angle)
        robot_pos[0] +=  robot_speed * math.sin(robot_angle)
        robot_pos[1] += robot_speed  * math.cos(robot_angle)
        
    if keys_pressed[pygame.K_UP]:
        print(robot_angle)
        robot_pos[0] +=  robot_speed * math.sin(robot_angle)
        robot_pos[1] += robot_speed * math.cos(robot_angle)

    # Boundary and collision detection
    robot_rect = pygame.Rect(robot_pos[0], robot_pos[1], robot_size[0], robot_size[1])
    for obstacle in obstacles:
        if robot_rect.colliderect(obstacle):
            # Move back if collides
            if keys_pressed[pygame.K_DOWN]:
                robot_pos[1] += robot_speed 
            if keys_pressed[pygame.K_UP]:
                robot_pos[1] -= robot_speed

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(30)  # Frames per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        
        if(keys_pressed[pygame.K_F2]):
            os.exit()
        
        move_robot(keys_pressed)
        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()
