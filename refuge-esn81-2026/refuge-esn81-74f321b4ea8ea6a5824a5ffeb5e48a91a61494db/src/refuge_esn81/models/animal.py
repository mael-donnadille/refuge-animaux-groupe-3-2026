from sqlalchemy import Column, Integer, String, ForeignKey
from refuge_esn81.database.database import Base
from sqlalchemy.orm import relationship

class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    # A compléter
    photo_url = Column(String(300))
    species_id = Column(Integer, ForeignKey("species.id"))

    # Relation : un animal appartient à une espèce
    species = relationship("Species", back_populates="animals")
