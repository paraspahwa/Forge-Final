"""
Subscription model for tracking payment history
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Subscription(Base):
    """Subscription history model"""
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Razorpay IDs
    razorpay_subscription_id = Column(String(255), nullable=True, index=True)
    razorpay_plan_id = Column(String(255), nullable=True)
    razorpay_payment_id = Column(String(255), nullable=True)
    razorpay_invoice_id = Column(String(255), nullable=True)
    
    # Plan info
    plan = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    currency = Column(String(3), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    
    # Period
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    
    # Metadata
    country_code = Column(String(2), nullable=True)
    ppp_ratio = Column(Numeric(3, 2), nullable=True)
    
    # Failure handling
    failure_count = Column(Integer, default=0)
    last_failure_reason = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cancelled_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    
    # Table indexes
    __table_args__ = (
        Index('idx_subscription_razorpay', 'razorpay_subscription_id'),
    )
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "plan": self.plan,
            "status": self.status,
            "currency": self.currency,
            "amount": float(self.amount),
            "current_period_start": self.current_period_start.isoformat() if self.current_period_start else None,
            "current_period_end": self.current_period_end.isoformat() if self.current_period_end else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }