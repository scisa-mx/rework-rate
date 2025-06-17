from datetime import datetime
from typing import Optional, Tuple

def remove_timezone_from_dates(
    start_date: Optional[datetime], 
    end_date: Optional[datetime]
) -> Tuple[Optional[datetime], Optional[datetime]]:
    
    """
    Remove timezone information from datetime objects.
    If the datetime is naive (no timezone), it remains unchanged.
    If the datetime is timezone-aware, it will be converted to naive.
    :params start_date: Optional[datetime] - The start date to process.
    :params end_date: Optional[datetime] - The end date to process.
    """

    if start_date:
        start_date = start_date.replace(tzinfo=None)
    if end_date:
        end_date = end_date.replace(tzinfo=None)
    return start_date, end_date