import random
from utils import registro


class Personagem:
    """
    Classe base de todos os personagens do jogo (herói, vilão e NPC).
    """

    def __init__(self, nome, idade, vida, ataque=5, defesa=0):
        self.nome = nome
        self.idade = idade
        self.vida = vida
        self.vida_max = vida
        self.ataque = ataque
        self.defesa = defesa
        self.falas = []        # lista de falas do personagem
        self.inventario = {}   # dicionário: item -> quantidade

    @property
    def vivo(self):
        return self.vida > 0

    def status(self):
        """Devolve os atributos do personagem em um dicionário."""
        return {
            "nome": self.nome,
            "idade": self.idade,
            "vida": self.vida,
            "vida_max": self.vida_max,
            "ataque": self.ataque,
            "defesa": self.defesa,
            "inventario": dict(self.inventario),
        }

    def receber_dano(self, dano_bruto):
        """Aplica o dano descontando a defesa (mínimo de 1) e devolve o dano real."""
        dano = max(1, dano_bruto - self.defesa)
        self.vida = max(0, self.vida - dano)
        return dano

    def atacar(self, alvo):
        """Ataca outro personagem. O dano varia um pouco a cada golpe."""
        dano_bruto = self.ataque + random.randint(0, 4)
        dano = alvo.receber_dano(dano_bruto)
        registro.adicionar(f"{self.nome} atacou {alvo.nome} e causou {dano} de dano.")
        return dano

    def upgrade_vida(self, incremento=10):
        """Aumenta a vida máxima e cura o mesmo valor."""
        self.vida_max += incremento
        self.vida = min(self.vida + incremento, self.vida_max)
        registro.adicionar(f"Vida de {self.nome} aumentou +{incremento} (agora {self.vida}/{self.vida_max}).")

    def update_nome(self, nome_editado):
        """
        Atualiza o nome do personagem.
        """
        self.nome = nome_editado

    def dialogar(self):
        """Devolve uma fala aleatória do personagem e a registra no histórico."""
        if not self.falas:
            return "..."
        fala = random.choice(self.falas)
        registro.adicionar(f'{self.nome} diz: "{fala}"')
        return fala

    def __str__(self):
        return f'Personagem: {self.nome}, Idade: {self.idade}, Vida: {self.vida}/{self.vida_max}'
