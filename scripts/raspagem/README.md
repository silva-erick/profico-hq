# Raspagem

Scripts para produção ou raspagem de dados.

## raspar_aasp

Para obter a [Tabela Prática para Cálculo de Atualização Monetária – IPCA-E](https://www.aasp.org.br/suporte-profissional/indices-economicos/indices-judiciais/tabela-pratica-para-calculo-de-atualizacao-monetaria-ipca-e/)
da AASP, utilize o seguinte comando:

```
python raspar_aasp.py --verbose
```

A tabela será salva em arquivo JSON: dados/brutos/aasp/conversao-monetaria.json.

## raspar_guiaquadrinhos

Para obter o total de obras catalogadas no [Guia dos Quadrinhos](www.guiadosquadrinhos.com)
por ano/mês, utilize o seguinte comando:

```
python raspar_guiaquadrinhos.py --verbose
```

A tabela será salva em arquivo JSON: dados/brutos/guiadosquadrinhos/totais.json.

## raspar_catarse

Para obter todas as campanhas realizadas em [Catarse](https://www.catarse.me/),
utilize o seguinte comando:

```
python raspar_catarse.py --verbose
```

Atenção aos arquivos gerados em dados/brutos/catarse:
- finished.json: lista resumo de todas as campanhas
- cities.json: lista de todos os municípios brasileiros (no Catarse)
- categories.json: lista de todas as categorias de campanhas (quadrinhos, jornalismo, etc)

Na pasta dados/brutos/catarse/campanhas haverá arquivos JSON (project_id.JSON)
para cada campanha, contendo:
- detalhes do projeto
- plano de recompensas
- pessoa responsável pela campanha


## raspar_apoiase

Para obter todas as campanhas realizadas em [apoia.se](https://apoia.se/),
utilize o seguinte comando:

```
python raspar_apoiase.py --verbose
```

Na pasta dados/brutos/apoiase/resumocampanhas haverá arquivos JSON (project_id.JSON)
para cada campanha, contendo:
- detalhes do projeto
- plano de recompensas
- pessoa responsável pela campanha