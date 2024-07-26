# Trabalho 2 ( ponderação TF-IDF e modelo vetorial )

## sobre: 
Para entender esse trabalho com mais detalhes entre no [enunciado](https://github.com/Eduardo-Pires/ORI-UFU/blob/main/trabalho%202/trab2_ori_2023-1.pdf), nele está descrito tudo o que é importante sobre o trabalho.

### arquivos importantes:
#### programa:
- **modelo_vetorial.py**: esse é o programa que foi desenvolvido durante o trabalho.
#### entrada:
- **base.txt e base_samba.txt**: nesses arquivo estão os caminhos de duas bases de arquivos que foram utilizadas nesse trabalho, esses arquivos estão nas pastas ```base_arquivos``` e ```base_arquivos_samba```.
- **consulta.txt, consulta2.txt, consulta3.txt e consulta4.txt**: nesses arquivo estão escritas diferentes consultas, que podem ser alteradas para diferentes resultados, para mais informações sobre como fazer sua própria consulta ler o [enunciado](https://github.com/Eduardo-Pires/ORI-UFU/blob/main/trabalho%202/trab2_ori_2023-1.pdf).
#### saída:
- **pesos.txt**: Arquivo contendo a ponderação TF-IDF de cada documento.
- **resposta.txt**: Arquivo contendo os nomes dos documentos que atendem à consulta.
#### verificação:
- **waxm...**: os arquivos com começo waxm fazem parte de um "corretor" construído pelo professor para que os alunos chequem a acurácia de suas respostas.
## como executar:
Para executar o trabalho é necessário ter o python e as bibliotecas necessárias instalados em seu computador, que são ```nltk```, ```string```, ```sys``` e ```math```.
### No terminal:
- **executando o programa**: dentro da pasta do trabalho, escreva a seguinte linha no terminal:
  - ```python modelo_vetorial.py base.txt consulta.txt```
- **executando a verificação**: dentro da pasta do trabalho, escreva a seguinte linha no terminal:
  - ```python waxm_corretor_vetorial.pyc base.txt consulta.txt modelo_vetorial.py```
