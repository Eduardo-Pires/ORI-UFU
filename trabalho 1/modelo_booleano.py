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
            tokens = [extrator.stem(token) for token in tokens if token.lower() not in stopwords and token not in pontuacao]
            for token in tokens:
                if token not in indiceInvertido:
                    indiceInvertido[token] = [(counter, 1)]  # Usando uma lista de tuplas
                else:
                    # Verificando se o documento já está na lista
                    doc_presente = False
                    for i, (doc_id, count) in enumerate(indiceInvertido[token]):
                        if doc_id == counter:
                            doc_presente = True
                            indiceInvertido[token][i] = (doc_id, count + 1)
                            break
                    if not doc_presente:
                        indiceInvertido[token].append((counter, 1))
        counter += 1
    print(indiceInvertido)


with open(arquivoConsulta, 'r', encoding='utf-8') as bc:
    consulta = bc.read()
