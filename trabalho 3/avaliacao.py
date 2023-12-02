import numpy as np
import matplotlib.pyplot as plt
import sys


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


def maximo(resposta, nivel):
    resposta_cortada = []
    for i in range(len(resposta)):
        if resposta[i][0] >= nivel:
            resposta_cortada.append(resposta[i][1])
    return max(resposta_cortada) if resposta_cortada != [] else 0


def interpolacao(precisao, revocacao, numero_consultas):
    resposta_interpolada = []
    niveis = np.round(np.arange(0.0, 1.1, 0.10), 2)

    for i in range(numero_consultas):
        respostas = [(revoc, prec) for revoc, prec in zip(revocacao[i], precisao[i])]
        aux_interpolar = [(nivel, maximo(respostas, nivel)) for nivel in niveis]
        resposta_interpolada.append(aux_interpolar)

    return resposta_interpolada


def calcular_media_respostas(respostas, numero_de_respostas):
    niveis = np.round(np.arange(0.0, 1.1, 0.10), 2)
    media_respostas = list(zip(niveis, np.zeros_like(niveis)))

    for i in range(numero_de_respostas):
        for j in range(len(respostas[i])):
            media_respostas[j] = (media_respostas[j][0], media_respostas[j][1] + respostas[i][j][1])

    for k in range(len(media_respostas)):
        media_respostas[k] = (media_respostas[k][0], media_respostas[k][1] / numero_de_respostas)

    with open("media.txt", "w", encoding='utf-8') as media_arquivo:
        for nivel, precisao in media_respostas:
            if nivel < 1:
                media_arquivo.write(f"{np.round(precisao, 2)} ")
            else:
                media_arquivo.write(f"{np.round(precisao, 2)}")
    return media_respostas


def plotar(eixo, respostas, titulo, cor):
    x = [resposta[0] * 100 for resposta in respostas]
    y = [resposta[1] * 100 for resposta in respostas]
    eixo.plot(x, y, label=titulo, color=cor)


def configurar_plotagem(resposta_interpolada, resposta_media, numero_consultas):
    cores = plt.colormaps['tab10']
    fig, eixos = plt.subplots(1, numero_consultas + 1, figsize=(15, 5))

    for i in range(numero_consultas):
        plotar(eixos[i], resposta_interpolada[i], f"Consulta {i + 1}", cor=cores(i))

    plotar(eixos[-1], resposta_media, "Média", cor=cores(numero_consultas))

    for eixo in eixos:
        eixo.set_xlabel('Revocação (%)')
        eixo.set_ylabel('Precisão (%)')
        eixo.legend()

    plt.tight_layout()
    plt.show()


def avaliar_sistema(referencia_arquivo):
    respostas = pre_processamento(referencia_arquivo)
    respostas_ideais = respostas["referencia"]
    respostas_do_sistema = respostas["sistema"]
    numero_consultas = respostas["ref_num"]

    precisao = []
    revocacao = []

    for i in range(numero_consultas):
        tamanho_ideais = len(respostas_ideais[i])
        count = 0

        aux_precisao = []
        aux_revocacao = []

        for j in range(len(respostas_do_sistema[i])):
            if respostas_do_sistema[i][j] in respostas_ideais[i]:
                count += 1
                aux_precisao.append(count / (j + 1))
                aux_revocacao.append(count / tamanho_ideais)

        precisao.append(aux_precisao)
        revocacao.append(aux_revocacao)
    resposta_interpolada = interpolacao(precisao, revocacao, numero_consultas)
    resposta_media = calcular_media_respostas(resposta_interpolada, numero_consultas)
    configurar_plotagem(resposta_interpolada, resposta_media, numero_consultas)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Entrada errada, favor chamar:  > python avaliacao.py referencia.txt")
        sys.exit("Erro: Número incorreto de argumentos")

    arquivo_referencia = sys.argv[1]
    avaliar_sistema(arquivo_referencia)
