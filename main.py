# Flappy Bird clone game
import pygame
import os
import random
import time


pygame.init()  # initialize pygame


# =====================================================================================================================
# constants
# =====================================================================================================================


FPS = 60
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 576, 1024
FLOOR_HEIGHT = 125
PIPES_VELOCITY = 7
PIPES_HEIGHTS = [400, 500, 600, 700, 800]
GRAVITY = 0.5
PIPES_SPAWN_RATE = 1300
BIRD_ANIMATION_RATE = 200
PIPES_SPAWN = pygame.USEREVENT
BIRD_ANIMATE = pygame.USEREVENT + 1
FONT = pygame.font.Font('assets/FlappyFont.ttf', 30)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # initialize a windows for pygame


# =====================================================================================================================
# assets
# =====================================================================================================================


BACKGROUND_DAY = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "background-day.png")))
BACKGROUND_NIGHT = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "background-night.png")))
FLOOR1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "floor.png")), (WIDTH, FLOOR_HEIGHT))
FLOOR2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "floor.png")), (WIDTH, FLOOR_HEIGHT))
BIRD_MID = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bluebird-midflap.png")))
BIRD_UP = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bluebird-upflap.png")))
BIRD_DOWN = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bluebird-downflap.png")))
BOTTOM_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "pipe-green.png")))
UPPER_PIPE = pygame.transform.flip(BOTTOM_PIPE, False, True)
MENU = pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "menu.png")))
GAME_ICON = pygame.image.load(os.path.join("assets", "fbcicon.ico"))


# =====================================================================================================================
# bird class
# =====================================================================================================================


class Bird:
    # constructor
    def __init__(self):
        self.bird_rect = BIRD_MID.get_rect(center=(100,512))
        self.bird_vel = 0
        self.birds = [BIRD_DOWN, BIRD_MID, BIRD_UP]
        self.bird_index = 0
    

    # return the bird rectangle
    def get_rect(self):
        return self.bird_rect


    # falling mechanics
    def fall(self):
        self.bird_vel += GRAVITY  # add the gravity to the number of pixels the fall
        self.bird_rect.centery += self.bird_vel  # add the number of pixels to fall to the rectangle

    
    # jump mechanics
    def jump(self):
        self.bird_vel = 0
        self.bird_vel -= 10

    
    #  return a rotated bird to draw on the window
    def rotate(self):
        img = self.birds[self.bird_index]
        pos = -self.bird_vel * 2
        rotated = pygame.transform.rotozoom(img, pos, 1)
        return rotated


    # update the index on the bird image
    def animate(self):
        self.bird_index += 1
        self.bird_index %= 3


    # reset the bird position
    def reset(self):
        self.bird_vel = 0
        self.bird_rect.center = (100, 512)


    # draw the bird on the window
    def draw(self):
        WIN.blit(self.rotate(), self.bird_rect)


# =====================================================================================================================
# pipe class
# =====================================================================================================================


class Pipe:
    # constructor
    def __init__(self):
        random_pipe_pos = random.choice(PIPES_HEIGHTS)
        self.bottom_pipe_rect = UPPER_PIPE.get_rect(midtop=(700, random_pipe_pos)) 
        self.upper_pipe_rect = BOTTOM_PIPE.get_rect(midbottom=(700, random_pipe_pos - 300))


    # return the bottom pipe rectangle
    def get_bottom_rect(self):
        return self.bottom_pipe_rect

    
    # return the upper pipe rectangle
    def get_upper_rect(self):
        return self.upper_pipe_rect


    # move the bottom and upper pipes on the window
    def move(self):
        self.bottom_pipe_rect.centerx -= PIPES_VELOCITY
        self.upper_pipe_rect.centerx -= PIPES_VELOCITY


    # draw the bottom and upper pipes on the window
    def draw(self):
        WIN.blit(BOTTOM_PIPE, self.bottom_pipe_rect)
        WIN.blit(UPPER_PIPE, self.upper_pipe_rect)


# =====================================================================================================================
# environment class
# =====================================================================================================================


class Environment:
    # constructor
    def __init__(self):
        self.floor_pos = 0
        self.time = time.localtime() # get the local time


    # draw background of the game on the window
    def draw_background(self):
        if self.time.tm_hour < 18 and self.time.tm_hour >= 6:  # between 6am to 6pm draw a day background
            WIN.blit(BACKGROUND_DAY, (0, 0))
        else:
            WIN.blit(BACKGROUND_NIGHT, (0, 0))


    # draw the moving floor of the game on the window    
    def draw_floor(self):
        if self.floor_pos < -WIDTH:
            self.floor_pos = 0
        self.floor_pos -= 1
        WIN.blit(FLOOR1, (self.floor_pos, HEIGHT - FLOOR_HEIGHT))
        WIN.blit(FLOOR2, (self.floor_pos + WIDTH, HEIGHT - FLOOR_HEIGHT))


# =====================================================================================================================
# game class
# =====================================================================================================================


class Game:
    # constructor
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.environment = Environment()
        self.score = 0
        self.highscore = 0
        self.active = False


    # start the game session
    def start_game(self):
        self.active = True
        self.score = 0


    # stop the game session
    def stop_game(self):
        self.active = False
        if self.score > self.highscore:
            self.highscore = self.score
        self.pipes.clear()  # clear the pipes list 
        self.bird.reset()   # reset the bird position


    # draw the menu before a game session
    def draw_menu(self):
        st = f"Highscore: {self.highscore}"
        curr_higscore = FONT.render(st, True, WHITE)
        highscore_rect = curr_higscore.get_rect(center=(WIDTH / 2, 800))
        WIN.blit(MENU, (100, 100))  # draw the menu image on the window
        WIN.blit(curr_higscore, highscore_rect)  # draw the highscore on the window


    # draw the score during a game session
    def draw_score(self):
        st = f"Score: {self.score}"
        game_score = FONT.render(st, True, WHITE)
        score_rect = game_score.get_rect(center=(WIDTH / 2, 50))
        WIN.blit(game_score, score_rect)  # draw the score on the window


    # update the score during a game session
    def update_score(self):
        self.score = 0
        for pipe in self.pipes:  # loop over all the pipes rectangles and check if the bird rectangle passed them
            if self.bird.get_rect().centerx > pipe.get_upper_rect().centerx:
                self.score += 1


    # return true if the bird rectangle hits a pipe or the borders of the window
    def collision(self):
        bird_rect = self.bird.get_rect()
        if bird_rect.top <= 0 or bird_rect.bottom >= 900:  # if the bird hit the borders
            return True
        for pipe in self.pipes:
            if bird_rect.colliderect(pipe.get_upper_rect()) or bird_rect.colliderect(pipe.get_bottom_rect()):  # if the bird hit one of the pipes
                return True
        return False


    # run the game
    def run(self):
        running = True
        clock = pygame.time.Clock()
        pygame.time.set_timer(PIPES_SPAWN, PIPES_SPAWN_RATE)  # timer for the pipes spawn event
        pygame.time.set_timer(BIRD_ANIMATE, BIRD_ANIMATION_RATE)  # timer for bird animation
        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # exit the game
                    running = False
                if event.type == BIRD_ANIMATE: # change the index of the bird images
                    self.bird.animate()
                if event.type == PIPES_SPAWN and self.active:  # add pipes to the pipes list
                    self.pipes.append(Pipe())
                if not self.active and event.type == pygame.MOUSEBUTTONDOWN:  # if the user pressed the mouse start the game
                    self.start_game()
                if self.active and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # if the user hit space
                    self.bird.jump()
            self.environment.draw_background()  # draw the background
            if self.active:  # if the game is active
                self.bird.fall()  # update bird position
                self.bird.draw()  # draw the bird
                for pipe in self.pipes:  # update the pipes position and draw them
                    pipe.move()
                    pipe.draw()
                self.update_score()  # updaate the score during session
                if self.collision():  # if a collision occured
                    self.stop_game()  # stop the game
            else:
                self.draw_menu()  # if the game is not active show the menu
            self.draw_score()  # draw the score
            self.environment.draw_floor()  # draw the floor (over the pipes)
            pygame.display.update()  # update the window
        pygame.quit()  # quit the game


# =====================================================================================================================
# main
# =====================================================================================================================


if __name__ == "__main__":
    pygame.display.set_icon(GAME_ICON)  # set the icon of the window
    pygame.display.set_caption("Flappy Bird")  # set the name of the window
    Game().run()  # start the game
