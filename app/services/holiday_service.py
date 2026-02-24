import httpx
from datetime import datetime, timedelta
from typing import List

from app.schemas.holiday_schema import Holiday
from app.services.agent_service import AgentService
from app.schemas.summary_schema import Summary
from app.services.holiday_cache_service import HolidayCacheService


class HolidayService:
    BASE_URL = "https://date.nager.at/api/v3/PublicHolidays"
    cache_service = HolidayCacheService()

    async def get_holidays(self, country: str, filter: str = str) -> List[Holiday]:
        year = datetime.now().year
        url = f"{HolidayService.BASE_URL}/{year}/{country}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response.raise_for_status()

            data = response.json()
            if filter:
                today = datetime.now().date()
                filterData = datetime
                match filter:
                    case "next-month":
                        filterData = today.replace(month=today.month + 1, day=1)
                        data = [
                            holiday
                            for holiday in data
                            if datetime.strptime(holiday["date"], "%Y-%m-%d").date()
                            >= filterData
                            and datetime.strptime(holiday["date"], "%Y-%m-%d").date()
                            <= filterData.replace(month=filterData.month + 1)
                        ]
                    case "current-month":
                        filterData = today.replace(day=1)
                        data = [
                            holiday
                            for holiday in data
                            if datetime.strptime(holiday["date"], "%Y-%m-%d").date()
                            >= filterData
                            and datetime.strptime(holiday["date"], "%Y-%m-%d").date()
                            <= filterData.replace(month=filterData.month + 1)
                        ]
                    case "next-week":
                        filterData = today + timedelta(days=7)
                        print(filterData)
                        data = [
                            holiday
                            for holiday in data
                            if datetime.strptime(holiday["date"], "%Y-%m-%d").date()
                            >= today
                            and datetime.strptime(holiday["date"], "%Y-%m-%d").date()
                            <= filterData
                        ]
                    case "current-week":
                        filterData = today - timedelta(days=today.weekday())
                        data = [
                            holiday
                            for holiday in data
                            if datetime.strptime(holiday["date"], "%Y-%m-%d").date()
                            >= filterData
                            and datetime.strptime(holiday["date"], "%Y-%m-%d").date()
                            <= filterData + timedelta(days=7)
                        ]

            agent = AgentService()
            # summaries: List[Summary] = await agent.run(
            #     names=[holiday["localName"] for holiday in data]
            # )
            # summary_map = {summary.name: summary for summary in summaries}

            summary_map = {}
            missing_names = []
            for holiday in data:
                name = holiday["localName"]
                cached = self.cache_service.get(name, country)

                if cached:
                    summary_map[name] = cached
                else:
                    missing_names.append(name)

            if missing_names:
                summaries: List[Summary] = await agent.run(names=missing_names)
                for summary in summaries:
                    summary_map[summary.name] = summary
                    self.cache_service.set(
                        holiday_summary=summary, holiday_country=country
                    )

            data = [
                Holiday(
                    localName=holiday["localName"],
                    date=holiday["date"],
                    countryCode=holiday["countryCode"],
                    type=holiday["types"][0] if holiday.get("types") else "Uknown",
                    summary=(
                        summary_map.get(holiday["localName"]).summary
                        if summary_map.get(holiday["localName"])
                        else "Uknown"
                    ),
                    category=(
                        summary_map.get(holiday["localName"]).category
                        if summary_map.get(holiday["localName"])
                        else "Uknown"
                    ),
                )
                for holiday in data
            ]
            return data
        except Exception as e:
            print(e)
            return [{"error": str(e)}]
