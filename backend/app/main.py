"""
Cartlytics – FastAPI Backend
Entry point: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.routers import kpis, sales, products, customers, geography


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    engine.dispose()


app = FastAPI(
    title="Cartlytics API",
    description="Customer, Sales & Revenue Analytics Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── routers ────────────────────────────────────────────────────────────────────
app.include_router(kpis.router,      prefix="/api/v1/kpis",      tags=["KPIs"])
app.include_router(sales.router,     prefix="/api/v1/sales",     tags=["Sales"])
app.include_router(products.router,  prefix="/api/v1/products",  tags=["Products"])
app.include_router(customers.router, prefix="/api/v1/customers", tags=["Customers"])
app.include_router(geography.router, prefix="/api/v1/geography", tags=["Geography"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "app": "Cartlytics API", "version": "1.0.0"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
