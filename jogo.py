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

# Tamanho de cada "casa" do chão: tudo anda de casa em casa (a tela tem 12 x 12 casas)
CASA = 50

# Cria a janela e coloca um título nela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Segura Aí!")

# Relógio que controla a velocidade do jogo
relogio = pygame.time.Clock()

# Cores no formato (Vermelho, Verde, Azul), de 0 a 255
VERMELHO = (220, 50, 50)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Fontes para escrever na tela (None = fonte padrão do pygame; o número é o tamanho)
fonte = pygame.font.Font(None, 40)
fonte_pequena = pygame.font.Font(None, 28)
fonte_grande = pygame.font.Font(None, 72)


# ============================================
# BLOCO 2 - Imagens
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
    "professora": carregar_imagem("professora.png"),
    "diretor": carregar_imagem("diretor.png"),
    "skate": carregar_imagem("skate.png"),
    "merendeira": carregar_imagem("merendeira.png"),
    "bicicleta": carregar_imagem("bicicleta.png"),
    "titulo": carregar_imagem("titulo.png"),
    "game_over": carregar_imagem("game_over.png"),
}

# Os três mapas que ficam se repetindo, nesta ordem: corredor das salas, cantina e parquinho
FUNDOS = [carregar_imagem("fundo1.png"), carregar_imagem("fundo2.png"), carregar_imagem("fundo3.png")]


# ============================================
# BLOCO 3 - Personagem e animações
# ============================================

# O personagem não sobe acima desta altura na tela: dali para cima, quem desce é o mundo (Bloco 5)
LINHA_LIMITE = 300

# Quantos quadros dura cada animação (60 quadros = 1 segundo)
TEMPO_PASSO = 12
TEMPO_BATIDA = 60

# O personagem é um dicionário com a posição, a animação atual e a faixa onde está
# ("faixa" = quantas faixas ele está acima da largada)
personagem = {"x": 250, "y": 550, "animacao": "parado", "tempo": 0, "faixa": 0}


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


def mover_personagem(personagem, tecla):
    """Anda uma casa na direção da seta. Devolve True se o mundo precisa descer."""
    if personagem["animacao"] == "batida":
        return False  # tonto depois da batida: não anda
    x_antes = personagem["x"]
    faixa_antes = personagem["faixa"]
    precisa_rolar = False
    if tecla == pygame.K_UP:
        personagem["faixa"] = personagem["faixa"] + 1
        if personagem["y"] > LINHA_LIMITE:
            personagem["y"] = personagem["y"] - CASA
        else:
            precisa_rolar = True  # já está no limite: o mundo desce no lugar dele subir
    if tecla == pygame.K_DOWN and personagem["y"] < ALTURA - CASA:
        personagem["y"] = personagem["y"] + CASA
        personagem["faixa"] = personagem["faixa"] - 1
    if tecla == pygame.K_LEFT and personagem["x"] > 0:
        personagem["x"] = personagem["x"] - CASA
    if tecla == pygame.K_RIGHT and personagem["x"] < LARGURA - CASA:
        personagem["x"] = personagem["x"] + CASA
    # Se andou, faz a animação do passo
    if personagem["x"] != x_antes or personagem["faixa"] != faixa_antes:
        comecar_animacao(personagem, "andando", TEMPO_PASSO)
    return precisa_rolar


