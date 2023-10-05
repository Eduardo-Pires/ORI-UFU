import nltk
import string
import sys

if len(sys.argv) != 3:
    print("entrada errada, favor chamar:  python modelo_booleano.py base.txt consulta.txt")
    sys.exit(1)

arquivoBase = sys.argv[1]
arquivoConsulta = sys.argv[2]

stopwords = nltk.corpus.stopwords.words("portuguese")
pontuacao = list(string.punctuation) + ['...', "''", '\x97', '..', '....']
extrator = nltk.stem.RSLPStemmer()

with open(arquivoBase, 'r', encoding='utf-8') as bf:
    indiceInvertido = {}
    counter = 1
    base = bf.readlines()
    base = [linha.strip() for linha in base]
    for filePath in base:
        with open(filePath, 'r') as arquivo:
            texto = arquivo.read()
            tokens = nltk.wordpunct_tokenize(texto)
            tokens = [extrator.stem(token) for token in tokens if
                      token.lower() not in stopwords and token not in pontuacao]
            for token in set(tokens):
                if token not in indiceInvertido:
                    indiceInvertido[token] = []
                indiceInvertido[token].append((counter, tokens.count(token)))
        counter += 1
    with open("indice.txt", "w", encoding='utf-8') as indice:
        for palavra, indices in indiceInvertido.items():
            sequenciaIndices = ' '.join([f"{indice[0]},{indice[1]}" for indice in indices])

            termo = f"{palavra}: {sequenciaIndices}\n"
            indice.write(termo)


def intersection(resultado, adicao):
    return list(set(resultado) & set(adicao))


def negation(resultado, remocao):
    return list(set(resultado) - set(remocao))


with open(arquivoConsulta, 'r', encoding='utf-8') as bc:
    consulta = bc.read()
    tokensConsulta = nltk.wordpunct_tokenize(consulta)
    tokensConsulta = [extrator.stem(token) for token in tokensConsulta if token not in stopwords]

    resultados = []
    i = 0
    while i < len(tokensConsulta):
        termo = tokensConsulta[i]

        if termo == "&":
            i += 1
            token = tokensConsulta[i]
            if token in indiceInvertido:
                resultados = intersection(resultados, indiceInvertido[token])
        elif termo == "|":
            i += 1
            token = tokensConsulta[i]
            if token in indiceInvertido:
                resultados = resultados + indiceInvertido[token]
        elif termo == "!":
            i += 1
            token = tokensConsulta[i]
            if token in indiceInvertido:
                resultados = negation(resultados, indiceInvertido[token])
        else:
            if termo in indiceInvertido:
                if resultados:
                    resultados = intersection(resultados, indiceInvertido[termo])
                else:
                    resultados = indiceInvertido[termo]
        i += 1

    resultadoFinal = [tupla[0] for tupla in resultados]

    with open("resposta.txt", "w", encoding='utf-8') as resposta_arquivo:
        resposta_arquivo.write(f"{len(resultadoFinal)}\n")
        for doc_id in resultadoFinal:
            resposta_arquivo.write(f"{base[doc_id - 1]}\n")  # -1 para compensar a indexação baseada em 1
