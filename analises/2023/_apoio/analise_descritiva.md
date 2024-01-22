# Análise Descritiva

A análise descritiva considera o conjunto de dados agrupado por modalidade de financiamento
coletivo. Visões complementares são apresentadas com a adição de mais uma dimensão
de agrupamento, tal como plataforma, unidade federativa, gênero ou menção a algum tema
de interesse à iniciativa profico-hq.


## Modalidade

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento.
| modalidade   |   total |   arrecadado |   total_sucesso |   arrecadado_sucesso |   taxa_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|--------:|-------------:|----------------:|---------------------:|---------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada |    1.335 |  25.609.919,37 |             830 |          24.063.279,83 |           62,2 |        28.991,90 |      44.961,94 |         41,82 |     679.297,66 |
| flex         |    1.468 |  18.362.275,04 |            1.383 |          18.362.131,94 |           94,2 |        13.277,03 |      33.934,83 |         10,77 |     708.972,78 |
| recorrente   |     684 |     43.186,96 |             152 |             43.186,96 |           22,2 |          284,12 |        650,58 |          1,09 |       5.087,08 |


## Plataforma

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Plataforma).
| modalidade   | origem   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:---------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | catarse  |    1.335 |             830 |      100,0 |           62,2 |     24.063.279,83 |        28.991,90 |      44.961,94 |         41,82 |     679.297,66 |
| flex         | apoia.se |       5 |               0 |        0,3 |            0,0 |            0,00 |            0,00 |          0,00 |          0,00 |          0,00 |
| flex         | catarse  |    1.463 |            1.383 |       99,7 |           94,5 |     18.362.131,94 |        13.277,03 |      33.934,83 |         10,77 |     708.972,78 |
| recorrente   | apoia.se |     627 |             137 |       91,7 |           21,9 |        39.550,44 |          288,69 |        682,40 |          1,09 |       5.087,08 |
| recorrente   | catarse  |      57 |              15 |        8,3 |           26,3 |         3.636,52 |          242,43 |        198,40 |         10,98 |        538,44 |


