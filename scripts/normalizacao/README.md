# Normalização

Scripts para normalização dos dados brutos.

# Execução

Para normalizar todas as campanhas de 2011 até o ano de 2023:

```
python normalizar.py --verbose -a 2023
```

# Tipos de normalização

## Valor monetário

O valor desejado, o valor arrecado e os valores das recompensas serão ajustados,
de acordo com a [Tabela Prática para Cálculo de Atualização Monetária – IPCA-E](https://www.aasp.org.br/suporte-profissional/indices-economicos/indices-judiciais/tabela-pratica-para-calculo-de-atualizacao-monetaria-ipca-e/)
da AASP, para o valor em dezembro do ano desejado.

## Lemmatização

O texto de apresentação da campanha é convertido de HTML para texto puro,
tokenizado (biblioteca spacy) e lemmatizado (biblioteca spacy).

## Frequência do Termo

A frequência no texto de todos os tokens classificados como NOUN pela
biblioteca spacy é calculada e anotada junto ao documento.

## IDF

O valor de IDF (Inverse Document Frequency) do termo é calculado quando
todo o corpus já foi lemmatizado.

## TF-IDF

Cálculo do TF-IDF para todos os tokens classificados como NOUN pela
biblioteca spacy.

A ideia é verificar se o índice pode auxiliar a identificar grandes temas
relacionados com as campanhas realizadas até então.

