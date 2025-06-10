from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from rpn_api_calculator.domain.calculation import Calculation

class CalculationService:
    @staticmethod
    async def create(session: AsyncSession, expression: str, result: float) -> Calculation:
        calculation = Calculation(expression=expression, result=result)
        session.add(calculation)
        await session.commit()
        await session.refresh(calculation)
        return calculation

    @staticmethod
    async def get(session: AsyncSession, calculation_id: UUID) -> Calculation | None:
        result = await session.execute(select(Calculation).where(Calculation.id == calculation_id))
        return result.scalars().first()

    @staticmethod
    async def update(session: AsyncSession, calculation_id: UUID, expression: str, result: float) -> Calculation | None:
        calculation = await CalculationService.get(session, calculation_id)
        if calculation:
            calculation.expression = expression
            calculation.result = result
            await session.commit()
            await session.refresh(calculation)
        return calculation

    @staticmethod
    async def delete(session: AsyncSession, calculation_id: UUID) -> bool:
        calculation = await CalculationService.get(session, calculation_id)
        if calculation:
            await session.delete(calculation)
            await session.commit()
            return True
        return False

    @staticmethod
    async def get_all(session: AsyncSession) -> list[Calculation]:
        result = await session.execute(select(Calculation).order_by(Calculation.created_at.desc()))
        return result.scalars().all()
