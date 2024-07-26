# Trabalho 1 ( índice invertido e modelo booleano )

## sobre: 
Para entender esse trabalho com mais detalhes entre no [enunciado](https://github.com/Eduardo-Pires/ORI-UFU/blob/main/trabalho%201/Enunciado%20trab1_ori.pdf), nele está descrito tudo o que é importante sobre o trabalho.

### arquivos importantes:
#### programa:
- **modelo_booleano.py**: esse é o programa que foi desenvolvido durante o trabalho:
#### entrada
- **base.txt**: nesse arquivo estão os caminhos da base de arquivos que foi usada para a execução do trabalho, esses arquivos estão na pasta ```base_arquivos```.
- **consulta.txt**: nesse arquivo em que deve ser escrita a consulta, para mais informações sobre como a consulta deve ser feita ler o [enunciado](https://github.com/Eduardo-Pires/ORI-UFU/blob/main/trabalho%201/Enunciado%20trab1_ori.pdf).
#### saída
- **resposta.txt**: nesse arquivo está a resposta para a consulta que foi feita.
- **indice.txt**: nesse arquivo está o índice invertido conforme a base de arquivos.
#### verificação:
- **waxm...**: os arquivos com começo waxm fazem parte de um "corretor" construído pelo professor para que os alunos chequem a acurácia de suas respostas.
## como executar:
Para executar o trabalho é necessário ter o python e as bibliotecas necessárias instalados em seu computador, que são ```nltk```, ```string``` e ```sys```.
### No terminal:
- **executando o programa**: dentro da pasta do trabalho, escreva a seguinte linha no terminal:
  - ```python modelo_booleano.py base.txt consulta.txt```
- **executando a verificação**: dentro da pasta do trabalho, escreva a seguinte linha no terminal:
  - ```python waxm_corretor_modelo_booleano.pyc  base.txt  consulta.txt   modelo_booleano.py```
