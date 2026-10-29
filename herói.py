from personagem import Personagem  # Importa a classe Personagem
from utils import registro

class Heroi(Personagem):
    """
    A classe Heroi representa as características de um herói no jogo.
    Herda da classe Personagem.
    """
    NIVEIS_VALIDOS = ['Baixa', 'Média', 'Alta']

    def __init__(self, nome, idade, vida, bondade, ataque, defesa):
        super().__init__(nome, idade, vida, ataque, defesa)
        if bondade not in self.NIVEIS_VALIDOS:
            raise ValueError(f"Nível de bondade inválido! Escolha entre {self.NIVEIS_VALIDOS}")
        self.bondade = bondade
        self.inventario = {"recarga": 2}

    def usar_recarga(self, cura=50):
        """Usa uma recarga de energia. Devolve True se conseguiu usar."""
        if self.inventario.get("recarga", 0) <= 0:
            registro.adicionar("Você não tem mais recargas de energia!")
            return False
        if self.vida >= self.vida_max:
            registro.adicionar("Sua energia já está cheia.")
            return False
        self.inventario["recarga"] -= 1
        self.vida = min(self.vida + cura, self.vida_max)
        registro.adicionar(f"{self.nome} usou uma recarga (+{cura}). Energia: {self.vida}/{self.vida_max}.")
        return True

    def __str__(self):
        return f'Herói: {self.nome}, Idade: {self.idade}, Vida: {self.vida}/{self.vida_max}, Bondade: {self.bondade}'