# profico-hq - scripts

## Requisitos

Você vai precisar de:
- [Python 3.11.2](https://www.python.org/downloads/): eu testei em Windows 11, mas tenho a expectativa
de que todos os scripts rodem sem necessidade de alteração em outros sistemas operacionais, tal como
GNU/Linux ou macOS.

## Preparação de seu ambiente

Acesse a página do [profico-hq](https://github.com/silva-erick/profico-hq), baixe o zip
e descompacte numa pasta de trabalho. Alternativamente, e clone o projeto com o comando:

```
git clone https://github.com/silva-erick/profico-hq.git
```

Acesse um terminal e navegue até a pasta do zip descompactado ou do projeto clonado.

Crie um virtual environment com o comando:

```
python.exe -m venv venv
```

No windows, ative o virtual environment para isolar as dependências específicas
desse projeto, evitando conflitos com outros projetos ou com o ambiente global do sistema:

```
.\venv\Scripts\activate.ps1
```

Mude a pasta de trabalho para scripts e baixe as bibliotecas necessárias:

```
pip install -r requirements.txt
```

## Scripts

### Produção (ou raspagem) de dados

Scripts para produção de dados a partir das fontes de dados:
- Catarse.me
- AASP
- Guia de Quadrinhos

### Normalizacao

Scripts para normalização dos dados produzidos no processo de raspagem:
- atualização de valores monetários
- classificação de autoria
- categorias de conteúdo
- análises de recompensas

### Banco de Dados

Scripts para criação de bancos de dados:
- sql
- csv