import pygame
import time
import random
import csv
import os

# --- CONFIGURAÇÕES INICIAIS ---
LARGURA_ECRA = 600
ALTURA_ECRA = 400
TAMANHO_BLOCO = 10
VELOCIDADE = 15

# Cores (R, G, B)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (213, 50, 80)
VERDE = (0, 255, 0)
AZUL = (50, 153, 213)

# Inicializar o Pygame
pygame.init()
ecra = pygame.display.set_mode((LARGURA_ECRA, ALTURA_ECRA))
pygame.display.set_caption('Snake Game - Projeto Python')
relogio = pygame.time.Clock()

# --- FUNÇÕES (MODULARIZAÇÃO - Requisito do Trabalho Prático) ---

def salvar_score_csv(pontuacao):
    """
    Pede o nome ao utilizador e guarda no ficheiro CSV.
    Cumpre o requisito de manipulação de ficheiros de texto.
    """
    print("\n--- GAME OVER ---")
    nome = input("Digite o seu nome para o Ranking: ")
    
    arquivo_existe = os.path.isfile('ranking.csv')
    
    # Abre o ficheiro em modo 'a' (append) para não apagar os anteriores
    with open('ranking.csv', 'a', newline='', encoding='utf-8') as ficheiro:
        escritor = csv.writer(ficheiro)
        # Se o ficheiro for novo, escreve o cabeçalho
        if not arquivo_existe:
            escritor.writerow(['Nome', 'Pontuacao'])
        
        escritor.writerow([nome, pontuacao])
    
    print(f"Score de {pontuacao} salvo com sucesso no ranking.csv!")

def desenhar_cobra(tamanho_bloco, lista_cobra):
    """Desenha a cobra no ecrã."""
    for bloco in lista_cobra:
        pygame.draw.rect(ecra, VERDE, [bloco[0], bloco[1], tamanho_bloco, tamanho_bloco])

def mensagem(msg, cor, deslocamento_y=0):
    """Escreve mensagens centradas com ajuste de altura."""
    fonte = pygame.font.SysFont("bahnschrift", 25)
    texto = fonte.render(msg, True, cor)
    
    # O centro é calculado: (Meio da Largura, Meio da Altura + Deslocamento)
    texto_rect = texto.get_rect(center=(LARGURA_ECRA / 2, (ALTURA_ECRA / 2) + deslocamento_y))
    
    ecra.blit(texto, texto_rect)

# --- FUNÇÃO PRINCIPAL DO JOGO ---

def jogo_snake():
    game_over = False
    game_close = False

    # Posição inicial
    x1 = LARGURA_ECRA / 2
    y1 = ALTURA_ECRA / 2
    x1_mudanca = 0
    y1_mudanca = 0

    lista_cobra = []
    comprimento_cobra = 1

    # Comida
    comida_x = round(random.randrange(0, LARGURA_ECRA - TAMANHO_BLOCO) / 10.0) * 10.0
    comida_y = round(random.randrange(0, ALTURA_ECRA - TAMANHO_BLOCO) / 10.0) * 10.0

    while not game_over:

        while game_close:
            ecra.fill(PRETO)
            
            # Linha 1 (O -20 faz o texto subir um bocadinho)
            mensagem("Perdeste! Que fraquinho...", VERMELHO, -20)
            
            # Linha 2 (O +20 faz o texto descer um bocadinho)
            mensagem("Pressione S (Sair) ou T (Tentar Novamente)", VERMELHO, 20)
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_t:
                        jogo_snake()

        # Controlo de teclas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_mudanca = -TAMANHO_BLOCO
                    y1_mudanca = 0
                elif event.key == pygame.K_RIGHT:
                    x1_mudanca = TAMANHO_BLOCO
                    y1_mudanca = 0
                elif event.key == pygame.K_UP:
                    y1_mudanca = -TAMANHO_BLOCO
                    x1_mudanca = 0
                elif event.key == pygame.K_DOWN:
                    y1_mudanca = TAMANHO_BLOCO
                    x1_mudanca = 0

        # Verificar se bateu nas paredes
        if x1 >= LARGURA_ECRA or x1 < 0 or y1 >= ALTURA_ECRA or y1 < 0:
            game_close = True

        x1 += x1_mudanca
        y1 += y1_mudanca
        ecra.fill(PRETO)
        
        # Desenhar Comida
        pygame.draw.rect(ecra, AZUL, [comida_x, comida_y, TAMANHO_BLOCO, TAMANHO_BLOCO])
        
        # Lógica da Cobra crescendo
        cabeca_cobra = []
        cabeca_cobra.append(x1)
        cabeca_cobra.append(y1)
        lista_cobra.append(cabeca_cobra)

        if len(lista_cobra) > comprimento_cobra:
            del lista_cobra[0]

        # Verificar se bateu nela própria
        for x in lista_cobra[:-1]:
            if x == cabeca_cobra:
                game_close = True

        desenhar_cobra(TAMANHO_BLOCO, lista_cobra)
        
        # Mostrar Pontuação
        fonte_pontos = pygame.font.SysFont("comicsansms", 35)
        valor = fonte_pontos.render("Score: " + str(comprimento_cobra - 1), True, BRANCO)
        ecra.blit(valor, [0, 0])

        pygame.display.update()

        # Comer a comida
        if x1 == comida_x and y1 == comida_y:
            comida_x = round(random.randrange(0, LARGURA_ECRA - TAMANHO_BLOCO) / 10.0) * 10.0
            comida_y = round(random.randrange(0, ALTURA_ECRA - TAMANHO_BLOCO) / 10.0) * 10.0
            comprimento_cobra += 1

        relogio.tick(VELOCIDADE)

    # FIM DE JOGO - Guardar no CSV
    # O -1 é porque a cobra começa com tamanho 1
    salvar_score_csv(comprimento_cobra - 1) 
    pygame.quit()
    quit()

# Iniciar o jogo
jogo_snake()