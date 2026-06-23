from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.analytics_service import analytics_service
from app.schemas.analytics import CustomerStatsRow, NewVsReturningRow, PurchaseFrequencyRow

router = APIRouter()


@router.get("/top-spenders", response_model=List[CustomerStatsRow])
def top_customers(
    start_date: Optional[date] = Query(None),
    end_date:   Optional[date] = Query(None),
    limit:      int             = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return analytics_service.top_customers(db, start_date, end_date, limit)


@router.get("/new-vs-returning", response_model=List[NewVsReturningRow])
def new_vs_returning(
    start_date: Optional[date] = Query(None),
    end_date:   Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    return analytics_service.new_vs_returning(db, start_date, end_date)


@router.get("/purchase-frequency", response_model=List[PurchaseFrequencyRow])
def purchase_frequency(
    start_date: Optional[date] = Query(None),
    end_date:   Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    return analytics_service.purchase_frequency(db, start_date, end_date)
