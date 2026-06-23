"""
Cartlytics – SQLAlchemy ORM Models
Mirrors the MySQL schema for type-safe queries and migrations.
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Date,
    DECIMAL, SmallInteger, ForeignKey, Enum as SAEnum,
    func,
)
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


# ── Enums ──────────────────────────────────────────────────────────────────────

class GenderEnum(str, enum.Enum):
    Male    = "Male"
    Female  = "Female"
    Other   = "Other"
    Unknown = "Unknown"

class RegionEnum(str, enum.Enum):
    North     = "North"
    South     = "South"
    East      = "East"
    West      = "West"
    Northeast = "Northeast"
    Northwest = "Northwest"
    Southeast = "Southeast"
    Southwest = "Southwest"
    Central   = "Central"

class SegmentEnum(str, enum.Enum):
    Consumer      = "Consumer"
    Corporate     = "Corporate"
    HomeOffice    = "Home Office"
    SmallBusiness = "Small Business"

class OrderStatusEnum(str, enum.Enum):
    pending   = "pending"
    confirmed = "confirmed"
    shipped   = "shipped"
    delivered = "delivered"
    returned  = "returned"
    cancelled = "cancelled"

class PaymentMethodEnum(str, enum.Enum):
    CreditCard    = "Credit Card"
    DebitCard     = "Debit Card"
    PayPal        = "PayPal"
    BankTransfer  = "Bank Transfer"
    CashOnDelivery= "Cash on Delivery"


# ── Category ───────────────────────────────────────────────────────────────────

class Category(Base):
    __tablename__ = "categories"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    name        = Column(String(100), nullable=False)
    slug        = Column(String(110), nullable=False, unique=True)
    description = Column(Text)
    parent_id   = Column(Integer, ForeignKey("categories.id"), nullable=True)
    is_active   = Column(SmallInteger, nullable=False, default=1)
    created_at  = Column(DateTime, server_default=func.now())
    updated_at  = Column(DateTime, server_default=func.now(), onupdate=func.now())

    parent      = relationship("Category", remote_side=[id], backref="children")
    products    = relationship("Product", back_populates="category")


# ── Product ────────────────────────────────────────────────────────────────────

class Product(Base):
    __tablename__ = "products"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    sku           = Column(String(50), nullable=False, unique=True)
    name          = Column(String(255), nullable=False)
    description   = Column(Text)
    category_id   = Column(Integer, ForeignKey("categories.id"), nullable=False)
    cost_price    = Column(DECIMAL(12, 2), nullable=False, default=0)
    selling_price = Column(DECIMAL(12, 2), nullable=False, default=0)
    stock_qty     = Column(Integer, nullable=False, default=0)
    brand         = Column(String(100))
    is_active     = Column(SmallInteger, nullable=False, default=1)
    created_at    = Column(DateTime, server_default=func.now())
    updated_at    = Column(DateTime, server_default=func.now(), onupdate=func.now())

    category    = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")


# ── Customer ───────────────────────────────────────────────────────────────────

class Customer(Base):
    __tablename__ = "customers"

    id             = Column(Integer, primary_key=True, autoincrement=True)
    email          = Column(String(255), nullable=False, unique=True)
    first_name     = Column(String(100), nullable=False)
    last_name      = Column(String(100), nullable=False)
    phone          = Column(String(20))
    gender         = Column(SAEnum(GenderEnum), nullable=False, default=GenderEnum.Unknown)
    date_of_birth  = Column(Date)
    city           = Column(String(100))
    state          = Column(String(100))
    region         = Column(SAEnum(RegionEnum), nullable=False, default=RegionEnum.Central)
    country        = Column(String(100), nullable=False, default="United States")
    zip_code       = Column(String(20))
    segment        = Column(SAEnum(SegmentEnum), nullable=False, default=SegmentEnum.Consumer)
    is_active      = Column(SmallInteger, nullable=False, default=1)
    created_at     = Column(DateTime, server_default=func.now())
    updated_at     = Column(DateTime, server_default=func.now(), onupdate=func.now())

    orders = relationship("Order", back_populates="customer")


# ── Order ──────────────────────────────────────────────────────────────────────

class Order(Base):
    __tablename__ = "orders"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    order_number     = Column(String(30), nullable=False, unique=True)
    customer_id      = Column(Integer, ForeignKey("customers.id"), nullable=False)
    status           = Column(SAEnum(OrderStatusEnum), nullable=False, default=OrderStatusEnum.pending)
    order_date       = Column(DateTime, nullable=False)
    shipped_date     = Column(DateTime)
    delivered_date   = Column(DateTime)
    shipping_city    = Column(String(100))
    shipping_state   = Column(String(100))
    shipping_region  = Column(SAEnum(RegionEnum), nullable=False, default=RegionEnum.Central)
    shipping_country = Column(String(100), nullable=False, default="United States")
    shipping_zip     = Column(String(20))
    payment_method   = Column(SAEnum(PaymentMethodEnum), nullable=False, default=PaymentMethodEnum.CreditCard)
    discount_pct     = Column(DECIMAL(5, 2), nullable=False, default=0)
    shipping_fee     = Column(DECIMAL(10, 2), nullable=False, default=0)
    subtotal         = Column(DECIMAL(14, 2), nullable=False, default=0)
    discount_amount  = Column(DECIMAL(14, 2), nullable=False, default=0)
    total_amount     = Column(DECIMAL(14, 2), nullable=False, default=0)
    notes            = Column(Text)
    created_at       = Column(DateTime, server_default=func.now())
    updated_at       = Column(DateTime, server_default=func.now(), onupdate=func.now())

    customer    = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


# ── OrderItem ──────────────────────────────────────────────────────────────────

class OrderItem(Base):
    __tablename__ = "order_items"

    id           = Column(Integer, primary_key=True, autoincrement=True)
    order_id     = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id   = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity     = Column(Integer, nullable=False, default=1)
    unit_price   = Column(DECIMAL(12, 2), nullable=False)
    unit_cost    = Column(DECIMAL(12, 2), nullable=False, default=0)
    discount_pct = Column(DECIMAL(5, 2), nullable=False, default=0)
    line_revenue = Column(DECIMAL(14, 2), nullable=False)
    line_cost    = Column(DECIMAL(14, 2), nullable=False)
    line_profit  = Column(DECIMAL(14, 2), nullable=False)
    created_at   = Column(DateTime, server_default=func.now())

    order   = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