## Unidade Federativa

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Unidade Federativa).
| modalidade   | geral_uf_br   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:--------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | AC            |       1 |               0 |        0,1 |            0,0 |            0,00 |            0,00 |          0,00 |          0,00 |          0,00 |
| tudo ou nada | AL            |       7 |               5 |        0,5 |           71,4 |        55.859,26 |        11.171,85 |       3.760,92 |       6.855,80 |      15.562,69 |
| tudo ou nada | AM            |      14 |               4 |        1,0 |           28,6 |        34.236,01 |         8.559,00 |       4.714,56 |       3.774,42 |      12.904,88 |
| tudo ou nada | BA            |      19 |               7 |        1,4 |           36,8 |       102.481,83 |        14.640,26 |       8.108,09 |       4.203,66 |      28.456,51 |
| tudo ou nada | CE            |      21 |               9 |        1,6 |           42,9 |       115.503,47 |        12.833,72 |      13.733,43 |       1.334,39 |      41.422,60 |
| tudo ou nada | DF            |      40 |              23 |        3,0 |           57,5 |       511.121,61 |        22.222,68 |      16.473,47 |         41,82 |      75.796,33 |
| tudo ou nada | ES            |      11 |               4 |        0,8 |           36,4 |        72.846,55 |        18.211,64 |      17.231,56 |       1.411,86 |      39.851,60 |
| tudo ou nada | GO            |      14 |              10 |        1,0 |           71,4 |       107.857,97 |        10.785,80 |       7.069,02 |        787,10 |      25.867,99 |
| tudo ou nada | MA            |       3 |               1 |        0,2 |           33,3 |         1.952,95 |         1.952,95 |          0,00 |       1.952,95 |       1.952,95 |
| tudo ou nada | MG            |     115 |              67 |        8,6 |           58,3 |      1.822.099,42 |        27.195,51 |      26.573,25 |       1.204,08 |     136.747,60 |
| tudo ou nada | MS            |       2 |               1 |        0,1 |           50,0 |        38.756,00 |        38.756,00 |          0,00 |      38.756,00 |      38.756,00 |
| tudo ou nada | MT            |       2 |               2 |        0,1 |          100,0 |        16.235,65 |         8.117,82 |       3.144,46 |       5.894,35 |      10.341,30 |
| tudo ou nada | PA            |      12 |               4 |        0,9 |           33,3 |       122.971,38 |        30.742,85 |       3.871,10 |      25.693,41 |      34.218,60 |
| tudo ou nada | PB            |      20 |              10 |        1,5 |           50,0 |       291.702,89 |        29.170,29 |      16.041,93 |       9.446,95 |      56.551,80 |
| tudo ou nada | PE            |      41 |              24 |        3,1 |           58,5 |       352.743,08 |        14.697,63 |      11.661,97 |         54,54 |      42.305,25 |
| tudo ou nada | PI            |      20 |              13 |        1,5 |           65,0 |       223.945,26 |        17.226,56 |       9.924,30 |       5.066,02 |      39.440,42 |
| tudo ou nada | PR            |      81 |              48 |        6,1 |           59,3 |      1.856.539,79 |        38.677,91 |      78.534,96 |        792,14 |     537.544,55 |
| tudo ou nada | RJ            |     152 |              94 |       11,4 |           61,8 |      1.992.588,12 |        21.197,75 |      24.242,49 |        143,20 |     154.365,98 |
| tudo ou nada | RN            |      20 |              11 |        1,5 |           55,0 |       159.498,10 |        14.499,83 |       5.851,10 |       3.938,46 |      23.993,89 |
| tudo ou nada | RO            |       1 |               0 |        0,1 |            0,0 |            0,00 |            0,00 |          0,00 |          0,00 |          0,00 |
| tudo ou nada | RS            |     102 |              67 |        7,6 |           65,7 |      1.556.583,95 |        23.232,60 |      18.896,23 |       1.496,11 |      85.108,68 |
| tudo ou nada | SC            |      26 |              14 |        1,9 |           53,8 |       380.975,10 |        27.212,51 |      24.288,71 |       5.156,31 |      82.775,70 |
| tudo ou nada | SE            |       1 |               0 |        0,1 |            0,0 |            0,00 |            0,00 |          0,00 |          0,00 |          0,00 |
| tudo ou nada | SP            |     609 |             412 |       45,6 |           67,7 |     14.246.781,43 |        34.579,57 |      53.785,60 |         94,90 |     679.297,66 |
| tudo ou nada | TO            |       1 |               0 |        0,1 |            0,0 |            0,00 |            0,00 |          0,00 |          0,00 |          0,00 |
| flex         | AL            |       6 |               5 |        0,4 |           83,3 |        20.618,50 |         4.123,70 |       3.042,21 |         52,78 |       8.487,42 |
| flex         | AM            |       4 |               3 |        0,3 |           75,0 |         5.966,55 |         1.988,85 |       1.491,59 |        621,84 |       3.579,71 |
| flex         | BA            |      25 |              21 |        1,7 |           84,0 |       130.434,36 |         6.211,16 |       9.050,77 |         28,49 |      39.043,46 |
| flex         | CE            |      38 |              37 |        2,6 |           97,4 |       292.839,62 |         7.914,58 |      11.620,26 |         60,22 |      42.352,39 |
| flex         | DF            |      30 |              29 |        2,0 |           96,7 |       141.740,83 |         4.887,61 |       6.274,28 |         11,93 |      19.696,84 |
| flex         | ES            |       6 |               3 |        0,4 |           50,0 |        19.243,05 |         6.414,35 |       3.637,51 |       3.221,88 |      10.374,39 |
| flex         | GO            |       6 |               5 |        0,4 |           83,3 |        18.754,48 |         3.750,90 |       4.503,41 |        907,13 |      11.657,13 |
| flex         | MA            |       4 |               4 |        0,3 |          100,0 |        10.257,69 |         2.564,42 |       1.204,75 |       1.415,31 |       3.759,17 |
| flex         | MG            |      71 |              67 |        4,8 |           94,4 |       482.605,55 |         7.203,07 |      10.740,03 |         35,53 |      55.069,70 |
| flex         | MS            |       6 |               5 |        0,4 |           83,3 |        21.988,60 |         4.397,72 |       2.989,46 |        620,57 |       8.364,98 |
| flex         | MT            |       2 |               2 |        0,1 |          100,0 |        19.225,07 |         9.612,53 |      10.123,51 |       2.454,14 |      16.770,93 |
| flex         | PA            |       6 |               5 |        0,4 |           83,3 |        22.468,65 |         4.493,73 |       5.633,18 |        100,76 |      12.609,40 |
| flex         | PB            |      26 |              25 |        1,8 |           96,2 |        92.454,99 |         3.698,20 |       8.668,49 |         81,93 |      37.589,60 |
| flex         | PE            |      60 |              58 |        4,1 |           96,7 |       313.526,53 |         5.405,63 |       5.143,84 |         62,13 |      26.068,83 |
| flex         | PI            |      10 |               6 |        0,7 |           60,0 |        29.669,49 |         4.944,92 |       4.672,47 |        821,54 |      13.165,19 |
| flex         | PR            |      64 |              59 |        4,4 |           92,2 |       688.481,13 |        11.669,17 |      13.175,20 |         48,19 |      59.310,53 |
| flex         | RJ            |     163 |             150 |       11,1 |           92,0 |      2.121.729,30 |        14.144,86 |      20.277,98 |         10,77 |     142.477,57 |
| flex         | RN            |       6 |               3 |        0,4 |           50,0 |        25.188,92 |         8.396,31 |      11.215,07 |        148,24 |      21.166,43 |
| flex         | RO            |       4 |               4 |        0,3 |          100,0 |         5.636,43 |         1.409,11 |       1.366,75 |        131,70 |       3.310,96 |
| flex         | RS            |     142 |             141 |        9,7 |           99,3 |      1.762.708,33 |        12.501,48 |      18.586,72 |         57,99 |     118.699,04 |
| flex         | SC            |      21 |              18 |        1,4 |           85,7 |        88.617,57 |         4.923,20 |       7.139,53 |         42,01 |      28.385,54 |
| flex         | SE            |       2 |               1 |        0,1 |           50,0 |         2.029,96 |         2.029,96 |          0,00 |       2.029,96 |       2.029,96 |
| flex         | SP            |     766 |             732 |       52,2 |           95,6 |     12.045.946,34 |        16.456,21 |      44.170,98 |         23,05 |     708.972,78 |
| recorrente   | AL            |       5 |               0 |        0,7 |            0,0 |            0,00 |            0,00 |          0,00 |          0,00 |          0,00 |
| recorrente   | AM            |      13 |               1 |        1,9 |            7,7 |            2,02 |            2,02 |          0,00 |          2,02 |          2,02 |
| recorrente   | AP            |       2 |               1 |        0,3 |           50,0 |           70,02 |           70,02 |          0,00 |         70,02 |         70,02 |
| recorrente   | BA            |      25 |               4 |        3,7 |           16,0 |          392,12 |           98,03 |         24,95 |         76,68 |        127,07 |
| recorrente   | CE            |      26 |               8 |        3,8 |           30,8 |          615,96 |           76,99 |         87,20 |          3,16 |        252,23 |
| recorrente   | DF            |      10 |               5 |        1,5 |           50,0 |         1.789,00 |          357,80 |        222,39 |        102,01 |        606,04 |
| recorrente   | ES            |      12 |               5 |        1,8 |           41,7 |          476,39 |           95,28 |        141,24 |         10,54 |        344,69 |
| recorrente   | GO            |       6 |               1 |        0,9 |           16,7 |          277,47 |          277,47 |          0,00 |        277,47 |        277,47 |
| recorrente   | MA            |      11 |               2 |        1,6 |           18,2 |           55,76 |           27,88 |         30,06 |          6,63 |         49,14 |
| recorrente   | MG            |      62 |              10 |        9,1 |           16,1 |         4.465,64 |          446,56 |       1.066,78 |          7,15 |       3.475,05 |
| recorrente   | MT            |       1 |               0 |        0,1 |            0,0 |            0,00 |            0,00 |          0,00 |          0,00 |          0,00 |
| recorrente   | PA            |      16 |               4 |        2,3 |           25,0 |          293,87 |           73,47 |         66,14 |          5,28 |        157,76 |
| recorrente   | PB            |      11 |               1 |        1,6 |            9,1 |          140,18 |          140,18 |          0,00 |        140,18 |        140,18 |
| recorrente   | PE            |      23 |               6 |        3,4 |           26,1 |         1.088,70 |          181,45 |        209,32 |          5,26 |        538,07 |
| recorrente   | PI            |       7 |               0 |        1,0 |            0,0 |            0,00 |            0,00 |          0,00 |          0,00 |          0,00 |
| recorrente   | PR            |      42 |              12 |        6,1 |           28,6 |         4.227,20 |          352,27 |        491,75 |          6,33 |       1.809,10 |
| recorrente   | RJ            |      86 |              22 |       12,6 |           25,6 |         6.116,28 |          278,01 |        408,56 |          3,80 |       1.594,03 |
| recorrente   | RN            |       7 |               0 |        1,0 |            0,0 |            0,00 |            0,00 |          0,00 |          0,00 |          0,00 |
| recorrente   | RO            |       2 |               0 |        0,3 |            0,0 |            0,00 |            0,00 |          0,00 |          0,00 |          0,00 |
| recorrente   | RS            |      55 |              14 |        8,0 |           25,5 |         4.193,00 |          299,50 |        239,17 |          1,09 |        657,08 |
| recorrente   | SC            |      14 |               2 |        2,0 |           14,3 |         2.207,97 |         1.103,99 |        918,36 |        454,61 |       1.753,37 |
| recorrente   | SE            |      10 |               1 |        1,5 |           10,0 |           53,86 |           53,86 |          0,00 |         53,86 |         53,86 |
| recorrente   | SP            |     229 |              53 |       33,5 |           23,1 |        16.721,53 |          315,50 |        902,69 |          3,80 |       5.087,08 |
| recorrente   | TO            |       1 |               0 |        0,1 |            0,0 |            0,00 |            0,00 |          0,00 |          0,00 |          0,00 |
| recorrente   | XX            |       8 |               0 |        1,2 |            0,0 |            0,00 |            0,00 |          0,00 |          0,00 |          0,00 |


## Gênero

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Gênero).
| modalidade   | autoria_classificacao   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:------------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | coletivo                |      44 |              29 |        3,3 |           65,9 |       710.060,78 |        24.484,85 |      25.328,68 |       4.520,87 |     111.934,90 |
| tudo ou nada | empresa                 |     117 |              83 |        8,8 |           70,9 |      4.257.136,76 |        51.290,80 |      65.495,08 |         54,54 |     264.585,91 |
| tudo ou nada | feminino                |     209 |             140 |       15,7 |           67,0 |      3.881.052,70 |        27.721,81 |      48.958,87 |         41,82 |     537.544,55 |
| tudo ou nada | masculino               |     959 |             576 |       71,8 |           60,1 |     15.212.724,00 |        26.410,98 |      40.119,88 |         94,90 |     679.297,66 |
| tudo ou nada | outros                  |       6 |               2 |        0,4 |           33,3 |         2.305,58 |         1.152,79 |        803,09 |        584,92 |       1.720,66 |
| flex         | coletivo                |      72 |              69 |        4,9 |           95,8 |      1.479.515,33 |        21.442,25 |      34.235,40 |         29,81 |     169.836,91 |
| flex         | empresa                 |     440 |             440 |       30,0 |          100,0 |      9.259.515,00 |        21.044,35 |      46.143,04 |         34,74 |     708.972,78 |
| flex         | feminino                |     182 |             176 |       12,4 |           96,7 |      1.145.985,99 |         6.511,28 |       6.521,40 |         35,53 |      29.736,69 |
| flex         | masculino               |     763 |             691 |       52,0 |           90,6 |      6.465.887,70 |         9.357,29 |      27.421,05 |         10,77 |     442.290,11 |
| flex         | outros                  |      11 |               7 |        0,7 |           63,6 |        11.227,92 |         1.603,99 |       2.112,50 |         42,36 |       5.515,84 |
| recorrente   | coletivo                |      28 |               7 |        4,1 |           25,0 |         1.146,91 |          163,84 |        138,02 |         32,56 |        353,58 |
| recorrente   | empresa                 |       9 |               2 |        1,3 |           22,2 |         1.022,28 |          511,14 |         38,60 |        483,84 |        538,44 |
| recorrente   | feminino                |      69 |              18 |       10,1 |           26,1 |         5.551,37 |          308,41 |        399,36 |          7,15 |       1.753,37 |
| recorrente   | masculino               |     101 |              25 |       14,8 |           24,8 |         9.304,80 |          372,19 |        661,58 |          6,10 |       2.998,54 |
| recorrente   | outros                  |     477 |             100 |       69,7 |           21,0 |        26.161,60 |          261,62 |        711,52 |          1,09 |       5.087,08 |


