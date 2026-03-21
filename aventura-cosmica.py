import pygame
import random

pygame.init()

# Tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo Geométrico")

clock = pygame.time.Clock()

# Fontes
fonte_grande = pygame.font.SysFont("Arial", 60)
fonte_media = pygame.font.SysFont("Arial", 30)

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)

# Estados
estado = "menu"

# Player
player = pygame.Rect(350, 550, 60, 20)
vel = 5

balas = []
balas_inimigos = []

# Criar inimigos
def criar_inimigos():
    lista = []
    for i in range(5):
        lista.append(pygame.Rect(100 + i * 120, 100, 40, 40))
    return lista

inimigos = criar_inimigos()
score = 0

# Botões
botao_comecar = pygame.Rect(300, 250, 200, 50)
botao_sair = pygame.Rect(300, 320, 200, 50)

# Desenhar triângulo
def desenhar_triangulo(x, y):
    pontos = [(x, y), (x - 5, y + 10), (x + 5, y + 10)]
    pygame.draw.polygon(tela, BRANCO, pontos)

# Loop
rodando = True
while rodando:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # MENU
        if estado == "menu":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_comecar.collidepoint(evento.pos):
                    estado = "jogo"
                if botao_sair.collidepoint(evento.pos):
                    rodando = False

        # JOGO
        elif estado == "jogo":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    balas.append([player.centerx, player.y])

    # ===== MENU =====
    if estado == "menu":
        tela.fill(PRETO)

        titulo = fonte_grande.render("Bem-vindo", True, BRANCO)
        tela.blit(titulo, (260, 150))

        pygame.draw.rect(tela, BRANCO, botao_comecar, 2)
        pygame.draw.rect(tela, BRANCO, botao_sair, 2)

        txt_comecar = fonte_media.render("Começar", True, BRANCO)
        txt_sair = fonte_media.render("Sair", True, BRANCO)

        tela.blit(txt_comecar, (330, 260))
        tela.blit(txt_sair, (360, 330))

    # ===== JOGO =====
    elif estado == "jogo":

        # Movimento
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and player.x > 0:
            player.x -= vel
        if teclas[pygame.K_RIGHT] and player.x < LARGURA - player.width:
            player.x += vel

        # Balas player
        for bala in balas[:]:
            bala[1] -= 7
            if bala[1] < 0:
                balas.remove(bala)

        # Inimigos atiram
        for inimigo in inimigos:
            if random.randint(0, 100) < 1:
                balas_inimigos.append([inimigo.centerx, inimigo.bottom])

        # Balas inimigas
        for bala in balas_inimigos[:]:
            bala[1] += 5
            if bala[1] > ALTURA:
                balas_inimigos.remove(bala)

        # Colisão player
        for bala in balas_inimigos:
            if player.collidepoint(bala[0], bala[1]):
                estado = "game_over"

        # Colisão inimigos
        for bala in balas[:]:
            for inimigo in inimigos[:]:
                if inimigo.collidepoint(bala[0], bala[1]):
                    balas.remove(bala)
                    inimigos.remove(inimigo)
                    score += 1
                    break

        # Reset inimigos
        if len(inimigos) == 0:
            inimigos = criar_inimigos()

        # Desenho
        tela.fill(PRETO)

        pygame.draw.rect(tela, VERDE, player)

        for inimigo in inimigos:
            pygame.draw.rect(tela, VERMELHO, inimigo)

        for bala in balas:
            desenhar_triangulo(bala[0], bala[1])

        for bala in balas_inimigos:
            pygame.draw.rect(tela, AMARELO, (bala[0], bala[1], 5, 10))

        texto = fonte_media.render(f"Pontos: {score}", True, BRANCO)
        tela.blit(texto, (10, 10))

    # ===== GAME OVER =====
    elif estado == "game_over":
        tela.fill(PRETO)

        texto = fonte_grande.render("GAME OVER", True, VERMELHO)
        tela.blit(texto, (220, 250))

    pygame.display.update()

pygame.quit()