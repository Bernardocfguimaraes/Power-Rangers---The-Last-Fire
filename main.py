import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from defs import iniciabanco
from defs import limpaTela
from defs import aguarde
import json
import math
import datetime
import speech_recognition as sr
import pyttsx3
import sys
from tkinter import messagebox
pygame.init()
iniciabanco()

tamanho = (1000,700)
largura = 1000
altura = 700
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
fps = pygame.time.Clock()

pygame.display.set_caption("Power Rangers - The Last Fire")
#icone  = pygame.image.load("assets/icone.png")

#pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
personagem = pygame.image.load("recursos/personagem.png")
inimigo = pygame.image.load("recursos/monstro.webp")
fundoStart = pygame.image.load("recursos/inicio.jpg")
fundoJogo = pygame.image.load("recursos/fundo.jpg")
fundoDead = pygame.image.load("recursos/morte.png")
boladefogo = pygame.image.load("recursos/boladefogo.png")
missileSound = pygame.mixer.Sound("recursos/boladefogosom.mp3")
explosaoSound = pygame.mixer.Sound("recursos/errosom.mp3")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("recursos/themesom.mp3")

personagem = pygame.transform.scale(personagem, (100, 100)) 
boladefogo = pygame.transform.scale(boladefogo, (80, 80))
monstroLargura = 300
monstroAltura = 300
monstro = pygame.transform.scale(inimigo, (monstroLargura, monstroAltura))

fonteMenu = pygame.font.SysFont('comicsans', 24)
nome = ""
pontos = 0

def iniciar_jogo():
    global pontos, nome
    pontos = 0

    pygame.mixer.music.play(-1)

    personagem_x = largura // 2 - 50
    personagem_y = altura - 150
    velocidade = 15

    projetil_x = random.randint(0, largura - 80)
    projetil_y = -80
    velocidade_projetil = 2
    aumento_velocidade = 0.01

    inimigo_x = largura // 2 - monstroLargura // 2
    inimigo_y = 50
    inimigo_velocidade = 1

    rodando = True
    pausado = False 

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado

        if pausado:
            texto_pausa = fonteMenu.render("GAME PAUSED - press space to continue", True, branco)
            texto_rect = texto_pausa.get_rect(center=(largura // 2, altura // 2))
            tela.blit(texto_pausa, texto_rect)
            pygame.display.update()
            fps.tick(10)
            continue

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            personagem_x -= velocidade
        if teclas[pygame.K_RIGHT]:
            personagem_x += velocidade

        if personagem_x < 0:
            personagem_x = 0
        elif personagem_x > largura - 100:
            personagem_x = largura - 100

        projetil_y += velocidade_projetil
        velocidade_projetil += aumento_velocidade

        if projetil_y > altura:
            projetil_x = random.randint(0, largura - 80)
            projetil_y = -80
            velocidade_projetil += 0.01
            pontuacao += 10

        personagem_rect = pygame.Rect(personagem_x, personagem_y, 100, 100)
        projetil_rect = pygame.Rect(projetil_x + 15, projetil_y + 15, 50, 50)

        if personagem_rect.colliderect(projetil_rect):
            game_over()

        inimigo_x += inimigo_velocidade
        if inimigo_x <= 0 or inimigo_x >= largura - monstroLargura:
            inimigo_velocidade *= -1

        tela.blit(fundoJogo, (0, 0))
        tela.blit(monstro, (inimigo_x, inimigo_y)) 
        tela.blit(personagem, (personagem_x, personagem_y)) 
        tela.blit(boladefogo, (projetil_x, projetil_y))

        texto_pontos = fonteMenu.render(f"Pontuação: {pontos}", True, branco)
        tela.blit(texto_pontos, (largura - texto_pontos.get_width() - 10, altura - texto_pontos.get_height() - 10))

        tempo = pygame.time.get_ticks() / 1000
        sol_x, sol_y = largura - 120, 120
        raio_sol = 60

        for i in range(raio_sol, 0, -1):
            intensidade = 255 - int((i / raio_sol) * 100)
            cor = (255, intensidade, 50)
            pygame.draw.circle(tela, cor, (sol_x, sol_y), i)

        brilho = 220 + int(10 * math.sin(tempo * 2))
        cor_raio = (255, brilho, 60)

        for i in range(12):
            angulo = math.radians(i * 30)
            offset = 5 * math.sin(tempo * 3 + i)
            comprimento = 30 + offset
            x1 = sol_x + int((raio_sol - 5) * math.cos(angulo))
            y1 = sol_y + int((raio_sol - 5) * math.sin(angulo))
            x2 = sol_x + int((raio_sol + comprimento) * math.cos(angulo))
            y2 = sol_y + int((raio_sol + comprimento) * math.sin(angulo))
            pygame.draw.line(tela, cor_raio, (x1, y1), (x2, y2), 2)

        for i in range(6):
            raio_aura = raio_sol + 20 + i * 10
            alpha = max(5, 50 - i * 7)
            aura_surface = pygame.Surface((raio_aura * 2, raio_aura * 2), pygame.SRCALPHA)
            pygame.draw.circle(aura_surface, (255, 200, 80, alpha), (raio_aura, raio_aura), raio_aura)
            tela.blit(aura_surface, (sol_x - raio_aura, sol_y - raio_aura))

        dica_pause = fonteMenu.render("(press space to pause)", True, (180, 180, 180))
        tela.blit(dica_pause, (10, 10))

        pygame.display.update()
        fps.tick(60)

def game_over():
    global nome, pontos

    pygame.mixer.music.stop()
    agora = datetime.datetime.now()
    data_hora = agora.strftime("%d/%m/%Y - (%H:%M:%S)")

    novo_registro = f"Jogador: {nome} - Pontuação: {pontos} - Data/Hora: {data_hora}\n"

    with open("log.dat", "a") as arquivo:
        arquivo.write(novo_registro)

    try:
        with open("log.dat", "r") as arquivo:
            linhas = arquivo.readlines()
            ultimos_registros = linhas[-5:]
    except FileNotFoundError:
        ultimos_registros = []

    botao_restart = pygame.Rect(largura // 2 - 110, altura // 2 + 50, 220, 50)
    botao_sair = pygame.Rect(largura // 2 - 110, altura // 2 + 120, 220, 50)

    tela.blit(fundoDead, (0, 0))

    fonte_titulo = pygame.font.SysFont('comicsans', 72)
    texto = fonte_titulo.render("GAME OVER", True, (255, 0, 0))
    rect = texto.get_rect(center=(largura // 2, altura // 2 - 50))
    tela.blit(texto, rect)

    pygame.draw.rect(tela, (0, 255, 0), botao_restart)
    pygame.draw.rect(tela, (255, 0, 0), botao_sair)

    fonte_botao = pygame.font.SysFont('comicsans', 30)
    texto_restart = fonte_botao.render("Restart Game", True, preto)
    texto_sair = fonte_botao.render("Quit Game", True, branco)

    tela.blit(texto_restart, (botao_restart.x + 35, botao_restart.y + 10))
    tela.blit(texto_sair, (botao_sair.x + 50, botao_sair.y + 10))

    fonte_pontuacao = pygame.font.SysFont('comicsans', 32)
    texto_pontos = fonte_pontuacao.render(f"Pontuação final: {pontos}", True, branco)
    tela.blit(texto_pontos, (largura // 2 - texto_pontos.get_width() // 2, altura // 2 + 190))

    fonte_registro = pygame.font.SysFont('comicsans', 20)
    y_offset = 10

    titulo_log = fonte_registro.render("Últimas 5 Jogadas:", True, branco)
    tela.blit(titulo_log, (largura - titulo_log.get_width() - 10, y_offset))

    y_offset += 30

    for registro in reversed(ultimos_registros):
        registro = registro.strip()
        texto_log = fonte_registro.render(registro, True, branco)
        tela.blit(texto_log, (largura - texto_log.get_width() - 10, y_offset))
        y_offset += 25

    pygame.display.update()

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)

    mensagem_falada = f"A pontuação final foi {pontos} pontos"
    engine.say(mensagem_falada)
    engine.runAndWait()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if botao_restart.collidepoint(mouse_pos):
                    iniciar_jogo()
                    return
                elif botao_sair.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        fps.tick(60)

def tela_boas_vindas(nome_jogador):
    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    rodando = False
                    iniciar_jogo()

        tela.fill(preto)

        titulo_fonte = pygame.font.SysFont('comicsans', 50)
        texto_fonte = pygame.font.SysFont('comicsans', 28)

        texto_bem_vindo = titulo_fonte.render(f"BEM-VINDO, {nome_jogador.upper()}!", True, branco)
        texto_jogo = texto_fonte.render("ESTE JOGO É O: FIGHT IN SPACE", True, branco)

        instrucoes = [
            "COMANDOS:",
            "- Use as setas <- -> para mover a nave",
            "- Desvie dos projéteis que caem do céu",
            "- Se for atingido, é GAME OVER!",
            "- Pressione 'Espaço' a qualquer momento para PAUSAR",
            "- Pressione ENTER para começar o jogo!"
        ]

        tela.blit(texto_bem_vindo, (largura // 2 - texto_bem_vindo.get_width() // 2, 100))
        tela.blit(texto_jogo, (largura // 2 - texto_jogo.get_width() // 2, 170))

        for i, linha in enumerate(instrucoes):
            linha_render = texto_fonte.render(linha, True, branco)
            tela.blit(linha_render, (100, 250 + i * 40))

        pygame.display.update()
        fps.tick(60)

def jogar():
    largura_janela = 400
    altura_janela = 100

    def obter_nome():
        global nome
        nome = entry_nome.get()
        if not nome.strip():
            messagebox.showwarning("Aviso", "Por favor, fale ou digite seu nome!")
        else:
            root.destroy()
            tela_boas_vindas(nome)

    def falar_nome():
        global nome
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            messagebox.showinfo("Fale agora", "Por favor, fale o seu nickname...")
            try:
                audio = recognizer.listen(source, timeout=5)
                nome_falado = recognizer.recognize_google(audio, language='pt-BR')
                entry_nome.delete(0, tk.END)
                entry_nome.insert(0, nome_falado)
            except sr.UnknownValueError:
                messagebox.showerror("Erro", "Não entendi o que você falou. Por favor, tente novamente ou digite seu nome.")
            except sr.RequestError:
                messagebox.showerror("Erro", "Não foi possível conectar ao serviço de reconhecimento.")
            except sr.WaitTimeoutError:
                messagebox.showerror("Erro", "Tempo de espera excedido. Por favor, tente novamente.")

    def ao_fechar_janela():
        messagebox.showwarning("Aviso", "Você precisa falar ou digitar um nome para continuar!")

    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    x = (largura_tela - largura_janela) // 2
    y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
    root.title("Nickname")
    root.protocol("WM_DELETE_WINDOW", ao_fechar_janela)

    label_instrucao = tk.Label(root, text="Fale ou digite seu nickname:")
    label_instrucao.pack()

    entry_nome = tk.Entry(root)
    entry_nome.pack()

    frame_botoes = tk.Frame(root)
    frame_botoes.pack()

    botao_falar = tk.Button(frame_botoes, text="Falar", command=falar_nome)
    botao_falar.pack(side=tk.LEFT, padx=5)

    botao_ok = tk.Button(frame_botoes, text="OK", command=obter_nome)
    botao_ok.pack(side=tk.LEFT, padx=5)

    root.mainloop()

def start():
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    while True:
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(mouse_pos):
                    jogar()
                if quitButton.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        tela.blit(fundoStart, (0, 0))

        sombra_start = fonteMenu.render("Iniciar Game", True, (50, 50, 50))
        startTexto = fonteMenu.render("Iniciar Game", True, branco)
        start_rect = startTexto.get_rect(topleft=(25, 12))
        tela.blit(sombra_start, (start_rect.x + 2, start_rect.y + 2))
        tela.blit(startTexto, start_rect)

        sombra_quit = fonteMenu.render("Sair do Game", True, (50, 50, 50))
        quitTexto = fonteMenu.render("Sair do Game", True, branco)
        quit_rect = quitTexto.get_rect(topleft=(25, 62))
        tela.blit(sombra_quit, (quit_rect.x + 2, quit_rect.y + 2))
        tela.blit(quitTexto, quit_rect)

        startButton = start_rect
        quitButton = quit_rect

        if startButton.collidepoint(mouse_pos) or quitButton.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.update()
        fps.tick(60)

start()