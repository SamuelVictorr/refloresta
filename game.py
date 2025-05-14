import pygame
import time
  
#Variáveis básicas: 
BACKGROUND_COLOR = (50, 50, 180)
ALTURA = 360
LARGURA = 640
SPEED = 2
GRAVIDADE = 0.5
TELA = pygame.display.set_mode((LARGURA, ALTURA),flags=pygame.SCALED)
cor_lixo = [(255, 0, 0), (255, 0, 0)]

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

# esquerda, topo, altura, largura
chao = pygame.Rect(10,340,500,5)
bloco = pygame.Rect(40,300,50,50)
bloco2 = pygame.Rect(200,150,50,50)
bloco3 = pygame.Rect(350,150,50,50) 
bloco4 = pygame.Rect(10, 100, 100, 20)
lixo1 = pygame.Rect(230, 330, 10, 10) #lixo bloco
lixo2 = pygame.Rect(250, 330, 10, 10)
objetos = [chao,bloco,bloco2,bloco3,bloco4]
lixos = [lixo1, lixo2]  #colisão de lixo

# music loop
pygame.mixer.init()        
pygame.mixer.music.load("somteste.mp3") #Test music
pygame.mixer.music.play(-1) #Music in loop

#Atualizar o movimento
colisions =[False,False,False,False] #Top bottom left right
def move(dx, dy):   
    global colisions
    for ojeto in objetos:
        playerpos[1] += dy
        player = pygame.Rect((playerpos[0], playerpos[1], playersize[0], playersize[1]))
        if player.collidelist(objetos) != -1:
            if dy > 0:
                colisions[0] = True
                player.bottom = objetos[player.collidelist(objetos)].top + 1
                playerpos[1] = player.top
            if dy < 0:
                colisions[1] = True
                player.top = objetos[player.collidelist(objetos)].bottom - 1
                playerpos[1] = player.top  

        for ob in objetos:
            if player.bottom == ob.top:
                print('topo')
            else:
                print('não topo')
            
        playerpos[0] += dx
        player = pygame.Rect((playerpos[0], playerpos[1], playersize[0], playersize[1]))
        for colision in list(player.collidelistall(objetos)):
            if player.collidelist(objetos) != -1 and player.bottom != objetos[colision].top + 1:
                if dx > 0:
                    colisions[2] = True
                    player.right = objetos[colision].left
                    playerpos[0] = player.left
                if dx < 0:
                    colisions[3] = True
                    player.left = objetos[colision].right
                    playerpos[0] = player.left
        if dx == 0:
            colisions[2],colisions[3] = False,False
                        
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
    if player.collidelist(objetos) != -1:
        if keys[pygame.K_SPACE]:
            y_speed = -8
        else:
            y_speed = 0
            
    if player.collidelist(objetos) == -1:
        y_speed += GRAVIDADE
    
    move(x_speed,y_speed)
    #Player
    pygame.draw.rect(TELA,(255,255,0),(playerpos[0], playerpos[1], playersize[0], playersize[1]))
    
    #chão
    for i in objetos:
        pygame.draw.rect(TELA,(255,255,255),i)

    #colisão do lixo
    collide_lixo = player.collidelistall(lixos)
    for i in range(len(lixos)):
        if i in collide_lixo:
            cor_lixo[i] = (0, 255, 0)
        else:
            cor_lixo[i] = (255, 0, 0)

    for i in range(len(lixos)):
        pygame.draw.rect(TELA, cor_lixo[i], lixos[i])
    
    pygame.display.flip() 
    
    
    relogio.tick(60)