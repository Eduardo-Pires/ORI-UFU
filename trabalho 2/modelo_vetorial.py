import nltk
import string
import sys
import math

stopwords = nltk.corpus.stopwords.words("portuguese")
pontuacao = list(string.punctuation) + ['...', "''", '\x97', '..', '....', "!...", ",."]
extrator = nltk.stem.RSLPStemmer()


def base_tfidf(base_arquivo):
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

                tokens_base = nltk.wordpunct_tokenize(texto)
                tokens_base = [extrator.stem(token) for token in tokens_base
                               if token.lower() not in stopwords and token not in pontuacao]

                all_tokens.update(tokens_base)

                for token in set(tokens_base):
                    documentos_com_token[token] = documentos_com_token.get(token, 0) + 1

                    tf = 1 + math.log10(tokens_base.count(token))
                    documentos_tfidf[documento][token] = tf

        for documento in base:
            for token in all_tokens:
                if token not in documentos_tfidf[documento]:
                    documentos_tfidf[documento][token] = 0
                else:
                    idf = math.log10(numero_de_documentos / documentos_com_token[token])
                    documentos_tfidf[documento][token] *= idf

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
        tf = 1 + math.log10(tokens.count(token)) if token in tokens else 0
        idf = math.log10(numero_de_documentos / documentos_com_token[token])

        termos_tfidf[token] = tf * idf

    return termos_tfidf


def similaridade_vetorial(base_arquivo, consulta_arquivo):
    argumentos = base_tfidf(base_arquivo)

    base_ponderacao = argumentos["ponderaçãoTFIDF"]
    base = argumentos["baseDeDocumentos"]
    all_tokens = argumentos["listaDeTokens"]

    with (open(consulta_arquivo, 'r', encoding='utf-8') as arquivo_de_consulta):
        consulta = arquivo_de_consulta.read()

        tokens_consulta = nltk.wordpunct_tokenize(consulta)
        tokens_consulta = [extrator.stem(token) for token in tokens_consulta
                           if token not in stopwords and token != '&']

        consulta_ponderacao = consulta_tfidf(tokens_consulta, argumentos)
        documento_similaridade = {documento: 0 for documento in base}
        documentos_validos = 0

        for documento in base:
            multiplica = 0
            quadrado_base = 0
            quadrado_consulta = 0
            for token in set(all_tokens):
                wij = base_ponderacao[documento][token]
                wiq = consulta_ponderacao[token]

                multiplica += wij * wiq
                quadrado_base += wij ** 2
                quadrado_consulta += wiq ** 2

            documento_similaridade[documento] = multiplica / (math.sqrt(quadrado_consulta) * math.sqrt(quadrado_base))
            documentos_validos += 1 if documento_similaridade[documento] >= 0.001 else 0

        documentos_similaridade_ordenado = sorted(documento_similaridade.items(), key=lambda x: x[1], reverse=True)

        with open("resposta.txt", "w", encoding='utf-8') as resposta_arquivo:
            resposta_arquivo.write(f"{documentos_validos}\n")
            for documento, similaridade in documentos_similaridade_ordenado:
                if similaridade >= 0.001:
                    resposta_arquivo.write(f"{documento}: {similaridade}\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Entrada errada, favor chamar:  > python modelo_vetorial.py base.txt consulta.txt")
        sys.exit(1)

    arquivo_base = sys.argv[1]
    arquivo_consulta = sys.argv[2]

    similaridade_vetorial(arquivo_base, arquivo_consulta)
