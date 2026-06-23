from fastapi import APIRouter, Depends, Query
from typing import Optional
from datetime import date
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.analytics_service import analytics_service
from app.schemas.analytics import KPIResponse

router = APIRouter()


@router.get("", response_model=KPIResponse, summary="Core business KPIs")
def get_kpis(
    start_date:  Optional[date] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    end_date:    Optional[date] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """
    Returns all core KPIs:
    - Total Revenue, Profit, Orders, AOV, Customers
    - Revenue & Profit Growth % vs prior period
    - Repeat Customer Rate
    """
    return analytics_service.kpis(db, start_date, end_date)
