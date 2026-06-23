from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.analytics_service import analytics_service
from app.schemas.analytics import MonthlySalesRow, CategorySalesRow

router = APIRouter()


@router.get("/monthly", response_model=List[MonthlySalesRow], summary="Monthly sales trends")
def monthly_sales(
    start_date: Optional[date] = Query(None),
    end_date:   Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    return analytics_service.monthly_sales(db, start_date, end_date)


@router.get("/categories", response_model=List[CategorySalesRow], summary="Category-wise revenue & profit")
def category_sales(
    start_date: Optional[date] = Query(None),
    end_date:   Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    return analytics_service.category_sales(db, start_date, end_date)
