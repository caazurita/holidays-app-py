from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import time
from app.routes.holidays import router as holidays_router

app = FastAPI(
    title="Holiday API",
    description="API to fetch upcoming holidays based on country and filter criteria",
    version="1.0.0",
)
app.get("/")(
    lambda: {
        "message": "Welcome to the Holiday API. Use /holidays/next-holidays to fetch upcoming holidays. Or visit https://github.com/caazurita/holidays-app-py for more details.",
        "body": {
            "country": "Country code (e.g., US, GB, IN)",
            "filter": "Filter criteria (e.g., current-month, next-month, next-year)",
            "exampleUrl": "http://localhost:8000/holidays/next-holidays?country=MX&filter=current-month",
        },
    }
)
app.include_router(holidays_router, prefix="/holidays", tags=["Holidays"])
items = []

# class Item(BaseModel):
#     name: str
#     is_done: bool = False

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.perf_counter() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response

# @app.get("/item/")
# async def root():
#     return {"message": "Hello World"}

# @app.post("/items/")
# async def create_item(item: Item):
#     items.append(item)
#     return items

# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: int):
#     if item_id < len(items):
#         return items[item_id]
#     else :
#         raise HTTPException(status_code=404, detail="Item not found")

# @app.get("/items/")
# async def read_items(limit: int = 10):
#     return {"items": items[0:limit]}
