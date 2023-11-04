import nltk
import string
import sys
import numpy

stopwords = nltk.corpus.stopwords.words("portuguese")
pontuacao = list(string.punctuation) + ['...', "''", '\x97', '..', '....', "!...", ",."]
extrator = nltk.stem.RSLPStemmer()


def gerador_de_tf_idf(base_arquivo):
    with (open(base_arquivo, 'r', encoding='utf-8') as bf):
        base = bf.readlines()
        base = [linha.strip() for linha in base]
        numero_documentos = len(base)
        doc_tfidf = {doc: {} for doc in base}
        documentos_com_token = {}
        all_tokens = set()

        for filePath in base:
            with open(filePath, 'r') as arquivo:
                termos_tfidf = {}
                texto = arquivo.read()
                tokens = nltk.wordpunct_tokenize(texto)
                tokens = [extrator.stem(token) for token in tokens if token.lower()
                          not in stopwords and token not in pontuacao]
                all_tokens.update(tokens)

                for token in set(tokens):
                    termos_tfidf[token] = 1 + numpy.log10(tokens.count(token))
                    documentos_com_token[token] = documentos_com_token.get(token, 0) + 1

                doc_tfidf[filePath] = termos_tfidf

        for doc in base:
            for token in all_tokens:
                if token not in doc_tfidf[doc]:
                    doc_tfidf[doc][token] = 0
                else:
                    doc_tfidf[doc][token] *= numpy.log10(numero_documentos / documentos_com_token[token])

        with open("pesos.txt", "w", encoding='utf-8') as peso:
            for documento, termos in doc_tfidf.items():
                sequencia_de_termos = ' '.join([f"{termo},{peso}" for termo, peso in termos.items() if peso != 0])
                string_doc_tfidf = f"{documento}: {sequencia_de_termos}\n"
                peso.write(string_doc_tfidf)

        return {
            "ponderaçãoTFIDF": doc_tfidf,
            "baseDeDocumentos": base,
            "listaDeTokens": all_tokens,
            "documentosComToken": documentos_com_token
        }


def consulta_tfidf(tokens, args):
    all_tokens = args["listaDeTokens"]
    base = args["baseDeDocumentos"]
    documentos_com_token = args["documentosComToken"]

    numero_documentos = len(base)
    termos_tfidf = {}

    for token in all_tokens:
        tf = 1 + numpy.log10(tokens.count(token)) if token in tokens else 0
        idf = numpy.log10(numero_documentos / documentos_com_token[token])
        termos_tfidf[token] = tf * idf

    return termos_tfidf


def similaridade(consulta_arquivo, args):
    base_ponderacao = args["ponderaçãoTFIDF"]
    base = args["baseDeDocumentos"]
    all_tokens = args["listaDeTokens"]

    with open(consulta_arquivo, 'r', encoding='utf-8') as bc:
        consulta = bc.read()
        tokens_consulta = nltk.wordpunct_tokenize(consulta)
        tokens_consulta = [extrator.stem(token) for token in tokens_consulta if token not in stopwords and token != '&']
        consulta_ponderacao = consulta_tfidf(tokens_consulta, args)
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

    arquivoBase = sys.argv[1]
    arquivoConsulta = sys.argv[2]

    similaridade(arquivoConsulta, gerador_de_tf_idf(arquivoBase))
