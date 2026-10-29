"""
O mapa do jogo: uma grade (lista de listas) onde 0 = chão e outros números = paredes.
"""
import math

LARGURA, ALTURA = 24, 14
PORTA = (7, 6)  # (x, y) da passagem entre a sala inicial e a arena
TAMANHO_TEXTURA = 256
METADE_TEXTURA = TAMANHO_TEXTURA // 2

class Mapa:
    def __init__(self):
        self.grade = [[1] * LARGURA for _ in range(ALTURA)]
        self._escavar(1, 1, 6, 12)    # sala inicial
        self._escavar(8, 1, 22, 12)   # arena
        self.grade[PORTA[1]][PORTA[0]] = 0  # abre a passagem
        for x, y in [(10, 3), (18, 3), (10, 9), (18, 9)]:  # pilares da arena
            self.grade[y][x] = 2

    def _escavar(self, x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.grade[y][x] = 0

    def selar_porta(self):
        """Fecha a passagem: a arena vira uma sala trancada."""
        self.grade[PORTA[1]][PORTA[0]] = 3

    def livre(self, x, y, raio=0.0):
        """True se a posição (com uma folga `raio`) não encosta em nenhuma parede."""
        for ox in (-raio, raio):
            for oy in (-raio, raio):
                cx, cy = int(x + ox), int(y + oy)
                if not (0 <= cx < LARGURA and 0 <= cy < ALTURA):
                    return False
                if self.grade[cy][cx] != 0:
                    return False
        return True

    def lancar_raio(self, px, py, rdx, rdy):
        """
        Algoritmo DDA do raycasting: anda de quadrado em quadrado ao longo do raio
        até bater numa parede. Devolve (distância perpendicular, tipo da parede,
        lado atingido, ponto exato do impacto na parede de 0 a 1).
        """
        mx, my = int(px), int(py)
        delta_x = abs(1 / rdx) if rdx != 0 else 1e30
        delta_y = abs(1 / rdy) if rdy != 0 else 1e30

        if rdx < 0:
            passo_x, lado_x = -1, (px - mx) * delta_x
        else:
            passo_x, lado_x = 1, (mx + 1 - px) * delta_x
        if rdy < 0:
            passo_y, lado_y = -1, (py - my) * delta_y
        else:
            passo_y, lado_y = 1, (my + 1 - py) * delta_y

        lado = 0
        tipo = 1
        while True:
            if lado_x < lado_y:
                lado_x += delta_x
                mx += passo_x
                lado = 0
            else:
                lado_y += delta_y
                my += passo_y
                lado = 1
            if not (0 <= mx < LARGURA and 0 <= my < ALTURA):
                tipo = 1
                break
            tipo = self.grade[my][mx]
            if tipo:
                break

        dist = (lado_x - delta_x) if lado == 0 else (lado_y - delta_y)
        if lado == 0:
            impacto = py + dist * rdy
        else:
            impacto = px + dist * rdx
        impacto -= math.floor(impacto)
        return dist, tipo, lado, impacto