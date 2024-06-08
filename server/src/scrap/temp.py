from server.src.database import get_db_context
from server.src.scrap.crud import update_task
from server.src.scrap.models import Task

with get_db_context() as session:
    new_task = Task(
        scrap_query="adsada",
        scrap_data="ajdbasjdasjdaskdab",
        status="InProgress",
    )

    session.add(new_task)
    session.commit()
    task = session.query(Task).filter(Task.id == 1).first()

    update_task(session, 1)
    print(task.scrap_query)
