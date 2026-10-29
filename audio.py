"""
Sons e músicas do jogo, usando pygame.mixer.

  - Efeitos (tiro, dano...): pygame.mixer.Sound  -> carregados na memória, tocam vários ao mesmo tempo.
  - Música de fundo:         pygame.mixer.music  -> tocada por "streaming", uma de cada vez.

Os arquivos ficam em assets/sons/. Se algum arquivo não existir, o jogo simplesmente
roda sem aquele som (não dá erro), então você pode trocar os arquivos aos poucos.
"""
import os
import pygame

PASTA_SONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "sons")
EXTENSOES = (".ogg", ".wav", ".mp3")

class Audio:
    def __init__(self):
        self.efeitos = {}      # dicionário: nome -> pygame.mixer.Sound
        self.mudo = False
        self.ativo = True
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except pygame.error:   # computador sem placa de som
            self.ativo = False

    def _caminhos(self, arquivo):
        """Caminhos possíveis: a extensão pedida primeiro, depois as outras."""
        base, ext = os.path.splitext(arquivo)
        ordem = [ext] if ext else []
        ordem += [e for e in EXTENSOES if e.lower() != ext.lower()]
        return [os.path.join(PASTA_SONS, base + e) for e in ordem]

    def _avisar(self, caminho, erro):
        print(f"[áudio] Não foi possível usar '{os.path.basename(caminho)}': {erro}")
        print("Dica: regrave como WAV PCM 16 bits ou use .ogg")

    def carregar(self, nome, arquivo, volume=0.25):
        """Carrega um efeito sonoro e o guarda com um apelido (ex.: "tiro")."""
        if not self.ativo:
            return
        for caminho in self._caminhos(arquivo):
            if not os.path.exists(caminho):
                continue
            try:
                som = pygame.mixer.Sound(caminho)
            except pygame.error as erro:
                self._avisar(caminho, erro)
                continue
            som.set_volume(volume)
            self.efeitos[nome] = som
            return

    def tocar(self, nome):
        som = self.efeitos.get(nome)
        if som and not self.mudo:
            for nome_efeito in self.efeitos:
                self.pausar_som(nome_efeito)
            som.play()

    def duracao(self, nome, padrao=1.0):
        """Duração em segundos de um efeito já carregado."""
        som = self.efeitos.get(nome)
        return som.get_length() if som else padrao

    def pausar_som(self, nome):
        som = self.efeitos.get(nome)
        if som:
            som.stop()

    def musica(self, arquivo, volume=0.4):
        """Troca a música de fundo (toca em loop). A anterior é interrompida."""
        if not self.ativo:
            return
        for caminho in self._caminhos(arquivo):
            if not os.path.exists(caminho):
                continue
            try:
                pygame.mixer.music.load(caminho)
            except pygame.error as erro:
                self._avisar(caminho, erro)
                continue
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)       # -1 = repetir para sempre
            if self.mudo:
                pygame.mixer.music.pause()
            return

    def pausar_musica(self):
        if self.ativo:
            pygame.mixer.music.pause()

    def retomar_musica(self):
        if self.ativo and not self.mudo:
            pygame.mixer.music.unpause()

    def parar_musica(self, fade_ms=600):
        if self.ativo:
            pygame.mixer.music.fadeout(fade_ms)

    def alternar_mudo(self):
        """Tecla M: liga/desliga todo o som."""
        self.mudo = not self.mudo
        if self.ativo:
            if self.mudo:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()