import pandas as pd
from datetime import datetime, timedelta
from . import config


def part_is_missing_or_unknown(value):
    if value.strip().upper() in ["UNK", "UN", "UK", "UNKNOWN"]:
        return True
    return False

def value_is_missing_or_unknown(value):
    # print(f"value: {value}")
    if not value or pd.isna(value) or value.strip() == "":
        return True
    value = value.strip().upper()
    for missing_value in ["NONE", "NULL", "UNK", "UK", "UNKNOWN"]:
        if missing_value in value:
            return True
    return False

def get_min_day_max_day_based_on_month(month,year):
    if part_is_missing_or_unknown(month):
        return 1, 31
    month=int(month)

    


    """
    Get minimum and maximum days for a given month, handling February specially.
    
    Args:
        month (int): Month number (1-12)
        year (int): Year number
        
    Returns:
        tuple: (min_day, max_day) for the given month
    """
    if month == 2:  # February
        # Check for leap year
        if not part_is_missing_or_unknown(year) and int(year) % 4 == 0 and (int(year) % 100 != 0 or int(year) % 400 == 0):
            return 1, 29
        return 1, 28
    elif month in [4, 6, 9, 11]:  # 30 day months
        return 1, 30
    else:  # 31 day months
        return 1, 31

# Helper function to get date range
def get_date_range(date_str):
    if value_is_missing_or_unknown(date_str):
        # If date value is missing, use 01-01-1970 to today
        today = datetime.now()
        return (
            datetime(1970, 1, 1),
            today
        )
    
    parts = date_str.split(config.date_spliter)
    today = datetime.now()
    
    # Handle partial missing cases
    # try:
    year, month, day = parts
    min_year_part,max_year_part=year,year
    min_month_part,max_month_part=month,month
    min_day_part,max_day_part=day,day
    
    # Handle missing year
    if part_is_missing_or_unknown(year):
        min_year_part=1970
        max_year_part=today.year
    # Handle missing month
    if part_is_missing_or_unknown(month):
        min_month_part=1
        max_month_part=12
    # Handle missing day
    if part_is_missing_or_unknown(day):
        min_day_part,max_day_part=get_min_day_max_day_based_on_month(month,year)
    # Create min and max timestamps from the ranges
    min_date = datetime(int(min_year_part), int(min_month_part), int(min_day_part))
    max_date = datetime(int(max_year_part), int(max_month_part), int(max_day_part))
    # print(f"min_date: {min_date}, max_date: {max_date}")
    return min_date, max_date
    # except ValueError as e:
    #     print(f"Error: {e}")
        # raise ValueError(f"Invalid date format: {date_str}")
            
    

# Helper function to get time range
def get_time_range(time_str):
    if value_is_missing_or_unknown(time_str):
        # If time is missing, use full day
        return (
            datetime(2000, 1, 1, 0, 0, 0),
            datetime(2000, 1, 1, 23, 59, 59, 999999)
        )
    
    parts = time_str.split(':')
    
    # Handle partial missing cases
    try:
        hour, minute, second = parts

        min_hour_part,max_hour_part=hour,hour
        min_minute_part,max_minute_part=minute,minute
        min_second_part,max_second_part=second,second
        
        # Handle missing hour
        if part_is_missing_or_unknown(hour):
            min_hour_part=0
            max_hour_part=23
        # Handle missing minute
        if part_is_missing_or_unknown(minute):
            min_minute_part=0
            max_minute_part=59
        # Handle missing second
        if part_is_missing_or_unknown(second):
            min_second_part=0
            max_second_part=59
        # Create min and max timestamps from the ranges
        min_time = datetime(2000, 1, 1, 
                            int(min_hour_part), 
                            int(min_minute_part),
                            int(min_second_part))
        max_time = datetime(2000, 1, 1,
                            int(max_hour_part),
                            int(max_minute_part), 
                            int(max_second_part),
                            999999)
        return min_time, max_time
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}")

def align_time(date_str, time_str,alignmentOpID=None):
    """
    Align time based on date and time strings, handling various missing/unknown cases.
    Handles partial missing information in dates and times.
    
    Args:
        date_str (str): Date string (format: YYYY-MM-DD or partial)
        time_str (str): Time string (format: HH:MM:SS or partial)
        
    Returns:
        tuple: (min_time, max_time) as datetime objects
    """
   

     
    
    # Get date and time ranges
    date_min, date_max = get_date_range(date_str)
    time_min, time_max = get_time_range(time_str)
    
    if date_min is None or time_min is None:
        raise ValueError("Invalid date or time format")
    
    # Combine the ranges
    min_time = datetime.combine(date_min.date(), time_min.time())
    max_time = datetime.combine(date_max.date(), time_max.time())
    
    if min_time.replace(microsecond=0) != max_time.replace(microsecond=0):
        print("\033[92mTime range detected:\033[0m")
        if alignmentOpID:
            print(f"\033[94mAlignment Operation ID: {alignmentOpID}\033[0m")
        print(f"\033[94mMin time: {min_time}\033[0m")
        print(f"\033[94mMax time: {max_time}\033[0m")
    return min_time, max_time
