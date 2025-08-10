from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AlphaFold CRUD API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"message": "Welcome to AlphaFold CRUD API"}

@app.post("/proteins/", response_model=schemas.Protein)
def create_protein(protein: schemas.ProteinCreate, db: Session = Depends(get_db)):
    db_protein = crud.get_protein_by_name(db, name=protein.name)
    if db_protein:
        raise HTTPException(status_code=400, detail="Protein already exists")
    return crud.create_protein(db=db, protein=protein)

@app.get("/proteins/", response_model=list[schemas.Protein])
def read_proteins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_proteins(db, skip=skip, limit=limit)

@app.get("/proteins/{protein_id}", response_model=schemas.Protein)
def read_protein(protein_id: int, db: Session = Depends(get_db)):
    db_protein = crud.get_protein(db, protein_id=protein_id)
    if db_protein is None:
        raise HTTPException(status_code=404, detail="Protein not found")
    return db_protein

@app.put("/proteins/{protein_id}", response_model=schemas.Protein)
def update_protein(protein_id: int, protein: schemas.ProteinUpdate, db: Session = Depends(get_db)):
    db_protein = crud.get_protein(db, protein_id=protein_id)
    if db_protein is None:
        raise HTTPException(status_code=404, detail="Protein not found")
    return crud.update_protein(db=db, protein_id=protein_id, protein=protein)

@app.delete("/proteins/{protein_id}")
def delete_protein(protein_id: int, db: Session = Depends(get_db)):
    db_protein = crud.get_protein(db, protein_id=protein_id)
    if db_protein is None:
        raise HTTPException(status_code=404, detail="Protein not found")
    crud.delete_protein(db=db, protein_id=protein_id)
    return {"detail": "Protein deleted"}