## Menções: Ângelo Agostini

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Ângelo Agostini).
| modalidade   | mencoes_angelo_agostini   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:--------------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False                     |    1.268 |             769 |       95,0 |           60,6 |     21.018.027,02 |        27.331,63 |      36.670,66 |         41,82 |     537.544,55 |
| tudo ou nada | True                      |      67 |              61 |        5,0 |           91,0 |      3.045.252,81 |        49.922,18 |     101.183,47 |       2.944,09 |     679.297,66 |
| flex         | False                     |    1.364 |            1.279 |       92,9 |           93,8 |     16.041.563,99 |        12.542,27 |      30.835,65 |         10,77 |     708.972,78 |
| flex         | True                      |     104 |             104 |        7,1 |          100,0 |      2.320.567,95 |        22.313,15 |      59.701,59 |        458,93 |     442.290,11 |
| recorrente   | False                     |     682 |             150 |       99,7 |           22,0 |        41.280,84 |          275,21 |        643,62 |          1,09 |       5.087,08 |
| recorrente   | True                      |       2 |               2 |        0,3 |          100,0 |         1.906,11 |          953,06 |       1.131,81 |        152,75 |       1.753,37 |


## Menções: CCXP

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: CCXP).
| modalidade   | mencoes_ccxp   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:---------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False          |    1.179 |             704 |       88,3 |           59,7 |     21.202.461,39 |        30.117,13 |      47.960,71 |         41,82 |     679.297,66 |
| tudo ou nada | True           |     156 |             126 |       11,7 |           80,8 |      2.860.818,44 |        22.704,91 |      20.582,18 |       1.720,66 |     154.365,98 |
| flex         | False          |    1.293 |            1.208 |       88,1 |           93,4 |     15.952.537,74 |        13.205,74 |      35.396,12 |         10,77 |     708.972,78 |
| flex         | True           |     175 |             175 |       11,9 |          100,0 |      2.409.594,20 |        13.769,11 |      21.333,70 |        313,27 |     121.747,80 |
| recorrente   | False          |     678 |             147 |       99,1 |           21,7 |        41.148,97 |          279,92 |        649,37 |          1,09 |       5.087,08 |
| recorrente   | True           |       6 |               5 |        0,9 |           83,3 |         2.037,99 |          407,60 |        752,99 |         40,66 |       1.753,37 |


## Menções: Disputa

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Disputa).
| modalidade   | mencoes_disputa   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False             |     935 |             585 |       70,0 |           62,6 |     17.530.337,95 |        29.966,39 |      50.451,48 |         41,82 |     679.297,66 |
| tudo ou nada | True              |     400 |             245 |       30,0 |           61,3 |      6.532.941,88 |        26.665,07 |      27.722,18 |        787,10 |     163.173,27 |
| flex         | False             |     900 |             837 |       61,3 |           93,0 |     10.673.965,92 |        12.752,65 |      40.423,18 |         10,77 |     708.972,78 |
| flex         | True              |     568 |             546 |       38,7 |           96,1 |      7.688.166,01 |        14.080,89 |      20.311,27 |         11,93 |     133.707,59 |
| recorrente   | False             |     622 |             130 |       90,9 |           20,9 |        34.215,34 |          263,19 |        554,63 |          3,80 |       3.475,05 |
| recorrente   | True              |      62 |              22 |        9,1 |           35,5 |         8.971,62 |          407,80 |       1.065,40 |          1,09 |       5.087,08 |


