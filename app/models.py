from sqlalchemy import Column, Integer, String
from .database import Base

class Protein(Base):
    __tablename__ = "proteins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    sequence = Column(String)
    predicted_structure_url = Column(String)
