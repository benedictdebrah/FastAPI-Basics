from .database import Base
from sqlalchemy import Column, Boolean,Integer,String
from sqlalchemy.sql.expression import null


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content =Column(String,nullable=False)
    published = Column(Boolean,default=True)
