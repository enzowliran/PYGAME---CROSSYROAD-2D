# ============================================================
# FERRAMENTA (não faz parte do jogo)
# Gera as imagens em pixel art da pasta "imagens/".
# Foi usada uma vez para criar os arquivos .png; o jogo só carrega os .png prontos.
# Rodar (de dentro da pasta do projeto):  python ferramentas/gerar_imagens.py
# ============================================================

import os
import random
import pygame

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "imagens")

# Cada letra do desenho vira uma cor. "." = transparente.
CORES = {
    "K": (34, 28, 38),     # contorno
    "S": (242, 194, 152),  # pele
    "s": (208, 152, 116),  # pele (sombra)
    "H": (92, 56, 32),     # cabelo
    "h": (138, 88, 50),    # cabelo (brilho)
    "W": (250, 250, 250),  # branco
    "E": (34, 28, 38),     # olho
    "B": (62, 124, 224),   # camiseta
    "b": (40, 86, 170),    # camiseta (sombra)
    "P": (58, 58, 98),     # calça
    "p": (40, 40, 70),     # calça (sombra)
    "O": (96, 60, 40),     # sapato
    "D": (120, 200, 255),  # gota de suor
    "M": (170, 60, 60),    # boca
    "R": (240, 140, 130),  # bochecha vermelha
    "Y": (255, 222, 60),   # estrela
    "A": (220, 70, 60),    # mochila
    "a": (160, 46, 40),    # mochila (sombra)
    "G": (150, 156, 166),  # metal do carrinho
    "g": (100, 106, 116),  # metal (sombra)
    "L": (250, 214, 60),   # balde amarelo
    "l": (200, 160, 30),   # balde (sombra)
    "C": (110, 190, 230),  # água
    "U": (90, 110, 80),    # uniforme do zelador
    "u": (64, 80, 56),     # uniforme (sombra)
    "T": (40, 40, 40),     # saco de lixo / roda
    "F": (190, 150, 100),  # cabo do esfregão
    "f": (235, 235, 220),  # esfregão
}

# ------------------------------------------------------------ personagem (de frente)
CABECA = [
    "................",
    ".....KKKKKK.....",
    "....KHHhhHHK....",
    "...KHHHHHHHHK...",
    "...KHHSSSSHHK.D.",
    "...KSSESSESSK.D.",
    "...KSSESSESSK...",
    "...KRSSMMSSRK...",
    "....KSSSSSSK....",
    ".....KKSSKK.....",
]
CORPO = [
    "...KBBBBBBBBK...",
    "..KBBBbbbbBBBK..",
    "..KSKSBbbBSKSK..",
]
PERNAS_PARADO = [
    "....KPPPPPPK....",
    "....KPPKKPPK....",
    "....KOOKKOOK....",
]
PERNAS_PASSO_1 = [
    "....KPPPPPPK....",
    "...KPPK.KOOK....",
    "...KOOK..KK.....",
]
PERNAS_PASSO_2 = [
    "....KPPPPPPK....",
    "....KOOK.KPPK...",
    ".....KK..KOOK...",
]

PARADO = CABECA + CORPO + PERNAS_PARADO
ANDANDO_1 = CABECA[:4] + ["...KHHSSSSHHK..."] + ["...KSSESSESSK.D."] + CABECA[6:] + CORPO + PERNAS_PASSO_1
ANDANDO_2 = CABECA[:4] + ["...KHHSSSSHHKD.."] + ["...KSSESSESSK..."] + CABECA[6:] + CORPO + PERNAS_PASSO_2

# Batida: olhos apertados (> <), boca aberta e estrelinhas girando
ROSTO_BATIDA = [
    "...KSESSSSESK...",
    "...KSSESSESSK...",
    "...KRSSKKSSRK...",
]
BATIDA_1 = [
    "..Y..........Y..",
    ".YYY.KKKKKK.YYY.",
    "..Y.KHHhhHHK.Y..",
    "...KHHHHHHHHK...",
    "...KHHSSSSHHK...",
] + ROSTO_BATIDA + CABECA[8:] + CORPO + PERNAS_PARADO
BATIDA_2 = [
    "Y..............Y",
    ".....KKKKKK.....",
    ".Y..KHHhhHHK..Y.",
    "YYY.KHHHHHH.KYYY",
    ".Y.KHHSSSSHHK.Y.",
] + ROSTO_BATIDA + CABECA[8:] + CORPO + PERNAS_PARADO
BATIDA_2[3] = "YYYKHHHHHHHHKYYY"

