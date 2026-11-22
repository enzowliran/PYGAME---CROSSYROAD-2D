# ============================================
# BLOCO 1 - Janela e configurações
# ============================================

import pygame
import random

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
# BLOCO 7 - Cenário
# ============================================

CINZA_CLARO = (200, 200, 200)
CINZA_ESCURO = (150, 150, 150)
AZUL_CLARO = (170, 210, 240)  # azulejo do banheiro
MARROM = (140, 90, 40)        # porta
BRANCO = (255, 255, 255)

# Fonte menor, só para escrever "WC" na porta
fonte_pequena = pygame.font.Font(None, 24)


def desenhar_cenario(tela):
    """Desenha o chão do corredor, a largada lá embaixo e o banheiro lá em cima."""
    # Chão: 12 faixas (600 / 50), alternando cinza claro e escuro
    for linha in range(12):
        y = linha * CASA
        if linha % 2 == 0:
            cor = CINZA_CLARO
        else:
            cor = CINZA_ESCURO
        pygame.draw.rect(tela, cor, (0, y, LARGURA, CASA))

    # Largada: a última faixa, lá embaixo, fica verde
    pygame.draw.rect(tela, VERDE, (0, ALTURA - CASA, LARGURA, CASA))

    # Banheiro: a primeira faixa, lá em cima, com azulejo azul
    pygame.draw.rect(tela, AZUL_CLARO, (0, 0, LARGURA, CASA))

    # Porta do banheiro, no meio da faixa de cima
    pygame.draw.rect(tela, MARROM, (250, 0, CASA, CASA))
    texto = fonte_pequena.render("WC", True, BRANCO)
    tela.blit(texto, (262, 17))


# ============================================
# BLOCO 8 - Telas (início, jogo e fim)
# ============================================

# Em qual tela o jogo está: "inicio", "jogo" ou "fim"
estado = "inicio"

# Frases de game over (uma é sorteada quando a barra enche)
FRASES_FIM = [
    "Não deu tempo...",
    "Ih, molhou tudo!",
    "Faltou só um pouquinho!",
    "Alguém chama a limpeza!",
]

# Frase que aparece na tela de fim
frase_fim = ""


def reiniciar_jogo(personagem, placar, barra):
    """Deixa tudo pronto para uma partida nova."""
    voltar_ao_comeco(personagem)
    zerar_pontos(placar)
    esvaziar_barra(barra)


def chegou_no_banheiro(personagem):
    """Devolve True se o personagem chegou na faixa de cima."""
    return personagem["y"] == 0


def desenhar_tela_inicio(tela):
    """Mostra o nome do jogo e como começar."""
    tela.fill(AZUL_CLARO)
    titulo = fonte.render("Segura Aí!", True, PRETO)
    instrucao = fonte_pequena.render("Aperte ESPAÇO para começar", True, PRETO)
    tela.blit(titulo, (220, 250))
    tela.blit(instrucao, (180, 320))


def desenhar_tela_fim(tela, placar, frase):
    """Mostra a frase do fim, os pontos e como jogar de novo."""
    tela.fill(AZUL_CLARO)
    texto_frase = fonte.render(frase, True, PRETO)
    texto_pontos = fonte.render("Pontos: " + str(placar["pontos"]), True, PRETO)
    instrucao = fonte_pequena.render("Aperte ESPAÇO para jogar de novo", True, PRETO)
    tela.blit(texto_frase, (100, 200))
    tela.blit(texto_pontos, (100, 260))
    tela.blit(instrucao, (100, 340))


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
            if estado == "jogo":
                mover_personagem(personagem, evento.key)
            elif evento.key == pygame.K_SPACE:
                reiniciar_jogo(personagem, placar, barra)
                estado = "jogo"

    # 2) Atualizar: só quando está jogando
    if estado == "jogo":
        mover_obstaculos(obstaculos)

        # Se bateu em alguém, volta para o começo e perde os pontos
        if bateu(personagem, obstaculos):
            voltar_ao_comeco(personagem)
            zerar_pontos(placar)

        # Chegou numa faixa nova? Ganha ponto
        atualizar_pontos(placar, personagem)

        # A barra enche com o tempo. Se encher, game over com frase sorteada
        encher_barra(barra)
        if barra_cheia(barra):
            estado = "fim"
            frase_fim = random.choice(FRASES_FIM)

        # Chegou ao banheiro: venceu!
        if chegou_no_banheiro(personagem):
            estado = "fim"
            frase_fim = "Ufa! Chegou a tempo!"

    # 3) Desenhar a tela certa
    if estado == "inicio":
        desenhar_tela_inicio(tela)
    elif estado == "jogo":
        desenhar_cenario(tela)
        desenhar_obstaculos(tela, obstaculos)
        desenhar_personagem(tela, personagem)
        desenhar_pontos(tela, placar)
        desenhar_barra(tela, barra)
    else:
        desenhar_tela_fim(tela, placar, frase_fim)

    # 4) Mostrar na tela o que foi desenhado
    pygame.display.update()

    # 5) Esperar para rodar a 60 quadros por segundo
    relogio.tick(60)

# Saiu do loop: desliga o pygame
pygame.quit()
