"""
Módulo de operações temporais
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Union, Literal


def add_time(
    date_obj: datetime,
    days: int = 0,
    months: int = 0,
    years: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0
) -> datetime:
    """
    ➕ Adiciona tempo a uma data.
    
    Args:
        date_obj (datetime): Data base
        days (int): Número de dias a adicionar
        months (int): Número de meses a adicionar
        years (int): Número de anos a adicionar
        hours (int): Número de horas a adicionar
        minutes (int): Número de minutos a adicionar
        seconds (int): Número de segundos a adicionar
        
    Returns:
        datetime: Nova data com o tempo adicionado
    """
    return date_obj + relativedelta(
        days=days,
        months=months,
        years=years,
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )


def subtract_time(
    date_obj: datetime,
    days: int = 0,
    months: int = 0,
    years: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0
) -> datetime:
    """
    ➖ Subtrai tempo de uma data.
    
    Args:
        date_obj (datetime): Data base
        days (int): Número de dias a subtrair
        months (int): Número de meses a subtrair
        years (int): Número de anos a subtrair
        hours (int): Número de horas a subtrair
        minutes (int): Número de minutos a subtrair
        seconds (int): Número de segundos a subtrair
        
    Returns:
        datetime: Nova data com o tempo subtraído
    """
    return date_obj - relativedelta(
        days=days,
        months=months,
        years=years,
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )


def calculate_difference(
    date1: datetime,
    date2: datetime,
    unit: Literal['days', 'seconds', 'minutes', 'hours', 'weeks', 'months', 'years'] = 'days'
) -> Union[int, float]:
    """
    📏 Calcula a diferença entre duas datas na unidade especificada.
    
    Args:
        date1 (datetime): Primeira data
        date2 (datetime): Segunda data
        unit (str): Unidade de medida ('days', 'seconds', 'minutes', 'hours', 'weeks', 'months', 'years')
        
    Returns:
        Union[int, float]: Diferença entre as datas na unidade especificada
    """
    delta = abs(date2 - date1)
    
    if unit == 'days':
        return delta.days
    elif unit == 'seconds':
        return delta.total_seconds()
    elif unit == 'minutes':
        return delta.total_seconds() / 60
    elif unit == 'hours':
        return delta.total_seconds() / 3600
    elif unit == 'weeks':
        return delta.days / 7
    elif unit == 'months':
        return (date2.year - date1.year) * 12 + (date2.month - date1.month)
    elif unit == 'years':
        return date2.year - date1.year
    else:
        raise ValueError(f"Unidade '{unit}' não suportada")


def get_week_number(date_obj: datetime) -> int:
    """
    📅 Retorna o número da semana do ano para uma data.
    
    Args:
        date_obj (datetime): Data para calcular a semana
        
    Returns:
        int: Número da semana (1-53)
    """
    return date_obj.isocalendar()[1]


def is_leap_year(year: int) -> bool:
    """
    🗓️ Verifica se um ano é bissexto.
    
    Args:
        year (int): Ano a ser verificado
        
    Returns:
        bool: True se o ano for bissexto, False caso contrário
    """
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def get_days_in_month(year: int, month: int) -> int:
    """
    📅 Retorna o número de dias em um mês específico.
    
    Args:
        year (int): Ano
        month (int): Mês (1-12)
        
    Returns:
        int: Número de dias no mês
    """
    if month == 2:
        return 29 if is_leap_year(year) else 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31 