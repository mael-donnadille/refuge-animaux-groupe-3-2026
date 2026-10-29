from sqlalchemy import Column, ForeignKey, Integer, String
from refuge_esn81.database.database import Base
from sqlalchemy.orm import relationship


class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    age = Column(Integer)
    description = Column(String(300))
    gender = Column(String(50))
    photo_url = Column(String(300))
    species_id = Column(Integer, ForeignKey("species.id"))

    species = relationship("Species", back_populates="animals")
