from datetime import datetime, timedelta

def to_airbnb_date_label(date_str: str) -> str:
    """
    Converts a date string like '2025-04-17' to Airbnb's aria-label format.
    :param date_str: Date string in format YYYY-MM-DD
    :return: Formatted string like 'Thursday, April 17, 2025'
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%d, %A, %B %Y")  # Airbnb format

def get_date_from_today(days_from_today: int) -> str:
    """
    Returns a date string in format 'YYYY-MM-DD' that is X days from today.
    :param days_from_today: how many days ahead (or negative for past)
    :return: date string like '2025-04-22'
    """
    target_date = datetime.today() + timedelta(days=days_from_today)
    return target_date.strftime("%Y-%m-%d")