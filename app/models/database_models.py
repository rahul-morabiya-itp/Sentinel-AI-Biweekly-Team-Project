from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Text

from app.core.database import Base


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)

    source = Column(String, nullable=False)

    prompt = Column(Text, nullable=False)

    response = Column(Text, nullable=False)

    intent = Column(String)

    risk_level = Column(String)

    pii_detected = Column(String)

    similarity_score = Column(Float)

    input_tokens = Column(Integer)

    output_tokens = Column(Integer)

    total_tokens = Column(Integer)

    latency = Column(Float)

    estimated_cost = Column(Float)

    optimization = Column(Text)
