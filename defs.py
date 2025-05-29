# funções do game
import os , time
import json
from datetime import datetime

def limpaTela():
    os.system('cls')
    
def aguarde(segundos):
    time.sleep(segundos)

def iniciabanco():
    try:
        banco = open('log.dat', 'r')
    except:
        print('O banco de dados não existe, criando...')
        banco = open('log.dat', 'w')
