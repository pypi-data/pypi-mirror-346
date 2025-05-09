"""
Módulo de conversão de datas e tempos
"""
from datetime import datetime
import pytz
from dateutil import parser
from dateutil.relativedelta import relativedelta


def string_to_datetime(date_str: str, date_format: str) -> datetime:
    """
    🕒 Converte uma string para um objeto datetime com o formato especificado.
    
    Args:
        date_str (str): String contendo a data
        date_format (str): Formato da data (ex: "%Y-%m-%d %H:%M:%S")
        
    Returns:
        datetime: Objeto datetime convertido
        
    Raises:
        ValueError: Se a string não puder ser convertida para o formato especificado
    """
    try:
        return datetime.strptime(date_str, date_format)
    except ValueError as e:
        raise ValueError(f"❌ Erro na conversão: {str(e)}")


def datetime_to_string(date_obj: datetime, date_format: str) -> str:
    """
    📝 Converte um objeto datetime para uma string com o formato especificado.
    
    Args:
        date_obj (datetime): Objeto datetime a ser convertido
        date_format (str): Formato desejado para a string
        
    Returns:
        str: String formatada
        
    Raises:
        TypeError: Se date_obj não for um objeto datetime
    """
    if not isinstance(date_obj, datetime):
        raise TypeError("❌ O parâmetro 'date_obj' deve ser um objeto datetime.")
    return date_obj.strftime(date_format)


def validate_date_string(date_str: str, date_format: str) -> bool:
    """
    ✅ Valida se uma string de data/hora corresponde ao formato especificado.
    
    Args:
        date_str (str): String a ser validada
        date_format (str): Formato esperado
        
    Returns:
        bool: True se a string for válida, False caso contrário
    """
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def convert_to_format(date_str: str, from_format: str, to_format: str) -> str:
    """
    🔄 Converte uma string de data de um formato para outro.
    
    Args:
        date_str (str): String de data original
        from_format (str): Formato original
        to_format (str): Formato desejado
        
    Returns:
        str: String convertida ou None se a conversão falhar
    """
    try:
        date_obj = datetime.strptime(date_str, from_format)
        return date_obj.strftime(to_format)
    except ValueError:
        return None


def convert_with_timezone(date_str: str, timezone: str) -> datetime:
    """
    🌐 Converte uma data para o fuso horário especificado.
    
    Args:
        date_str (str): String de data/hora
        timezone (str): Nome do fuso horário (ex: "America/Sao_Paulo")
        
    Returns:
        datetime: Objeto datetime convertido ou None se a conversão falhar
    """
    try:
        date_obj = parser.parse(date_str)
        target_timezone = pytz.timezone(timezone)
        return date_obj.astimezone(target_timezone)
    except Exception:
        return None 