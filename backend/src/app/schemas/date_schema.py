from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import List # <--- Add this

#1. Output schema for Weekday Request
class WeekdayResponse(BaseModel):
    year: int
    month: int
    day: int
    weekday_number: int
    weekday_name: str

class DateRangeRequest(BaseModel):
    start_date: date 
    end_date: date 

    @field_validator('end_date')
    @classmethod
    def check_date_order(cls, v, info):
        if 'start_date' in info.data and v < info.data['start_date']:
            raise ValueError('end_date must be after start_date')
        return v
    
class SaturdayCountResponse(BaseModel):
    start_date: date 
    end_date: date 
    saturday_count: int
    matching_dates: List[date] 