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
import pyaudio

pygame.init()
iniciabanco()

tamanho = (1000,700)
largura = 1000
altura = 700
tela = pygame.display.set_mode( tamanho ) 
fps = pygame.time.Clock()

pygame.display.set_caption("Power Rangers - The Last Fire")
icone  = pygame.image.load("recursos/icon.png")
pygame.display.set_icon(icone)

branco = (255,255,255)
preto = (0, 0 ,0 )
personagem = pygame.image.load("recursos/personagem.png")
monstro = pygame.image.load("recursos/monstro.png")
fundoComeco = pygame.image.load("recursos/inicio.png")
fundoJogo = pygame.image.load("recursos/fundo.png")
fundoDead = pygame.image.load("recursos/morte.png")
boladefogo = pygame.image.load("recursos/boladefogo.webp")
colisao = pygame.mixer.Sound("recursos/errosom.mp3")
fonteMenu = pygame.font.SysFont("comicsans",18, True)
fonteMorte = pygame.font.SysFont("arial",120, True)
pygame.mixer.music.load("recursos/themesom.mp3")

personagem = pygame.transform.scale(personagem, (150, 167)) 
personagem_rect = personagem.get_rect(midbottom=(largura // 2, altura - 10))
boladefogo = pygame.transform.scale(boladefogo, (80, 80))
monstroLargura = 200
monstroAltura = 200
monstro = pygame.transform.scale(monstro, (monstroLargura, monstroAltura))

fonteMenu = pygame.font.SysFont('comicsans', 24, True)
nome = ""
pontos = 0

def iniciar_jogo():
    global pontos, nome
    pontos = 0
    pygame.mixer.music.play(-1)

    personagem_x = largura // 2 - 75
    personagem_y = altura - 167
    personagem_rect = pygame.Rect(personagem_x, personagem_y, 150, 167)

    boladefogo_x = random.randint(0, largura - 80)
    boladefogo_y = -80
    boladefogo_rect = pygame.Rect(boladefogo_x, boladefogo_y, 80, 80)
    velocidade = 15
    velocidade_boladefogo = 2
    aumento_velocidade = 0.01

    monstro_x = largura // 2 - monstroLargura // 2
    monstro_y = 50
    monstro_velocidade = 1

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
            texto_pausa = fonteMenu.render("JOGO PAUSADO - PRESSIONE ESPAÇO PARA CONTINUAR", True, branco)
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

        boladefogo_y += velocidade_boladefogo
        velocidade_boladefogo += aumento_velocidade

        if boladefogo_y > altura:
            boladefogo_x = random.randint(0, largura - 80)
            boladefogo_y = -80
            velocidade_boladefogo += 0.01
            pontos += 10

        personagem_rect = pygame.Rect(personagem_x, personagem_y, 100, 100)
        boladefogo_rect = pygame.Rect(boladefogo_x + 15, boladefogo_y + 15, 50, 50)

        if personagem_rect.colliderect(boladefogo_rect):
            colisao.play()
            game_over()

        tela.blit(fundoJogo, (0, 0))
        tela.blit(personagem, (personagem_x, personagem_y)) 
        tela.blit(boladefogo, (boladefogo_x, boladefogo_y))

        texto_pontos = fonteMenu.render(f"Pontuação: {pontos}", True, branco)
        tela.blit(texto_pontos, (largura - texto_pontos.get_width() - 10, altura - texto_pontos.get_height() - 10))

#              OLHOOOOO
        tempo = pygame.time.get_ticks() / 1000
        olho_x, olho_y = largura - 120, 120
        raio_base = 60
        raio_variacao = math.sin(tempo * 2) * 5
        raio_atual = raio_base + raio_variacao

        brilho_surface = pygame.Surface((largura, altura), pygame.SRCALPHA)

        for i in range(1, 6):
            alpha = max(0, 50 - i * 10)
            raio_brilho = int(raio_atual + i * 15)
            cor_brilho = (100, 0, 0, alpha)
            pygame.draw.circle(brilho_surface, cor_brilho, (olho_x, olho_y), raio_brilho)

            tela.blit(brilho_surface, (0, 0))

        for i in range(int(raio_atual), 0, -1):
            intensidade = 160 - int((i / raio_atual) * 50)
            r = intensidade + 30
            g = intensidade - 50
            b = intensidade - 50
            cor = (min(255, max(0, r)), min(255, max(0, g)), min(255, max(0, b)))
            pygame.draw.circle(tela, cor, (olho_x, olho_y), i)

            pupila_width = int(raio_atual * 0.2)
            pupila_height = int(raio_atual * 0.65)

            offset_x = int(math.sin(tempo * 1.5) * 5)
            offset_y = int(math.cos(tempo * 1.5) * 3)

            pygame.draw.ellipse(
            tela,
        (0, 0, 0),
    (
        olho_x - pupila_width // 2 + offset_x,
        olho_y - pupila_height // 2 + offset_y,
        pupila_width,
        pupila_height,
    ),
)

        pygame.draw.circle(tela, (255, 255, 255, 180), (olho_x - 15, olho_y - 20), 8)
        pygame.draw.circle(tela, (255, 255, 255, 100), (olho_x + 10, olho_y - 10), 4)

        veias_surface = pygame.Surface((largura, altura), pygame.SRCALPHA)

#           MONSTROOO
        monstro_x += monstro_velocidade
        if monstro_x <= 0 or monstro_x >= largura - monstroLargura:
            monstro_velocidade *= -1
        tela.blit(monstro, (monstro_x, monstro_y))

        for i in range(4):  
            angulo = math.radians(i * 90 + math.sin(tempo + i) * 10)
            comprimento = raio_atual + 15 + math.sin(tempo * 2 + i) * 3
            x1 = olho_x + int((raio_atual - 5) * math.cos(angulo))
            y1 = olho_y + int((raio_atual - 5) * math.sin(angulo))
            x2 = olho_x + int((comprimento) * math.cos(angulo))
            y2 = olho_y + int((comprimento) * math.sin(angulo))
            pygame.draw.line(veias_surface, (120, 0, 0, 150), (x1, y1), (x2, y2), 2)

        tela.blit(veias_surface, (0, 0))

        fontePAUSE = pygame.font.SysFont('comicsans', 24, italic=True)
        dica_pause = fontePAUSE.render("(Press Space to Pause)", False, branco)
        rect_dica = dica_pause.get_rect(topleft=(10, 10))
        borda_rect = pygame.Rect(rect_dica.left - 5, rect_dica.top - 3, rect_dica.width + 10, rect_dica.height + 6)
        pygame.draw.rect(tela, (0, 0, 0), borda_rect, width=1, border_radius=6)  
        tela.blit(dica_pause, rect_dica)

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
# GAME OVER
    texto = fonteMorte.render("GAME OVER", True, (0, 0, 0))
    rect = texto.get_rect(center=(largura // 2, altura // 2 - 50))

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                contorno = fonteMorte.render("GAME OVER", True, (255, 255, 255))
            tela.blit(contorno, rect.move(dx, dy))
            tela.blit(texto, rect)

    pygame.draw.rect(tela, branco, botao_restart, width=2, border_radius=8)
    pygame.draw.rect(tela, branco, botao_sair, width=2, border_radius=8)

    fonte_botao = pygame.font.SysFont('comicsans', 30)
    texto_restart = fonte_botao.render("Restart Game", True, branco)
    texto_sair = fonte_botao.render("Quit Game", True, branco)
    rect_restart = texto_restart.get_rect(center=botao_restart.center)
    rect_sair = texto_sair.get_rect(center=botao_sair.center)

    tela.blit(texto_restart, rect_restart)
    tela.blit(texto_sair, rect_sair)

    fonte_pontuacao = pygame.font.SysFont('comicsans', 32)
    texto_pontos = fonte_pontuacao.render(f"Pontuação final: {pontos}", True, branco)
    rect_pontos = texto_pontos.get_rect(center=(largura // 2, altura // 2 + 200))
    fundo_rect = pygame.Rect(rect_pontos.left - 10, rect_pontos.top - 5, rect_pontos.width + 20, rect_pontos.height + 10)
    pygame.draw.rect(tela, (0, 0, 0), fundo_rect, border_radius=10)
    tela.blit(texto_pontos, rect_pontos)

    fonte_registro = pygame.font.SysFont('arial', 20)
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
    mensagem_falada = False
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

        titulo_fonte = pygame.font.SysFont('arial', 50)
        texto_fonte = pygame.font.SysFont('times new roman', 28)

        texto_bem_vindo = titulo_fonte.render(f"VAMOS PARA BATALHA, {nome_jogador.upper()}!", True, branco)
        texto_jogo = texto_fonte.render("BEM VINDO A POWER RANGERS - THE LAST FIRE", True, (255, 0, 0))

        instrucoes = [
            "COMANDOS E INSTRUÇÕES:",
            "- Utilize as setas do teclado para movimentar o boneco.",
            "- DETALHE: Você só pode se movimentar para direita ou esquerda.",
            "- OBJETIVO: Não seja atingido pelas bolas de fogo que caem do céu.",
            "- A cada bola de fogo desviada, você ganha 10 pontos.",
            "- Se você for atingido, o jogo acaba.",
            "- Pressione a tecla 'Espaço' para PAUSAR caso necessário.",
            "- Pressione ENTER para começar o jogo!.",
            "É HORA DE MORFAR"
        ]
        
        if not mensagem_falada:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 1)

            mensagemfalada1 = "É HORA DE MORFAR"
            engine.say(mensagemfalada1)
            engine.runAndWait()
            mensagem_falada = True

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
            messagebox.showwarning("VOCÊ DEVE FALAR OU DIGITAR SEU NOME PARA PROSSEGUIR")
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
    root.title("NOME DO JOGADOR")
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

        tela.blit(fundoComeco, (0, 0))

        sombra_start = fonteMenu.render("Iniciar Jogo", True, (50, 50, 50))
        startTexto = fonteMenu.render("Iniciar Jogo", True, branco)
        start_rect = startTexto.get_rect(centerx=largura // 2, y=altura // 2 + 100) 
        pygame.draw.rect(tela, (100, 0, 0), start_rect.inflate(20, 20))  
        tela.blit(sombra_start, (start_rect.x + 2, start_rect.y + 2))
        tela.blit(startTexto, start_rect)

        sombra_quit = fonteMenu.render("Sair do Jogo", True, (50, 50, 50))
        quitTexto = fonteMenu.render("Sair do Jogo", True, branco)
        quit_rect = quitTexto.get_rect(centerx=largura // 2, y=altura // 2 + 160)
        pygame.draw.rect(tela, (255, 100, 100), quit_rect.inflate(8, 8))  
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