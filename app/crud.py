from sqlalchemy.orm import Session
from . import models, schemas

def get_protein(db: Session, protein_id: int):
    return db.query(models.Protein).filter(models.Protein.id == protein_id).first()

def get_protein_by_name(db: Session, name: str):
    return db.query(models.Protein).filter(models.Protein.name == name).first()

def get_proteins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Protein).offset(skip).limit(limit).all()

def create_protein(db: Session, protein: schemas.ProteinCreate):
    db_protein = models.Protein(
        name=protein.name,
        sequence=protein.sequence,
        predicted_structure_url=protein.predicted_structure_url,
    )
    db.add(db_protein)
    db.commit()
    db.refresh(db_protein)
    return db_protein

def update_protein(db: Session, protein_id: int, protein: schemas.ProteinUpdate):
    db_protein = get_protein(db, protein_id)
    if db_protein:
        db_protein.name = protein.name
        db_protein.sequence = protein.sequence
        db_protein.predicted_structure_url = protein.predicted_structure_url
        db.commit()
        db.refresh(db_protein)
    return db_protein

def delete_protein(db: Session, protein_id: int):
    db_protein = get_protein(db, protein_id)
    if db_protein:
        db.delete(db_protein)
        db.commit()
    return db_protein
