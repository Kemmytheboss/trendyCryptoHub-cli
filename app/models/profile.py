from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    full_name = Column(String)
    bio = Column(String)


    user = relationship('User', back_populates='profile')


    @classmethod
    def create_for_user(cls, db, user, **kwargs):
    profile = cls(user_id=user.id, **kwargs)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile