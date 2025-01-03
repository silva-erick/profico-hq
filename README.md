# profico-hq

A iniciativa *profico-hq* reúne scripts, dados e análises sobre histórias em quadrinhos (HQ)
que tiveram campanhas de arrecadação conduzidas em plataformas de financiamento coletivo
no Brasil.

>[!NOTE]
>Chegou aqui para ver o relatório anual? Link direto: [Relatório Anual 2023](./analises/README.md).

## Por que esse nome?

O termo profico-hq vem de:
- profico, combinação de PRojetos de FInanciamento COletivo
- HQ, sigla para histórias em quadrinhos

Mas profico lembra profícuo que, segundo o [Dicio](https://www.dicio.com.br/proficuo/), 
é um adjetivo e significa algo:

> Cujo resultado é produtivo, proveitoso, útil ou lucrativo; proficiente.

Ou então:

> Que tende a ser rentável; que possui êxito; rendoso: ele realizou um trabalho profícuo e foi promovido.

## Objetivos

Essa iniciativa nasceu como um projeto de Iniciação Científica em 2020, durante
minha graduação em Design Gráfico. Como leitor de histórias em quadrinhos e entusiasta
do financiamento coletivo, queria entender um pouco desse mercado.

À época, eu publiquei os scripts e a dissertação no github
(analise-campanhas-hq)[https://github.com/silva-erick/analise-campanhas-hq] e já imaginava
que esse trabalho poderia vazar para fora da academia, bem como explorar outras linhas de
análise dos dados. É o que vou tentar fazer por aqui.

## Conceitos básicos

O _Financiamento Coletivo_ é uma maneira de viabilizar projetos ou iniciativas de várias naturezas
a partir do esforço de pessoas entusiastas ou interessadas. Com a popularização da internet,
alguns empreendimentos surgiram como _plataformas_ de financiamento coletivo, oferecendo
mecanismos de divulgação e arrecadação de doações, normalmente reservando um percentual
do total arrecadado das campanhas que foram bem sucedidas.

O sucesso de uma campanha de arrecadação depende da modalidade. Uma campanha _Tudo ou Nada_
será considerada bem sucedida se o valor total arrecadado na data de encerramento
atingiu a meta estabelecida pelas pessoas autoras do projeto. Por outro lado, uma campanha
_Flex_ será considerada bem sucedida se receber qualquer doação, mesmo que não atinja
a meta estabelecida na data de encerramento.

## Origens dos dados

A principal fonte de dados para este trabalho é [Catarse.me](https://www.catarse.me),
seguido de [Apoia.se](https://www.apoia.se).

Os valores monetários nas campanhas, tal como meta, total levantado ou valor de recompensas
é nominal e se refere à época de execução da campanha. Para ter uma base de comparação mais adequada,
vou usar a [Tabela Prática para Cálculo de Atualização Monetária – IPCA-E](https://www.aasp.org.br/suporte-profissional/indices-economicos/indices-judiciais/tabela-pratica-para-calculo-de-atualizacao-monetaria-ipca-e/),
que possui uma maneira bem prática para atualização de um valor monetário para o valor presente.

Para ter uma ideia da participação das HQ viabilizadas com campanhas de financiamento coletivo,
decidi considerar a página de lançamentos do [Guia dos Quadrinhos](http://guiadosquadrinhos.com/),
que se consiste num banco de dados centralizado e de boa qualidade.

## Estrutura do projeto

O projeto está público para que possa ser revisado, criticado ou utilizado por qualquer
pessoa interessada no assunto.

### Análises

Uma tentativa minha de, a partir dos dados produzidos, fazer análises para entender um pouco
da dinâmica do mercado brasileiro de histórias em quadrinhos viabilizadas a partir plataformas
de financiamento coletivo.

### Dados

Se você tem interesse em analisar e interpretar os dados, a pasta _dados_ tem a seguinte estrutura:
- brutos: os dados brutos produzidos a partir das origens dos dados. Os bancos de dados e os arquivos
de CSV são construídos a partir desses arquivos.
- sql: os arquivos de banco de dados em SQLite em tabelas analíticas e sintéticas.
- csv: parecido com o sql, mas em formato CSV.

### bin

Se você gosta de programação, vai encontrar os vários scripts usados na produção de dados
ou nas análises e relatórios na pasta _bin_. Tudo em python e, na medida do possível,
em português brasileiro, para facilitar o acesso.
