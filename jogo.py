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
LARANJA = (255, 150, 50)
VERMELHO = (220, 50, 50)
PRETO = (0, 0, 0)

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
# BLOCO 3 - Obstáculos
# ============================================

def criar_obstaculo(x, y, velocidade, largura, cor):
    """Cria um obstáculo (um dicionário) com posição, velocidade, tamanho e cor."""
    return {"x": x, "y": y, "velocidade": velocidade, "largura": largura, "cor": cor}


# Lista com todos os obstáculos do corredor.
# Aluno: lento e pequeno (laranja). Carrinho de limpeza: rápido e comprido (vermelho).
# Velocidade positiva anda para a direita; negativa anda para a esquerda.
obstaculos = [
    criar_obstaculo(0, 450, 2, 50, LARANJA),
    criar_obstaculo(300, 450, 2, 50, LARANJA),
    criar_obstaculo(100, 350, -5, 100, VERMELHO),
    criar_obstaculo(400, 250, 3, 50, LARANJA),
    criar_obstaculo(200, 150, -6, 100, VERMELHO),
]


def mover_obstaculos(obstaculos):
    """Anda com cada obstáculo. Quem sai de um lado da tela volta pelo outro."""
    for obstaculo in obstaculos:
        obstaculo["x"] = obstaculo["x"] + obstaculo["velocidade"]
        if obstaculo["x"] > LARGURA:
            obstaculo["x"] = -obstaculo["largura"]
        if obstaculo["x"] < -obstaculo["largura"]:
            obstaculo["x"] = LARGURA


def desenhar_obstaculos(tela, obstaculos):
    """Desenha cada obstáculo como um retângulo da sua cor."""
    for obstaculo in obstaculos:
        pygame.draw.rect(tela, obstaculo["cor"], (obstaculo["x"], obstaculo["y"], obstaculo["largura"], CASA))


# ============================================
# BLOCO 4 - Colisão
# ============================================

def bateu(personagem, obstaculos):
    """Devolve True se o personagem está encostando em algum obstáculo."""
    retangulo_personagem = pygame.Rect(personagem["x"], personagem["y"], CASA, CASA)
    for obstaculo in obstaculos:
        retangulo_obstaculo = pygame.Rect(obstaculo["x"], obstaculo["y"], obstaculo["largura"], CASA)
        if retangulo_personagem.colliderect(retangulo_obstaculo):
            return True
    return False


def voltar_ao_comeco(personagem):
    """Coloca o personagem de volta na posição inicial, lá embaixo."""
    personagem["x"] = 250
    personagem["y"] = 550


# ============================================
# BLOCO 5 - Pontuação
# ============================================

# Fonte para escrever na tela (None = fonte padrão do pygame, tamanho 40)
fonte = pygame.font.Font(None, 40)

# O placar guarda os pontos e a faixa mais alta que o personagem já alcançou
placar = {"pontos": 0, "menor_y": 550}


def atualizar_pontos(placar, personagem):
    """Ganha 1 ponto cada vez que o personagem chega numa faixa nova, mais para cima."""
    if personagem["y"] < placar["menor_y"]:
        placar["menor_y"] = personagem["y"]
        placar["pontos"] = placar["pontos"] + 1


def zerar_pontos(placar):
    """Volta o placar para o começo."""
    placar["pontos"] = 0
    placar["menor_y"] = 550


def desenhar_pontos(tela, placar):
    """Escreve os pontos no canto de cima da tela."""
    texto = fonte.render("Pontos: " + str(placar["pontos"]), True, PRETO)
    tela.blit(texto, (10, 10))


# ============================================
# BLOCO 6 - Barra de aperto
# ============================================

APERTO_MAXIMO = 100
VELOCIDADE_APERTO = 0.1  # quanto enche por quadro: 100 / 0.1 = 1000 quadros, uns 17 segundos

# A barra também é um dicionário, igual ao personagem e ao placar
barra = {"aperto": 0}


def encher_barra(barra):
    """Enche um pouquinho a barra (chamada todo quadro)."""
    barra["aperto"] = barra["aperto"] + VELOCIDADE_APERTO


def barra_cheia(barra):
    """Devolve True se a barra chegou no máximo."""
    return barra["aperto"] >= APERTO_MAXIMO


def esvaziar_barra(barra):
    """Volta a barra para zero."""
    barra["aperto"] = 0


def desenhar_barra(tela, barra):
    """Desenha a barra no canto de cima, à direita: vermelho por dentro, contorno preto."""
    largura_cheia = int(barra["aperto"] * 2)  # 100 de aperto = 200 pixels
    pygame.draw.rect(tela, VERMELHO, (390, 10, largura_cheia, 20))
    pygame.draw.rect(tela, PRETO, (390, 10, 200, 20), 2)


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

    # 2) Atualizar: os obstáculos andam sozinhos
    mover_obstaculos(obstaculos)

    # Se bateu em alguém, volta para o começo e perde os pontos
    if bateu(personagem, obstaculos):
        voltar_ao_comeco(personagem)
        zerar_pontos(placar)

    # Chegou numa faixa nova? Ganha ponto
    atualizar_pontos(placar, personagem)

    # A barra de aperto enche com o tempo. Se encher, recomeça tudo
    encher_barra(barra)
    if barra_cheia(barra):
        voltar_ao_comeco(personagem)
        zerar_pontos(placar)
        esvaziar_barra(barra)

    # 3) Desenhar
    tela.fill(VERDE)
    desenhar_obstaculos(tela, obstaculos)
    desenhar_personagem(tela, personagem)
    desenhar_pontos(tela, placar)
    desenhar_barra(tela, barra)

    # 4) Mostrar na tela o que foi desenhado
    pygame.display.update()

    # 5) Esperar para rodar a 60 quadros por segundo
    relogio.tick(60)

# Saiu do loop: desliga o pygame
pygame.quit()
