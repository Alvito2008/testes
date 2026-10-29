"""
Renderização 3D por raycasting: para cada coluna da tela lançamos um raio,
descobrimos a parede atingida e desenhamos uma linha vertical cuja altura
depende da distância. Depois desenhamos os sprites (NPC, chefe) por cima.
"""
import math
import pygame
 
COR_PAREDE = {1: (40, 90, 190), 2: (95, 115, 150), 3: (200, 40, 70)}  # azul Ceres, aço, porta selada vermelha
COR_CEU = (8, 10, 40)
PLANO = 0.66        # controla o campo de visão (~66 graus)
DIST_MAX = 16.0
 
 
def renderizar(tela, mapa, px, py, ang, entidades, alarme=0.0):
    largura, altura = tela.get_size()
    dir_x, dir_y = math.cos(ang), math.sin(ang)
    plano_x, plano_y = -dir_y * PLANO, dir_x * PLANO
 
    # teto e chão (chão em faixas para dar sensação de profundidade)
    cor_teto = (COR_CEU[0] + int(110 * alarme), COR_CEU[1], COR_CEU[2])  # alarme: teto pisca em vermelho
    tela.fill(cor_teto, (0, 0, largura, altura // 2))
    faixas = 8
    altura_faixa = (altura // 2) // faixas + 1
    for i in range(faixas):
        tom = 25 + i * 9
        tela.fill((tom // 5, tom // 3, tom), (0, altura // 2 + i * (altura // 2) // faixas, largura, altura_faixa))
 
    zbuffer = [0.0] * largura
    for col in range(largura):
        camera = 2 * col / largura - 1
        rdx = dir_x + plano_x * camera
        rdy = dir_y + plano_y * camera
        dist, tipo, lado, impacto = mapa.lancar_raio(px, py, rdx, rdy)
        dist = max(dist, 0.0001)
        zbuffer[col] = dist
 
        h = int(altura / dist)
        topo = (altura - h) // 2
        fator = max(0.2, 1 - dist / DIST_MAX)
        if lado == 1:
            fator *= 0.7
        if int(impacto * 4) % 2:
            fator *= 0.88  # listras verticais = "tijolos"
        base = COR_PAREDE.get(tipo, (150, 150, 150))
        cor = (int(base[0] * fator), int(base[1] * fator), int(base[2] * fator))
        pygame.draw.line(tela, cor, (col, max(topo, 0)), (col, min(topo + h, altura - 1)))
 
    # sprites: do mais distante para o mais próximo
    det = plano_x * dir_y - dir_x * plano_y
    ordenadas = sorted(entidades, key=lambda e: -((e.x - px) ** 2 + (e.y - py) ** 2))
    for e in ordenadas:
        dx, dy = e.x - px, e.y - py
        lateral = (dir_y * dx - dir_x * dy) / det
        profundidade = (-plano_y * dx + plano_x * dy) / det
        if profundidade < 0.2:
            continue
        tam = int(altura / profundidade)   # altura de uma parede nessa distância
        imagem = e.imagem_atual
        larg_img, alt_img = imagem.get_size()
        alt_sprite = int(tam * e.escala)
        larg_sprite = int(alt_sprite * larg_img / alt_img)   # mantém a proporção da imagem
        if alt_sprite <= 0 or larg_sprite <= 0:
            continue
        centro = int((largura / 2) * (1 + lateral / profundidade))
        x0 = centro - larg_sprite // 2
        y0 = (altura + tam) // 2 - alt_sprite              # os "pés" ficam no chão
        y0 -= int((0.5 + 0.5 * math.sin(e.tempo * 3.0)) * e.flutuacao * tam)   # flutuação (só para cima)
 
        if e.flash > 0:
            imagem = imagem.copy()
            imagem.fill((110, 110, 110), special_flags=pygame.BLEND_RGB_ADD)
        imagem = pygame.transform.scale(imagem, (larg_sprite, alt_sprite))
        for c in range(max(0, x0), min(largura, x0 + larg_sprite)):
            if zbuffer[c] > profundidade:
                tela.blit(imagem, (c, y0), (c - x0, 0, 1, alt_sprite))