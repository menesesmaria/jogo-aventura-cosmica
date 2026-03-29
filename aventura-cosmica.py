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
fonte_grande = pygame.font.SysFont("Arial", 50)
fonte_media = pygame.font.SysFont("Arial", 25)

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)

# Estados
estado = "menu"

# Dificuldade
dificuldade = "medio"

# Player
player_x = 400
player_y = 550
vel = 5

balas = []
balas_inimigos = []

# Estrelas
estrelas = [[random.randint(0, LARGURA), random.randint(0, ALTURA)] for _ in range(80)]

# Configurações por dificuldade
def configurar_dificuldade():
    if dificuldade == "facil":
        return 5, 0.5, 4
    elif dificuldade == "medio":
        return 7, 1, 5
    else:  # dificil
        return 9, 2, 6

# Criar inimigos
def criar_inimigos(qtd):
    lista = []
    for i in range(qtd):
        lista.append(pygame.Rect(80 + i * 100, 100, 40, 40))
    return lista

vel_bala_inimigo, chance_tiro, qtd_inimigos = configurar_dificuldade()
inimigos = criar_inimigos(qtd_inimigos)

score = 0

# Botões
botao_facil = pygame.Rect(300, 250, 200, 40)
botao_medio = pygame.Rect(300, 300, 200, 40)
botao_dificil = pygame.Rect(300, 350, 200, 40)
botao_sair = pygame.Rect(300, 400, 200, 40)
botao_ok = pygame.Rect(300, 350, 200, 50)

# Reset
def resetar_jogo():
    global balas, balas_inimigos, inimigos, score, player_x
    balas = []
    balas_inimigos = []
    inimigos = criar_inimigos(qtd_inimigos)
    score = 0
    player_x = 400

# Player
def desenhar_player(x, y):
    pontos = [(x, y), (x - 25, y + 40), (x + 25, y + 40)]
    pygame.draw.polygon(tela, VERDE, pontos)

# Fundo
def desenhar_fundo():
    tela.fill(PRETO)
    for estrela in estrelas:
        pygame.draw.circle(tela, BRANCO, estrela, 2)

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

                if botao_facil.collidepoint(evento.pos):
                    dificuldade = "facil"
                    vel_bala_inimigo, chance_tiro, qtd_inimigos = configurar_dificuldade()
                    inimigos = criar_inimigos(qtd_inimigos)
                    estado = "jogo"

                if botao_medio.collidepoint(evento.pos):
                    dificuldade = "medio"
                    vel_bala_inimigo, chance_tiro, qtd_inimigos = configurar_dificuldade()
                    inimigos = criar_inimigos(qtd_inimigos)
                    estado = "jogo"

                if botao_dificil.collidepoint(evento.pos):
                    dificuldade = "dificil"
                    vel_bala_inimigo, chance_tiro, qtd_inimigos = configurar_dificuldade()
                    inimigos = criar_inimigos(qtd_inimigos)
                    estado = "jogo"

                if botao_sair.collidepoint(evento.pos):
                    rodando = False

        # JOGO
        elif estado == "jogo":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    balas.append([player_x, player_y])

        # GAME OVER
        elif estado == "game_over":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_ok.collidepoint(evento.pos):
                    resetar_jogo()
                    estado = "menu"

    # MENU
    if estado == "menu":
        tela.fill(PRETO)

        tela.blit(fonte_grande.render("Escolha a Dificuldade", True, BRANCO), (180, 150))

        pygame.draw.rect(tela, BRANCO, botao_facil, 2)
        pygame.draw.rect(tela, BRANCO, botao_medio, 2)
        pygame.draw.rect(tela, BRANCO, botao_dificil, 2)
        pygame.draw.rect(tela, BRANCO, botao_sair, 2)

        tela.blit(fonte_media.render("Fácil", True, BRANCO), (360, 260))
        tela.blit(fonte_media.render("Médio", True, BRANCO), (355, 310))
        tela.blit(fonte_media.render("Difícil", True, BRANCO), (350, 360))
        tela.blit(fonte_media.render("Sair", True, BRANCO), (360, 410))

    # JOGO
    elif estado == "jogo":

        desenhar_fundo()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and player_x > 0:
            player_x -= vel
        if teclas[pygame.K_RIGHT] and player_x < LARGURA:
            player_x += vel

        # Balas player
        for bala in balas[:]:
            bala[1] -= 7
            if bala[1] < 0:
                balas.remove(bala)

        # Inimigos atiram
        for inimigo in inimigos:
            if random.random() < 0.01 * chance_tiro:
                balas_inimigos.append([inimigo.centerx, inimigo.bottom])

        # Balas inimigas
        for bala in balas_inimigos[:]:
            bala[1] += vel_bala_inimigo
            if bala[1] > ALTURA:
                balas_inimigos.remove(bala)

        # Colisão player
        player_rect = pygame.Rect(player_x - 25, player_y, 50, 40)

        for bala in balas_inimigos:
            if player_rect.collidepoint(bala[0], bala[1]):
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
            inimigos = criar_inimigos(qtd_inimigos)

        # Desenho
        desenhar_player(player_x, player_y)

        for inimigo in inimigos:
            pygame.draw.rect(tela, VERMELHO, inimigo)

        for bala in balas:
            pygame.draw.circle(tela, BRANCO, (bala[0], bala[1]), 5)

        for bala in balas_inimigos:
            pygame.draw.circle(tela, AMARELO, (bala[0], bala[1]), 5)

        tela.blit(fonte_media.render(f"Pontos: {score}", True, BRANCO), (10, 10))

    # GAME OVER
    elif estado == "game_over":
        desenhar_fundo()

        tela.blit(fonte_grande.render("GAME OVER", True, VERMELHO), (220, 200))

        pygame.draw.rect(tela, BRANCO, botao_ok, 2)
        tela.blit(fonte_media.render("OK", True, BRANCO), (370, 365))

    pygame.display.update()

pygame.quit()