"""
Funções auxiliares do jogo: registro de ações (log) e quebra de texto.
"""
import time
from datetime import datetime


class RegistroAcoes:
    """Guarda o histórico de tudo o que acontece no jogo (requisito do README)."""

    def __init__(self):
        self.eventos = []  # lista de dicionários: {"hora": ..., "texto": ..., "t": ...}

    def adicionar(self, texto):
        self.eventos.append({
            "hora": datetime.now().strftime("%H:%M:%S"),
            "texto": texto,
            "t": time.time(),
        })

    def recentes(self, s=6, quantidade=4):
        """Últimos eventos ocorridos nos últimos `s` segundos."""
        agora = time.time()
        validos = [ev["texto"] for ev in self.eventos if agora - ev["t"] <= s]
        return validos[-quantidade:]

    def limpar(self):
        self.eventos.clear()

    def salvar(self, caminho="registro_do_jogo.txt"):
        with open(caminho, "w", encoding="utf-8") as arquivo:
            for e in self.eventos:
                arquivo.write(f"[{e['hora']}] {e['texto']}\n")


# Instância única, usada por todas as classes
registro = RegistroAcoes()


def quebrar_texto(texto, fonte, largura_max):
    """Quebra um texto em várias linhas que cabem em `largura_max` pixels."""
    linhas = []
    atual = ""
    for palavra in texto.split():
        teste = (atual + " " + palavra).strip()
        if fonte.size(teste)[0] <= largura_max:
            atual = teste
        else:
            linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas
