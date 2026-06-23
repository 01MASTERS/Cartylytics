from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.analytics_service import analytics_service
from app.schemas.analytics import ProductPerformanceRow

router = APIRouter()


@router.get("/top-revenue", response_model=List[ProductPerformanceRow])
def top_by_revenue(
    start_date:  Optional[date] = Query(None),
    end_date:    Optional[date] = Query(None),
    category_id: Optional[int]  = Query(None),
    limit:       int             = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    return analytics_service.top_products_revenue(db, start_date, end_date, category_id, limit)


@router.get("/top-profit", response_model=List[ProductPerformanceRow])
def top_by_profit(
    start_date:  Optional[date] = Query(None),
    end_date:    Optional[date] = Query(None),
    category_id: Optional[int]  = Query(None),
    limit:       int             = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    return analytics_service.top_products_profit(db, start_date, end_date, category_id, limit)
