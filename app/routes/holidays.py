from fastapi import APIRouter
from app.schemas.filter_schema import Filter
from app.schemas.holiday_schema import Holiday
from app.services.holiday_service import HolidayService

router = APIRouter()
holiday_service = HolidayService()


@router.get("/next-holidays")
async def get_next_holidays(country: str, filter: Filter):
    holidays = await holiday_service.get_holidays(country, filter)
    if not holidays:
        return []
    return {"succes": True, "body": holidays}
