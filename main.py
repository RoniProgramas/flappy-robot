import pygame
import random
import sys

# Configurações iniciais
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cyber Flappy - Pressione ESPAÇO para jogar!")

# Cores do tema cyberpunk
COLORS = {
    "bg": (0, 0, 30),
    "robot": (0, 255, 100),
    "laser": (255, 50, 150),
    "ground": (30, 30, 60),
    "text": (255, 150, 0)
}

# Classe do Robô
class Robot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        self._draw_robot()
        self.rect = self.image.get_rect(center=(WIDTH//4, HEIGHT//2))
        self.velocity = 0
        self.gravity = 0.8

    def _draw_robot(self):
        pygame.draw.circle(self.image, COLORS["robot"], (20, 20), 15, 4)
        pygame.draw.line(self.image, COLORS["robot"], (20, 25), (20, 35), 4)

    def jump(self):
        self.velocity = -12

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

# Classe dos Obstáculos
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 80
        self.gap = 200
        self.image = pygame.Surface((self.width, HEIGHT), pygame.SRCALPHA)
        self._create_obstacle()
        self.rect = self.image.get_rect(midleft=(WIDTH, 0))
        self.passed = False

    def _create_obstacle(self):
        obstacle_height = random.randint(100, HEIGHT - self.gap - 100)
        pygame.draw.rect(self.image, COLORS["laser"], (0, 0, self.width, obstacle_height))
        pygame.draw.rect(self.image, COLORS["laser"], 
                        (0, obstacle_height + self.gap, self.width, HEIGHT))

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

# Sistema de jogo
class Game:
    def __init__(self):
        self.robot = Robot()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.robot)
        self.score = 0
        self.font = pygame.font.Font(None, 48)
        self.running = True

    def spawn_obstacle(self):
        obstacle = Obstacle()
        self.obstacles.add(obstacle)
        self.all_sprites.add(obstacle)

    def check_collisions(self):
        if pygame.sprite.spritecollide(self.robot, self.obstacles, False) or \
           self.robot.rect.top < 0 or \
           self.robot.rect.bottom > HEIGHT - 50:
            self.running = False

    def draw_ground(self):
        pygame.draw.rect(screen, COLORS["ground"], (0, HEIGHT-50, WIDTH, 50))

    def run(self):
        clock = pygame.time.Clock()
        obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(obstacle_timer, 1500)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == obstacle_timer:
                    self.spawn_obstacle()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.robot.jump()

            screen.fill(COLORS["bg"])
            self.draw_ground()
            
            self.all_sprites.update()
            self.check_collisions()
            self.all_sprites.draw(screen)
            
            # Mostrar pontuação
            score_text = self.font.render(f"Score: {self.score}", True, COLORS["text"])
            screen.blit(score_text, (20, 20))
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