## Menções: Erotismo

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Erotismo).
| modalidade   | mencoes_erotismo   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:-------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False              |    1.212 |             748 |       90,8 |           61,7 |     21.757.202,10 |        29.087,17 |      46.703,04 |         41,82 |     679.297,66 |
| tudo ou nada | True               |     123 |              82 |        9,2 |           66,7 |      2.306.077,73 |        28.122,90 |      23.954,89 |       1.990,95 |     125.535,74 |
| flex         | False              |    1.261 |            1.179 |       85,9 |           93,5 |     15.125.494,32 |        12.829,09 |      35.228,72 |         10,77 |     708.972,78 |
| flex         | True               |     207 |             204 |       14,1 |           98,6 |      3.236.637,62 |        15.865,87 |      25.100,56 |         45,24 |     200.069,51 |
| recorrente   | False              |     661 |             147 |       96,6 |           22,2 |        37.037,76 |          251,96 |        526,38 |          1,09 |       3.475,05 |
| recorrente   | True               |      23 |               5 |        3,4 |           21,7 |         6.149,20 |         1.229,84 |       2.169,93 |          6,63 |       5.087,08 |


## Menções: Fantasia

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Fantasia).
| modalidade   | mencoes_fantasia   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:-------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False              |    1.056 |             650 |       79,1 |           61,6 |     19.246.444,23 |        29.609,91 |      48.242,72 |         41,82 |     679.297,66 |
| tudo ou nada | True               |     279 |             180 |       20,9 |           64,5 |      4.816.835,60 |        26.760,20 |      30.295,09 |         94,90 |     264.585,91 |
| flex         | False              |    1.142 |            1.065 |       77,8 |           93,3 |     12.621.534,92 |        11.851,21 |      29.509,21 |         10,77 |     475.290,95 |
| flex         | True               |     326 |             318 |       22,2 |           97,5 |      5.740.597,02 |        18.052,19 |      45.474,47 |         43,14 |     708.972,78 |
| recorrente   | False              |     643 |             136 |       94,0 |           21,2 |        41.223,62 |          303,11 |        684,06 |          1,09 |       5.087,08 |
| recorrente   | True               |      41 |              16 |        6,0 |           39,0 |         1.963,34 |          122,71 |        134,98 |          5,28 |        538,44 |


## Menções: Ficcao Científica

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Ficcao Científica).
| modalidade   | mencoes_ficcao_cientifica   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:----------------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False                       |    1.039 |             651 |       77,8 |           62,7 |     18.661.633,68 |        28.666,10 |      44.525,52 |         41,82 |     679.297,66 |
| tudo ou nada | True                        |     296 |             179 |       22,2 |           60,5 |      5.401.646,15 |        30.176,79 |      46.623,44 |         54,54 |     537.544,55 |
| flex         | False                       |    1.116 |            1.045 |       76,0 |           93,6 |     13.073.618,33 |        12.510,64 |      30.558,59 |         23,05 |     475.290,95 |
| flex         | True                        |     352 |             338 |       24,0 |           96,0 |      5.288.513,61 |        15.646,49 |      42.686,00 |         10,77 |     708.972,78 |
| recorrente   | False                       |     613 |             135 |       89,6 |           22,0 |        41.147,50 |          304,80 |        685,67 |          1,09 |       5.087,08 |
| recorrente   | True                        |      71 |              17 |       10,4 |           23,9 |         2.039,45 |          119,97 |        157,26 |          2,02 |        538,44 |


## Menções: FIQ

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: FIQ).
| modalidade   | mencoes_fiq   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:--------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False         |    1.116 |             668 |       83,6 |           59,9 |     19.242.021,98 |        28.805,42 |      46.481,14 |         41,82 |     679.297,66 |
| tudo ou nada | True          |     219 |             162 |       16,4 |           74,0 |      4.821.257,85 |        29.760,85 |      38.181,98 |       1.405,43 |     396.557,50 |
| flex         | False         |    1.321 |            1.241 |       90,0 |           93,9 |     15.644.764,94 |        12.606,58 |      28.732,87 |         10,77 |     475.290,95 |
| flex         | True          |     147 |             142 |       10,0 |           96,6 |      2.717.367,00 |        19.136,39 |      63.151,50 |         39,63 |     708.972,78 |
| recorrente   | False         |     647 |             141 |       94,6 |           21,8 |        39.262,48 |          278,46 |        662,54 |          1,09 |       5.087,08 |
| recorrente   | True          |      37 |              11 |        5,4 |           29,7 |         3.924,48 |          356,77 |        489,37 |         10,98 |       1.753,37 |


## Menções: Folclore

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Folclore).
| modalidade   | mencoes_folclore   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:-------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False              |    1.135 |             690 |       85,0 |           60,8 |     19.555.959,93 |        28.341,97 |      44.866,48 |         41,82 |     679.297,66 |
| tudo ou nada | True               |     200 |             140 |       15,0 |           70,0 |      4.507.319,89 |        32.195,14 |      45.455,39 |       1.081,47 |     396.557,50 |
| flex         | False              |    1.177 |            1.098 |       80,2 |           93,3 |     13.275.158,23 |        12.090,31 |      28.982,02 |         10,77 |     475.290,95 |
| flex         | True               |     291 |             285 |       19,8 |           97,9 |      5.086.973,71 |        17.849,03 |      48.299,83 |         55,43 |     708.972,78 |
| recorrente   | False              |     660 |             141 |       96,5 |           21,4 |        41.071,67 |          291,29 |        669,07 |          1,09 |       5.087,08 |
| recorrente   | True               |      24 |              11 |        3,5 |           45,8 |         2.115,28 |          192,30 |        337,60 |          6,10 |       1.135,98 |


