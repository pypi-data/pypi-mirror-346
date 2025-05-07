from .time_alignment import align_time
from .teae_flag_deriver import derive_teae_flag
from . import config



def set_date_spliter(spliter):
    """
    Set the date spliter character used for parsing dates.
    
    Args:
        spliter (str): The character to use as the date spliter (e.g. '-', '/', etc.)
        
    Example:
        set_date_spliter('-')  # Sets date format to use hyphens like '2023-12-31'
        set_date_spliter('/')  # Sets date format to use slashes like '2023/12/31'
    """
    config.date_spliter = spliter




