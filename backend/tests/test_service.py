from datetime import date
from app.services.date_service import date_service

def test_get_weekday_info():
    # Test a known date: Jan 15, 2025 is a Wednesday (2)
    result = date_service.get_weekday_info(2025, 1, 15)
    assert result["weekday_number"] == 2
    assert result["weekday_name"] == "Wednesday"

def test_get_weekday_leap_year():
    # Test leap year behavior: Feb 29, 2024 is a Thursday (3)
    result = date_service.get_weekday_info(2024, 2, 29)
    assert result["weekday_number"] == 3
    assert result["weekday_name"] == "Thursday"

def test_count_mid_saturdays_2026():
    # Test the specific case we discussed (2026 has 1 Saturday on the 15th: Aug 15)
    start = date(2026, 1, 1)
    end = date(2026, 12, 31)
    count = date_service.count_mid_saturdays(start, end)
    assert count == 1

def test_count_mid_saturdays_multi_year():
    # Test a longer range
    # 2025 has: Feb 15 (Sat), Mar 15 (Sat), Nov 15 (Sat) -> Total 3
    start = date(2025, 1, 1)
    end = date(2025, 12, 31)
    count = date_service.count_mid_saturdays(start, end)
    assert count == 3

def test_count_mid_saturdays_empty():
    # Test a range with no Saturdays
    # Jan 2024: 15th is Mon. Feb 2024: 15th is Thu.
    start = date(2024, 1, 1)
    end = date(2024, 2, 28)
    count = date_service.count_mid_saturdays(start, end)
    assert count == 0