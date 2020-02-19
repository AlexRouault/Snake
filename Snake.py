import pygame
import random

###############
# Classes

class SnakeBody:
    def __init__(self, pos):
        self.pos = pos
        self.rect = pygame.Rect(pos[0] * tile_size + 1, pos[1] * tile_size + 1, tile_size-1, tile_size-1)

    def __add__(self, tup): # Allows us to easily add a vector to the position using '+'
        return SnakeBody((self.pos[0] + tup[0], self.pos[1] + tup[1]))

    def draw(self, colour):
        pygame.draw.rect(screen, colour, self.rect)


class Snake:
    def __init__(self, pos):
        self.body = [SnakeBody(pos)]
        self.length = 1

    def draw(self):
        green = (150,255,0)
        yellow = (230,255,0)
        for i in range(len(self.body)):
            if i % 2:
                self.body[i].draw(yellow)
            else:
                self.body[i].draw(green)

    def move(self, dir, food):
        if dir != (0,0): # Prevent new piece from being added if snake is not moving
            new_head = self.body[0] + dir
            self.body = [new_head] + self.body # add new_head to front of body
        
        if self.body[0].pos == food.pos: # Eat the food
            food.respawn(self)
            self.length += 1
        elif dir != (0,0): # Prevent tail from being removed if we aren't moving:
            # Didn't eat, so remove tail to maintain size
            self.body.pop()

        # Detect collision with wall
        if self.body[0].pos[0] < 0 or self.body[0].pos[0] >= width:
            return False
        if self.body[0].pos[1] < 0 or self.body[0].pos[1] >= height:
            return False

        # Detect collision with self
        if len(self.body) != 1: # Avoid out of range case when length is 1
            for i in range(1, len(self.body)): # every non-head body piece
                if self.body[0].pos == self.body[i].pos:
                    return False
                    
        return True # Continue game

    def contains(self, pos): # Determines whether a cell is part of the snake
        for seg in self.body:
            if pos == seg.pos:
                return True
        return False


class Food:
    def __init__(self, snake):
        self.pos = None
        self.rect = None
        self.respawn(snake)
    def respawn(self, snake):
        self.pos = (random.randint(0,width-1), random.randint(0,height-1))
        self.rect = pygame.Rect(self.pos[0]*tile_size + 1, self.pos[1]*tile_size + 1, tile_size-1, tile_size-1)
        if snake.contains(self.pos):
            self.respawn(snake)
    def draw(self):
        pygame.draw.rect(screen, (255,0,0), self.rect)

class Button:
    def __init__(self, x, y, width, height, text_colour, bg_colour, text):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x - width/2, y - height/2, width, height)
        self.text_colour = text_colour
        self.bg_colour = bg_colour
        self.font = pygame.font.SysFont('comicsansms', 16)

        self.textSurf = self.font.render(str(text), True, text_colour, bg_colour) 
        self.textRect = self.textSurf.get_rect()
        self.textRect.center = (x, y)

    def update(self, text):
        self.textSurf = self.font.render(str(text), True, self.text_colour, self.bg_colour)
        self.textRect = self.textSurf.get_rect()
        self.textRect.center = (self.x, self.y)

    def check(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self):
        pygame.draw.rect(screen, self.bg_colour, self.rect)
        screen.blit(self.textSurf, self.textRect)


###########


def playgame(speed):

    global tile_size

    # Resize screen
    sc_width = width * tile_size
    sc_height = height * tile_size
    size = [sc_width, sc_height]
    pygame.display.set_mode(size)

    # initialize game variables
    snake = Snake((width//2, height//2))
    food = Food(snake)
    score_text = Button(sc_width - 20, 20, 40, 40, (0,0,0), (255,255,255), snake.length)

    # initialize clock. used later in the loop.
    clock = pygame.time.Clock()
    # MOVEEVENT = pygame.USEREVENT+1
    # pygame.time.set_timer(MOVEEVENT, t)
    
    # Loop until the user clicks close button
    cont = True
    dir = (0,0)
    while cont:
        # Event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == 273: # up
                    dir = (0,-1)
                elif event.key == 274: # down
                    dir = (0,1)
                elif event.key == 275: # right
                    dir = (1,0)
                elif event.key == 276: # left
                    dir = (-1,0)

        # game logic
        cont = snake.move(dir, food)
    
        # draw background
        screen.fill((255,255,255)) 
        for v_line in range(1, width):
            pygame.draw.line(screen, (240, 240, 240), (v_line * tile_size, 0), (v_line * tile_size, sc_height))
        for h_line in range(1, height):
            pygame.draw.line(screen, (240, 240, 240), (0, h_line * tile_size), (sc_width, h_line * tile_size))
        
        # draw foreground
        score_text.draw()
        snake.draw()
        food.draw()
        
    
        # Update display
        pygame.display.update()

        clock.tick(speed)

def setupscreen():

    global width
    global height

    black = (0,0,0)
    white = (255,255,255)
    grey = (200,200,200)

    rates = [2, 2.5, 3, 4, 5, 6] # motion frequency
    speed = len(rates) // 2 # index of rates

    width_text = Button(50, 40, 60, 30, black, white, 'width')
    width_dec = Button(200, 40, 40, 30, black, grey, '-')
    width_val = Button(250, 40, 40, 30, black, white, width)
    width_inc = Button(300, 40, 40, 30, black, grey, '+')

    height_text = Button(50, 80, 60, 30, black, white, 'height')
    height_dec = Button(200, 80, 40, 30, black, grey, '-')
    height_val = Button(250, 80, 40, 30, black, white, height)
    height_inc = Button(300, 80, 40, 30, black, grey, '+')

    speed_text = Button(50, 120, 60, 30, black, white, 'speed')
    speed_dec = Button(200, 120, 40, 30, black, grey, '-')
    speed_val = Button(250, 120, 40, 30, black, white, speed + 1)
    speed_inc = Button(300, 120, 40, 30, black, grey, '+')

    begin_button = Button(250, 180, 60, 30, black, grey, "begin")

    clock = pygame.time.Clock()

    while True:

        # Event handlers
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if width_dec.check() and width > 7:
                    width -= 2
                    width_val.update(width)
                if width_inc.check() and width < 31:
                    width += 2
                    width_val.update(width)
                if height_dec.check() and height > 7:
                    height -= 2
                    height_val.update(height)
                if height_inc.check() and height < 31:
                    height += 2
                    height_val.update(height)
                if speed_dec.check() and speed > 0:
                    speed -= 1
                    speed_val.update(speed + 1)
                if speed_inc.check() and speed < len(rates) - 1:
                    speed += 1
                    speed_val.update(speed + 1)
                if begin_button.check():
                    playgame(rates[speed])
                    pygame.display.set_mode([420, 220])

        # draw background
        screen.fill((255,255,255))

        # draw foreground
        width_text.draw()
        width_dec.draw()
        width_val.draw()
        width_inc.draw()
        height_text.draw()
        height_dec.draw()
        height_val.draw()
        height_inc.draw()
        speed_text.draw()
        speed_dec.draw()
        speed_val.draw()
        speed_inc.draw()
        begin_button.draw()

        # Update display
        pygame.display.update()

        clock.tick(10)



###############
 
# initialize game engine
width = 21
height = 11
tile_size = 20

pygame.init()
screen = pygame.display.set_mode([width * tile_size, height * tile_size])
pygame.display.set_caption('Snake')

setupscreen()
 
# close the window and quit
pygame.quit()