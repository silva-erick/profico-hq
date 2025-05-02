def ler_arquivo(caminho_arq):
    """
    ler o conteúdo de um arquivo texto com o caminho_arq informado
    """

    with open(caminho_arq, 'r', encoding='utf8') as arq:
        template = arq.read()
        arq.close()

    return template
