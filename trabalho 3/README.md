# Trabalho 3 (Avaliação de Algoritmos de Recuperação da Informação)

## sobre: 
Para entender esse trabalho com mais detalhes entre no [enunciado](https://github.com/Eduardo-Pires/ORI-UFU/blob/main/trabalho%203/trab3_ori_2023-1.pdf), nele está descrito tudo o que é importante sobre o trabalho.

### arquivos importantes:
#### programa:
- **avaliacao.py**: esse é o programa que foi desenvolvido durante o trabalho.
#### entrada:
- **referencia.txt e referencia2.txt**: arquivos contendo as referências para a avaliação, para entender como elas funcionam ler no [enunciado](https://github.com/Eduardo-Pires/ORI-UFU/blob/main/trabalho%203/trab3_ori_2023-1.pdf).
#### saída:
- **media.txt**: o programa gera um arquivo com a precisão média do sistema da referência em cada um dos 11 níveis padrão de revocação.
- **Gráficos de precisão e revocação**: O programa gera gráficos que mostram a precisão e a revocação das consultas feitas, além de uma média dessas métricas. Os gráficos são exibidos automaticamente após a execução do programa.
#### verificação:
- **waxm...**: os arquivos com começo waxm fazem parte de um "corretor" construído pelo professor para que os alunos chequem a acurácia de suas respostas.
## como executar:
Para executar o trabalho é necessário ter o python e as bibliotecas necessárias instalados em seu computador, que são `numpy`, `matplotlib` e `sys`.
### No terminal:
- **executando o programa**: dentro da pasta do trabalho, escreva a seguinte linha no terminal:
  - ```python avaliacao.py referencia.txt```
