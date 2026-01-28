from fastapi import APIRouter, HTTPException, Query, Depends, Request
from datetime import date
from typing import Annotated

from fastapi.encoders import jsonable_encoder

from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from app.schemas.date_schema import WeekdayResponse, SaturdayCountResponse, DateRangeRequest
from app.services.date_service import date_service
from app.core.limiter import limiter 
from fastapi_cache.decorator import cache  

router = APIRouter()

@router.get("/weekday", response_model=WeekdayResponse)
@limiter.limit("60/minute") # 1 request per second per user is plenty
@cache(expire=3600)  # <--- Cache this result for 1 hour
async def get_weekday(
    request: Request, # <--- Required for limiter
    year: int = Query(..., ge=1, le=9999, description="Year (1-9999)"),
    month: int = Query(..., ge=1, le=12, description="Month (1-12)"),
    day: int = Query(15, ge=1, le=31, description="Day of month")
):
    """
    Get the weekday number and name for a specific date.
    """
    try:
        # We delegate the logic to the service
        result = date_service.get_weekday_info(year, month, day)
        
        return WeekdayResponse(
            year=year,
            month=month,
            day=day,
            weekday_number=result["weekday_number"],
            weekday_name=result["weekday_name"]
        )
    except ValueError as e:
        # Handle invalid dates (e.g., February 30th)
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/matching-dates", response_model=SaturdayCountResponse) # You might rename the Response Model later, but this works
@limiter.limit("60/minute") # 1 request per second per user is plenty
@cache(expire=3600)  # <--- Cache this result for 1 hour
async def find_matching_dates(
    request: Request,
    start_date: date,
    end_date: date,
    weekday: int = Query(5, ge=0, le=6, description="0=Mon, 6=Sun"),
    day_of_month: int = Query(15, ge=1, le=31)
):
    # Call service with new params
    result = date_service.count_matching_dates(
        start_date, 
        end_date, 
        weekday, 
        day_of_month
    )

    return SaturdayCountResponse(
        start_date=start_date,
        end_date=end_date,
        saturday_count=result["count"],
        matching_dates=result["dates"]
    )