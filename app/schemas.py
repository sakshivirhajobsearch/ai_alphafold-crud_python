from pydantic import BaseModel

class ProteinBase(BaseModel):
    name: str
    sequence: str
    predicted_structure_url: str

class ProteinCreate(ProteinBase):
    pass

class ProteinUpdate(ProteinBase):
    pass

class Protein(ProteinBase):
    id: int

    class Config:
        from_attributes = True  # updated from orm_mode for Pydantic v2
