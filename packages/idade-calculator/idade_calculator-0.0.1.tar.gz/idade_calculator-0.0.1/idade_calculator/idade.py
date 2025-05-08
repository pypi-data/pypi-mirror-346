def idade(nascimento: str) -> int:
    """
    Calcula a idade com base na data de nascimento fornecida.

    Args:
        nascimento (str): Data de nascimento no formato 'YYYY-MM-DD'.

    Returns:
        int: Idade em anos.
    """
    from datetime import datetime

    # Converte a string de nascimento para um objeto datetime
    data_nascimento = datetime.strptime(nascimento, '%Y-%m-%d')
    
    # Obtém a data atual
    data_atual = datetime.now()
    
    # Calcula a idade
    idade = data_atual.year - data_nascimento.year
    
    # Verifica se o aniversário já ocorreu este ano
    if (data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1
    
    return idade