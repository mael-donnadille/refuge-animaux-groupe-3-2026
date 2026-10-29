from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from refuge_esn81.database.database import Base

class Species(Base):
    __tablename__ = "species"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)

    # Relation bidirectionnelle avec Animal
    animals = relationship("Animal", back_populates="species")
