import nltk
import string
import sys
import numpy

stopwords = nltk.corpus.stopwords.words("portuguese")
pontuacao = list(string.punctuation) + ['...', "''", '\x97', '..', '....', "!...", ",."]
extrator = nltk.stem.RSLPStemmer()


def gerador_de_tfidf(base_arquivo):
    with open(base_arquivo, 'r', encoding='utf-8') as arquivos_de_base:
        base = arquivos_de_base.readlines()
        base = [linha.strip() for linha in base]

        numero_de_documentos = len(base)
        documentos_tfidf = {documento: {} for documento in base}

        documentos_com_token = {}
        all_tokens = set()

        for documento in base:
            with open(documento, 'r') as caminho_arquivo:
                texto = caminho_arquivo.read()

                tokens = nltk.wordpunct_tokenize(texto)
                tokens = [extrator.stem(token) for token in tokens if token.lower()
                          not in stopwords and token not in pontuacao]

                all_tokens.update(tokens)

                termos_tfidf = {}
                for token in set(tokens):
                    termos_tfidf[token] = 1 + numpy.log10(tokens.count(token))
                    documentos_com_token[token] = documentos_com_token.get(token, 0) + 1

                documentos_tfidf[documento] = termos_tfidf

        for documento in base:
            for token in all_tokens:
                if token not in documentos_tfidf[documento]:
                    documentos_tfidf[documento][token] = 0
                else:
                    documentos_tfidf[documento][token] *= numpy.log10(numero_de_documentos / documentos_com_token[token])

        with open("pesos.txt", "w", encoding='utf-8') as arquivo_de_pesos:
            for documento, termos in documentos_tfidf.items():
                sequencia_de_termos = ' '.join([f"{termo},{peso}" for termo, peso in termos.items() if peso != 0])
                linha_pesos_de_documento = f"{documento}: {sequencia_de_termos}\n"

                arquivo_de_pesos.write(linha_pesos_de_documento)

        return {
            "ponderaçãoTFIDF": documentos_tfidf,
            "baseDeDocumentos": base,
            "listaDeTokens": all_tokens,
            "documentosComToken": documentos_com_token
        }


def consulta_tfidf(tokens, argumentos):
    all_tokens = argumentos["listaDeTokens"]
    base = argumentos["baseDeDocumentos"]
    documentos_com_token = argumentos["documentosComToken"]

    numero_de_documentos = len(base)

    termos_tfidf = {}

    for token in all_tokens:
        tf = 1 + numpy.log10(tokens.count(token)) if token in tokens else 0
        idf = numpy.log10(numero_de_documentos / documentos_com_token[token])

        termos_tfidf[token] = tf * idf

    return termos_tfidf


def similaridade(consulta_arquivo, argumentos):
    base_ponderacao = argumentos["ponderaçãoTFIDF"]
    base = argumentos["baseDeDocumentos"]
    all_tokens = argumentos["listaDeTokens"]

    with open(consulta_arquivo, 'r', encoding='utf-8') as arquivo_de_consulta:
        consulta = arquivo_de_consulta.read()

        tokens_consulta = nltk.wordpunct_tokenize(consulta)
        tokens_consulta = [extrator.stem(token) for token in tokens_consulta if token not in stopwords and token != '&']

        consulta_ponderacao = consulta_tfidf(tokens_consulta, argumentos)
        print(consulta_ponderacao)


"""
     resultados = []

    resultadoFinal = [tupla[0] for tupla in resultados]

    def intersection(resultado, adicao):
        return list(set(resultado) & set(adicao))
        
   #     with open("resposta.txt", "w", encoding='utf-8') as respostaArquivo:
            respostaArquivo.write(f"{len(resultadoFinal)}\n")
            for idDocumento in resultadoFinal:
                respostaArquivo.write(f"{base[idDocumento - 1]}\n")

"""
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Entrada errada, favor chamar:  > python modelo_vetorial.py base.txt consulta.txt")
        sys.exit(1)

    arquivo_base = sys.argv[1]
    arquivo_consulta = sys.argv[2]

    similaridade(arquivo_consulta, gerador_de_tfidf(arquivo_base))
