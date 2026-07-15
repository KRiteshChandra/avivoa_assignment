from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from db import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(255), nullable=True)
    topic = Column(Text, nullable=True)
    sentiment = Column(String(50), nullable=True)
    outcomes = Column(Text, nullable=True)
    followup = Column(Text, nullable=True)
    raw_input = Column(Text, nullable=True)  # original user text, useful for debugging/demo
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "hcp_name": self.hcp_name,
            "topic": self.topic,
            "sentiment": self.sentiment,
            "outcomes": self.outcomes,
            "followup": self.followup,
            "raw_input": self.raw_input,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }