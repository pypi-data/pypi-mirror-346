"""
smart_time_py - Uma biblioteca avançada para manipulação de datas e tempos em Python.
"""

from .analysis import (TimeGroup, analyze_seasonality,
                       calculate_temporal_stats, detect_temporal_patterns,
                       group_dates)
from .converter import (add_time, auto_validate_date, calculate_difference,
                        convert_to_format, convert_with_timezone,
                        datetime_to_string, is_valid_date, string_to_datetime,
                        subtract_time, validate_date_string)
from .formatters import format_iso, format_natural, format_relative
from .holidays import (add_holiday, get_holidays, get_working_days, is_holiday,
                       remove_holiday)
from .periods import DateRange, PeriodType, TimePeriod
from .timezone import (convert_timezone, get_available_timezones,
                       get_timezone_info, is_dst_active)

__version__ = "1.2.0"
__author__ = "Roberto Lima"
__email__ = "robertolima.izphera@gmail.com"
