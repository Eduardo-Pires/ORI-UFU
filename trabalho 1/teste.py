import sys

def ler_documento(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return set(arquivo.read().split())
    except FileNotFoundError:
        print(f"O arquivo {nome_arquivo} não foi encontrado.")
        sys.exit(1)

if len(sys.argv) != 3:
    print("Uso: python teste.py indice.txt indiceProf.txt")
    sys.exit(1)

arquivo_a = sys.argv[1]
arquivo_b = sys.argv[2]

palavras_a = ler_documento(arquivo_a)
palavras_b = ler_documento(arquivo_b)

palavras_em_a_mas_nao_em_b = palavras_a - palavras_b
palavras_em_b_mas_nao_em_a = palavras_b - palavras_a

with open("diferenças.txt", 'w', encoding='utf-8') as arquivo_c:
    arquivo_c.write("Palavras em A, mas não em B:\n")
    for palavra in palavras_em_a_mas_nao_em_b:
        arquivo_c.write(palavra + "\n")

    arquivo_c.write("\nPalavras em B, mas não em A:\n")
    for palavra in palavras_em_b_mas_nao_em_a:
        arquivo_c.write(palavra + "\n")

print("Processamento concluído. Resultados escritos em diferenças.txt.")
