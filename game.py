import pygame


pygame.init()
width,height = 640,640
screen = pygame.display.set_mode((width, height))

player_size = 64
player_x = width //2    #starting position of player
player_y = 600
player_x_change = 0
player_y_change = 0
player_speed = 0.3
clock = pygame.time.Clock()
frame_count = 0     #used for spawning enemies

previous_state = None

#define different states for different windows, start with 2 levels + menu and restart screen = 4
game_state = ['MENU', 'LEVEL_1', 'LEVEL_2','LEVEL_3 ','LEVEL_4','game_over']
state_index = 0     #initially set to 0
checkpoint = 0
reached_star = False #used to incremenet state_index by only one per collision

menu_font = pygame.font.SysFont('Arial', 64)
menu_play_font = pygame.font.SysFont('Arial', 36)
level_font = pygame.font.SysFont('Arial', 36)
font_disclaimer = pygame.font.SysFont('Arial', 20)


#load images
background_level_1 = pygame.image.load("road_background.jpg")
car_left = pygame.image.load("car_left.png")
car_right = pygame.image.load("car_right.png")
person = pygame.image.load("user.png")
endpoint = pygame.image.load("star.png")
background_level_2 = pygame.image.load("level_2.png")

class Car:
    def __init__(self,x,y,direction):
        self.speed = 0.3    #maybe set to random
        self.width = 32     #for collision checking
        self.height = 32
        self.x = x      #starting position of the car
        self.y = y
        self.direction = direction  #defines direction, -1 for left, 1 for right

    def update(self):
        self.x = self.x + self.speed*self.direction

        #if car exits boundary of game
        if self.direction == 1:     #moving right
            if self.x >= 640:
                self.x = 0

        elif self.direction == -1:  #moving left
            if self.x + 32 <= 0:
                self.x = 640        #respawn at right side

        self.rect = pygame.Rect(self.x, self.y, 32,32)  #define rectangle for collision
    def draw(self,screen):

        if self.direction == -1:
            screen.blit(car_left, (self.x,self.y))
        elif self.direction == 1:
            screen.blit(car_right, (self.x,self.y))


def player():
    screen.blit(person, (player_x,player_y))

def check_collisions():
    global game_state, state_index, checkpoint, reached_star
    player_rect = pygame.Rect(player_x, player_y, 32,32)
    star_rect = pygame.Rect(304,50,32,32)
    for car in cars[:]:
        if player_rect.colliderect(car.rect):
            state_index = 5     #game_over screen

    if player_rect.colliderect(star_rect):
        if not reached_star:
            reached_star = True
            state_index += 1        #next index in game_state
            checkpoint += 1