## Menções: Herois

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Herois).
| modalidade   | mencoes_herois   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:-----------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False            |    1.059 |             673 |       79,3 |           63,6 |     20.588.794,41 |        30.592,56 |      48.256,73 |         41,82 |     679.297,66 |
| tudo ou nada | True             |     276 |             157 |       20,7 |           56,9 |      3.474.485,41 |        22.130,48 |      25.554,86 |        989,68 |     161.153,63 |
| flex         | False            |    1.114 |            1.040 |       75,9 |           93,4 |     12.864.610,35 |        12.369,82 |      35.964,90 |         10,77 |     708.972,78 |
| flex         | True             |     354 |             343 |       24,1 |           96,9 |      5.497.521,58 |        16.027,76 |      26.716,10 |         11,93 |     203.551,22 |
| recorrente   | False            |     640 |             141 |       93,6 |           22,0 |        35.908,18 |          254,67 |        536,75 |          1,09 |       3.475,05 |
| recorrente   | True             |      44 |              11 |        6,4 |           25,0 |         7.278,78 |          661,71 |       1.479,40 |         10,98 |       5.087,08 |


## Menções: HQMIX

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: HQMIX).
| modalidade   | mencoes_hqmix   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:----------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False           |    1.213 |             722 |       90,9 |           59,5 |     20.304.271,96 |        28.122,26 |      37.985,48 |         41,82 |     537.544,55 |
| tudo ou nada | True            |     122 |             108 |        9,1 |           88,5 |      3.759.007,87 |        34.805,63 |      76.815,19 |        787,10 |     679.297,66 |
| flex         | False           |    1.300 |            1.215 |       88,6 |           93,5 |     15.608.053,44 |        12.846,13 |      31.586,75 |         10,77 |     708.972,78 |
| flex         | True            |     168 |             168 |       11,4 |          100,0 |      2.754.078,50 |        16.393,32 |      47.599,93 |        105,57 |     442.290,11 |
| recorrente   | False           |     679 |             149 |       99,3 |           21,9 |        41.126,16 |          276,01 |        645,56 |          1,09 |       5.087,08 |
| recorrente   | True            |       5 |               3 |        0,7 |           60,0 |         2.060,80 |          686,93 |        931,61 |         31,49 |       1.753,37 |


## Menções: Humor

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Humor).
| modalidade   | mencoes_humor   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:----------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False           |    1.064 |             633 |       79,7 |           59,5 |     17.565.621,62 |        27.749,80 |      37.329,02 |         41,82 |     537.544,55 |
| tudo ou nada | True            |     271 |             197 |       20,3 |           72,7 |      6.497.658,21 |        32.983,04 |      63.531,59 |         54,54 |     679.297,66 |
| flex         | False           |    1.191 |            1.110 |       81,1 |           93,2 |     12.813.838,47 |        11.544,00 |      23.215,13 |         10,77 |     475.290,95 |
| flex         | True            |     277 |             273 |       18,9 |           98,6 |      5.548.293,47 |        20.323,42 |      59.929,42 |         76,12 |     708.972,78 |
| recorrente   | False           |     630 |             131 |       92,1 |           20,8 |        30.146,28 |          230,12 |        475,50 |          1,09 |       3.475,05 |
| recorrente   | True            |      54 |              21 |        7,9 |           38,9 |        13.040,68 |          620,98 |       1.260,03 |         25,34 |       5.087,08 |


## Menções: Jogos

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Jogos).
| modalidade   | mencoes_jogos   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:----------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False           |    1.051 |             629 |       78,7 |           59,8 |     18.458.513,51 |        29.345,81 |      42.800,98 |         41,82 |     537.544,55 |
| tudo ou nada | True            |     284 |             201 |       21,3 |           70,8 |      5.604.766,32 |        27.884,41 |      51.240,25 |       1.411,86 |     679.297,66 |
| flex         | False           |    1.147 |            1.068 |       78,1 |           93,1 |     13.714.158,76 |        12.840,97 |      34.241,82 |         10,77 |     708.972,78 |
| flex         | True            |     321 |             315 |       21,9 |           98,1 |      4.647.973,18 |        14.755,47 |      32.882,80 |         40,22 |     475.290,95 |
| recorrente   | False           |     623 |             135 |       91,1 |           21,7 |        35.385,59 |          262,12 |        548,23 |          1,09 |       3.475,05 |
| recorrente   | True            |      61 |              17 |        8,9 |           27,9 |         7.801,37 |          458,90 |       1.200,33 |          6,10 |       5.087,08 |


