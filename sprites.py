"""
Imagens do jogo. Tudo é desenhado por código (sem arquivos externos), mas se você
colocar PNGs com fundo transparente na pasta assets/ eles são usados no lugar:
    assets/ridley_fechada.png -> Ridley de boca fechada (quadro 1)
    assets/ridley_aberta.png  -> Ridley de boca aberta, rugindo (quadro 2)
    assets/npc.png      -> imagem do NPC (Baby Metroid)
    assets/arma.png     -> canhão de braço fixo na tela
    assets/vitoria.png  -> imagem comemorativa da tela de vitória
    assets/upgrade.png  -> imagem exibida no meio da tela ao pegar o upgrade de energia
"""
import math
import os
import pygame

PASTA_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def carregar_imagem(nome_arquivo, fallback):
    """Carrega assets/<nome_arquivo>; se não existir, usa a função `fallback`."""
    caminho = os.path.join(PASTA_ASSETS, nome_arquivo)
    if os.path.exists(caminho):
        try:
            return pygame.image.load(caminho).convert_alpha()
        except pygame.error:
            pass
    return fallback()


def criar_sprite_npc():
    """Cápsula com o bebê Metroid."""
    s = pygame.Surface((64, 64), pygame.SRCALPHA)
    # cápsula de vidro com o bebê Metroid
    pygame.draw.rect(s, (60, 70, 95), (40, 25, 22, 5))                                  # tampa
    pygame.draw.rect(s, (60, 70, 95), (40, 54, 22, 8))                                  # base
    pygame.draw.rect(s, (120, 235, 200), (42, 30, 18, 24))                              # vidro
    pygame.draw.circle(s, (80, 200, 110), (51, 41), 7)                                  # cúpula do Metroid
    pygame.draw.circle(s, (230, 60, 60), (48, 40), 2)                                   # núcleos
    pygame.draw.circle(s, (230, 60, 60), (54, 40), 2)
    for x in (47, 51, 55):                                                              # tentáculos
        pygame.draw.line(s, (60, 160, 90), (x, 46), (x, 51), 2)
    return s


def criar_sprite_boss(boca_aberta=False):
    """Ridley: corpo roxo, asas magenta e olhos laranja. `boca_aberta=True` = rugindo."""
    s = pygame.Surface((64, 64), pygame.SRCALPHA)
    corpo, escuro, claro = (118, 98, 170), (70, 55, 115), (160, 140, 210)
    asa, asa_esc = (225, 45, 140), (150, 25, 95)
    dente, olho = (240, 240, 228), (255, 150, 30)

    pygame.draw.polygon(s, asa, [(42, 30), (63, 5), (59, 22), (63, 38), (50, 44)])      # asa direita
    pygame.draw.polygon(s, asa, [(22, 30), (1, 5), (5, 22), (1, 38), (14, 44)])         # asa esquerda
    for ponta in ((63, 5), (59, 22), (63, 38)):
        pygame.draw.line(s, asa_esc, (42, 30), ponta, 1)
        pygame.draw.line(s, asa_esc, (22, 30), (64 - ponta[0], ponta[1]), 1)

    pygame.draw.line(s, escuro, (32, 54), (46, 61), 4)                                  # cauda
    pygame.draw.line(s, escuro, (46, 61), (58, 54), 3)

    pygame.draw.polygon(s, escuro, [(22, 46), (31, 46), (29, 63), (15, 63)])            # pernas
    pygame.draw.polygon(s, escuro, [(33, 46), (42, 46), (49, 63), (35, 63)])
    for x in (15, 19, 23, 35, 39, 43):                                                  # garras dos pés
        pygame.draw.line(s, dente, (x, 63), (x + 1, 60), 1)

    pygame.draw.polygon(s, corpo, [(22, 28), (42, 28), (45, 40), (40, 53), (24, 53), (19, 40)])  # tronco
    for y in (34, 39, 44):                                                              # costelas
        pygame.draw.line(s, claro, (25, y), (39, y), 1)
    pygame.draw.polygon(s, corpo, [(28, 20), (36, 20), (38, 30), (26, 30)])             # pescoço

    pygame.draw.polygon(s, corpo, [(20, 30), (25, 32), (14, 47), (9, 44)])              # braços
    pygame.draw.polygon(s, corpo, [(44, 30), (39, 32), (50, 47), (55, 44)])
    for dx in (0, 3, 6):                                                                # garras das mãos
        pygame.draw.line(s, dente, (9 + dx, 44), (6 + dx, 50), 1)
        pygame.draw.line(s, dente, (55 - dx, 44), (58 - dx, 50), 1)

    pygame.draw.polygon(s, claro, [(24, 5), (40, 5), (43, 14), (38, 21), (26, 21), (21, 14)])  # crânio
    pygame.draw.polygon(s, escuro, [(24, 5), (20, 0), (29, 3)])                         # chifres
    pygame.draw.polygon(s, escuro, [(40, 5), (44, 0), (35, 3)])
    pygame.draw.rect(s, olho, (26, 10, 5, 3))                                           # olhos
    pygame.draw.rect(s, olho, (34, 10, 5, 3))
    if boca_aberta:                                                                     # rugindo
        pygame.draw.rect(s, (60, 10, 30), (26, 17, 12, 13))                             # boca aberta
        for x in (27, 31, 35):                                                          # dentes de cima
            pygame.draw.polygon(s, dente, [(x, 17), (x + 2, 17), (x + 1, 22)])
        for x in (28, 33):                                                              # dentes de baixo
            pygame.draw.polygon(s, dente, [(x, 30), (x + 2, 30), (x + 1, 26)])
        pygame.draw.polygon(s, escuro, [(26, 30), (38, 30), (36, 35), (28, 35)])        # mandíbula baixa
    else:
        pygame.draw.rect(s, (60, 10, 30), (27, 18, 10, 4))                              # boca
        for x in (27, 31, 35):                                                          # dentes
            pygame.draw.polygon(s, dente, [(x, 18), (x + 2, 18), (x + 1, 23)])
        pygame.draw.polygon(s, escuro, [(26, 22), (38, 22), (36, 28), (28, 28)])        # mandíbula
    return s