def Menu():
    menu_name_text = menu_font.render("Cross the road", True, (0,0,0))
    screen.blit(menu_name_text,(width // 2 - menu_name_text.get_width() // 2, height // 2 - 200))

    menu_play_text = menu_play_font.render("Press space to begin", True, (0,0,0))
    screen.blit(menu_play_text, (width // 2 - menu_play_text.get_width() // 2, height // 2 - 100))

    control_text = font_disclaimer.render("W,A,S,D to move, reach star to win", True, (0,0,0))
    screen.blit(control_text, (width // 2 - control_text.get_width() // 2, height // 2 + 120))

def level_1():
    global reached_star
    reached_star = False #used for debouncing the incrementation of state_index variable
    level_1_text = level_font.render("Level 1", True, (0,0,0))
    screen.blit(level_1_text,(width // 2 - level_1_text.get_width() // 2, 25))

    screen.blit(endpoint, (304, 50))        #640//2 - 16 = 304

def level_2():
    global reached_star, frame_count
    reached_star = False
    level_2_text = level_font.render("Level 2", True, (0, 0, 0))
    screen.blit(level_2_text, (width // 2 - level_2_text.get_width() // 2, 25))

    screen.blit(endpoint, (304, 50))  # 640//2 - 16 = 304

def level_3():
    global reached_star, frame_count
    reached_star = False
    level_3_text = level_font.render("Level 3", True, (0, 0, 0))
    screen.blit(level_3_text, (width // 2 - level_3_text.get_width() // 2, 25))

    screen.blit(endpoint, (304, 50))  # 640//2 - 16 = 304

def level_4():
    global reached_star, frame_count
    reached_star = False
    level_4_text = level_font.render("Level 4", True, (0, 0, 0))
    screen.blit(level_4_text, (width // 2 - level_4_text.get_width() // 2, 25))

    screen.blit(endpoint, (304, 50))  # 640//2 - 16 = 304
def game_over():
    screen.fill((0,0,0))
    game_over_text = menu_font.render("Game Over", True, (255,0,0))
    screen.blit(game_over_text, (width //2 - game_over_text.get_width()//2, 100))

    respawn_note = menu_play_font.render("Press R to respawn from checkpoint", True, (255,255,255))
    screen.blit(respawn_note, (width//2 - respawn_note.get_width()//2, 180))


cars = []


running = True
while running:
    events = pygame.event.get()
    clock.tick(1500)      #capped fps = 1500, roughly 1500 frames/loops per second



    for event in events:        #Master quit command (valid from any window)
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    for event in events:        #main player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_y_change = -player_speed
                print('w')

            elif event.key == pygame.K_s:
                player_y_change = player_speed

            elif event.key == pygame.K_a:
                player_x_change = -player_speed

            elif event.key == pygame.K_d:
                player_x_change = player_speed
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                player_x_change = 0
            elif event.key in (pygame.K_w, pygame.K_s):
                player_y_change = 0
    #screen.fill((0,0,0))

    if state_index == 0:        #menu
        screen.blit(background_level_1, (0, 0))
        Menu()
        if previous_state != state_index:
            cars = [Car(640, 306, -1)]  # left moving car suitable for loading screen
        for event in events:  # Master quit command (valid from any window)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state_index += 1
                    checkpoint += 1



    elif state_index == 1:          #level 1
        screen.blit(background_level_1, (0, 0))
        if previous_state != state_index:
            cars = [Car(640, 306, -1)]  # left moving car suitable for loading screen

        #screen.blit(background_level_1, (0, 0))
        level_1()
        player()


    elif state_index == 2:

        if previous_state != state_index:               #At first instance of level 2, previous state != state_index, ensuring position of player reset only once
            player_x = width // 2  # Reset X position
            player_y = 600


            cars = [Car(0, 439, 1), Car(640,368, -1),Car(640,315,-1), Car(0,265, 1), Car(0,215,1), Car(0, 162,1)]
            frame_count = 0     #ensure it is at 0

        screen.blit(background_level_2, (0, 0))
        level_2()
        player()
        frame_count += 1
        if frame_count == 1500:     #allows for more cars to be spawned in per row at specific times other than start...
            cars.append(Car(0, 439, 1))


    elif state_index == 3:
        if previous_state != state_index:               #At first instance of level 2, previous state != state_index, ensuring position of player reset only once
            player_x = width // 2  # Reset X position
            player_y = 600
            cars = [Car(0, 439, 1), Car(640,368, -1),Car(640,315,-1), Car(0,265, 1), Car(0,215,1), Car(0, 162,1)]
            frame_count = 0     #ensure it is at 0

        screen.blit(background_level_2, (0, 0))
        level_3()
        player()
        frame_count += 1

        if frame_count == 1500:  # allows for more cars to be spawned in per row at specific times other than start...
            cars.append(Car(0, 439, 1))
            cars.append(Car(640,368,-1))

        elif frame_count == 2000:
            cars.append(Car(640,315,-1))
            cars.append(Car(0,265,1))

        elif frame_count == 2500:
            cars.append(Car(0,215,1))
            cars.append(Car(0,162,1))


    elif state_index == 4:  # game_over_screen

        if previous_state != state_index:               #At first instance of level 2, previous state != state_index, ensuring position of player reset only once
            player_x = width // 2  # Reset X position
            player_y = 600
            cars = [Car(640, 439, -1), Car(640,368, -1),Car(640,315,-1), Car(0,265, 1), Car(0,215,1), Car(640, 162,-1)]
            frame_count = 0     #ensure it is at 0

        screen.blit(background_level_2, (0, 0))
        level_4()
        player()
        frame_count += 1

        if frame_count == 1500:  # allows for more cars to be spawned in per row at specific times other than start...
            cars.append(Car(640, 439, -1))
            cars.append(Car(640,368,-1))

        elif frame_count == 2000:
            cars.append(Car(640,315,-1))
            cars.append(Car(0,265,1))
            cars.append(Car(0, 215, 1))
            cars.append(Car(0, 162, -1))

        elif frame_count == 2500:
            cars.append(Car(0,215,1))
            cars.append(Car(0,162,-1))
            cars.append(Car(640, 439, -1))
            cars.append(Car(640, 368, -1))
            cars.append(Car(640, 315, -1))
            cars.append(Car(0, 265, 1))

        elif frame_count == 3000:
            cars.append(Car(0, 215, 1))
            cars.append(Car(0, 162, -1))
            cars.append(Car(640, 439, -1))
            cars.append(Car(640, 368, -1))
            cars.append(Car(640, 315, -1))
            cars.append(Car(0, 265, 1))


        #player_x_change, player_y_change = player_movement(events)
    for car in cars[:]:
        car.update()
        car.draw(screen)

    previous_state = state_index    #update for next frame

    if state_index == 5:  # game_over_screen

        game_over()
        cars = []  # empty the list
        previous_state = None

        for event in events:  # main player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state_index = checkpoint
                    player_x = width // 2
                    player_y = 600

    #movement of player
    player_x += player_x_change
    player_y += player_y_change

    if player_x >= 640 - 32:
        player_x = 640 - 32

    elif player_x <= 0:
        player_x = 0

    if player_y >= 640 - 32:
        player_y = 640 - 32

    elif player_y <= 0:
        player_y = 0

    check_collisions()
    pygame.display.update()
