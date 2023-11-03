import nltk
import string
import sys
import numpy

stopwords = nltk.corpus.stopwords.words("portuguese")
pontuacao = list(string.punctuation) + ['...', "''", '\x97', '..', '....', "!...", ",."]
extrator = nltk.stem.RSLPStemmer()


def geradorDeTF_IDF(arquivoBase):
    with (open(arquivoBase, 'r', encoding='utf-8') as bf):
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
                tokens = [extrator.stem(token) for token in tokens if token.lower()
                          not in stopwords and token not in pontuacao]
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
                    docTFIDF[doc][token] *= numpy.log10(numeroDocumentos / documentosComToken[token])

        with open("pesos.txt", "w", encoding='utf-8') as peso:
            for documento, termos in docTFIDF.items():
                sequenciaDeTermos = ' '.join([f"{termo},{peso}" for termo, peso in termos.items() if peso != 0])
                stringDocTFIDF = f"{documento}: {sequenciaDeTermos}\n"
                peso.write(stringDocTFIDF)

        return{
            "ponderaçãoTF_IDF": docTFIDF,
            "baseDeDocumentos": base,
            "listaDeTokens": allTokens,
            "documentosComToken": documentosComToken
        }

def consultaTFIDF(tokens, args):
    allTokens = args["listaDeTokens"]
    base = args["baseDeDocumentos"]
    documentosComToken = args["documentosComToken"]

    numeroDocumentos = len(base)
    termosTFIDF = {token: 1 + numpy.log10(tokens.count(token)) for token in set(tokens)}

    for token in allTokens:
        if token not in termosTFIDF:
            termosTFIDF[token] = 0
        else:
            termosTFIDF[token] *= numpy.log10(numeroDocumentos / documentosComToken[token])

    return termosTFIDF

def intersection(resultado, adicao):
    return list(set(resultado) & set(adicao))

def similaridade(arquivoConsulta, args):
    basePonderacao = args["ponderaçãoTF_IDF"]
    base = args["baseDeDocumentos"]
    allTokens = args["listaDeTokens"]

    with open(arquivoConsulta, 'r', encoding='utf-8') as bc:
        consulta = bc.read()
        tokensConsulta = nltk.wordpunct_tokenize(consulta)
        tokensConsulta = [extrator.stem(token) for token in tokensConsulta if token not in stopwords and token != '&']
        consultaPonderacao = consultaTFIDF(tokensConsulta, args)

        resultados = []

        resultadoFinal = [tupla[0] for tupla in resultados]

        with open("resposta.txt", "w", encoding='utf-8') as respostaArquivo:
            respostaArquivo.write(f"{len(resultadoFinal)}\n")
            for idDocumento in resultadoFinal:
                respostaArquivo.write(f"{base[idDocumento - 1]}\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Entrada errada, favor chamar:  > python modelo_vetorial.py base.txt consulta.txt")
        sys.exit(1)

    arquivoBase = sys.argv[1]
    arquivoConsulta = sys.argv[2]

    similaridade(arquivoConsulta, geradorDeTF_IDF(arquivoBase))
