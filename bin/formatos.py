from datetime import datetime, timedelta

def eh_int(s):
    """
    Verificar se uma string é um número inteiro conhecido pelo python.
    """
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def eh_float(s):
    """
    Verifica se uma string é um número float conhecido pelo python.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def como_inteiro(val, cultura=''):
    """
    converter um valor de string para inteiro

    se cultura é pt-br, tratar separar de milhares (.) e decimais(,)
    """
    if cultura=='pt-br':
        return como_inteiro(val.replace('.', '').replace(',', '.'))
    
    if eh_int(val):
        return int(val)
    
    return None

def como_numerico(val, cultura=''):
    """
    converter um valor de string para numérico

    se cultura é pt-br, tratar separar de milhares (.) e decimais(,)
    """
    if cultura=='pt-br':
        return como_numerico(val.replace('.', '').replace(',', '.'))
    
    if eh_float(val):
        return float(val)
    
    return None

def calcular_diferenca_dias(data_inicial_str, data_final_str):
    """
    Calcular a diferença de didas entre data_inicial e data_final
    """

    # Converter as strings em objetos datetime
    data_inicial = datetime.fromisoformat(data_inicial_str.replace('Z', ''))
    
    if data_final_str is None or data_final_str == '':
        # Se a data final for None, use a data atual
        data_final = datetime.utcnow()
    else:
        data_final = datetime.fromisoformat(data_final_str.replace('Z', ''))
    
    # Calcular a diferença em dias
    diferenca = data_final - data_inicial
    
    # Extrair a parte dos dias da diferença
    diferenca_em_dias = diferenca.days
    
    return diferenca_em_dias


def parse_data(data_str):
    """
    ler data como YMD HMSF ou YMD HMS

    gera erro se não estiver no formato esperado
    """
    try:
        # Tenta converter com fração de segundo
        data_obj = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S.%f')
        return data_obj
    except ValueError:
        try:
            # Tenta converter sem fração de segundo
            data_obj = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S')
            return data_obj
        except ValueError:
            raise ValueError("Formato de data inválido.")

def parse_ymd(data_str):
    """
    ler data como ymd

    gera erro se não estiver no formato esperado
    """
    try:
        # Tenta converter com fração de segundo
        data_obj = datetime.strptime(data_str, '%Y-%m-%d')
        return data_obj
    except ValueError:
        raise ValueError("Formato de data inválido.")

def formatar_num0_ptbr(number):
    """
    formatar um número sem casas decimais, em pt-br
    """
    return f"{number:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_num1_ptbr(number):
    """
    formatar um número com uma casa decimal, em pt-br
    """
    return f"{number:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_num2_ptbr(number):
    """
    formatar um número com duas casas decimais, em pt-br
    """
    return f"{number:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    