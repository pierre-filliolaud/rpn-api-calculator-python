from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from rpn_api_calculator.db.database import Base

class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    expression = Column(String, nullable=False)
    result = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Calculation(id={self.id}, expression='{self.expression}', result={self.result})>"
