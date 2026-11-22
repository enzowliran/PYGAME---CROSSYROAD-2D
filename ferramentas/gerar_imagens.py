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


# ------------------------------------------------------------ fundos
# Cada fundo tem 12 faixas (de cima para baixo). TEM que ser igual à lista FAIXAS_FUNDO do jogo.py
FAIXAS_FUNDO = [
    ["livre", "corredor", "corredor", "corredor", "livre", "corredor",
     "corredor", "livre", "corredor", "corredor", "livre", "livre"],
    ["livre", "corredor", "corredor", "livre", "corredor", "corredor",
     "corredor", "livre", "livre", "corredor", "corredor", "livre"],
]
F = 25          # tamanho de uma faixa no desenho pequeno (vira 50 pixels na escala 2)
LADO = 300      # o desenho pequeno tem 300 x 300 e vira 600 x 600


def varia(cor, quanto, sorteio):
    """Cor parecida, um pouco mais clara ou escura (textura)."""
    d = sorteio.randint(-quanto, quanto)
    return tuple(max(0, min(255, c + d)) for c in cor)


def ponto(sup, x, y, cor):
    if 0 <= x < LADO and 0 <= y < LADO:
        sup.set_at((x, y), cor)


def piso_azulejo(sup, y0, sorteio):
    """Faixa livre do fundo 1: azulejos creme, alinhados com as casas do jogo."""
    for coluna in range(LADO // F):
        base = (232, 220, 192) if (coluna + y0 // F) % 2 == 0 else (220, 206, 176)
        base = varia(base, 4, sorteio)
        pygame.draw.rect(sup, base, (coluna * F, y0, F, F))
        pygame.draw.line(sup, (255, 248, 228), (coluna * F + 1, y0 + 1), (coluna * F + F - 2, y0 + 1))
        pygame.draw.line(sup, (255, 248, 228), (coluna * F + 1, y0 + 1), (coluna * F + 1, y0 + F - 2))
        pygame.draw.rect(sup, (176, 160, 132), (coluna * F, y0, F, F), 1)
        for _ in range(6):
            ponto(sup, coluna * F + sorteio.randint(2, F - 3), y0 + sorteio.randint(2, F - 3), varia(base, 18, sorteio))


def piso_madeira(sup, y0, sorteio):
    """Faixa livre do fundo 2: assoalho de madeira (tábuas)."""
    for linha in range(5):
        y = y0 + linha * 5
        x = -sorteio.randint(0, 40)
        while x < LADO:
            comprimento = sorteio.randint(30, 60)
            cor = varia((178, 122, 72), 12, sorteio)
            pygame.draw.rect(sup, cor, (x, y, comprimento, 5))
            for _ in range(comprimento // 6):
                gx = x + sorteio.randint(1, comprimento - 2)
                pygame.draw.line(sup, varia(cor, 20, sorteio), (gx, y + 2), (gx + sorteio.randint(2, 6), y + 2))
            pygame.draw.line(sup, (120, 78, 44), (x, y + 4), (x + comprimento, y + 4))
            pygame.draw.line(sup, (120, 78, 44), (x, y), (x, y + 4))
            x = x + comprimento


def piso_corredor(sup, y0, sorteio, base):
    """Faixa de corredor (onde andam os obstáculos): piso liso com marcas de uso."""
    pygame.draw.rect(sup, base, (0, y0, LADO, F))
    for _ in range(160):
        ponto(sup, sorteio.randint(0, LADO - 1), y0 + sorteio.randint(0, F - 1), varia(base, 10, sorteio))
    for _ in range(4):  # marcas de sapato / riscos
        x = sorteio.randint(0, LADO - 20)
        y = y0 + sorteio.randint(4, F - 5)
        escura = tuple(max(0, c - 22) for c in base)
        pygame.draw.line(sup, escura, (x, y), (x + sorteio.randint(6, 18), y))


def bordas(sup, faixas, cor_tracejado, cor_borda, listras_alerta):
    """Linhas entre faixas de corredor (tracejadas) e na beirada dos corredores."""
    for i in range(12):
        if faixas[i] != "corredor":
            continue
        y0 = i * F
        if i > 0 and faixas[i - 1] == "corredor":
            for x in range(4, LADO, 16):
                pygame.draw.line(sup, cor_tracejado, (x, y0), (x + 7, y0))
        if i == 0 or faixas[i - 1] != "corredor":
            desenhar_beirada(sup, y0, cor_borda, listras_alerta)
        if i == 11 or faixas[i + 1] != "corredor":
            desenhar_beirada(sup, y0 + F - 3, cor_borda, listras_alerta)


def desenhar_beirada(sup, y, cor, listras_alerta):
    if listras_alerta:
        for x in range(0, LADO, 8):
            pygame.draw.polygon(sup, (250, 200, 40), [(x, y), (x + 4, y), (x + 7, y + 3), (x + 3, y + 3)])
            pygame.draw.polygon(sup, (40, 40, 40), [(x + 4, y), (x + 8, y), (x + 11, y + 3), (x + 7, y + 3)])
    else:
        pygame.draw.rect(sup, cor, (0, y, LADO, 3))


def ralo(sup, x, y):
    pygame.draw.rect(sup, (150, 150, 150), (x, y, 9, 9))
    pygame.draw.rect(sup, (90, 90, 90), (x, y, 9, 9), 1)
    for i in range(2, 8, 2):
        pygame.draw.line(sup, (70, 70, 70), (x + 2, y + i), (x + 6, y + i))


def papel(sup, x, y, sorteio):
    pygame.draw.polygon(sup, (245, 245, 240), [(x, y), (x + 5, y + 1), (x + 4, y + 5), (x - 1, y + 4)])
    pygame.draw.line(sup, (150, 170, 220), (x + 1, y + 2), (x + 3, y + 2))


def placa_wc(sup, x, y0, cor):
    """'WC' com seta pintada no chão: o banheiro está sempre lá na frente!"""
    fonte = pygame.font.Font(None, 16)
    texto = fonte.render("WC", False, cor)
    sup.blit(texto, (x, y0 + 7))
    pygame.draw.line(sup, cor, (x + 22, y0 + 18), (x + 22, y0 + 7), 2)
    pygame.draw.polygon(sup, cor, [(x + 18, y0 + 9), (x + 22, y0 + 4), (x + 26, y0 + 9)])



def poca(sup, x, y, sorteio):
    """Poça d'água (alguém não segurou...)."""
    agua = pygame.Surface((26, 12), pygame.SRCALPHA)
    pygame.draw.ellipse(agua, (130, 190, 240, 150), (0, 2, 18, 9))
    pygame.draw.ellipse(agua, (130, 190, 240, 150), (9, 0, 17, 10))
    pygame.draw.line(agua, (235, 248, 255, 220), (6, 4), (10, 4))
    sup.blit(agua, (x, y))


def amarelinha(sup, x, y0):
    cores = [(230, 80, 80), (250, 190, 50), (80, 170, 90), (70, 130, 220), (170, 90, 200)]
    for i in range(5):
        pygame.draw.rect(sup, cores[i], (x + i * 10, y0 + 6, 9, 13), 1)
        pygame.draw.line(sup, cores[i], (x + i * 10 + 3, y0 + 12), (x + i * 10 + 5, y0 + 12))


def tapete(sup, y0):
    """Tapete da entrada, na largada (duas faixas de baixo)."""
    pygame.draw.rect(sup, (150, 40, 50), (90, y0 + 4, 120, 2 * F - 8))
    pygame.draw.rect(sup, (220, 180, 70), (90, y0 + 4, 120, 2 * F - 8), 2)
    pygame.draw.rect(sup, (220, 180, 70), (96, y0 + 10, 108, 2 * F - 20), 1)
    fonte = pygame.font.Font(None, 16)
    texto = fonte.render("BEM-VINDO", False, (240, 220, 160))
    sup.blit(texto, (150 - texto.get_width() // 2, y0 + F - 4))


def folha(sup, x, y, sorteio):
    cor = sorteio.choice([(200, 120, 40), (180, 150, 40), (150, 80, 30)])
    pygame.draw.polygon(sup, cor, [(x, y + 2), (x + 3, y), (x + 6, y + 2), (x + 3, y + 4)])
    pygame.draw.line(sup, (100, 60, 20), (x, y + 2), (x + 6, y + 2))


def texto_no_chao(sup, texto, x, y, cor, tamanho):
    fonte = pygame.font.Font(None, tamanho)
    imagem = fonte.render(texto, False, cor)
    imagem.set_alpha(170)
    sup.blit(imagem, (x, y))


def luz_das_janelas(sup, sorteio):
    """Faixas de luz entrando pelas janelas, na diagonal, por cima de tudo."""
    luz = pygame.Surface((LADO, LADO), pygame.SRCALPHA)
    x = sorteio.randint(-80, 0)
    while x < LADO:
        largura = sorteio.randint(18, 30)
        pygame.draw.polygon(luz, (255, 250, 220, 26), [(x, 0), (x + largura, 0), (x + largura + 120, LADO), (x + 120, LADO)])
        x = x + largura + sorteio.randint(50, 90)
    sup.blit(luz, (0, 0))


def gerar_fundo(numero):
    sorteio = random.Random(100 + numero)
    faixas = FAIXAS_FUNDO[numero]
    sup = pygame.Surface((LADO, LADO))
    for i in range(12):
        y0 = i * F
        if faixas[i] == "livre":
            if numero == 0:
                piso_azulejo(sup, y0, sorteio)
            else:
                piso_madeira(sup, y0, sorteio)
        else:
            if numero == 0:
                piso_corredor(sup, y0, sorteio, (96, 112, 138))
            else:
                piso_corredor(sup, y0, sorteio, (128, 128, 124))
    if numero == 0:
        bordas(sup, faixas, (220, 226, 236), (60, 70, 90), False)
    else:
        bordas(sup, faixas, (240, 240, 230), (0, 0, 0), True)

    # detalhes nas faixas livres
    for i in range(12):
        if faixas[i] != "livre":
            continue
        y0 = i * F
        for _ in range(2):
            papel(sup, sorteio.randint(5, LADO - 10), y0 + sorteio.randint(4, F - 8), sorteio)
        if numero == 0:
            if i == 0:
                placa_wc(sup, 135, y0, (60, 110, 190))
            if i == 4:
                ralo(sup, 233, y0 + 8)
                poca(sup, 240, y0 + 10, sorteio)
            if i == 7:
                amarelinha(sup, 30, y0)
                ralo(sup, 258, y0 + 8)
            if i == 10:
                tapete(sup, y0)
        else:
            for _ in range(5):
                folha(sup, sorteio.randint(5, LADO - 10), y0 + sorteio.randint(3, F - 6), sorteio)
            if i == 0:
                texto_no_chao(sup, "CANTINA", 110, y0 + 6, (90, 50, 20), 22)
            if i in (3, 7):
                placa_wc(sup, 35 if i == 3 else 235, y0, (250, 240, 220))
            if i == 8:
                poca(sup, 160, y0 + 8, sorteio)
            if i == 11:
                ralo(sup, 135, y0 + 8)

    luz_das_janelas(sup, sorteio)
    return pygame.transform.scale(sup, (LADO * 2, LADO * 2))


def gerar_fundos():
    salvar(gerar_fundo(0), "fundo1.png")
    salvar(gerar_fundo(1), "fundo2.png")


if __name__ == "__main__":
    pygame.init()
    os.makedirs(PASTA, exist_ok=True)
    gerar_personagens()
    gerar_fundos()
    print("imagens geradas em", os.path.abspath(PASTA))
