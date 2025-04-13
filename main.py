# Pygame recreation in pygame with extra features

#imports
from board import boards #import tilemaps from board file
import pygame
import math

pygame.init()

game_version = "4"
game_icon = pygame.image.load('assets/player_images/1.png')


#Window options
WIDTH = 900
HEIGHT = 950 # 50 extra pixels, so that there is space for amount of coins & lives.
fps = 60
pygame.display.set_icon(game_icon)
pygame.display.set_caption(f'Pacman - Version {game_version}')
font = pygame.font.Font('freesansbold.ttf', 20) # set font
screen = pygame.display.set_mode([WIDTH, HEIGHT]) # set screen size
timer = pygame.time.Clock()
PI = math.pi # sets pi as a variable, so that it can be easily called in future without having to use math.pi

colour = 'blue' #colour for all of the tilemap shapes. (excl powerups & coins.)

player_x = 450 # Player starting position x
player_y = 663# Player starting position y
direction = 0 # Player starting direction (right)
counter = 0
flicker = False # flicker for powerup tiles
valid_turns = [False, False, False, False] #R,L,U,D
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_count = 0
eaten_ghosts = [False,False,False,False]
moving = False
startup_counter = 0
lives = 3

player_images = []
for i in range(1,5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45,45))) #loads player image and animation states

blinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45,45)) #loads ghost images
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45,45))#loads ghost images
inky_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45,45))#loads ghost images
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45,45))#loads ghost images
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45,45))#loads ghost images
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45,45))#loads ghost images

#sets directions and starting position for ghost sprites
blinky_x = 56
blinky_y = 58
blinky_direction = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 440
pinky_y = 438
pinky_direction = 2
clyde_x = 380
clyde_y = 438
clyde_direction = 2

targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y),] # shows current target of the 4 different ghosts
blinky_dead = False #ghost dead = true, alive = false
inky_dead = False
pinky_dead = False
clyde_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False
ghost_speed = 2 #(same as player speed)


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id): # initialise ghost class and define variables
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.checkCollisions()
        self.rect = self.draw()

    def draw(self): # decide what image to draw based on current conditions
        if (not powerup and not self.dead) or (eaten_ghosts[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))

        elif powerup and not self.dead and not eaten_ghosts[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))

        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))

        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36)) # draw hitboxes for ghosts
        return ghost_rect

    def checkCollisions(self):
        #R,L,U,D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH//30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True # up
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True # left
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True # right
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True # down
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True # up

            if self.direction == 2 or self.direction == 3: # if moving up/down
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True # down
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True # up
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True # left
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True # right

            if self.direction == 0 or self.direction == 1: #if moving left/right
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True # down
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True # up
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True # left
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True # right
        else: #allow to move off screen and appear on other side like the player character does
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480: # check if ghost currently inside of box coordinates
            self.in_box = True
        else:
            self.in_box = False

        return self.turns, self.in_box

    def moveClyde(self):
        # r,l,u,d
        #clyde will turn when it would be an advantage for pursuit

        if self.direction == 0: # if facing right
            if self.target[0] > self.x_pos and self.turns[0]: # keep going current direction as far as you can to get to target
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:#target below, and can turn down
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:#target higher, collided on right
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:#target behind, can turn left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]: # if going right, target not there
                if self.target[1] > self.y_pos and self.turns[3]: # if target below
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed

        elif self.direction == 1: # if facing left
            if self.target[1] > self.y_pos and self.turns[3]: # going left, but can go down
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]: # hit to the left
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]: # can go right, target right
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed

        elif self.direction == 2: # if facing up
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]: #keep going up
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]: #go left
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]: #go left
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed

        elif self.direction == 3: # if facing down
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:# if off screen to left (makes the ghost look like they are catching up to you, moves a short distance closer to player)
            self.x_pos = 900
        elif self.x_pos > 900: # if off screen to right (makes the ghost look like they are catching up to you, moves a short distance closer to player)
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction
    

#draws text on bottom of screen e.g score
def drawMisc():
    bottom_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(bottom_text, (10,920))

    if powerup: # powerup indicator in bottom bar when powerup active
        pygame.draw.circle(screen, 'blue', (140, 930), 15)

    for i in range(lives): # display pacman icons based on how many lives remaining
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))

#eating items &scoring appropriately
def checkCollision(score, powerup, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH//30
    if 0 < player_x < 870:
        if level[center_y//num1][center_x//num2] == 1:
            level[center_y//num1][center_x//num2] = 0
            score +=10
        if level[center_y//num1][center_x//num2] == 2:
            level[center_y//num1][center_x//num2] = 0
            score +=50
            powerup = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]

    return score, powerup, power_count, eaten_ghosts

#function for drawing the player sprite
def drawPlayer():
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y)) # RIGHT
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y)) # LEFT
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y)) # UP
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y)) # DOWN



#function for drawing the tilemap board
level = boards

