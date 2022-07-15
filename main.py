import pygame
from pygame import mixer
# importing Fighter class from fighter module
from fighter import Fighter

# related to loading and playing different sounds and music
mixer.init()
# related to running and working of everying thing
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("tournament fight")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game variables

# countdown before the start of game
intro_count = 3

# last_count_update stores number of millisecond
# pygame.time.get_ticks() returns number of millisecond since
# start of programme
last_count_update = pygame.time.get_ticks()

# player scores. [P1, P2]
score = [0, 0]

# When either of player gets killed
# round_over become True
round_over = False

# time gap between the start of
# fresh round and last round
ROUND_OVER_COOLDOWN = 2000

#define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load music and sounds

# loads, set volume and play background music
# plays complete music in loop
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)

# loads and sets volume of sound of sword
# plays when warrior swings sword
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)

# loads and sets volume of sound of music
# plays when wizard swings wand
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

#load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# load spritesheets
# png which contains multiple image of warrior in different
# actions
# how it is used?
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# load vicory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# define number of steps in each animation
# used in function load_images
# number of images in each row in spritesheet
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# define font
# probably loads font style which gets used for
# displaying count and score
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

# general purpose function for drawing text 
# on screen
def draw_text(text, font, text_col, x, y):
  # produces image of font
  img = font.render(text, True, text_col)
  # draws font on screen
  screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
  # scales background image to the width and height of screen
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  # draws that background image
  screen.blit(scaled_bg, (0, 0))

# general purpose function for drawing health bar
# of warrior and wizard. Probably gets called each
# time when one of them got hit by other
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, RED, (x, y, 400, 30))
  pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


# creating two fighter objects by calling Fighter class
# Arguments: player number, intial x co-ordinates, initial y co-ordinates, ???, size, scale and offset, list of png images, number of images in each row in spritesheet, sound of sword
fighter_1 = Fighter(1 , 200 , 400 , False , WARRIOR_DATA , warrior_sheet , WARRIOR_ANIMATION_STEPS , sword_fx )
fighter_2 = Fighter(2, 700, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# game loop
run = True
while run:

  # probably runs loop 50 time every second
  clock.tick(FPS)

  # draw background
  draw_bg()

  # show player stats
  draw_health_bar(fighter_1.health, 20, 20)
  draw_health_bar(fighter_2.health, 580, 20)

  # draws player score
  # score represents number of kills
  draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
  draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

  # update countdown
  if intro_count <= 0: # countdown finished
    # move fighters 
    # ???
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
  else:
    # this else block is understood
    #display count timer
    draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    #update count timer
    # 1000 millisecond == 1 second
    if (pygame.time.get_ticks() - last_count_update) >= 1000:
      intro_count -= 1
      last_count_update = pygame.time.get_ticks()

  # update fighters
  # ???
  fighter_1.update()
  fighter_2.update()

  # draw fighters after updating
  # ???
  fighter_1.draw(screen)
  fighter_2.draw(screen)
  
  '''
        Code below this is understood
  ''' 

  # check for player defeat
  # understood
  if round_over == False:
    if fighter_1.alive == False:
      score[1] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
    elif fighter_2.alive == False:
      score[0] += 1
      round_over = True
      round_over_time = pygame.time.get_ticks()
  else:
    # display victory image
    screen.blit(victory_img, (360, 150))
    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
      round_over = False
      intro_count = 3
      fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
      fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

  # terminates game loop when player
  # clicks close button
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  # game closes when score of either of player
  # becomes 3
  for x in score:
    if score[0] == 3 or score[1] == 3:
      run = False


  #update display
  pygame.display.update()




#exit pygame
pygame.quit()