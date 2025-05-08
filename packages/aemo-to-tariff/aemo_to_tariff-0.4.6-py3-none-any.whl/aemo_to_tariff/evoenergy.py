# aemo_to_tariff/evoenergy.py
from datetime import datetime
from zoneinfo import ZoneInfo
from datetime import time

def time_zone():
    return 'Australia/ACT'

def battery_tariff(customer_type: str):
    """
    Get the battery tariff for a given customer type.

    Parameters:
    - customer_type (str): The customer type ('Residential' or 'Business').

    Returns:
    - str: The battery tariff code.
    """
    if customer_type == 'Residential':
        return '017'
    elif customer_type == 'Business':
        return '090'
    else:
        raise ValueError("Invalid customer type. Must be 'Residential' or 'Business'.")

tariffs = {
    '015': {
        'name': 'Residential TOU Network (closed)',
        'periods': [
            ('Peak', time(7, 0), time(9, 0), 14.063),
            ('Peak', time(17, 0), time(20, 0), 14.063),
            ('Shoulder', time(9, 0), time(17, 0), 6.285),
            ('Shoulder', time(20, 0), time(22, 0), 6.285),
            ('Off-peak', time(22, 0), time(7, 0), 3.210)
        ],
        'peak_months': [11, 12, 1, 2, 3, 6, 7, 8]  # November–March and June–August
    },
    '016': {
        'name': 'Residential TOU Network (closed) XMC',
        'periods': [
            ('Peak', time(7, 0), time(9, 0), 14.063),
            ('Peak', time(17, 0), time(20, 0), 14.063),
            ('Shoulder', time(9, 0), time(17, 0), 6.285),
            ('Shoulder', time(20, 0), time(22, 0), 6.285),
            ('Off-peak', time(22, 0), time(7, 0), 3.210)
        ],
        'peak_months': [11, 12, 1, 2, 3, 6, 7, 8]  # November–March and June–August
    },
    '017': {
        'name': 'New Residential TOU Network',
        'periods': [
            ('Peak', time(7, 0), time(9, 0), 14.109),
            ('Peak', time(17, 0), time(21, 0), 14.109),
            ('Solar Soak', time(11, 0), time(15, 0), 1.757),
            ('Off-peak', time(21, 0), time(7, 0), 3.918),
            ('Off-peak', time(9, 0), time(11, 0), 3.918),
            ('Off-peak', time(15, 0), time(17, 0), 3.918)
        ],
        'fixed_daily_charge': 32.757,  # Fixed daily charge in c/day
        'peak_months': [11, 12, 1, 2, 3, 6, 7, 8]  # November–March and June–August
    },
    '018': {
        'name': 'New Residential TOU Network XMC',
        'periods': [
            ('Peak', time(7, 0), time(9, 0), 14.109),
            ('Peak', time(17, 0), time(21, 0), 14.109),
            ('Solar Soak', time(11, 0), time(15, 0), 1.757),
            ('Off-peak', time(21, 0), time(7, 0), 3.918),
            ('Off-peak', time(9, 0), time(11, 0), 3.918),
            ('Off-peak', time(15, 0), time(17, 0), 3.918)
        ],
        'fixed_daily_charge': 48.257,  # Fixed daily charge in c/day
        'peak_months': [11, 12, 1, 2, 3, 6, 7, 8]  # November–March and June–August
    },
    '090': {
        'name': 'Component Charge Applicability',
        'periods': [
            ('Peak', time(7, 0), time(17, 0), 17.518),  # 7am-5pm weekdays
            ('Shoulder', time(17, 0), time(22, 0), 10.990),  # 5pm-10pm weekdays
            ('Off-peak', time(22, 0), time(7, 0), 5.110),  # All other times
        ],
        'fixed_daily_charge': 76.676  # Fixed daily charge in c/day
    }
}


def get_periods(tariff_code: str):
    tariff = tariffs.get(tariff_code)
    if not tariff:
        raise ValueError(f"Unknown tariff code: {tariff_code}")

    return tariff['periods']

def convert_feed_in_tariff(interval_datetime: datetime, tariff_code: str, rrp: float):
    """
    Convert RRP from $/MWh to c/kWh for SA Power Networks.

    Parameters:
    - interval_datetime (datetime): The interval datetime.
    - tariff_code (str): The tariff code.
    - rrp (float): The Regional Reference Price in $/MWh.

    Returns:
    - float: The price in c/kWh.
    """
    rrp_c_kwh = rrp / 10
    
    return rrp_c_kwh

def convert(interval_datetime: datetime, tariff_code: str, rrp: float):
    """
    Convert RRP from $/MWh to c/kWh for Evoenergy.

    Parameters:
    - interval_time (str): The interval time.
    - tariff (str): The tariff code.
    - rrp (float): The Regional Reference Price in $/MWh.

    Returns:
    - float: The price in c/kWh.
    """
    interval_time = interval_datetime.astimezone(ZoneInfo(time_zone())).time()
    current_month = interval_datetime.month

    rrp_c_kwh = rrp / 10
    tariff = tariffs[tariff_code]
    gst = 1.1
    is_peak_month = current_month in tariff.get('peak_months', [])

    # Find the applicable period and rate
    for period_name, start, end, rate in tariff['periods']:
        if period_name == 'Peak' and not is_peak_month:
            continue  # Skip peak period if not in peak months

        if start <= interval_time < end:
            total_price = rrp_c_kwh + (rate * gst)
            return total_price

        # Handle overnight periods (e.g., 22:00 to 07:00)
        if start > end and (interval_time >= start or interval_time < end):
            total_price = rrp_c_kwh + (rate * gst)
            return total_price

    # Otherwise, this terrible approximation
    slope = 1.037869032618134
    intercept = 5.586606750833143
    return rrp_c_kwh * slope + intercept
