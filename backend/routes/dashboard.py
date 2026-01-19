from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from core.database import get_session
from core.security import get_current_user
from models.task import Task

router = APIRouter(tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(session: Session = Depends(get_session), current_user_id: str = Depends(get_current_user)):
    # Count completed and pending tasks for current user
    stmt_completed = select(Task).where(Task.user_id == int(current_user_id), Task.status == True)
    stmt_pending = select(Task).where(Task.user_id == int(current_user_id), Task.status == False)

    completed = session.exec(stmt_completed).all()
    pending = session.exec(stmt_pending).all()

    # upcomingDeadlines is a simple approximation: tasks with a due_date in future within 7 days (if due_date exists)
    upcoming = 0
    try:
        from datetime import datetime, timedelta
        upcoming_threshold = datetime.utcnow() + timedelta(days=7)
        stmt_upcoming = select(Task).where(Task.user_id == int(current_user_id), Task.due_date != None, Task.due_date <= upcoming_threshold)
        upcoming = len(session.exec(stmt_upcoming).all())
    except Exception:
        # models may not have due_date, ignore
        upcoming = 0

    return {
        "tasksCompleted": len(completed),
        "pendingTasks": len(pending),
        "upcomingDeadlines": upcoming,
    }
