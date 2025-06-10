from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
import csv
from io import StringIO
from sqlalchemy.ext.asyncio import AsyncSession
from rpn_api_calculator.service.calculation_service import CalculationService
from rpn_api_calculator.db.database import get_db

router = APIRouter()

class CalculationCreate(BaseModel):
    expression: str
    result: float

class CalculationRead(BaseModel):
    id: UUID
    expression: str
    result: float
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

@router.post('/calculations/', response_model=CalculationRead)
async def create_calculation(calculation: CalculationCreate, session: AsyncSession = Depends(get_db)):
    return await CalculationService.create(session, calculation.expression, calculation.result)

@router.get('/calculations/export')
async def export_calculations(session: AsyncSession = Depends(get_db)):
    calculations = await CalculationService.get_all(session)

    # Create CSV in memory
    output = StringIO()
    writer = csv.writer(output)

    # Write header
    writer.writerow(['id', 'expression', 'result', 'created_at'])

    # Write data
    for calc in calculations:
        writer.writerow([
            calc.id,
            calc.expression,
            calc.result,
            calc.created_at.isoformat()
        ])

    # Prepare response
    response = Response(content=output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=calculations.csv"
    response.headers["Content-Type"] = "text/csv"

    return response

@router.get('/calculations/', response_model=list[CalculationRead])
async def list_calculations(session: AsyncSession = Depends(get_db)):
    return await CalculationService.get_all(session)

@router.get('/calculations/{calculation_id}', response_model=CalculationRead)
async def read_calculation(calculation_id: UUID, session: AsyncSession = Depends(get_db)):
    calculation = await CalculationService.get(session, calculation_id)
    if not calculation:
        raise HTTPException(status_code=404, detail='Calculation not found')
    return calculation

@router.put('/calculations/{calculation_id}', response_model=CalculationRead)
async def update_calculation(calculation_id: UUID, calculation: CalculationCreate, session: AsyncSession = Depends(get_db)):
    updated = await CalculationService.update(session, calculation_id, calculation.expression, calculation.result)
    if not updated:
        raise HTTPException(status_code=404, detail='Calculation not found')
    return updated

@router.delete('/calculations/{calculation_id}')
async def delete_calculation(calculation_id: UUID, session: AsyncSession = Depends(get_db)):
    deleted = await CalculationService.delete(session, calculation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Calculation not found')
    return {'ok': True}