# ------------------------------------------------------------ aluno (de lado, andando para a direita)
ALUNO = [
    "................",
    "......KKKKK.....",
    ".....KHHHHHK....",
    "....KHHHHHHHK...",
    "....KHHHHSSSK...",
    "....KHHHSSESK...",
    "....KHHSSSSSK...",
    ".....KHSSSMK....",
    "......KKSSK.....",
    "...KKKBBBBBK....",
    "..KAAKBBBBBBK...",
    "..KAaKBBBSSK....",
    "..KAaKBBBBK.....",
    "...KKKPPPPK.....",
    "....KPPK.KPPK...",
    "...KOOK...KOOK..",
]

# ------------------------------------------------------------ zelador empurrando o carrinho (para a direita)
CARRINHO = [
    "................................",
    "....KKKKK.......................",
    "...KUUUUUK......................",
    "..KKKKKKKKK.............F.......",
    "...KSSSSESK.............F.......",
    "...KSSSSSSK.............F.......",
    "....KSSSSK...KKKKKKKKKKKFKKKKK..",
    "...KUUUUUUKSSKGGGGGGGGGKFKLLLLK.",
    "..KUUUuUUUUKKKGTTTTTTTGKFKLCCLK.",
    "..KUUUuUUUK..KGTTTTTTTGKfKLLLLK.",
    "..KUUUuUUUK..KGTTTTTTTGKfflllLK.",
    "...KUUUUUK...KGGGGGGGGGGGGGGGGK.",
    "...KUUKUUK...KggggggggggggggggK.",
    "...KUUKUUK....KK..........KK....",
    "..KOOK.KOOK..KTTK........KTTK...",
    "..KKK..KKK....KK..........KK....",
]

# Variações de roupa dos alunos (troca as cores da camiseta, cabelo e mochila)
VARIACOES_ALUNO = [
    {"B": (220, 70, 70), "b": (160, 46, 46), "H": (40, 30, 26), "A": (60, 120, 220), "a": (40, 86, 170)},
    {"B": (70, 170, 90), "b": (46, 120, 62), "H": (200, 150, 60), "A": (240, 170, 50), "a": (190, 120, 30)},
    {"B": (150, 90, 200), "b": (104, 60, 150), "H": (130, 60, 30), "A": (230, 230, 230), "a": (170, 170, 170)},
]


# ------------------------------------------------------------ 5 obstáculos novos (de lado, para a direita)
CORES.update({
    "V": (200, 70, 110),   # roupa colorida (professora / merendeira)
    "Q": (238, 238, 232),  # branco (touca, avental, gola, vapor)
    "N": (60, 64, 80),     # terno do diretor
    "n": (40, 42, 56),     # terno (sombra)
    "Z": (200, 140, 70),   # madeira do skate
    "I": (196, 202, 210),  # panela
    "J": (220, 60, 60),    # quadro da bicicleta
    "j": (150, 36, 40),    # quadro (sombra)
})

PROFESSORA = [
    "................",
    "......KKKKK.....",
    ".....KHHHHHK....",
    "....KHHHHHHHK...",
    "....KHHHHSSSK...",
    "....KHHHSSESK...",
    "...KHHHHSSSSK...",
    "...KHHHKSSMK....",
    "...KHHK.KSSK....",
    "....KKVVVVVK....",
    "....KVVVVLLLK...",
    "....KVVVVAAAK...",
    "....KVVVVBBK....",
    "....KVVVVVVK....",
    ".....KSK.KSK....",
    "....KOOK.KOOK...",
]

DIRETOR = [
    "................",
    "......KKKKK.....",
    ".....KGGGGGK....",
    "....KGGGSSSSK...",
    "....KGGSSSSSK...",
    "....KGSSKKEKK...",
    "....KGSSSSSSK...",
    ".....KSSSSMK....",
    "......KKSSK.....",
    "....KKNNQAQK....",
    "...KNNNNNANNK...",
    "...KNnNNNANSSK..",
    "...KNnNNNNNK....",
    "....KNNNNNNK....",
    "....KnnK.KnnK...",
    "...KKKKK.KKKKK..",
]

SKATE = [
    "................",
    "......KKKKKK....",
    ".....KAAAAAAKK..",
    "....KHAAAAAAAAK.",
    "....KHHSSSSSK...",
    "....KHSSSSESK...",
    "....KHSSSSSSK...",
    ".....KSSSSMK....",
    "......KKSSK.....",
    "....KKBBBBBKSK..",
    "...KSKBBBBBBK...",
    "....KKBBBBBK....",
    ".....KPPPPPK....",
    "....KOOK.KOOK...",
    "..KZZZZZZZZZZK..",
    "...KTK.....KTK..",
]

