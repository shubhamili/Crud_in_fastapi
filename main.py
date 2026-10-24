from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse
from config import settings

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

Base.metadata.create_all(bind=engine)



@app.get("/")
def home():
    return {"message": f"Welcome to {settings.APP_NAME}"}



@app.post("/tasks", response_model= TaskResponse, status_code=201)
def create_task(task:TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(**task.model_dump())

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task



@app.get("/tasks", response_model=list[TaskResponse], status_code=200)
def get_tasks(db:Session = Depends(get_db)):
    return db.query(Task).all()



@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id:int, db:Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

