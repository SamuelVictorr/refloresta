import pygame
import time
  
#Variáveis básicas: 
BACKGROUND_COLOR = (50, 50, 180)
ALTURA = 360
LARGURA = 640
SPEED = 2
GRAVIDADE = 0.5
TELA = pygame.display.set_mode((LARGURA, ALTURA),flags=pygame.SCALED)
 
x_speed = 0
y_speed = 0
dx=0

relogio = pygame.time.Clock()

fullscreen = True 
# Set the caption of the screen 
pygame.display.set_caption('Refloresta') 


# Variable to keep our game loop running 
running = True
playersize = [20, 20]
playerpos = [0, 0]

chao = pygame.Rect(10,340,500,5)
bloco = pygame.Rect(10,300,50,50)
#Atualizar o movimento
def move(dx, dy):   
    playerpos[1] += dy
    player = pygame.Rect((playerpos[0], playerpos[1], playersize[0], playersize[1]))
    if player.colliderect(chao):
        if dy > 0:
            player.bottom = chao.top + 1
            playerpos[1] = player.top

    playerpos[0] += dx
    player = pygame.Rect((playerpos[0], playerpos[1], playersize[0], playersize[1]))
    if player.colliderect(chao) and player.bottom != chao.top + 1:
        if dx > 0:
            player.right = chao.left
            playerpos[0] = player.left
        if dx < 0:
            player.left = chao.right
            playerpos[0] = player.left
            
# game loop 
while running: 
    TELA.fill(BACKGROUND_COLOR) #Clear the screen
# for loop through the event queue   
    
    for event in pygame.event.get(): 
      
        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            running = False

    #For the user input
    keys = pygame.key.get_pressed()
    
    #Handle key presses
    x_speed = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * SPEED
    
    player = pygame.Rect((playerpos[0], playerpos[1], playersize[0], playersize[1]))
    if player.colliderect(chao):
        print('colidiu')
        if keys[pygame.K_SPACE]:
            y_speed = -10
        else:
            y_speed = 0
            
    if not player.colliderect(chao):
        y_speed += GRAVIDADE
    
    move(x_speed,y_speed)
    #Player
    pygame.draw.rect(TELA,(255,255,0),(playerpos[0], playerpos[1], playersize[0], playersize[1]))
    
    #chão
    pygame.draw.rect(TELA,(255,255,255),chao)
    pygame.draw.rect(TELA,(255,255,255),bloco)
    
    pygame.display.flip() 
    
    relogio.tick(60)