def imagem_do_personagem(personagem):
    """Escolhe o quadro certo da animação atual."""
    if personagem["animacao"] == "andando":
        quadro = (personagem["tempo"] // 6) % 2  # troca de quadro a cada 6 quadros
        return IMAGENS["andando"][quadro]
    if personagem["animacao"] == "batida":
        quadro = (personagem["tempo"] // 8) % 2  # estrelinhas trocam a cada 8 quadros
        return IMAGENS["batida"][quadro]
    return IMAGENS["parado"]


def desenhar_personagem(tela, personagem):
    """Desenha o quadro certo da animação: com pulinho ao andar e tremendo na batida."""
    x = personagem["x"]
    y = personagem["y"]
    if personagem["animacao"] == "andando":
        y = y - min(personagem["tempo"], TEMPO_PASSO - personagem["tempo"])  # sobe e desce
    if personagem["animacao"] == "batida" and personagem["tempo"] > 0:
        x = x + random.randint(-3, 3)  # tremendo
    tela.blit(imagem_do_personagem(personagem), (x, y))


def voltar_ao_comeco(personagem):
    """Coloca o personagem de volta na posição inicial, lá embaixo, parado."""
    personagem["x"] = 250
    personagem["y"] = 550
    personagem["animacao"] = "parado"
    personagem["tempo"] = 0
    personagem["faixa"] = 0


# ============================================
# BLOCO 4 - Obstáculos
# ============================================

# Cada tipo de obstáculo: imagens possíveis, largura, velocidades possíveis e quantos vão por faixa
TIPOS_OBSTACULO = {
    "aluno":      {"imagens": IMAGENS["alunos"],         "largura": CASA,     "velocidades": [1, 2, 3], "quantos": 2},
    "professora": {"imagens": [IMAGENS["professora"]],   "largura": CASA,     "velocidades": [1, 2],    "quantos": 2},
    "diretor":    {"imagens": [IMAGENS["diretor"]],      "largura": CASA,     "velocidades": [1],       "quantos": 2},
    "skate":      {"imagens": [IMAGENS["skate"]],        "largura": CASA,     "velocidades": [4, 5],    "quantos": 2},
    "zelador":    {"imagens": [IMAGENS["carrinho"]],     "largura": 2 * CASA, "velocidades": [3, 4, 5], "quantos": 1},
    "merendeira": {"imagens": [IMAGENS["merendeira"]],   "largura": 2 * CASA, "velocidades": [2, 3],    "quantos": 1},
    "bicicleta":  {"imagens": [IMAGENS["bicicleta"]],    "largura": 2 * CASA, "velocidades": [5, 6],    "quantos": 1},
}

# Lista com todos os obstáculos na tela. Começa vazia: eles são sorteados faixa por faixa (Bloco 5).
obstaculos = []


def criar_obstaculo(x, y, velocidade, largura, imagem):
    """Cria um obstáculo (um dicionário). Se anda para a esquerda, a imagem é espelhada."""
    if velocidade < 0:
        imagem = pygame.transform.flip(imagem, True, False)
    return {"x": x, "y": y, "velocidade": velocidade, "largura": largura, "imagem": imagem}


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
# BLOCO 5 - Mapa infinito
# ============================================

# Cada fundo tem 12 faixas (600 / 50)
FAIXAS_POR_FUNDO = 12

# Tipo de cada faixa de cada fundo, de cima para baixo: "livre" (seguro) ou "corredor" (tem obstáculos)
FAIXAS_FUNDO = [
    # corredor das salas: granilite (livre) e corredor de madeira
    ["livre", "corredor", "corredor", "livre", "corredor", "corredor",
     "corredor", "livre", "corredor", "corredor", "livre", "livre"],
    # cantina: piso xadrez (livre) e passagem de lajota
    ["livre", "corredor", "corredor", "livre", "corredor", "corredor",
     "livre", "corredor", "corredor", "corredor", "livre", "livre"],
    # parquinho: grama (livre) e trilha de terra
    ["livre", "corredor", "livre", "corredor", "corredor", "corredor",
     "livre", "corredor", "corredor", "livre", "corredor", "livre"],
]

# Quem pode aparecer em cada mapa ("aluno" repetido = aparece mais vezes no sorteio)
OBSTACULOS_DO_MAPA = [
    ["aluno", "aluno", "professora", "diretor", "zelador"],   # corredor das salas
    ["aluno", "aluno", "merendeira", "zelador"],              # cantina
    ["aluno", "aluno", "skate", "bicicleta"],                 # parquinho
]

# O mundo guarda quantas faixas já desceram desde a largada
mundo = {"linhas_roladas": 0}


def qual_fundo(numero):
    """Diz qual dos fundos (0, 1 ou 2) a faixa de número 'numero' do mapa usa."""
    return (numero // FAIXAS_POR_FUNDO) % len(FUNDOS)  # 0, 1, 2, 0, 1, 2...


def tipo_da_faixa(numero):
    """Diz se a faixa de número 'numero' do mapa (0 = largada) é "livre" ou "corredor"."""
    linha = FAIXAS_POR_FUNDO - 1 - numero % FAIXAS_POR_FUNDO  # a lista é de cima para baixo
    return FAIXAS_FUNDO[qual_fundo(numero)][linha]


def criar_obstaculos_da_faixa(obstaculos, y, numero):
    """Se a faixa é corredor, sorteia um tipo de obstáculo do mapa, a velocidade e o sentido."""
    if tipo_da_faixa(numero) == "livre":
        return
    nome = random.choice(OBSTACULOS_DO_MAPA[qual_fundo(numero)])
    tipo = TIPOS_OBSTACULO[nome]
    direcao = random.choice([1, -1])  # 1 = para a direita, -1 = para a esquerda
    velocidade = random.choice(tipo["velocidades"]) * direcao
    x = random.randint(0, 250)
    for i in range(tipo["quantos"]):  # se forem 2, o segundo vai 300 pixels depois
        imagem = random.choice(tipo["imagens"])
        obstaculos.append(criar_obstaculo(x + i * 300, y, velocidade, tipo["largura"], imagem))


def montar_mapa_inicial(obstaculos, mundo):
    """Começo da partida: mundo na largada e obstáculos sorteados nas 12 faixas da tela."""
    mundo["linhas_roladas"] = 0
    obstaculos.clear()
    for numero in range(FAIXAS_POR_FUNDO):
        y = ALTURA - CASA - numero * CASA  # faixa 0 lá embaixo (y = 550), faixa 11 lá em cima (y = 0)
        criar_obstaculos_da_faixa(obstaculos, y, numero)


def rolar_mundo(obstaculos, mundo):
    """O mundo desce uma faixa: some quem saiu por baixo e nasce uma faixa nova em cima."""
    mundo["linhas_roladas"] = mundo["linhas_roladas"] + 1
    for obstaculo in obstaculos:
        obstaculo["y"] = obstaculo["y"] + CASA
    for obstaculo in obstaculos[:]:  # [:] = cópia da lista, para poder remover itens durante o for
        if obstaculo["y"] >= ALTURA:
            obstaculos.remove(obstaculo)
    numero_da_faixa_nova = mundo["linhas_roladas"] + FAIXAS_POR_FUNDO - 1
    criar_obstaculos_da_faixa(obstaculos, 0, numero_da_faixa_nova)


def desenhar_fundo(tela, mundo):
    """Desenha os dois pedaços de fundo que aparecem na tela, um em cima do outro."""
    primeiro = mundo["linhas_roladas"] // FAIXAS_POR_FUNDO
    for numero in [primeiro, primeiro + 1]:
        y = mundo["linhas_roladas"] * CASA - numero * ALTURA
        tela.blit(FUNDOS[numero % len(FUNDOS)], (0, y))


# ============================================
# BLOCO 6 - Colisão
# ============================================

def bateu(personagem, obstaculos):
    """Devolve True se o personagem está encostando em algum obstáculo."""
    retangulo_personagem = pygame.Rect(personagem["x"], personagem["y"], CASA, CASA)
    for obstaculo in obstaculos:
        retangulo_obstaculo = pygame.Rect(obstaculo["x"], obstaculo["y"], obstaculo["largura"], CASA)
        if retangulo_personagem.colliderect(retangulo_obstaculo):
            return True
    return False


# ============================================
# BLOCO 7 - Pontuação e recorde
# ============================================

# O placar guarda os pulos da partida (a faixa mais alta alcançada) e o recorde
placar = {"pontos": 0, "recorde": 0}


def atualizar_pontos(placar, personagem):
    """Se o personagem chegou numa faixa nova (mais alta que todas), ganha ponto e devolve True."""
    if personagem["faixa"] > placar["pontos"]:
        placar["pontos"] = personagem["faixa"]
        return True
    return False


def zerar_pontos(placar):
    """Volta os pontos para zero (o recorde continua)."""
    placar["pontos"] = 0


def guardar_recorde(placar):
    """Se a partida passou do recorde, ela vira o novo recorde."""
    if placar["pontos"] > placar["recorde"]:
        placar["recorde"] = placar["pontos"]


def desenhar_sombra(tela, y, altura, quanto):
    """Pinta um retângulo preto transparente por cima (quanto: 0 = invisível, 255 = preto)."""
    sombra = pygame.Surface((LARGURA, altura))
    sombra.set_alpha(quanto)
    tela.blit(sombra, (0, y))


def desenhar_pontos(tela, placar):
    """Escreve os pulos e o recorde numa tarja escura no alto da tela."""
    desenhar_sombra(tela, 0, 40, 150)
    texto = fonte_pequena.render("Pulos: " + str(placar["pontos"]) + "    Recorde: " + str(placar["recorde"]), True, BRANCO)
    tela.blit(texto, (10, 12))


# ============================================
# BLOCO 8 - Barra de aperto
# ============================================

APERTO_MAXIMO = 100
VELOCIDADE_APERTO = APERTO_MAXIMO / (7 * 60)  # enche em 7 segundos (7 x 60 quadros)

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
    """Desenha a barra no canto de cima, à direita: vermelho por dentro, contorno branco."""
    largura_cheia = int(barra["aperto"] * 2)  # 100 de aperto = 200 pixels
    pygame.draw.rect(tela, VERMELHO, (390, 10, largura_cheia, 20))
    pygame.draw.rect(tela, BRANCO, (390, 10, 200, 20), 2)


# ============================================
# BLOCO 9 - Telas (início, jogo e fim)
# ============================================

# Em qual tela o jogo está: "inicio", "jogo" ou "fim"
estado = "inicio"

# Frases de game over: uma é sorteada quando a barra enche...
FRASES_FIM = [
    "Não deu tempo...",
    "Ih, molhou tudo!",
    "Faltou só um pouquinho!",
    "Alguém chama a limpeza!",
]

# ...e outra quando o personagem bate em alguém
FRASES_BATIDA = [
    "Trombou no colega!",
    "Atropelado pelo carrinho!",
    "Olha por onde anda!",
    "Pressa demais dá nisso!",
]

# Frase que aparece na tela de fim
frase_fim = ""


def reiniciar_jogo(personagem, placar, barra, obstaculos, mundo):
    """Deixa tudo pronto para uma partida nova."""
    voltar_ao_comeco(personagem)
    zerar_pontos(placar)
    esvaziar_barra(barra)
    montar_mapa_inicial(obstaculos, mundo)


def escrever_no_meio(tela, texto, fonte, y):
    """Escreve um texto branco centralizado na horizontal, na altura y."""
    imagem = fonte.render(texto, True, BRANCO)
    x = (LARGURA - imagem.get_width()) // 2
    tela.blit(imagem, (x, y))


def desenhar_imagem_no_meio(tela, imagem, y):
    """Desenha uma imagem centralizada na horizontal, na altura y."""
    x = (LARGURA - imagem.get_width()) // 2
    tela.blit(imagem, (x, y))


def desenhar_tela_inicio(tela):
    """Mostra o fundo escurecido, o título em pixel art, o personagem grande e como começar."""
    tela.blit(FUNDOS[0], (0, 0))
    desenhar_sombra(tela, 0, ALTURA, 160)
    desenhar_imagem_no_meio(tela, IMAGENS["titulo"], 90)
    personagem_grande = pygame.transform.scale(IMAGENS["parado"], (150, 150))
    desenhar_imagem_no_meio(tela, personagem_grande, 190)
    escrever_no_meio(tela, "Atravesse a escola sem trombar em ninguém.", fonte_pequena, 380)
    escrever_no_meio(tela, "Cada faixa nova esvazia a barra de aperto!", fonte_pequena, 410)
    escrever_no_meio(tela, "Aperte ESPAÇO para começar", fonte, 480)


def desenhar_tela_fim(tela, placar, frase):
    """Escurece o jogo parado e mostra GAME OVER, a frase, os pulos, o recorde e como jogar de novo."""
    desenhar_sombra(tela, 0, ALTURA, 170)
    desenhar_imagem_no_meio(tela, IMAGENS["game_over"], 100)
    escrever_no_meio(tela, frase, fonte, 225)
    escrever_no_meio(tela, "Pulos: " + str(placar["pontos"]), fonte_grande, 275)
    escrever_no_meio(tela, "Recorde: " + str(placar["recorde"]), fonte, 345)
    escrever_no_meio(tela, "Aperte ESPAÇO para jogar de novo", fonte_pequena, 430)


# ============================================
# BLOCO 10 - Sons
# ============================================

# Música de fundo: carrega o arquivo e toca para sempre (-1 = repetir sem parar)
pygame.mixer.music.load("musica.wav")
pygame.mixer.music.play(-1)

# Efeito de batida: fica guardado numa variável para tocar quando precisar
som_batida = pygame.mixer.Sound("batida.wav")


# ============================================
# BLOCO 11 - Loop principal
# ============================================

rodando = True
while rodando:

    # 1) Ler o que o jogador fez
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if estado == "jogo":
                if mover_personagem(personagem, evento.key):
                    rolar_mundo(obstaculos, mundo)
            elif evento.key == pygame.K_SPACE:
                reiniciar_jogo(personagem, placar, barra, obstaculos, mundo)
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

        # Quando a animação de batida acaba: game over
        if terminou_batida(personagem):
            guardar_recorde(placar)
            estado = "fim"
            frase_fim = random.choice(FRASES_BATIDA)

        # Chegou numa faixa nova? Ganha ponto e a barra de aperto esvazia
        if atualizar_pontos(placar, personagem):
            esvaziar_barra(barra)

        # A barra enche com o tempo. Se encher, game over com frase sorteada
        encher_barra(barra)
        if barra_cheia(barra):
            guardar_recorde(placar)
            estado = "fim"
            frase_fim = random.choice(FRASES_FIM)

    # 3) Desenhar a tela certa
    if estado == "inicio":
        desenhar_tela_inicio(tela)
    else:
        # No jogo e no fim, desenha a escola (no fim ela fica parada, por baixo da mensagem)
        desenhar_fundo(tela, mundo)
        desenhar_obstaculos(tela, obstaculos)
        desenhar_personagem(tela, personagem)
        desenhar_pontos(tela, placar)
        desenhar_barra(tela, barra)
        if estado == "fim":
            desenhar_tela_fim(tela, placar, frase_fim)

    # 4) Mostrar na tela o que foi desenhado
    pygame.display.update()

    # 5) Esperar para rodar a 60 quadros por segundo
    relogio.tick(60)

# Saiu do loop: desliga o pygame
pygame.quit()
