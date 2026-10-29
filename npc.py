from personagem import Personagem


class NPC(Personagem):
    """
    Personagem não jogável. Conversa com o herói e concede um bônus de vida.
    """

    def __init__(self, nome, idade, vida, falas, bonus_vida=30):
        super().__init__(nome, idade, vida, ataque=0, defesa=0)
        self.falas = falas
        self.bonus_vida = bonus_vida
        self.indice = 0
        self.interagido = False

    def proxima_fala(self):
        """Devolve a próxima fala da conversa, ou None quando ela termina."""
        if self.indice >= len(self.falas):
            return None
        fala = self.falas[self.indice]
        self.indice += 1
        return fala

    def __str__(self):
        return f'NPC: {self.nome}, Idade: {self.idade}'