def criar_trofeu():
    """Imagem comemorativa padrão (um troféu), usada se assets/vitoria.png não existir."""
    s = pygame.Surface((300, 300), pygame.SRCALPHA)
    ouro, escuro = (240, 190, 40), (180, 130, 20)
    pygame.draw.arc(s, ouro, (10, 50, 90, 100), math.pi / 2, 3 * math.pi / 2, 10)        # alças
    pygame.draw.arc(s, ouro, (200, 50, 90, 100), -math.pi / 2, math.pi / 2, 10)
    pygame.draw.polygon(s, ouro, [(60, 30), (240, 30), (220, 150), (150, 200), (80, 150)])  # taça
    pygame.draw.rect(s, escuro, (135, 195, 30, 50))
    pygame.draw.rect(s, ouro, (90, 240, 120, 30))
    pontos = []
    for i in range(10):                                                                  # estrela
        raio = 42 if i % 2 == 0 else 17
        ang = -math.pi / 2 + i * math.pi / 5
        pontos.append((150 + raio * math.cos(ang), 95 + raio * math.sin(ang)))
    pygame.draw.polygon(s, (255, 255, 210), pontos)
    return s


def criar_arma():
    """Canhão de braço padrão, usado se assets/arma.png não existir."""
    s = pygame.Surface((120, 180), pygame.SRCALPHA)
    pygame.draw.rect(s, (70, 70, 80), (40, 40, 40, 140))
    pygame.draw.rect(s, (110, 110, 125), (48, 10, 24, 40))
    pygame.draw.rect(s, (255, 200, 60), (56, 0, 8, 12))
    pygame.draw.rect(s, (30, 30, 40), (40, 40, 40, 140), 3)
    return s


def criar_icone_upgrade():
    """Ícone padrão do upgrade (um tanque de energia), usado se assets/upgrade.png não existir."""
    s = pygame.Surface((160, 160), pygame.SRCALPHA)
    pygame.draw.rect(s, (20, 40, 110), (20, 20, 120, 120), border_radius=18)
    pygame.draw.rect(s, (80, 200, 255), (20, 20, 120, 120), 6, border_radius=18)
    pygame.draw.rect(s, (255, 190, 40), (40, 40, 80, 80), border_radius=8)
    pygame.draw.rect(s, (60, 30, 0), (56, 52, 8, 56))                                   # letra E
    for y in (52, 76, 100):
        pygame.draw.rect(s, (60, 30, 0), (56, y, 48, 8))
    return s