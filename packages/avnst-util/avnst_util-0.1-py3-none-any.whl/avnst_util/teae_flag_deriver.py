from .time_alignment import align_time
def derive_teae_flag(first_dose_date,first_dose_time,ae_start_date,ae_start_time,opID=None):
    """
    Derive TEAE flag by comparing AE start date/time with first dose date/time
    
    Returns:
    1 = AE definitely occurred after first dose
    0 = AE definitely occurred before first dose  
    2 = AE timing overlaps with first dose timing or timing uncertain
    None = Unable to determine timing
    """
    try:
        # Get first dose date/time range
        first_dose_min, first_dose_max  = align_time(
            first_dose_date,
            first_dose_time,
            f"{opID} First Dose"
        )
        ae_start_min, ae_start_max = align_time(
            ae_start_date,
            ae_start_time,
            f"{opID} AE Start "
        )
        
        # if x["SUBJID"]=="165-028":
        #     print(f"First dose date/time: {x['d_firstdosedate']} {x['d_firstdosetime']}")
        #     print(f"First dose date/time: {first_dose_min} {first_dose_max}")
        # if first_dose_min is None or first_dose_max is None:
        #     # print(f"First dose date/time is None: {x['d_firstdosedate']} {x['d_firstdosetime']}")
        #     return None
            
        # # Get AE start date/time range
        # # ae_start_min, ae_start_max = format_date_time(
        # #     x['AESTDAT'],
        # #     x['AESTTIM']
        # # )
       
        
       
        # if ae_start_min is None or ae_start_max is None:
        #     # print(f"AE start date/time is None: {x['d_AESTDTC']}")
        #     return None
        
     
        # Compare ranges:
        # If AE min is after first dose max -> definitely after
        if ae_start_min > first_dose_max:
            return 1
        # If AE max is before first dose min -> definitely before  
        elif ae_start_max < first_dose_min:
            return 0
        # If ranges overlap -> timing uncertain
        else:
            return 2
            
    except Exception as e:
        raise e