MERENDEIRA = [
    "..................Q..Q..........",
    "....KKKKK.........Q..Q..Q.......",
    "...KQQQQQK.......Q..Q..Q........",
    "..KQQQQQQQK....KKKKKKK.KKKKKK...",
    "...KSSSSESK....KIIIIIK.KIIIIK...",
    "...KSSSSSSK....KIIIIIK.KIIIIK...",
    "....KSSSSK...KKKKKKKKKKKKKKKKKK.",
    "...KVVVVVVKSSKGGGGGGGGGGGGGGGGK.",
    "..KVQQQQQVVKKKGggggggggggggggGK.",
    "..KVQQQQQVK..KGGGGGGGGGGGGGGGGK.",
    "..KVQQQQQVK..KGggggggggggggggGK.",
    "...KVVVVVK...KGGGGGGGGGGGGGGGGK.",
    "...KSSKSSK...KggggggggggggggggK.",
    "...KSSKSSK....KK..........KK....",
    "..KOOK.KOOK..KTTK........KTTK...",
    "..KKK..KKK....KK..........KK....",
]

# Criança de bicicleta: o corpo é desenhado por letras; a bicicleta, com linhas e círculos
CICLISTA = [
    "................................",
    "..........KKKKK.................",
    ".........KJJJJJK................",
    "........KJJJJJJJK...............",
    "........KHHHSSESK...............",
    "........KHHSSSSSK...............",
    ".........KKSSMK.................",
    "........KBBBBBKK................",
    ".......KBBBBBBBSSSSSK...........",
    ".......KBBBBBBK.................",
    "........KPPPPPK.................",
    ".........KPPKPK.................",
    "..........KOKOK.................",
    "................................",
    "................................",
    "................................",
]


def bicicleta_imagem():
    """Criança de bicicleta (2 casas)."""
    peq = pygame.Surface((32, 16), pygame.SRCALPHA)
    k = CORES["K"]
    pygame.draw.circle(peq, k, (6, 11), 4, 2)     # roda de trás
    pygame.draw.circle(peq, k, (24, 11), 4, 2)    # roda da frente
    peq.set_at((6, 11), CORES["G"])
    peq.set_at((24, 11), CORES["G"])
    tubos = [((6, 11), (12, 12)), ((6, 11), (10, 8)), ((10, 8), (12, 12)),
             ((12, 12), (20, 7)), ((10, 8), (20, 7)), ((20, 7), (24, 11))]
    for a, b in tubos:
        pygame.draw.line(peq, CORES["j"], (a[0], a[1] + 1), (b[0], b[1] + 1))
        pygame.draw.line(peq, CORES["J"], a, b)
    pygame.draw.line(peq, k, (20, 7), (21, 5))     # guidão
    pygame.draw.line(peq, k, (20, 5), (22, 5))
    pygame.draw.line(peq, k, (8, 7), (12, 7))      # banco
    for y, linha in enumerate(CICLISTA):
        for x, letra in enumerate(linha):
            if letra != ".":
                peq.set_at((x, y), CORES[letra])
    grande = pygame.transform.scale(peq, (96, 48))
    quadro = pygame.Surface((100, 50), pygame.SRCALPHA)
    quadro.blit(grande, (2, 2))
    return quadro


