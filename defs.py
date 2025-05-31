# funções do game
import os , time
import json
from datetime import datetime



def iniciabanco():
    try:
        banco = open('log.dat', 'r')
    except:
        print('O banco de dados não existe, criando...')
        banco = open('log.dat', 'w')
