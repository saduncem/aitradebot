"""Database models for the trading system.

Defines SQLAlchemy ORM models for storing candlestick data, wallet
assets, trade fills, and ledger entries.
"""

from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

from .database import Base  # Import the declarative base from database.py


class Candle(Base):
    __tablename__ = "candles"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    close_time = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


class WalletAsset(Base):
    __tablename__ = "wallet_assets"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    free = Column(Float, default=0.0)
    locked = Column(Float, default=0.0)


class TradeFill(Base):
    __tablename__ = "trade_fills"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    side = Column(String)
    price = Column(Float)
    qty = Column(Float)
    fee = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
