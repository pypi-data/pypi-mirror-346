"""
Exemplos de uso avançado da biblioteca smart_time_py
"""
from datetime import datetime, timedelta
from smart_time_py import (
    # Conversão e validação
    string_to_datetime,
    datetime_to_string,
    is_valid_date,
    
    # Operações temporais
    add_time,
    subtract_time,
    calculate_difference,
    
    # Feriados
    is_holiday,
    add_holiday,
    get_holidays,
    get_working_days,
    
    # Períodos
    TimePeriod,
    DateRange,
    get_overlapping_periods,
    
    # Formatação
    format_relative,
    format_natural,
    format_iso,
    
    # Fusos horários
    get_timezone_info,
    convert_timezone,
    get_timezone_abbreviation
)


def main():
    """Função principal com exemplos de uso"""
    print("=== Exemplos de Uso Avançado do Smart Time Py ===\n")
    
    # 1. Conversão e Validação
    print("1. Conversão e Validação:")
    date_str = "2024-02-25 14:30:00"
    date_obj = string_to_datetime(date_str, "%Y-%m-%d %H:%M:%S")
    print(f"String para datetime: {date_obj}")
    print(f"Datetime para string: {datetime_to_string(date_obj, '%d/%m/%Y %H:%M')}")
    print(f"Data válida? {is_valid_date('2024-02-25', '%Y-%m-%d')}\n")
    
    # 2. Operações Temporais
    print("2. Operações Temporais:")
    future_date = add_time(date_obj, days=5, months=1)
    print(f"Data futura: {future_date}")
    past_date = subtract_time(date_obj, years=1)
    print(f"Data passada: {past_date}")
    diff_days = calculate_difference(date_obj, future_date, "days")
    print(f"Diferença em dias: {diff_days}\n")
    
    # 3. Feriados
    print("3. Feriados:")
    print(f"É feriado hoje? {is_holiday(datetime.now())}")
    print("Feriados de 2024:")
    for holiday in get_holidays(year=2024):
        print(f"- {holiday['date']}: {holiday['name']}")
    print(f"Dias úteis em fevereiro: {get_working_days(datetime(2024, 2, 1), datetime(2024, 2, 29))}\n")
    
    # 4. Períodos
    print("4. Períodos:")
    period = TimePeriod(
        start=datetime(2024, 2, 1),
        end=datetime(2024, 2, 29),
        name="Fevereiro 2024"
    )
    print(f"Período: {period.name} ({period.days} dias)")
    
    date_range = DateRange(
        start=datetime(2024, 2, 1),
        end=datetime(2024, 2, 29),
        include_weekends=False
    )
    print(f"Dias úteis no período: {len(date_range)}\n")
    
    # 5. Formatação
    print("5. Formatação:")
    print(f"Formato relativo: {format_relative(datetime.now() - timedelta(days=2))}")
    print(f"Formato natural: {format_natural(datetime.now())}")
    print(f"Formato ISO: {format_iso(datetime.now())}\n")
    
    # 6. Fusos Horários
    print("6. Fusos Horários:")
    tz_info = get_timezone_info("America/Sao_Paulo")
    print(f"Informações do fuso horário: {tz_info}")
    
    converted_date = convert_timezone(
        datetime.now(),
        "America/Sao_Paulo",
        "Europe/London"
    )
    print(f"Data convertida: {converted_date}")
    print(f"Abreviação do fuso horário: {get_timezone_abbreviation('America/Sao_Paulo')}")


if __name__ == "__main__":
    main() 