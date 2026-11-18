# ============================================
# BLOCO 1 - Janela e loop principal
# ============================================

import pygame

# Liga o pygame (sempre a primeira coisa)
pygame.init()

# Tamanho da janela, em pixels
LARGURA = 600
ALTURA = 600

# Cria a janela e coloca um título nela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu Crossy Road")

# Relógio que controla a velocidade do jogo
relogio = pygame.time.Clock()

# Cores no formato (Vermelho, Verde, Azul), de 0 a 255
VERDE = (100, 200, 100)

# Loop principal: roda sem parar até o jogador fechar a janela
rodando = True
while rodando:

    # 1) Ler o que o jogador fez (teclado, mouse, fechar janela...)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # 2) Desenhar
    tela.fill(VERDE)

    # 3) Mostrar na tela o que foi desenhado
    pygame.display.update()

    # 4) Esperar o tempo certo para rodar a 60 quadros por segundo
    relogio.tick(60)

# Saiu do loop: desliga o pygame
pygame.quit()
