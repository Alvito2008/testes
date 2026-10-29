import math
import random
import pygame
import raycaster
import sprites
from audio import Audio
from herói import Heroi
from mapa import Mapa
from mundo import Entidade
from npc import NPC
from utils import registro, quebrar_texto
from vilao import Vilao
from config import *

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Estação Ceres - Encontro com Ridley")
        self.relogio = pygame.time.Clock()
        self.interno = pygame.Surface(RESOLUCAO)
        self.veu = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)

        self.fonte = pygame.font.Font(None, 32)
        self.fonte_peq = pygame.font.Font(None, 24)
        self.fonte_media = pygame.font.Font(None, 52)
        self.fonte_grande = pygame.font.Font(None, 120)

        self.sprite_npc = sprites.carregar_imagem("npc.png", sprites.criar_sprite_npc)
        self.sprite_boss = sprites.carregar_imagem("ridley_fechada.png", sprites.criar_sprite_boss)
        self.sprite_boss_aberta = sprites.carregar_imagem(
            "ridley_aberta.png", lambda: sprites.criar_sprite_boss(boca_aberta=True))
        img = sprites.carregar_imagem("vitoria.png", sprites.criar_trofeu)
        l, a = img.get_size()
        esc = min(420 / l, 300 / a)
        self.img_vitoria = pygame.transform.smoothscale(img, (int(l * esc), int(a * esc)))

        arma = sprites.carregar_imagem("arma.png", sprites.criar_arma)
        l, a = arma.get_size()
        self.img_arma = pygame.transform.smoothscale(arma, (int(l * 1.5), int(a * 1.5)))

        img = sprites.carregar_imagem("upgrade.png", sprites.criar_icone_upgrade)
        l, a = img.get_size()
        esc = min(360 / l, 360 / a)
        escalar = pygame.transform.scale if esc > 1 else pygame.transform.smoothscale
        self.img_upgrade = escalar(img, (int(l * esc), int(a * esc)))

        self.audio = Audio()
        for nome in ("tiro", "acerto", "dano", "dialogo", "upgrade", "porta",
                     "rugido", "recarga", "vitoria", "morte"):
            self.audio.carregar(nome, nome + ".wav")

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.rodando = True
        self.novo_jogo()

    def novo_jogo(self):
        self.mapa = Mapa()
        self.heroi = Heroi('Samus Aran', 27, 99, 'Alta', 18, 5)
        self.px, self.py, self.ang = 3.5, 6.5, 0.0

        self.npc = NPC('Metroid bebê', 41, 50, falas=[
            "(SAMUS) Como um bebê Metroid pode dar tanto trabalho de proteger?",
            "(SAMUS) Algo está errado, os alarmes da estação dispararam e os sensores detectam uma presença enorme.",
            "(SAMUS) Que bom que eu trouxe um Tanque de Energia extra. Ele aumentará minha energia máxima.",
            "(SAMUS) É o Ridley! Ele veio atrás do bebê Metroid, tenho que impedi-lo!",
        ], bonus_vida=100)
        self.ent_npc = Entidade(self.npc, 12.5, 6.5, self.sprite_npc, escala=0.5)
        self.vilao = None
        self.ent_boss = None

        self.estado = "jogando"   # jogando | dialogo | morreu | vitoria
        self.fala_atual = ""
        self.cd_ataque = 0.0
        self.cd_boss = 0.0
        self.tempo_upgrade = 0.0     # tempo restante da pausa do upgrade
        self.duracao_upgrade = 1.0
        self.flash_dano = 0.0
        self.flash_tiro = 0.0
        self.faixa_texto = ""
        self.faixa_tempo = 0.0
        self.tempo_total = 0.0
        pygame.mouse.get_rel()
        self.audio.musica("ambiente.wav")
        registro.adicionar("Missão iniciada. Encontre o bebê Metroid.")

        def entidades(self):
            lista = []
            if self.ent_npc.ativa:
                lista.append(self.ent_npc)
            if self.ent_boss and self.ent_boss.ativa:
                lista.append(self.ent_boss)
            return lista