## Menções: LGBTQIA+

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: LGBTQIA+).
| modalidade   | mencoes_lgbtqiamais   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:----------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False                 |    1.253 |             772 |       93,9 |           61,6 |     22.460.722,20 |        29.094,20 |      45.405,66 |         41,82 |     679.297,66 |
| tudo ou nada | True                  |      82 |              58 |        6,1 |           70,7 |      1.602.557,62 |        27.630,30 |      38.892,54 |        721,79 |     264.456,52 |
| flex         | False                 |    1.333 |            1.249 |       90,8 |           93,7 |     16.220.233,31 |        12.986,58 |      35.064,85 |         10,77 |     708.972,78 |
| flex         | True                  |     135 |             134 |        9,2 |           99,3 |      2.141.898,62 |        15.984,32 |      20.504,04 |         23,05 |     103.442,87 |
| recorrente   | False                 |     669 |             149 |       97,8 |           22,3 |        40.771,69 |          273,64 |        645,11 |          1,09 |       5.087,08 |
| recorrente   | True                  |      15 |               3 |        2,2 |           20,0 |         2.415,27 |          805,09 |        862,73 |         66,60 |       1.753,37 |


## Menções: Mídia Independente

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Mídia Independente).
| modalidade   | mencoes_midia_independente   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:-----------------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False                        |    1.195 |             733 |       89,5 |           61,3 |     19.844.396,73 |        27.072,85 |      42.641,35 |         41,82 |     679.297,66 |
| tudo ou nada | True                         |     140 |              97 |       10,5 |           69,3 |      4.218.883,10 |        43.493,64 |      57.897,48 |       1.405,43 |     264.585,91 |
| flex         | False                        |    1.363 |            1.283 |       92,8 |           94,1 |     16.638.713,83 |        12.968,60 |      34.573,22 |         10,77 |     708.972,78 |
| flex         | True                         |     105 |             100 |        7,2 |           95,2 |      1.723.418,10 |        17.234,18 |      24.079,23 |         42,01 |     133.783,37 |
| recorrente   | False                        |     607 |             134 |       88,7 |           22,1 |        34.891,86 |          260,39 |        550,02 |          1,09 |       3.475,05 |
| recorrente   | True                         |      77 |              18 |       11,3 |           23,4 |         8.295,10 |          460,84 |       1.164,13 |          5,26 |       5.087,08 |


## Menções: Política

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Política).
| modalidade   | mencoes_politica   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:-------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False              |    1.095 |             676 |       82,0 |           61,7 |     19.080.546,64 |        28.225,66 |      47.064,71 |         41,82 |     679.297,66 |
| tudo ou nada | True               |     240 |             154 |       18,0 |           64,2 |      4.982.733,19 |        32.355,41 |      34.162,57 |         54,54 |     215.281,29 |
| flex         | False              |    1.109 |            1.032 |       75,5 |           93,1 |     13.033.206,06 |        12.629,08 |      37.221,11 |         10,77 |     708.972,78 |
| flex         | True               |     359 |             351 |       24,5 |           97,8 |      5.328.925,88 |        15.182,13 |      21.474,72 |         28,49 |     157.001,80 |
| recorrente   | False              |     620 |             128 |       90,6 |           20,6 |        33.225,36 |          259,57 |        546,57 |          2,02 |       3.475,05 |
| recorrente   | True               |      64 |              24 |        9,4 |           37,5 |         9.961,59 |          415,07 |       1.052,58 |          1,09 |       5.087,08 |


## Menções: Questões de Gênero

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Questões de Gênero).
| modalidade   | mencoes_questoes_genero   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:--------------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False                     |    1.300 |             806 |       97,4 |           62,0 |     23.440.366,37 |        29.082,34 |      45.408,96 |         41,82 |     679.297,66 |
| tudo ou nada | True                      |      35 |              24 |        2,6 |           68,6 |       622.913,46 |        25.954,73 |      26.184,68 |       3.366,14 |     123.112,70 |
| flex         | False                     |    1.402 |            1.318 |       95,5 |           94,0 |     16.941.887,64 |        12.854,24 |      28.902,39 |         10,77 |     475.290,95 |
| flex         | True                      |      66 |              65 |        4,5 |           98,5 |      1.420.244,30 |        21.849,91 |      87.169,62 |        100,54 |     708.972,78 |
| recorrente   | False                     |     677 |             150 |       99,0 |           22,2 |        40.838,28 |          272,26 |        643,16 |          1,09 |       5.087,08 |
| recorrente   | True                      |       7 |               2 |        1,0 |           28,6 |         2.348,68 |         1.174,34 |        818,87 |        595,31 |       1.753,37 |


## Menções: Religiosidade

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Religiosidade).
| modalidade   | mencoes_religiosidade   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:------------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False                   |     975 |             619 |       73,0 |           63,5 |     17.443.278,03 |        28.179,77 |      38.750,17 |         41,82 |     537.544,55 |
| tudo ou nada | True                    |     360 |             211 |       27,0 |           58,6 |      6.620.001,80 |        31.374,42 |      59.614,09 |        322,20 |     679.297,66 |
| flex         | False                   |    1.032 |             960 |       70,3 |           93,0 |     11.579.638,68 |        12.062,12 |      25.131,27 |         10,77 |     475.290,95 |
| flex         | True                    |     436 |             423 |       29,7 |           97,0 |      6.782.493,26 |        16.034,26 |      48.218,37 |         42,01 |     708.972,78 |
| recorrente   | False                   |     630 |             134 |       92,1 |           21,3 |        34.541,87 |          257,78 |        549,21 |          1,09 |       3.475,05 |
| recorrente   | True                    |      54 |              18 |        7,9 |           33,3 |         8.645,09 |          480,28 |       1.163,40 |          6,10 |       5.087,08 |


