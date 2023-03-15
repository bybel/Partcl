import random
import pygame
from enum import Enum
# from SpatialHashGrid import *

HEIGHT = 800
WIDTH = 800
NB_PARTICLES = 100

V_MAX = 2

class regime(Enum):
    HERBIVORE = 0
    CARNIVORE = 1
    PLANT = 2

types_colors = [(0, 0, 255), (255, 0, 0), (0, 255, 0)]

# Definde attraction matrix
attraction_matrix = [
    [random.randrange(-10, 11) for j in range(3)] for i in range(3)]
for i in range(3):
    attraction_matrix[1][i] = -10
    attraction_matrix[i][1] = -10


print(attraction_matrix)

# Define a particle class


class Particle:
    def __init__(self, x, y, vx, vy, ax, ay, type, cam=False):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(vx, vy)
        self.acceleration = pygame.Vector2(ax, ay)
        self.type = regime(type)
        self.size = 1
        self.dead = False
        
    def die(self):
        self.dead = True


# Create a list of particles
particles = []

# Initialize the particles


def init_particles(num_particles):
    for i in range(num_particles):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        type = random.randint(0, 3 - 1)
        particle = Particle(x, y, 0, 0, 0, 0, type)
        particles.append(particle)
    return particles
        


# Update the particles
def update_particles():
    for particle in particles:
        if not particle.dead:
            
            if particle.type == regime.PLANT:
                particle.velocity *= 0.99
                particle.acceleration = 0            
            # neighbour = grid._get_nearby_cells(particle, 200)
            for other in particles:
                if other.dead:
                    continue
                if other == particle:
                    continue

                dl = other.position - particle.position
                distance = dl.length()
                
                # Collision
                if distance <= particle.size + other.size:
                    
                    if(other.type == regime.PLANT and particle.type == regime.HERBIVORE):
                        particle.size += other.size
                        particle.velocity += -particle.velocity * 0.7
                        other.die()
                    elif(other.type == regime.HERBIVORE and particle.type == regime.CARNIVORE):
                        particle.size += other.size
                        other.die()
                    elif(other.type == regime.CARNIVORE and particle.type == regime.HERBIVORE):
                        if other.size > particle.size:
                            particle.die()
                            other.velocity += -other.velocity * 0.7
                            other.size += particle.size
                    elif(other.type == regime.CARNIVORE and particle.type == regime.CARNIVORE):
                        if(particle.size > WIDTH/4):
                            other.die()
                            particle.velocity += -particle.velocity * 0.7
                            particle.size += other.size
                            
                    tmp = particle.velocity
                    particle.velocity = other.velocity 
                    other.velocity = tmp
                    
                    if distance < particle.size + other.size:
                        dl.scale_to_length(particle.size + other.size)
                        particle.position = other.position - dl
                        other.position = particle.position + dl
                        
                
                
                
                particle.acceleration = 1/(distance**1) * dl.normalize()
                particle.acceleration *= attraction_matrix[particle.type.value][other.type.value]
                
                if distance > WIDTH-particle.position.x:
                    particle.acceleration.x *= -1
                if distance > HEIGHT-particle.position.y:
                    particle.acceleration.y *= -1
                if distance > WIDTH-other.position.x:
                    particle.acceleration.x *= -1
                if distance > HEIGHT-other.position.y:
                    particle.acceleration.y *= -1
                
                # repulsion
                if distance < 20:
                    particle.acceleration = -1 * particle.acceleration
        
            # add_rotational_wind(particle)
            particle.velocity += particle.acceleration
            
            # Limit the velocity
            if particle.velocity.length() > V_MAX:
                particle.velocity.scale_to_length(V_MAX)

            # Update the position
            particle.position += particle.velocity  
            
            
        

        # Make the world a torus
            if particle.position.x > WIDTH:
                particle.position.x -= WIDTH
            elif particle.position.x < 0:
                particle.position.x += WIDTH
            if particle.position.y > HEIGHT:
                particle.position.y -= HEIGHT
            elif particle.position.y < 0:
                particle.position.y += HEIGHT
        

    
    
    

# Render the particles


def render_particles(screen):
    for particle in particles:
        
        if not particle.dead:  
            pygame.draw.circle(screen,
                            types_colors[particle.type.value],
                            (int(particle.position.x), int(particle.position.y)),
                            particle.size)
        


def add_rotational_wind(particle):
    center = pygame.Vector2(WIDTH/2, HEIGHT/2)
    distance = particle.position.length() - center.length()
    particle.acceleration += 1/distance * center * 0.0005

def main():


    # Initialize Pygame
    pygame.init()

    # Set the screen size
    screen = pygame.display.set_mode((WIDTH, HEIGHT))


    # Initialize the particles
    particles = init_particles(NB_PARTICLES)

    # Run the simulation
    running = True
    cc = 0
    coef = 0.2
    rand_ass_cola = (random.randint(0, 255) * coef, random.randint(0, 255) * coef, random.randint(0, 255) * coef)
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        cc += 1
        
        if cc % 100 == 0:
            for i in range(10):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                type = regime.PLANT.value
                particle = Particle(x, y, 0, 0, 0, 0, type)
                particles.append(particle)
        
        # Update the particles
        update_particles()

        pygame.time.delay(5)

        # Clear the screen
        screen.fill(rand_ass_cola)

        # Render the particles
        render_particles(screen)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()


main()
