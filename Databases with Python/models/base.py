from arrow import now
from sqlalchemy.orm import declarative_base
from main import session
from sqlalchemy import column,DateTime
from datetime import datetime
from sqlalchemy.sql import func


Model = declarative_base()
Model_query = session.query_property()


from sqlalchemy import Column, DateTime


class TimedStampedModel(Model):
    __abstract__ = True

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())