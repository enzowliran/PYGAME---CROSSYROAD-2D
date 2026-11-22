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
VERMELHO = (220, 50, 50)
PRETO = (0, 0, 0)

# ============================================
# BLOCO 10 - Imagens e animações
# (fica aqui em cima porque os blocos 2 e 3 já usam as imagens)
# ============================================

def carregar_imagem(nome):
    """Abre uma imagem .png da pasta imagens (com fundo transparente)."""
    return pygame.image.load("imagens/" + nome).convert_alpha()


# Todas as imagens do jogo, num dicionário. As animações são listas de quadros.
IMAGENS = {
    "parado": carregar_imagem("jogador_parado.png"),
    "andando": [carregar_imagem("jogador_andando1.png"), carregar_imagem("jogador_andando2.png")],
    "batida": [carregar_imagem("jogador_batida1.png"), carregar_imagem("jogador_batida2.png")],
    "alunos": [carregar_imagem("aluno1.png"), carregar_imagem("aluno2.png"), carregar_imagem("aluno3.png")],
    "carrinho": carregar_imagem("carrinho.png"),
}

# Quantos quadros dura cada animação (60 quadros = 1 segundo)
TEMPO_PASSO = 12
TEMPO_BATIDA = 60


def comecar_animacao(personagem, nome, duracao):
    """Liga uma animação ("andando" ou "batida") por um certo número de quadros."""
    personagem["animacao"] = nome
    personagem["tempo"] = duracao


def atualizar_animacao(personagem):
    """Diminui o tempo da animação. Quando o passo acaba, o personagem fica parado."""
    if personagem["tempo"] > 0:
        personagem["tempo"] = personagem["tempo"] - 1
    if personagem["animacao"] == "andando" and personagem["tempo"] == 0:
        personagem["animacao"] = "parado"


def terminou_batida(personagem):
    """Devolve True quando a animação de batida já acabou."""
    return personagem["animacao"] == "batida" and personagem["tempo"] == 0


def imagem_do_personagem(personagem):
    """Escolhe o quadro certo da animação atual."""
    if personagem["animacao"] == "andando":
        quadro = (personagem["tempo"] // 6) % 2  # troca de quadro a cada 6 quadros
        return IMAGENS["andando"][quadro]
    if personagem["animacao"] == "batida":
        quadro = (personagem["tempo"] // 8) % 2  # estrelinhas trocam a cada 8 quadros
        return IMAGENS["batida"][quadro]
    return IMAGENS["parado"]


# ============================================
# BLOCO 2 - Personagem
# ============================================

# Tamanho de cada "casa" do chão: o personagem anda de casa em casa
CASA = 50

# O personagem é um dicionário com a posição e a animação atual
personagem = {"x": 250, "y": 550, "animacao": "parado", "tempo": 0}


def mover_personagem(personagem, tecla):
    """Anda uma casa na direção da seta apertada, sem sair da tela."""
    if personagem["animacao"] == "batida":
        return  # tonto depois da batida: não anda
    x_antes = personagem["x"]
    y_antes = personagem["y"]
    if tecla == pygame.K_UP and personagem["y"] > 0:
        personagem["y"] = personagem["y"] - CASA
    if tecla == pygame.K_DOWN and personagem["y"] < ALTURA - CASA:
        personagem["y"] = personagem["y"] + CASA
    if tecla == pygame.K_LEFT and personagem["x"] > 0:
        personagem["x"] = personagem["x"] - CASA
    if tecla == pygame.K_RIGHT and personagem["x"] < LARGURA - CASA:
        personagem["x"] = personagem["x"] + CASA
    # Se mudou de lugar, faz a animação do passo
    if personagem["x"] != x_antes or personagem["y"] != y_antes:
        comecar_animacao(personagem, "andando", TEMPO_PASSO)


def desenhar_personagem(tela, personagem):
    """Desenha o quadro certo da animação: com pulinho ao andar e tremendo na batida."""
    x = personagem["x"]
    y = personagem["y"]
    if personagem["animacao"] == "andando":
        y = y - min(personagem["tempo"], TEMPO_PASSO - personagem["tempo"])  # sobe e desce
    if personagem["animacao"] == "batida":
        x = x + random.randint(-3, 3)  # tremendo
    tela.blit(imagem_do_personagem(personagem), (x, y))


# ============================================
# BLOCO 3 - Obstáculos
# ============================================

def criar_obstaculo(x, y, velocidade, largura, imagem):
    """Cria um obstáculo (um dicionário). Se anda para a esquerda, a imagem é espelhada."""
    if velocidade < 0:
        imagem = pygame.transform.flip(imagem, True, False)
    return {"x": x, "y": y, "velocidade": velocidade, "largura": largura, "imagem": imagem}


# Lista com todos os obstáculos do corredor.
# Aluno: lento e pequeno (1 casa). Zelador com carrinho de limpeza: rápido e comprido (2 casas).
# Velocidade positiva anda para a direita; negativa anda para a esquerda.
obstaculos = [
    criar_obstaculo(0, 450, 2, 50, IMAGENS["alunos"][0]),
    criar_obstaculo(300, 450, 2, 50, IMAGENS["alunos"][1]),
    criar_obstaculo(100, 350, -5, 100, IMAGENS["carrinho"]),
    criar_obstaculo(400, 250, 3, 50, IMAGENS["alunos"][2]),
    criar_obstaculo(200, 150, -6, 100, IMAGENS["carrinho"]),
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
    """Desenha a imagem de cada obstáculo na posição dele."""
    for obstaculo in obstaculos:
        tela.blit(obstaculo["imagem"], (obstaculo["x"], obstaculo["y"]))


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
    """Coloca o personagem de volta na posição inicial, lá embaixo, parado."""
    personagem["x"] = 250
    personagem["y"] = 550
    personagem["animacao"] = "parado"
    personagem["tempo"] = 0


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
# BLOCO 9 - Sons
# ============================================

# Música de fundo: carrega o arquivo e toca para sempre (-1 = repetir sem parar)
pygame.mixer.music.load("musica.wav")
pygame.mixer.music.play(-1)

# Efeito de batida: fica guardado numa variável para tocar quando precisar
som_batida = pygame.mixer.Sound("batida.wav")


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

        # Se bateu em alguém, toca a batida e começa a animação de batida
        if personagem["animacao"] != "batida" and bateu(personagem, obstaculos):
            som_batida.play()
            comecar_animacao(personagem, "batida", TEMPO_BATIDA)

        # Conta o tempo da animação
        atualizar_animacao(personagem)

        # Quando a animação de batida acaba, volta para o começo e perde os pontos
        if terminou_batida(personagem):
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
