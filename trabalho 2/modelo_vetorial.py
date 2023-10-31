import nltk
import string
import sys
import numpy

stopwords = nltk.corpus.stopwords.words("portuguese") + ["pra", "porque", "sobre", "pois",
                                                         "embora", "daqui", "enquanto"]
pontuacao = list(string.punctuation) + ['...', "''", '\x97', '..', '....', "!...", ",."]
extrator = nltk.stem.RSLPStemmer()

def geradorDeTF_IDF(arquivoBase):
    with open(arquivoBase, 'r', encoding='utf-8') as bf:
        base = bf.readlines()
        base = [linha.strip() for linha in base]
        numeroDocumentos = len(base)
        docTFIDF = {doc: {} for doc in base}
        documentosComToken = {}
        allTokens = set()

        for filePath in base:
            with open(filePath, 'r') as arquivo:
                termosTFIDF = {}
                texto = arquivo.read()
                tokens = nltk.wordpunct_tokenize(texto)
                tokens = [extrator.stem(token) for token in tokens if token.lower() not in stopwords and token not in pontuacao]
                allTokens.update(tokens)

                for token in set(tokens):
                    termosTFIDF[token] = 1 + numpy.log10(tokens.count(token))
                    documentosComToken[token] = documentosComToken.get(token, 0) + 1

                docTFIDF[filePath] = termosTFIDF

        for doc in base:
            for token in allTokens:
                if token not in docTFIDF[doc]:
                    docTFIDF[doc][token] = 0
                else:
                    docTFIDF[doc][token] *= numeroDocumentos / documentosComToken[token]

        print(docTFIDF)
        return {"docTFIDF": docTFIDF, "baseDeDocumentos": base}




"""
   #with open("indice.txt", "w", encoding='utf-8') as indice:
            for palavra, indices in termosTFIDF.items():
                sequenciaIndices = ' '.join([f"{indice[0]},{indice[1]}" for indice in indices])

                termo = f"{palavra}: {sequenciaIndices}\n"
                indice.write(termo)
def intersection(resultado, adicao):
    return list(set(resultado) & set(adicao))


def negation(resultado, remocao):
    return list(set(resultado) - set(remocao))


def modeloBooleano(arquivoConsulta, indiceInvertido, base):
    with open(arquivoConsulta, 'r', encoding='utf-8') as bc:
        consulta = bc.read()
        tokensConsulta = nltk.wordpunct_tokenize(consulta)
        tokensConsulta = [extrator.stem(token) for token in tokensConsulta if token not in stopwords]

        resultados = []

        i = 0
        while i < len(tokensConsulta):
            termo = tokensConsulta[i]

            match termo:
                case "&":
                    if i + 1 < len(tokensConsulta) and tokensConsulta[i + 1] == "!":
                        token = tokensConsulta[i + 2]
                        if token in indiceInvertido:
                            resultados = negation(resultados, indiceInvertido[token])
                        i += 2
                    elif i + 1 < len(tokensConsulta):
                        token = tokensConsulta[i + 1]
                        if token in indiceInvertido:
                            resultados = intersection(resultados, indiceInvertido[token])
                        i += 1
                case "|":
                    if i + 1 < len(tokensConsulta) and tokensConsulta[i + 1] == "!":
                        token = tokensConsulta[i + 2]
                        if token in indiceInvertido:
                            resultados = negation(resultados, indiceInvertido[token])
                        i += 2
                    elif i + 1 < len(tokensConsulta):
                        token = tokensConsulta[i + 1]
                        if token in indiceInvertido:
                            resultados = resultados + indiceInvertido[token]
                        i += 1
                case "!":
                    if i + 1 < len(tokensConsulta):
                        token = tokensConsulta[i + 1]
                        if token in indiceInvertido:
                            resultados = negation(resultados, indiceInvertido[token])
                        i += 1
                case _:
                    if termo in indiceInvertido:
                        if resultados:
                            resultados = intersection(resultados, indiceInvertido[termo])
                        else:
                            resultados = indiceInvertido[termo]
            i += 1

        resultadoFinal = [tupla[0] for tupla in resultados]

        with open("resposta.txt", "w", encoding='utf-8') as respostaArquivo:
            respostaArquivo.write(f"{len(resultadoFinal)}\n")
            for idDocumento in resultadoFinal:
                respostaArquivo.write(f"{base[idDocumento - 1]}\n")
"""

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Entrada errada, favor chamar:  > python modelo_vetorial.py base.txt consulta.txt")
        sys.exit(1)

    arquivoBase = sys.argv[1]
    arquivoConsulta = sys.argv[2]

    argumentos = geradorDeTF_IDF(arquivoBase)

    #modeloBooleano(arquivoConsulta, argumentos["indiceInvertido"], argumentos["baseDeDocumentos"])
