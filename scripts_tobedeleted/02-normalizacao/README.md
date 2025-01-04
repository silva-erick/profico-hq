# Normalização

Scripts para normalização dos dados brutos.

# normalizar.py

Para normalizar todas as campanhas de 2011 até um determinando ano de interesse:

```
python 01-normalizar.py --verbose -a 2023
```

## Tipos de normalização

### Conversão HTML para TXT

Para facilitar a análise ou classificação automática de conteúdo, o texto em HTML será convertido para texto puro.

### Valor monetário

O valor desejado, o valor arrecado e os valores das recompensas serão ajustados,
de acordo com a [Tabela Prática para Cálculo de Atualização Monetária – IPCA-E](https://www.aasp.org.br/suporte-profissional/indices-economicos/indices-judiciais/tabela-pratica-para-calculo-de-atualizacao-monetaria-ipca-e/)
da AASP, para o valor em dezembro do ano desejado.

### Gênero

Se a pessoa é indivíduo, verificar se o gênero é determinável a partir do nome público:
- masculino 
- feminino

Do contrário, avaliar se:
- coletivo de pessoas autoras
- empresa
- outros
