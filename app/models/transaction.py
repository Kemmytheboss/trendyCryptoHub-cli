from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Transaction(Base):
    __tablename__ = 'transactions'


    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tx_type = Column(String)
    amount = Column(Float)
    asset = Column(String)


    user = relationship('User', back_populates='transactions')