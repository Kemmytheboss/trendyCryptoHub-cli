from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.user_role import user_roles


class User(Base):
    __tablename__ = 'users'


    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


    profile = relationship('Profile', uselist=False, back_populates='user')
    wallets = relationship('Wallet', back_populates='user')
    transactions = relationship('Transaction', back_populates='user')
    roles = relationship('Role', secondary=user_roles, back_populates='users')


    @classmethod
    def create(cls, db, **kwargs):
        obj = cls(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj


    @classmethod
    def get_all(cls, db):
        return db.query(cls).all()


    @classmethod
    def find_by_id(cls, db, _id):
        return db.query(cls).filter(cls.id == _id).first()


    @classmethod
    def find_by_email(cls, db, email):
        return db.query(cls).filter(cls.email == email).first()


    def delete(self, db):
        db.delete(self)
        db.commit()