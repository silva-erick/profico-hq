import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import math

CAMINHO_ANALISES = "../dados/analises"
CAMINHO_SQL = "./banco/sql"
CAMINHO_SQL_CRIACAO = "./banco/sql/01-criacao"
CAMINHO_SQL_CARGA = "./banco/sql/02-carga"
CAMINHO_SQL_ANALISES = "./banco/sql/03-analises"
CAMINHO_BRUTO_CAMPANHAS_CATARSE = "../dados/brutos/catarse/campanhas"
CAMINHO_NORMALIZADOS = "../dados/normalizados"
CAMINHO_NORMALIZADOS_LANCAMENTOS = "../dados/normalizados/{ano}/apoio/lancamentos.json"
CAMINHO_NORMALIZADOS_MUNICIPIOS = "../dados/normalizados/{ano}/apoio/cities.json"



