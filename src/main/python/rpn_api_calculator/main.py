from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from rpn_api_calculator.api.calculation_resource import router as calculation_router
from rpn_api_calculator.api.health import router as health_router
from rpn_api_calculator.db.database import get_db, engine
from rpn_api_calculator.db.database import Base

app = FastAPI(title="RPN API Calculator")

app.include_router(calculation_router, prefix="/api")
app.include_router(health_router, prefix="/api")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
