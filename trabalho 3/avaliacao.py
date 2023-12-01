import numpy as np
import matplotlib.pyplot as plt
import sys
from functools import reduce

def pre_processamento(referencia_arquivo):
    with open(referencia_arquivo, 'r', encoding='utf-8') as ref:
        base = ref.readlines()
        base = [linha.strip() for linha in base]
        numero_de_referencias = int(base[0])

        respostas_ideais = [vetor.split() for vetor in base[1:numero_de_referencias + 1]]

        respostas_do_sistema = [vetor.split() for vetor in base[numero_de_referencias + 1:]]

        return {
            "ref_num": numero_de_referencias,
            "referencia": respostas_ideais,
            "sistema": respostas_do_sistema
        }

def cobertura(referencia_arquivo):
    respostas = pre_processamento(referencia_arquivo)
    respostas_ideais = respostas["referencia"]
    respostas_do_sistema = respostas["sistema"]
    precisao = []
    revocacao = []

    for i in range(respostas["ref_num"]):
        tamanho_ideais = len(respostas_ideais[i])
        count = 0
        aux_precisao = [0] * len(respostas_do_sistema[i])
        aux_revocacao = [0] * len(respostas_do_sistema[i])
        for j in range(len(respostas_do_sistema[i])):
            if respostas_do_sistema[i][j] in respostas_ideais[i]:
                count += 1
                aux_precisao[j] = count / (j + 1)
                aux_revocacao[j] = count / tamanho_ideais

        precisao.append(aux_precisao)
        revocacao.append(aux_revocacao)
    print(precisao)
    print(revocacao)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Entrada errada, favor chamar:  > python avaliacao.py referencia.txt")
        sys.exit("Erro: Número incorreto de argumentos")

    arquivo_referencia = sys.argv[1]
    cobertura(arquivo_referencia)
