"""
Módulo de validação de datas e tempos
"""
from datetime import datetime
from dateutil import parser
from typing import Optional, Union


def is_valid_date(date_str: str, date_format: str) -> bool:
    """
    ✅ Verifica se a string corresponde ao formato de data especificado.
    
    Args:
        date_str (str): String de data a ser validada
        date_format (str): Formato esperado
        
    Returns:
        bool: True se a string for válida, False caso contrário
    """
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def auto_validate_date(date_str: str) -> bool:
    """
    🤖 Tenta identificar automaticamente se uma string é uma data válida.
    
    Args:
        date_str (str): String a ser validada
        
    Returns:
        bool: True se a string for uma data válida, False caso contrário
    """
    try:
        parser.parse(date_str)
        return True
    except ValueError:
        return False


def validate_date_range(
    start_date: Union[str, datetime],
    end_date: Union[str, datetime],
    date_format: Optional[str] = None
) -> bool:
    """
    📅 Valida se um intervalo de datas é válido (data final maior que data inicial).
    
    Args:
        start_date (Union[str, datetime]): Data inicial
        end_date (Union[str, datetime]): Data final
        date_format (Optional[str]): Formato da data (necessário se as datas forem strings)
        
    Returns:
        bool: True se o intervalo for válido, False caso contrário
        
    Raises:
        ValueError: Se o formato da data não for especificado para strings
    """
    if isinstance(start_date, str):
        if not date_format:
            raise ValueError("Formato da data deve ser especificado para strings")
        start_date = datetime.strptime(start_date, date_format)
    
    if isinstance(end_date, str):
        if not date_format:
            raise ValueError("Formato da data deve ser especificado para strings")
        end_date = datetime.strptime(end_date, date_format)
    
    return end_date >= start_date


def validate_time_string(time_str: str, time_format: str = "%H:%M:%S") -> bool:
    """
    ⏰ Valida se uma string representa um horário válido.
    
    Args:
        time_str (str): String de horário
        time_format (str): Formato do horário
        
    Returns:
        bool: True se o horário for válido, False caso contrário
    """
    try:
        datetime.strptime(time_str, time_format)
        return True
    except ValueError:
        return False


def validate_datetime_string(
    datetime_str: str,
    datetime_format: str = "%Y-%m-%d %H:%M:%S"
) -> bool:
    """
    📅⏰ Valida se uma string representa uma data e hora válidas.
    
    Args:
        datetime_str (str): String de data e hora
        datetime_format (str): Formato da data e hora
        
    Returns:
        bool: True se a data e hora forem válidas, False caso contrário
    """
    try:
        datetime.strptime(datetime_str, datetime_format)
        return True
    except ValueError:
        return False 