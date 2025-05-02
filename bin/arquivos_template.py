import re
import arquivos

def extrair_campos_template(template):
    """
    extrair campos do template
    """
    # Match the pattern $(something)
    matches = re.findall(r'\$\(([^)]+)\)', template)
    # Use set to remove duplicates
    unique_fields = list(set(matches))
    return unique_fields

def processar_template(caminho_template, valores_mapeados):
    """
    processar um arquivo de template, substituindo as variáveis
    """
    conteudo_template = arquivos.ler_arquivo(caminho_template)
    campos_template = extrair_campos_template(conteudo_template)

    for campo in campos_template:
        if not campo in valores_mapeados:
            continue

        conteudo_template = conteudo_template.replace(f'$({campo})', str(valores_mapeados[campo]))

    return conteudo_template
