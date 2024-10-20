from sqlalchemy.orm import joinedload 
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from auth.models import User
from database import get_db
from task.models import Task 
from auth.auth import get_current_user

router = APIRouter(
    prefix="/task",
    tags=["Task"]
)

@router.get("/history")
def get_task_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = (
        db.query(Task)
        .filter(Task.user_id == current_user.id)
        .options(joinedload(Task.results)) 
        .all()
    )
    
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this user.")

    return tasks
@router.delete("/history/{task_id}", response_model=dict)
def delete_task(task_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"detail": "Task deleted successfully"}