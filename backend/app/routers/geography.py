from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.analytics_service import analytics_service
from app.schemas.analytics import RegionalSalesRow

router = APIRouter()


@router.get("/regions", response_model=List[RegionalSalesRow])
def regional_sales(
    start_date: Optional[date] = Query(None),
    end_date:   Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    return analytics_service.regional_sales(db, start_date, end_date)
