from datetime import datetime, timedelta

def eh_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def eh_float(s):
    try:
        float(s.replace('.', '', 1))
        return True
    except ValueError:
        return False
    
def como_inteiro(val, cultura=''):
    if cultura=='pt-br':
        return como_inteiro(val.replace('.', '').replace(',', '.'))
    
    if eh_int(val):
        return int(val)
    
    return None

def como_numerico(val, cultura=''):
    if cultura=='pt-br':
        return como_numerico(val.replace('.', '').replace(',', '.'))
    
    if eh_float(val):
        return float(val)
    
    return None

def calcular_diferenca_dias(data_inicial_str, data_final_str):
    # Converter as strings em objetos datetime
    data_inicial = datetime.fromisoformat(data_inicial_str.replace('Z', ''))
    
    if data_final_str is None:
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
