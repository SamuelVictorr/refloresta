import pygame
import sys

pygame.init()

#configurações da tela
BACKGROUND_COLOR = (50, 50, 180)
ALTURA = 360
LARGURA = 640
TELA = pygame.display.set_mode((LARGURA, ALTURA), flags=pygame.SCALED)
pygame.display.set_caption('Refloresta')

#cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)
VERDE_ESCURO = (0, 150, 0)
VERMELHO = (200, 0, 0)
VERMELHO_ESCURO = (150, 0, 0)
cor_lixo = [(200, 100, 50), (VERDE)]

#fontes
fonte_grande = pygame.font.Font(None, 60)
fonte_pequena = pygame.font.Font(None, 36)

class Botao:
    def __init__(self, x, y, largura, altura, texto, cor, cor_hover): 
        #estrutura parecida com o menu do dafluffy(alterar posteriormente para o CD codes, caso necessário)
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.cor_hover = cor_hover
        self.cor_atual = cor
        
    def desenhar(self, superficie):
        pygame.draw.rect(superficie, self.cor_atual, self.rect) #retângulo normal
        pygame.draw.rect(superficie, PRETO, self.rect, 2)  # borda
        
        texto_surf = fonte_pequena.render(self.texto, True, PRETO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        superficie.blit(texto_surf, texto_rect)
        
    def verificar_clique(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False
    
    def verificar_hover(self, pos): #verifica se o mouse está em cima do botão
        if self.rect.collidepoint(pos):
            self.cor_atual = self.cor_hover
        else:
            self.cor_atual = self.cor

def tela_inicial():
    botao_iniciar = Botao(LARGURA//2 - 100, ALTURA//2, 200, 50, "Iniciar Jogo", VERDE, VERDE_ESCURO)
    botao_sair = Botao(LARGURA//2 - 100, ALTURA//2 + 70, 200, 50, "Sair", VERMELHO, VERMELHO_ESCURO)
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.verificar_clique(evento.pos):
                    return  #sai da tela inicial e inicia o jogo
                if botao_sair.verificar_clique(evento.pos):
                    pygame.quit()
                    sys.exit()
        
        #atualiza hover dos botões
        mouse_pos = pygame.mouse.get_pos()
        botao_iniciar.verificar_hover(mouse_pos)
        botao_sair.verificar_hover(mouse_pos)
        
        #desenha a tela
        TELA.fill(BACKGROUND_COLOR)
        
        #título
        titulo = fonte_grande.render("REFLORESTA", True, BRANCO)
        titulo_rect = titulo.get_rect(center=(LARGURA//2, ALTURA//3))
        TELA.blit(titulo, titulo_rect)
        
        #botões
        botao_iniciar.desenhar(TELA)
        botao_sair.desenhar(TELA)
        
        pygame.display.flip()
        pygame.time.Clock().tick(60)

#chama a tela inicial 
tela_inicial()

SPEED = 2
GRAVIDADE = 0.5
x_speed = 0
y_speed = 0
dx = 0

relogio = pygame.time.Clock()

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
running = True
while running: 
    TELA.fill(BACKGROUND_COLOR) #Clear the screen
    
    for event in pygame.event.get():       
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