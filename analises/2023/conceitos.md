# Conceitos

## Financiamento Coletivo

Antes da _internet_, era comum que um projeto cultural fosse financiado
por um limitado grupo de pessoas físicas ou jurídicas.

Este mecenato podia ser praticado por estas pessoas por diferentes motivos.
O primeiro seria a _filantropia_, isto é, a vontade de promover o bem-estar
humano e social através do financiamento da arte e projetos de cultura.
A filantropia, contudo, não é excludente a outros motivos mais materialistas,
tal como a _autopromoção_, quando a pessoa deseja vincular seu nome ou marca
ao projeto patrocinado, ou a obtenção de _vantagens fiscais_,
tal como acontece com a [Lei Rouanet](https://www.gov.br/secom/pt-br/fatos/brasil-contra-fake/noticias/2023/3/o-que-voce-precisa-saber-sobre-a-lei-rouanet).

No início do século XXI, a sociedade testemunhou uma série
de transformações - certamente catalizadas pela _internet_ - que viabilizaram
uma nova forma de captação de recursos: o _financiamento coletivo_
ou _crowdfunding_.

Com as _redes sociais_, por exemplo, artistas e pessoas produtoras culturais
podem interagir de maneira mais horizontal com o público. O _comércio eletrônico_
consolidou o hábito de _compra à distância_ com a redução dos _custos logísticos_,
a oferta de _meios de pagamento digitais_ e o surgimento da economia de plataforma,
com destaque para as _plataformas de financiamento coletivo_.

Nesse contexto, o financiamento coletivo acontece numa lógica invertida: em vez
de poucas pessoas investindo grandes parcelas no projeto, observamos muitas pessoas
realizando contribuições de pequeno volume.

É importante destacar que nem a _internet_, nem as plataformas de _crowdfunding_
são obrigatórias para a execução de campanhas de financiamento coletivo, mas
elas certamente potencializam os esforços de divulgação e arrecadação destas
campanhas.

## Modalidades de Financiamento

Neste relatório, a _modalidade_ é uma característica determinante das campanhas
para diversas análises e recortes. Nas plataformas de financiamento coletivo
estudadas neste relatório, [Catarse](https://www.catarse.me/)
e [Apoia.se](https://apoia.se/), é possível destacar três modalidades
de financiamento coletivo:

- recorrente;
- tudo ou nada (campanha pontual);
- flex (campanha pontual).

> [!WARNING] 
> As modalidades de financiamento a seguir são categorias de análise deste relatório.
> Por favor, antes de lançar uma campanha de financiamento coletivo, leia as regras,
> recomendações e termos de uso da plataforma.

### Campanhas Recorrentes

A modalidade **recorrente** funciona num modelo de assinatura e não tem data
de encerramento. É utilizada por indivíduos, coletivos ou empresas que precisam
de apoio contínuo e organizam um modelo de negócio que se apoie na arrecadação
continuada, mês a mês.

O modo como cada plataforma de financiamento coletivo lida com as categorias pode
interferir um pouco nas análises. Enquanto em [Catarse](https://www.catarse.me/)
a categoria _quadrinhos_ é para uma campanha de arrecadação voltada para a
produção de quadrinhos, em [Apoia.se](https://apoia.se/) uma campanha pode ter
múltiplas categorias. Dessa forma, no conjunto de dados analisados vamos encontrar
campanhas de indivíduos, coletivos ou empresas voltadas para o financiamento:

- de quadrinhos, especificamente; ou
- de projetos de divulgação de conteúdo geek, tal como canais de youtube, podcasts,
sites ou blogs.

Neste relatório, a campanha recorrente será considerada _bem sucedida_ se receber
ao menos _um apoio de qualquer valor_.

### Campanhas Pontuais

As campanhas pontuais têm duração predefinida, isto é, as pessoas que as organizam
precisam definir uma data de encerramento e uma meta de arrecadação.

Para ser considerada _bem sucedida_, a campanha da modalidade **tudo ou nada**
precisa atingir ou ultrapassar a meta até a data de encerramento. Quando não é
bem sucedida, o dinheiro é ressarcido para as pessoas que apoiaram.

A campanha na modalidade **flex** se diferencia da **tudo ou nada** por não
obrigar o atingimento da meta na data de encerramento. Dessa forma, se não for
cancelada pelas pessoas organizadoras ou pela plataforma de financiamento coletivo,
uma campanha flex será considerada _bem sucedida_ se receber pelo menos um apoio
na data de encerramento.

A tabela a seguir resume em que condições uma campanha pode falhar ou terminar
bem sucedida nas plataformas.

| situação                             | tudo ou nada | flex          |
|--------------------------------------|--------------|---------------|
| ultrapassou a meta                   | bem sucedida | bem sucedida  |
| atingiu a meta                       | bem sucedida | bem sucedida  |
| recebeu pelo menos uma contribuição  | falhou       | bem sucedida  |
| cancelamento antes do encerramento   | falhou       | falhou        |

Os comportamentos diferentes de cada modalidade sugerem usos diferentes. Se a pessoa
organizadora da campanha não possui os recursos para executar o projeto, a modalidade
**tudo ou nada** seria mais adequada porque não implica em compromissos de entrega
com a comunidade apoiadora - de fato, as pessoas apoiadoras são ressarcidas pela
plataforma quando a campanha não é bem sucedida. Por outro lado, se a pessoa
organizadora possui os recursos para viabilizar o projeto, a campanha na modalidade
**flex** pode ser funcionar como um canal de pré-venda.

## Correção Monetária

O valor desejado (meta), o valor arrecado e os valores das recompensas serão ajustados,
de acordo com a [Tabela Prática para Cálculo de Atualização Monetária – IPCA-E](https://www.aasp.org.br/suporte-profissional/indices-economicos/indices-judiciais/tabela-pratica-para-calculo-de-atualizacao-monetaria-ipca-e/)
da AASP, para o valor em dezembro do ano base do relatório (2023, neste caso).

## Classificação de Conteúdo

Um mesmo script python de classificação é utilizado como base para a identificação de gênero
de pessoas autoras ou para a categorização do conteúdo do texto da campanha. A ideia básica
é manter, para cada categoria, uma lista de palavras chave e possíveis variações escritas
na forma de [expressões regulares](https://pt.wikipedia.org/wiki/Express%C3%A3o_regular),
categorizadas como:

- pesquisa exata
- pesquisa aproximada: começa com
- pesquisa aproximada: contém

Para maiores informações, consulte o script de normalização,
[scripts/01-normalizar.py](../../scripts/02-normalizacao/01-normalizar.py), ou os arquivos
de padrões e palavras chave de cada categoria.

### Menções

O arquivo [mencoes.json](../../scripts/02-normalizacao/mencoes.json) contém padrões
e palavras chaves que são usados para testar o pertencimento dos textos das campanhas
a uma determinada categoria de interesse:
- Ângelo Agostini
- CCXP
- Disputa
- Erotismo
- Fantasia
- Ficcao Científica
- FIQ
- Folclore
- Herois
- HQMIX
- Humor
- Jogos
- LGBTQIA+
- Mídia Independente
- Política
- Questões de Gênero
- Religiosidade
- Salões de Humor
- Terror
- Webformatos
- Zine

### Gênero

Na maior parte dos casos, foi possível identificar se quem organiza a campanha é uma
pessoa _individual_, que pode ter gênero determinado como _masculino_ ou _feminino_,
ou um _coletivo_, que pode ser classificado como _empresa_ ou como _coletivo_ de artistas.

Além do arquivo com padrões e palavras chave de gênero de pessoas autoras,
[autorias.json](../../scripts/02-normalizacao/autorias.json), o script também utiliza
um dataset de nomes construído a partir de dados do Censo do IBGE para determinar se
um primeiro nome tem maior frequência no gênero masculino ou feminino.

#### Empresas

A análise dos dados apontou uma série de nomes públicos relacionados a empresas,
organizações, institutos, associações e similares. Foi construída uma base de
conhecimento contendo as seguintes regras para o nome público:
- possui palavras fortes como LTDA, Eireli ou editora
- está numa lista conhecida de empresas

#### Coletivo

A categoria coletivo segue regras parecidas às de empresas, mas no contexto
de coletivos de artistas. O nome público:
- possui palavras frotes como coletivo, equipe, estúdio, studio, selo ou grupo
- está numa lista conhecida de coletivos

#### Individual

Quando o nome público de autoria associado à campanha não foi classificado
como _empresa_ ou _coletivo_, verifica-se se o nome público:
- está numa lista conhecida de nomes de artistas ou personas marcados como
_masculino_ ou _feminino_;
- tem como primeira palavra mais frequente (acima de 75%) como
_masculino_ ou _feminino_. Neste caso, utilizou-se o
[dataset de nomes do brasil.io](https://brasil.io/dataset/genero-nomes/nomes/),
construído a partir do Censo do IBGE.

#### Outros

Nos casos onde não foi possível classificar a autoria, a categoria _outros_
foi utilizada.