def drawBoard():
    num1 = ((HEIGHT - 50) // 32) #to leave space for the score & number of lives remaining.
    num2 = (WIDTH // 30)
    # the two above are using floor division, so that the output will always be an integer
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 + (0.5*num1)), 4) #draw small circles (coins)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'gold', (j * num2 + (0.5*num2), i * num1 + (0.5*num1)), 10) #draw large circles (powerups)
            if level[i][j] == 3:
                pygame.draw.line(screen, colour, (j * num2 + (0.5*num2), i * num1), (j * num2 + (0.5*num2), i * num1 + num1), 3) # draw vertical walls
            if level[i][j] == 4:
                pygame.draw.line(screen, colour, (j * num2 , i * num1 + (0.5*num1)), (j * num2 + num2, i * num1 + (0.5*num1)), 3) # draw horizontal walls
            if level[i][j] == 5:
                pygame.draw.arc(screen, colour, [(j*num2 - (num2*0.4)) - 2, (i * num1 + (0.5*num1)), num2, num1], 0, PI/2, 3) # draw curve for corners
            if level[i][j] == 6:
                pygame.draw.arc(screen, colour, [(j*num2 + (num2*0.5)), (i * num1 + (0.5*num1)), num2, num1], PI/2, PI, 3) # draw curve for corners
            if level[i][j] == 7:
                pygame.draw.arc(screen, colour, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI / 2, 3) # draw curve for corners
            if level[i][j] == 8:
                pygame.draw.arc(screen, colour, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2, 2 * PI, 3) # draw curve for corners
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2 , i * num1 + (0.5*num1)), (j * num2 + num2, i * num1 + (0.5*num1)), 3) # draw horizontal walls (ghost area gate)


#collision checker - spots direct near open spaces in all directions of the player sprite

def checkPosition(centerx, centery):
    turns = [False, False, False, False] #R,L,U,D
    num1 = (HEIGHT-50)//32
    num2 = (WIDTH//30)
    num3 = 15
    #check collisions based on center x and center y of player + or - num3
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery//num1][(centerx - num3)//num2] <3:
                turns[1] = True
        if direction == 1:
            if level[centery//num1][(centerx + num3)//num2] <3:
                turns[0] = True
        if direction == 2:
            if level[(centery+num3)//num1][centerx//num2] <3:
                turns[3] = True
        if direction == 3:
            if level[(centery-num3)//num1][centerx//num2] <3:
                turns[2] = True

        if direction == 0 or direction == 1: # check for moving left or right
            if 12 <= centerx % num2 <= 18: # if centerx mod num2 between 12 and 18, rough midpoint of tile - to calculate above or below
                if level[(centery + num1) //num1][centerx //num2] < 3: # if position directly below open
                    turns[3] = True
                if level[(centery - num1) //num1][centerx //num2] < 3: # if position directly above open
                    turns[2] = True
            if 12 <= centery % num1 <= 18: # if centerx mod num2 between 12 and 18, rough midpoint of tile - to calculate left or right
                if level[centery//num1][(centerx - num3) //num2] < 3: # if position directly left open
                    turns[1] = True
                if level[centery//num1][(centerx + num3) //num2] < 3: # if position directly right open
                    turns[0] = True

        if direction == 2 or direction == 3: # check for moving up or down
            if 12 <= centerx % num2 <= 18: # if centerx mod num2 between 12 and 18, rough midpoint of tile - to calculate above or below
                if level[(centery + num3) //num1][centerx //num2] < 3: # if position directly below open
                    turns[3] = True
                if level[(centery - num3) //num1][centerx //num2] < 3: # if position directly above open
                    turns[2] = True
            if 12 <= centery % num1 <= 18: # if centerx mod num2 between 12 and 18, rough midpoint of tile - to calculate left or right
                if level[centery//num1][(centerx - num2) //num2] < 3: # if position directly left open
                    turns[1] = True
                if level[centery//num1][(centerx + num2) //num2] < 3: # if position directly right open
                    turns[0] = True

    else:
        turns[0] = True
        turns[1] = True

    return turns

def movePlayer(play_x, play_y):
    #r,l,u,d
    if direction == 0 and valid_turns[0]:
        play_x += player_speed
    elif direction == 1 and valid_turns[1]:
        play_x -= player_speed
    if direction == 2 and valid_turns[2]:
        play_y -= player_speed
    elif direction == 3 and valid_turns[3]:
        play_y += player_speed
    return play_x, play_y
    

#game loop
run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
        
    else:
        counter = 0
        flicker = True
    
    if powerup and power_count < 600:
        power_count += 1
    elif powerup and power_count >=600:
        power_count = 0
        powerup = False
        eaten_ghosts = [False,False,False,False]
    
    if  startup_counter < 180:
        moving = False
        startup_counter +=1
    else:
         moving = True

    screen.fill('black')
    drawBoard()
    drawPlayer()
    drawMisc()
    
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speed, blinky_img, blinky_direction, blinky_dead, blinky_box, 0) # init blinky
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speed, inky_img, inky_direction, inky_dead, inky_box, 1) # init inky
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speed, pinky_img, pinky_direction, pinky_dead, pinky_box, 2) # init pinky
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speed, clyde_img, clyde_direction, clyde_dead, clyde_box, 3) # init clyde
    
    center_x = player_x + 23
    center_y = player_y + 24
    valid_turns = checkPosition(center_x,center_y) # calls checkPosition, checks for valid turn and passes the center point for the player sprite
    if moving: # only allow the player to move after the startup counter
        player_x, player_y = movePlayer(player_x,player_y)
        pinky_x, pinky_y, pinky_direction = pinky.moveClyde()
        blinky_x, blinky_y, blinky_direction = blinky.moveClyde()
        inky_x, inky_y, inky_direction = inky.moveClyde()
        clyde_x, clyde_y, clyde_direction = clyde.moveClyde()
    score, powerup, power_count, eaten_ghosts = checkCollision(score, powerup, power_count, eaten_ghosts)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:    #Register direction changes with arrow keys
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:    #Register direction changes with arrow keys
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction
            if event.key == pygame.K_ESCAPE: #Register game quit with escape
                pygame.quit()

    if direction_command == 0 and valid_turns[0]:
        direction = 0
    if direction_command == 1 and valid_turns[1]:
        direction = 1
    if direction_command == 2 and valid_turns[2]:
        direction = 2
    if direction_command == 3 and valid_turns[3]:
        direction = 3
    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897





    pygame.display.flip()
pygame.quit()