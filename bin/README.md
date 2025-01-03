# profico-hq - bin

## Requisitos

Você vai precisar de:
- Um computador com sistema operacional capaz de rodar scritps Python, tal como Linux ou Windows. Eu testei
em Linux.
- [Python 3.x](https://www.python.org/downloads/)
- Git (opcional)

## Preparação de seu ambiente

Se você tem o git instalado, pode clonar o projeto a partir do GitHub:

```
git clone https://github.com/silva-erick/profico-hq.git
```

Ou faça o download do arquivo zip na página do [profico-hq](https://github.com/silva-erick/profico-hq).
Mova o arquivo zip para uma pasta de sua preferência e descompacte o conteúdo.

Acesse um terminal (no Windows, pode ser um terminal em PowerShell) e navegue até a pasta onde você clonou ou descompactou
os fontes do profico-hq.

### Virtual Environment no Windows

No terminal, navegue até a pasta do projeto profico-hq, em seguida, acesse a pasta bin. Digite:

Crie um virtual environment com o comando:

```
python.exe -m venv venv
```

Ative o virtual environment para isolar as dependências específicas
desse projeto, evitando conflitos com outros projetos ou com o ambiente global do sistema:

```
.\venv\Scripts\activate.ps1
```

Instale as dependências:

```
pip install -r requirements.txt
```

### Virtual Environment no Linux

No terminal, navegue até a pasta do projeto profico-hq, me seguida, acesse a pasta bin. Digite:

```
python3 -m venv venv
```

E ative o virtual environement:

```
source venv/bin/activate
```

Instale as dependências:

```
pip install -r requirements.txt
```

## Scripts

### Produção (ou raspagem) de dados

Scripts para produção de dados a partir das fontes de dados:
- Catarse.me
- Apoia.se
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