## Menções: Salões de Humor

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Salões de Humor).
| modalidade   | mencoes_saloes_humor   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:-----------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False                  |    1.319 |             818 |       98,8 |           62,0 |     23.900.709,90 |        29.218,47 |      45.235,92 |         41,82 |     679.297,66 |
| tudo ou nada | True                   |      16 |              12 |        1,2 |           75,0 |       162.569,93 |        13.547,49 |      10.287,95 |        459,39 |      29.349,35 |
| flex         | False                  |    1.454 |            1.369 |       99,0 |           94,2 |     18.218.816,15 |        13.308,12 |      34.075,01 |         10,77 |     708.972,78 |
| flex         | True                   |      14 |              14 |        1,0 |          100,0 |       143.315,79 |        10.236,84 |      15.061,82 |         88,75 |      50.948,86 |
| recorrente   | False                  |     683 |             152 |       99,9 |           22,3 |        43.186,96 |          284,12 |        650,58 |          1,09 |       5.087,08 |
| recorrente   | True                   |       1 |               0 |        0,1 |            0,0 |            0,00 |            0,00 |          0,00 |          0,00 |          0,00 |


## Menções: Terror

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Terror).
| modalidade   | mencoes_terror   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:-----------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False            |     839 |             503 |       62,8 |           60,0 |     14.584.160,44 |        28.994,35 |      39.962,68 |         41,82 |     396.557,50 |
| tudo ou nada | True             |     496 |             327 |       37,2 |           65,9 |      9.479.119,39 |        28.988,13 |      51.783,65 |        787,10 |     679.297,66 |
| flex         | False            |     784 |             710 |       53,4 |           90,6 |      7.672.819,51 |        10.806,79 |      24.052,24 |         10,77 |     374.565,15 |
| flex         | True             |     684 |             673 |       46,6 |           98,4 |     10.689.312,43 |        15.883,08 |      41.769,03 |         29,81 |     708.972,78 |
| recorrente   | False            |     613 |             126 |       89,6 |           20,6 |        33.433,96 |          265,35 |        563,00 |          1,09 |       3.475,05 |
| recorrente   | True             |      71 |              26 |       10,4 |           36,6 |         9.753,00 |          375,12 |        980,44 |          6,10 |       5.087,08 |


## Menções: Webformatos

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Webformatos).
| modalidade   | mencoes_webformatos   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:----------------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False                 |    1.216 |             741 |       91,1 |           60,9 |     21.958.385,24 |        29.633,45 |      46.925,01 |         41,82 |     679.297,66 |
| tudo ou nada | True                  |     119 |              89 |        8,9 |           74,8 |      2.104.894,58 |        23.650,50 |      22.257,37 |       3.458,60 |     136.747,60 |
| flex         | False                 |    1.363 |            1.280 |       92,8 |           93,9 |     16.983.750,32 |        13.268,55 |      32.710,94 |         10,77 |     708.972,78 |
| flex         | True                  |     105 |             103 |        7,2 |           98,1 |      1.378.381,62 |        13.382,35 |      46.750,77 |        298,26 |     475.290,95 |
| recorrente   | False                 |     649 |             135 |       94,9 |           20,8 |        41.633,14 |          308,39 |        684,95 |          2,02 |       5.087,08 |
| recorrente   | True                  |      35 |              17 |        5,1 |           48,6 |         1.553,82 |           91,40 |        144,49 |          1,09 |        575,83 |


## Menções: Zine

A tabela a seguir considera apenas as campanhas bem sucedidas, apresentando as medidas
de estatística descritiva para cada modalidade de financiamento e dimensão em destaque
(Menções: Zine).
| modalidade   | mencoes_zine   |   total |   total_sucesso |   particip |   taxa_sucesso |   valor_sucesso |   media_sucesso |   std_sucesso |   min_sucesso |   max_sucesso |
|:-------------|:---------------|--------:|----------------:|-----------:|---------------:|----------------:|----------------:|--------------:|--------------:|--------------:|
| tudo ou nada | False          |    1.171 |             718 |       87,7 |           61,3 |     21.747.572,18 |        30.289,10 |      47.556,14 |         41,82 |     679.297,66 |
| tudo ou nada | True           |     164 |             112 |       12,3 |           68,3 |      2.315.707,64 |        20.675,96 |      20.218,38 |         54,54 |     161.153,63 |
| flex         | False          |    1.256 |            1.172 |       85,6 |           93,3 |     16.260.444,87 |        13.874,10 |      36.136,28 |         10,77 |     708.972,78 |
| flex         | True           |     212 |             211 |       14,4 |           99,5 |      2.101.687,07 |         9.960,60 |      16.847,68 |         35,53 |     200.069,51 |
| recorrente   | False          |     656 |             143 |       95,9 |           21,8 |        42.082,31 |          294,28 |        668,40 |          1,09 |       5.087,08 |
| recorrente   | True           |      28 |               9 |        4,1 |           32,1 |         1.104,65 |          122,74 |        166,63 |          6,10 |        538,44 |


