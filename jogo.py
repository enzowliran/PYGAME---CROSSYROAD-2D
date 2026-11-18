# ============================================
# BLOCO 1 - Janela e configurações
# ============================================

import pygame

# Liga o pygame (sempre a primeira coisa)
pygame.init()

# Tamanho da janela, em pixels
LARGURA = 600
ALTURA = 600

# Cria a janela e coloca um título nela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Segura Aí!")

# Relógio que controla a velocidade do jogo
relogio = pygame.time.Clock()

# Cores no formato (Vermelho, Verde, Azul), de 0 a 255
VERDE = (100, 200, 100)
AZUL = (50, 100, 255)

# ============================================
# BLOCO 2 - Personagem
# ============================================

# Tamanho de cada "casa" do chão: o personagem anda de casa em casa
CASA = 50

# O personagem é um dicionário com a posição dele
personagem = {"x": 250, "y": 550}


def mover_personagem(personagem, tecla):
    """Anda uma casa na direção da seta apertada, sem sair da tela."""
    if tecla == pygame.K_UP and personagem["y"] > 0:
        personagem["y"] = personagem["y"] - CASA
    if tecla == pygame.K_DOWN and personagem["y"] < ALTURA - CASA:
        personagem["y"] = personagem["y"] + CASA
    if tecla == pygame.K_LEFT and personagem["x"] > 0:
        personagem["x"] = personagem["x"] - CASA
    if tecla == pygame.K_RIGHT and personagem["x"] < LARGURA - CASA:
        personagem["x"] = personagem["x"] + CASA


def desenhar_personagem(tela, personagem):
    """Desenha o personagem como um quadrado azul."""
    pygame.draw.rect(tela, AZUL, (personagem["x"], personagem["y"], CASA, CASA))


# ============================================
# LOOP PRINCIPAL
# ============================================

rodando = True
while rodando:

    # 1) Ler o que o jogador fez
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            mover_personagem(personagem, evento.key)

    # 2) Desenhar
    tela.fill(VERDE)
    desenhar_personagem(tela, personagem)

    # 3) Mostrar na tela o que foi desenhado
    pygame.display.update()

    # 4) Esperar para rodar a 60 quadros por segundo
    relogio.tick(60)

# Saiu do loop: desliga o pygame
pygame.quit()
