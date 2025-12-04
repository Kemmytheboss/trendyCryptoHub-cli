from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    network = Column(String)
    address = Column(String)


    user = relationship('User', back_populates='wallets')


    @classmethod
    def create(cls, db, **kwargs):
    obj = cls(**kwargs)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj