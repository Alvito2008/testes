import math


class Entidade:
    """
    Liga um Personagem (dados do jogo) a uma posição no mapa e a uma imagem (sprite).
    """

    def __init__(self, personagem, x, y, sprite, escala=1.0, sprite_boca_aberta=None, flutuacao=0.0):
        self.personagem = personagem
        self.x = x
        self.y = y
        self.sprite = sprite
        self.escala = escala  # tamanho relativo: 1.0 = altura da parede, 0.5 = metade
        self.sprite_boca_aberta = sprite_boca_aberta   # 2º quadro da animação (usado ao rugir)
        self.rugindo = 0.0     # tempo restante com a boca aberta
        self.flutuacao = flutuacao   # quanto o sprite sobe e desce (fração da altura da parede)
        self.tempo = 0.0       # relógio da entidade (para a flutuação)
        self.flash = 0.0     # tempo restante do "piscar" ao levar dano
        self.ativa = True    # False = não aparece nem colide (ex.: NPC que sumiu)

    @property
    def imagem_atual(self):
        """Escolhe o quadro da animação: boca aberta enquanto estiver rugindo."""
        if self.rugindo > 0 and self.sprite_boca_aberta is not None:
            return self.sprite_boca_aberta
        return self.sprite

    def distancia(self, x, y):
        return math.hypot(self.x - x, self.y - y)