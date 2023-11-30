import numpy as np
import matplotlib.pyplot as plt
import sys


def pre_processamento(referencia_arquivo):
    with open(referencia_arquivo, 'r', encoding='utf-8') as ref:
        base = ref.readlines()
        base = [linha.strip() for linha in base]
        numero_de_referencias = int(base[0])

        respostas_ideais = [vetor.split() for vetor in base[1:numero_de_referencias + 1]]
        respostas_ideais = [[int(valor) for valor in vetor] for vetor in respostas_ideais]

        respostas_do_sistema = [vetor.split() for vetor in base[numero_de_referencias + 1:]]
        respostas_do_sistema = [[int(valor) for valor in vetor] for vetor in respostas_do_sistema]

        return {
            "referencia": respostas_ideais,
            "sistema": respostas_do_sistema
        }

#def intersection(relevantes, algoritmo):
#    return list(set(relevantes) & set(algoritmo))


def cobertura(referencia_arquivo):
    respostas = pre_processamento(referencia_arquivo)
    respostas_ideais = respostas["referencia"]
    respostas_do_sistema = respostas["sistema"]


"""    
   #with open("pesos.txt", "w", encoding='utf-8') as arquivo_de_pesos:
            for documento, termos in documentos_tfidf.items():
                sequencia_de_termos = ' '.join([f"{termo},{peso}" for termo, peso in termos.items() if peso != 0])
                linha_pesos_de_documento = f"{documento}: {sequencia_de_termos}\n"

                arquivo_de_pesos.write(linha_pesos_de_documento)

        return {

        }

def similaridade_vetorial(base_arquivo, consulta_arquivo):
        with open("resposta.txt", "w", encoding='utf-8') as resposta_arquivo:
            resposta_arquivo.write(f"{documentos_validos}\n")
            for documento, similaridade in documentos_similaridade_ordenado:
                if similaridade >= 0.001:
                    resposta_arquivo.write(f"{documento}: {similaridade}\n")

"""

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Entrada errada, favor chamar:  > python avaliacao.py referencia.txt")
        sys.exit(1)

    arquivo_referencia = sys.argv[1]
    pre_processamento(arquivo_referencia)

    # similaridade_vetorial(arquivo_base, arquivo_consulta)
