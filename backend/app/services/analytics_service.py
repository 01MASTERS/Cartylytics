"""
Cartlytics – Analytics Service
Business logic layer between routers and repositories.
"""

from typing import Optional
from datetime import date
from sqlalchemy.orm import Session

from app.repositories import analytics_repo as repo


class AnalyticsService:

    # KPIs
    def kpis(self, db: Session, start: Optional[date], end: Optional[date]):
        return repo.get_kpis(db, start, end)

    # Sales
    def monthly_sales(self, db: Session, start: Optional[date], end: Optional[date]):
        return repo.get_monthly_sales(db, start, end)

    def category_sales(self, db: Session, start: Optional[date], end: Optional[date]):
        return repo.get_category_sales(db, start, end)

    # Products
    def top_products_revenue(
        self, db: Session, start: Optional[date], end: Optional[date],
        category_id: Optional[int], limit: int
    ):
        return repo.get_top_products_by_revenue(db, start, end, category_id, limit)

    def top_products_profit(
        self, db: Session, start: Optional[date], end: Optional[date],
        category_id: Optional[int], limit: int
    ):
        return repo.get_top_products_by_profit(db, start, end, category_id, limit)

    # Customers
    def top_customers(self, db: Session, start: Optional[date], end: Optional[date], limit: int):
        return repo.get_top_customers(db, start, end, limit)

    def new_vs_returning(self, db: Session, start: Optional[date], end: Optional[date]):
        return repo.get_new_vs_returning(db, start, end)

    def purchase_frequency(self, db: Session, start: Optional[date], end: Optional[date]):
        return repo.get_purchase_frequency(db, start, end)

    # Geography
    def regional_sales(self, db: Session, start: Optional[date], end: Optional[date]):
        return repo.get_regional_sales(db, start, end)


analytics_service = AnalyticsService()
