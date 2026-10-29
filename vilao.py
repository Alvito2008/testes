from personagem import Personagem

class Vilao(Personagem):
    """
    A classe Vilao representa as características de um vilão no jogo.
    Herda da classe Personagem.
    """
    NIVEIS_VALIDOS = ['Baixa', 'Média', 'Alta']

    def __init__(self, nome, idade, vida, maldade, ataque, defesa, falas_vilao=None):
        super().__init__(nome, idade, vida, ataque, defesa)
        if maldade not in self.NIVEIS_VALIDOS:
            raise ValueError(f"Nível de maldade inválido! Escolha entre {self.NIVEIS_VALIDOS}")
        self.maldade = maldade
        self.falas_vilao = falas_vilao or ["Seu fim chegou, herói!", "Ninguém sai vivo daqui!"]

    def __str__(self):
        return f'Vilão: {self.nome}, Idade: {self.idade}, Vida: {self.vida}/{self.vida_max}, Maldade: {self.maldade}'