def desenho_para_imagem(desenho, escala, tamanho, cores=CORES):
    """Transforma uma lista de textos numa imagem pixelada, centralizada num quadro do tamanho pedido."""
    altura = len(desenho)
    largura = len(desenho[0])
    pequena = pygame.Surface((largura, altura), pygame.SRCALPHA)
    for y in range(altura):
        assert len(desenho[y]) == largura, desenho[y]
        for x in range(largura):
            letra = desenho[y][x]
            if letra != ".":
                pequena.set_at((x, y), cores[letra])
    grande = pygame.transform.scale(pequena, (largura * escala, altura * escala))
    quadro = pygame.Surface(tamanho, pygame.SRCALPHA)
    quadro.blit(grande, ((tamanho[0] - largura * escala) // 2, tamanho[1] - altura * escala))
    return quadro


def salvar(imagem, nome):
    pygame.image.save(imagem, os.path.join(PASTA, nome))


def gerar_personagens():
    casa = (50, 50)
    salvar(desenho_para_imagem(PARADO, 3, casa), "jogador_parado.png")
    salvar(desenho_para_imagem(ANDANDO_1, 3, casa), "jogador_andando1.png")
    salvar(desenho_para_imagem(ANDANDO_2, 3, casa), "jogador_andando2.png")
    salvar(desenho_para_imagem(BATIDA_1, 3, casa), "jogador_batida1.png")
    salvar(desenho_para_imagem(BATIDA_2, 3, casa), "jogador_batida2.png")
    for numero, variacao in enumerate(VARIACOES_ALUNO):
        cores = dict(CORES)
        cores.update(variacao)
        salvar(desenho_para_imagem(ALUNO, 3, casa, cores), "aluno" + str(numero + 1) + ".png")
    salvar(desenho_para_imagem(CARRINHO, 3, (100, 50)), "carrinho.png")
    salvar(desenho_para_imagem(PROFESSORA, 3, casa), "professora.png")
    salvar(desenho_para_imagem(DIRETOR, 3, casa), "diretor.png")
    salvar(desenho_para_imagem(SKATE, 3, casa), "skate.png")
    salvar(desenho_para_imagem(MERENDEIRA, 3, (100, 50)), "merendeira.png")
    salvar(bicicleta_imagem(), "bicicleta.png")


# ------------------------------------------------------------ 3 mapas (fundos)
# Cada fundo tem 12 faixas (de cima para baixo). TEM que ser igual à lista FAIXAS_FUNDO do jogo.py
F = 25        # uma faixa no desenho pequeno (vira 50 px)
LADO = 300    # desenho pequeno 300 x 300 -> 600 x 600

FAIXAS_FUNDO = [
    # 1 - corredor das salas
    ["livre", "corredor", "corredor", "livre", "corredor", "corredor",
     "corredor", "livre", "corredor", "corredor", "livre", "livre"],
    # 2 - cantina
    ["livre", "corredor", "corredor", "livre", "corredor", "corredor",
     "livre", "corredor", "corredor", "corredor", "livre", "livre"],
    # 3 - parquinho
    ["livre", "corredor", "livre", "corredor", "corredor", "corredor",
     "livre", "corredor", "corredor", "livre", "corredor", "livre"],
]


def clamp(c):
    return max(0, min(255, c))


def tom(cor, d):
    return tuple(clamp(c + d) for c in cor)


def varia(cor, quanto, s):
    return tom(cor, s.randint(-quanto, quanto))


def px(sup, x, y, cor):
    if 0 <= x < LADO and 0 <= y < LADO:
        sup.set_at((x, y), cor)


def texto(sup, msg, x, y, cor, tamanho, sombra=None, centro=False):
    fonte = pygame.font.Font(None, tamanho)
    img = fonte.render(msg, False, cor)
    if centro:
        x = x - img.get_width() // 2
    if sombra:
        sup.blit(fonte.render(msg, False, sombra), (x + 1, y + 1))
    sup.blit(img, (x, y))


def seta_cima(sup, x, y, cor):
    pygame.draw.line(sup, cor, (x, y + 10), (x, y + 2), 2)
    pygame.draw.polygon(sup, cor, [(x - 4, y + 4), (x, y - 1), (x + 4, y + 4)])


def placa_proximo(sup, y0, msg, cor_fundo, cor_texto):
    """Plaquinha pintada no chão avisando o próximo ambiente."""
    largura = 74
    x = 150 - largura // 2
    pygame.draw.rect(sup, tom(cor_fundo, -40), (x + 1, y0 + 5, largura, 16))
    pygame.draw.rect(sup, cor_fundo, (x, y0 + 4, largura, 16))
    pygame.draw.rect(sup, tom(cor_fundo, 40), (x, y0 + 4, largura, 16), 1)
    texto(sup, msg, 150 - 6, y0 + 8, cor_texto, 15, centro=True)
    seta_cima(sup, x + largura - 9, y0 + 6, cor_texto)


# ------------------------------------------------------------------ 1. CORREDOR DAS SALAS
def granilite(sup, y0, s):
    """Piso de granilite (o 'piso de escola'): cinza claro com pedrinhas."""
    base = (206, 204, 196)
    pygame.draw.rect(sup, base, (0, y0, LADO, F))
    for _ in range(520):
        cor = s.choice([(150, 148, 142), (236, 234, 228), (176, 160, 140), (120, 130, 140), (225, 215, 200)])
        px(sup, s.randint(0, LADO - 1), y0 + s.randint(0, F - 1), cor)
    for x in range(0, LADO, 50):   # juntas de dilatação (filete metálico)
        pygame.draw.line(sup, (168, 166, 160), (x, y0), (x, y0 + F - 1))


def assoalho(sup, y0, s):
    """Corredor de madeira encerada, tábuas no sentido do corredor."""
    for linha in range(5):
        y = y0 + linha * 5
        x = -s.randint(0, 60)
        while x < LADO:
            comp = s.randint(40, 80)
            cor = varia((190, 132, 74), 10, s)
            pygame.draw.rect(sup, cor, (x, y, comp, 5))
            for _ in range(comp // 5):  # veios
                gx = x + s.randint(1, comp - 3)
                gy = y + s.randint(1, 3)
                pygame.draw.line(sup, tom(cor, -18), (gx, gy), (gx + s.randint(2, 7), gy))
            pygame.draw.line(sup, tom(cor, 22), (x, y), (x + comp, y))          # brilho da cera
            pygame.draw.line(sup, (112, 70, 36), (x, y + 4), (x + comp, y + 4))  # fresta
            pygame.draw.line(sup, (112, 70, 36), (x, y), (x, y + 4))
            x = x + comp


def rodape(sup, y, em_cima):
    """Borda de madeira escura entre o corredor e o hall (não é rua: é o acabamento do piso)."""
    pygame.draw.rect(sup, (92, 58, 32), (0, y, LADO, 2))
    pygame.draw.line(sup, (140, 96, 56), (0, y if em_cima else y + 1), (LADO, y if em_cima else y + 1))


def capacho_sala(sup, x, y0, nome, cor):
    pygame.draw.rect(sup, tom(cor, -50), (x + 1, y0 + 4, 34, 18))
    pygame.draw.rect(sup, cor, (x, y0 + 3, 34, 18))
    for i in range(x + 2, x + 33, 2):
        pygame.draw.line(sup, tom(cor, -18), (i, y0 + 5), (i, y0 + 18))
    pygame.draw.rect(sup, tom(cor, 45), (x, y0 + 3, 34, 18), 1)
    texto(sup, nome, x + 17, y0 + 8, (250, 245, 230), 15, centro=True)


def brasao(sup, cx, y0):
    """Brasão da escola embutido no granilite."""
    cy = y0 + 12
    pygame.draw.circle(sup, (40, 70, 140), (cx, cy), 10)
    pygame.draw.circle(sup, (230, 190, 70), (cx, cy), 10, 1)
    pygame.draw.polygon(sup, (240, 240, 235), [(cx - 5, cy - 3), (cx, cy - 6), (cx + 5, cy - 3), (cx + 5, cy + 4), (cx - 5, cy + 4)])
    pygame.draw.line(sup, (40, 70, 140), (cx, cy - 4), (cx, cy + 3))  # livro aberto
    pygame.draw.line(sup, (40, 70, 140), (cx - 3, cy - 1), (cx - 1, cy - 1))
    pygame.draw.line(sup, (40, 70, 140), (cx + 1, cy - 1), (cx + 3, cy - 1))


def lapis(sup, x, y):
    pygame.draw.line(sup, (240, 190, 40), (x, y), (x + 7, y))
    px(sup, x + 8, y, (230, 200, 160))
    px(sup, x + 9, y, (40, 40, 40))
    px(sup, x - 1, y, (230, 130, 140))


def bolinha_papel(sup, x, y):
    pygame.draw.circle(sup, (245, 245, 240), (x, y), 2)
    px(sup, x - 1, y, (200, 200, 205))
    px(sup, x + 1, y + 1, (190, 190, 200))


def borracha(sup, x, y):
    pygame.draw.rect(sup, (240, 120, 140), (x, y, 5, 3))
    pygame.draw.rect(sup, (90, 140, 220), (x + 3, y, 2, 3))


def mapa_corredor(s):
    sup = pygame.Surface((LADO, LADO))
    faixas = FAIXAS_FUNDO[0]
    for i, tipo in enumerate(faixas):
        if tipo == "livre":
            granilite(sup, i * F, s)
        else:
            assoalho(sup, i * F, s)
    for i, tipo in enumerate(faixas):
        if tipo == "corredor":
            if i == 0 or faixas[i - 1] != "corredor":
                rodape(sup, i * F, True)
            if i == 11 or faixas[i + 1] != "corredor":
                rodape(sup, i * F + F - 2, False)
    # detalhes
    placa_proximo(sup, 0, "CANTINA", (60, 110, 190), (255, 255, 255))
    capacho_sala(sup, 30, 3 * F, "1ºA", (60, 120, 70))
    capacho_sala(sup, 236, 3 * F, "1ºB", (150, 60, 60))
    capacho_sala(sup, 132, 7 * F, "2ºA", (70, 80, 150))
    brasao(sup, 150, 10 * F)
    texto(sup, "BOAS-VINDAS!", 150, 11 * F + 8, (90, 90, 100), 16, centro=True)
    for i, tipo in enumerate(faixas):
        if tipo == "livre":
            y0 = i * F
            lapis(sup, s.randint(10, 280), y0 + s.randint(5, 20))
            bolinha_papel(sup, s.randint(10, 290), y0 + s.randint(5, 20))
            if s.random() < 0.5:
                borracha(sup, s.randint(10, 280), y0 + s.randint(5, 18))
    return sup


# ------------------------------------------------------------------ 2. CANTINA
def xadrez(sup, y0, s):
    """Piso xadrez da cantina (área das mesas)."""
    lado = 12
    for linha in range(3):
        for coluna in range(LADO // lado + 1):
            x = coluna * lado - 6
            y = y0 + linha * 9 - 1
            clara = (coluna + linha) % 2 == 0
            cor = varia((236, 232, 220), 3, s) if clara else varia((70, 150, 120), 3, s)
            pygame.draw.rect(sup, cor, (x, y, lado, 9))
            pygame.draw.line(sup, tom(cor, 18), (x, y), (x + lado - 1, y))


def lajota(sup, y0, s):
    """Passagem da cantina: lajotas quadradas de cerâmica (onde a galera passa com a bandeja)."""
    pygame.draw.rect(sup, (150, 128, 112), (0, y0, LADO, F))   # rejunte
    for linha in range(2):
        for coluna in range(LADO // 12 + 1):
            x = coluna * 12 + 1
            y = y0 + linha * 12 + 1
            cor = varia((184, 92, 62), 7, s)
            pygame.draw.rect(sup, cor, (x, y, 11, 11))
            pygame.draw.line(sup, tom(cor, 26), (x, y), (x + 9, y))          # brilho
            pygame.draw.line(sup, tom(cor, 26), (x, y), (x, y + 9))
            pygame.draw.line(sup, tom(cor, -22), (x + 10, y + 1), (x + 10, y + 10))
            if s.random() < 0.15:
                px(sup, x + s.randint(2, 8), y + s.randint(2, 8), tom(cor, 30))


def borda_cantina(sup, y):
    pygame.draw.rect(sup, (110, 110, 112), (0, y, LADO, 2))
    pygame.draw.line(sup, (170, 170, 172), (0, y), (LADO, y))


def pegadas(sup, x, y0):
    """Adesivos de pezinhos da fila do lanche."""
    for i in range(3):
        cx = x + i * 14
        pygame.draw.ellipse(sup, (250, 200, 40), (cx, y0 + 6, 4, 7))
        pygame.draw.ellipse(sup, (250, 200, 40), (cx + 5, y0 + 10, 4, 7))
        px(sup, cx + 1, y0 + 5, (250, 200, 40))
        px(sup, cx + 6, y0 + 9, (250, 200, 40))


def suco(sup, x, y, s):
    agua = pygame.Surface((24, 12), pygame.SRCALPHA)
    pygame.draw.ellipse(agua, (240, 150, 40, 190), (0, 2, 16, 9))
    pygame.draw.ellipse(agua, (240, 150, 40, 190), (8, 0, 16, 10))
    pygame.draw.line(agua, (255, 230, 170, 230), (5, 4), (9, 4))
    sup.blit(agua, (x, y))
    pygame.draw.rect(sup, (250, 250, 250), (x + 22, y + 1, 5, 7))   # caixinha caída
    pygame.draw.rect(sup, (240, 150, 40), (x + 22, y + 3, 5, 3))


def casca_banana(sup, x, y):
    pygame.draw.polygon(sup, (245, 215, 60), [(x, y + 3), (x + 3, y), (x + 4, y + 3)])
    pygame.draw.polygon(sup, (245, 215, 60), [(x + 4, y + 3), (x + 8, y + 1), (x + 6, y + 5)])
    pygame.draw.polygon(sup, (230, 195, 50), [(x + 3, y + 4), (x + 4, y + 8), (x + 1, y + 6)])
    px(sup, x + 4, y + 3, (110, 80, 30))


def bandeja(sup, x, y):
    pygame.draw.rect(sup, (90, 130, 190), (x, y, 16, 10))
    pygame.draw.rect(sup, (60, 90, 140), (x, y, 16, 10), 1)
    pygame.draw.circle(sup, (250, 250, 250), (x + 5, y + 5), 3)
    pygame.draw.circle(sup, (230, 120, 60), (x + 5, y + 5), 1)
    pygame.draw.rect(sup, (220, 200, 140), (x + 10, y + 2, 4, 6))


def guardanapo(sup, x, y):
    pygame.draw.polygon(sup, (250, 250, 250), [(x, y), (x + 5, y + 1), (x + 4, y + 5), (x, y + 4)])


def mapa_cantina(s):
    sup = pygame.Surface((LADO, LADO))
    faixas = FAIXAS_FUNDO[1]
    for i, tipo in enumerate(faixas):
        if tipo == "livre":
            xadrez(sup, i * F, s)
        else:
            lajota(sup, i * F, s)
    for i, tipo in enumerate(faixas):
        if tipo == "corredor":
            if i == 0 or faixas[i - 1] != "corredor":
                borda_cantina(sup, i * F)
            if i == 11 or faixas[i + 1] != "corredor":
                borda_cantina(sup, i * F + F - 2)
    placa_proximo(sup, 0, "PARQUINHO", (70, 150, 70), (255, 255, 255))
    # letreiro e detalhes
    pygame.draw.rect(sup, (150, 40, 40), (96, 10 * F + 3, 108, 19))
    pygame.draw.rect(sup, (240, 200, 70), (96, 10 * F + 3, 108, 19), 1)
    texto(sup, "CANTINA", 150, 10 * F + 7, (255, 240, 200), 20, sombra=(90, 20, 20), centro=True)
    pegadas(sup, 20, 3 * F)
    pegadas(sup, 220, 6 * F)
    suco(sup, 180, 3 * F + 7, s)
    casca_banana(sup, 120, 6 * F + 8)
    bandeja(sup, 40, 11 * F + 7)
    for i, tipo in enumerate(faixas):
        if tipo == "livre":
            for _ in range(2):
                guardanapo(sup, s.randint(5, 290), i * F + s.randint(4, 18))
            for _ in range(6):  # migalhas
                px(sup, s.randint(0, 299), i * F + s.randint(2, 22), (210, 170, 90))
    return sup


# ------------------------------------------------------------------ 3. PARQUINHO
def grama(sup, y0, s):
    pygame.draw.rect(sup, (96, 168, 72), (0, y0, LADO, F))
    for _ in range(420):
        x = s.randint(0, LADO - 1)
        y = y0 + s.randint(0, F - 1)
        cor = s.choice([(80, 150, 60), (118, 188, 88), (70, 136, 54), (130, 196, 96)])
        px(sup, x, y, cor)
        if s.random() < 0.3:
            px(sup, x, y - 1, tom(cor, 20))


def flor(sup, x, y, cor):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        px(sup, x + dx, y + dy, cor)
    px(sup, x, y, (250, 220, 70))


def terra(sup, y0, s):
    """Trilha de terra batida, por onde a criançada corre."""
    pygame.draw.rect(sup, (182, 140, 92), (0, y0, LADO, F))
    for _ in range(380):
        px(sup, s.randint(0, LADO - 1), y0 + s.randint(0, F - 1),
           s.choice([(164, 122, 78), (198, 158, 108), (150, 112, 72)]))
    for _ in range(12):  # pedrinhas
        x = s.randint(0, LADO - 3)
        y = y0 + s.randint(2, F - 4)
        pygame.draw.rect(sup, (150, 146, 140), (x, y, 2, 2))
        px(sup, x, y, (200, 196, 190))
    for _ in range(3):  # marcas de tênis
        x = s.randint(0, LADO - 30)
        y = y0 + s.randint(4, F - 8)
        for k in range(3):
            pygame.draw.ellipse(sup, (160, 118, 76), (x + k * 10, y + (k % 2) * 4, 5, 3))


def beira_grama(sup, y, s, para_baixo):
    """Grama 'invadindo' a trilha: borda irregular, nada de linha reta de rua."""
    for x in range(LADO):
        altura = s.choice([1, 1, 2, 2, 3])
        for k in range(altura):
            yy = y + k if para_baixo else y - k
            px(sup, x, yy, s.choice([(96, 168, 72), (80, 150, 60), (118, 188, 88)]))


def caixa_areia(sup, x, y0, s):
    pygame.draw.rect(sup, (130, 90, 50), (x, y0 + 2, 56, 21))
    pygame.draw.rect(sup, (236, 214, 150), (x + 2, y0 + 4, 52, 17))
    for _ in range(60):
        px(sup, x + s.randint(3, 52), y0 + s.randint(5, 19), s.choice([(220, 196, 130), (246, 226, 170)]))
    pygame.draw.rect(sup, (220, 60, 60), (x + 10, y0 + 9, 6, 6))     # baldinho
    pygame.draw.rect(sup, (250, 240, 240), (x + 10, y0 + 9, 6, 1))
    pygame.draw.line(sup, (60, 120, 220), (x + 30, y0 + 12), (x + 38, y0 + 16), 2)  # pazinha
    pygame.draw.circle(sup, (180, 150, 100), (x + 44, y0 + 10), 3)   # castelinho


def amarelinha(sup, x, y0):
    pygame.draw.rect(sup, (190, 190, 186), (x - 3, y0 + 3, 61, 19))
    cores = [(230, 80, 80), (250, 190, 50), (80, 170, 90), (70, 130, 220), (170, 90, 200)]
    for i in range(5):
        pygame.draw.rect(sup, cores[i], (x + i * 11, y0 + 5, 10, 15), 1)
        texto(sup, str(i + 1), x + i * 11 + 3, y0 + 8, cores[i], 13)


def bola(sup, x, y):
    pygame.draw.circle(sup, (250, 250, 250), (x, y), 4)
    pygame.draw.circle(sup, (40, 40, 40), (x, y), 4, 1)
    pygame.draw.circle(sup, (40, 40, 40), (x, y), 1)


def poca(sup, x, y):
    agua = pygame.Surface((22, 10), pygame.SRCALPHA)
    pygame.draw.ellipse(agua, (120, 170, 220, 170), (0, 1, 22, 8))
    pygame.draw.line(agua, (230, 245, 255, 220), (5, 3), (9, 3))
    sup.blit(agua, (x, y))


def mapa_parquinho(s):
    sup = pygame.Surface((LADO, LADO))
    faixas = FAIXAS_FUNDO[2]
    for i, tipo in enumerate(faixas):
        if tipo == "livre":
            grama(sup, i * F, s)
        else:
            terra(sup, i * F, s)
    for i, tipo in enumerate(faixas):
        if tipo == "corredor":
            if i == 0 or faixas[i - 1] != "corredor":
                beira_grama(sup, i * F, s, True)
            if i == 11 or faixas[i + 1] != "corredor":
                beira_grama(sup, i * F + F - 1, s, False)
    for i, tipo in enumerate(faixas):
        if tipo == "livre":
            for _ in range(7):
                flor(sup, s.randint(3, 296), i * F + s.randint(3, 21),
                     s.choice([(250, 250, 250), (240, 120, 160), (250, 200, 60), (170, 140, 240)]))
    placa_proximo(sup, 0, "SALAS", (150, 100, 50), (255, 255, 255))
    caixa_areia(sup, 30, 6 * F, s)
    amarelinha(sup, 205, 6 * F)
    bola(sup, 140, 2 * F + 12)
    poca(sup, 60, 9 * F + 7)
    caixa_areia(sup, 215, 11 * F, s)
    for _ in range(6):  # folhas na trilha
        i = s.choice([k for k, t in enumerate(faixas) if t == "corredor"])
        x = s.randint(3, 295)
        y = i * F + s.randint(3, 20)
        pygame.draw.polygon(sup, s.choice([(200, 120, 40), (170, 150, 40)]), [(x, y + 2), (x + 3, y), (x + 6, y + 2), (x + 3, y + 4)])
    return sup


def luz_janelas(sup, s, forca):
    luz = pygame.Surface((LADO, LADO), pygame.SRCALPHA)
    x = s.randint(-80, 0)
    while x < LADO:
        largura = s.randint(18, 30)
        pygame.draw.polygon(luz, (255, 250, 220, forca), [(x, 0), (x + largura, 0), (x + largura + 120, LADO), (x + 120, LADO)])
        x = x + largura + s.randint(50, 90)
    sup.blit(luz, (0, 0))


def sombra_arvores(sup, s):
    sombra = pygame.Surface((LADO, LADO), pygame.SRCALPHA)
    for _ in range(4):
        x = s.randint(0, LADO)
        y = s.randint(0, LADO)
        pygame.draw.ellipse(sombra, (20, 50, 20, 45), (x - 30, y - 15, 60, 30))
    sup.blit(sombra, (0, 0))


def gerar_fundo(numero):
    s = random.Random(200 + numero)
    if numero == 0:
        sup = mapa_corredor(s)
        luz_janelas(sup, s, 24)
    elif numero == 1:
        sup = mapa_cantina(s)
        luz_janelas(sup, s, 18)
    else:
        sup = mapa_parquinho(s)
        sombra_arvores(sup, s)
    return pygame.transform.scale(sup, (LADO * 2, LADO * 2))



# ------------------------------------------------------------ letreiros (fonte pixel art 5x7)
LETRAS = {
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", ".#.#.", ".#.#.", "..#.."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "Í": ["...#.", "..#..", ".###.", "..#..", "..#..", "..#..", ".###."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
}


def letreiro(msg, escala, cor, cor_clara, cor_escura, gotas):
    """Texto em pixel art: letras 5x7 com brilho em cima, sombra embaixo e contorno."""
    largura = len(msg) * 6
    peq = pygame.Surface((largura + 2, 7 + 2 + (3 if gotas else 0)), pygame.SRCALPHA)
    pontos = []
    for i, letra in enumerate(msg):
        for y, linha in enumerate(LETRAS[letra]):
            for x, c in enumerate(linha):
                if c == "#":
                    pontos.append((1 + i * 6 + x, 1 + y))
    contorno = (30, 10, 14)
    for (x, y) in pontos:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (1, 1)]:
            peq.set_at((x + dx, y + dy), contorno)
    for (x, y) in pontos:
        if y <= 2:
            peq.set_at((x, y), cor_clara)
        elif y >= 6:
            peq.set_at((x, y), cor_escura)
        else:
            peq.set_at((x, y), cor)
    if gotas:  # gotinhas de suor escorrendo
        for x in gotas:
            peq.set_at((x, 9), (120, 200, 255))
            peq.set_at((x, 10), (120, 200, 255))
    return pygame.transform.scale(peq, (peq.get_width() * escala, peq.get_height() * escala))



def gerar_fundos():
    for numero in range(3):
        salvar(gerar_fundo(numero), "fundo" + str(numero + 1) + ".png")


def gerar_letreiros():
    """GAME OVER vermelho com gotinhas de suor, e o título do jogo em amarelo."""
    salvar(letreiro("GAME OVER", 8, (220, 40, 40), (255, 110, 100), (150, 20, 30), [12, 30, 44]), "game_over.png")
    salvar(letreiro("SEGURA AÍ!", 7, (250, 200, 50), (255, 240, 150), (200, 130, 20), None), "titulo.png")


if __name__ == "__main__":
    pygame.init()
    os.makedirs(PASTA, exist_ok=True)
    gerar_personagens()
    gerar_fundos()
    gerar_letreiros()
    print("imagens geradas em", os.path.abspath(PASTA))
