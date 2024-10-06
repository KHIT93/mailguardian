from fastapi import Depends
import importlib
import logging
import rich
from sqlmodel import Session, select
import time
from typing import Optional, Annotated
import typer
from mailguardian.app.dependencies import get_database_session
from mailguardian.app.models.task import Task, TaskState
from mailguardian.config.app import settings
from mailguardian.database.connect import Database, engine

logger = logging.getLogger(__name__)

app: typer.Typer = typer.Typer()

@app.command('run')
def run_task():
    # NOTE: typer does as of 0.12.5 not suppport injecting a database session. As a workaround, we create the session manually here
    # Use a new mailguardian.app.models.Task model
    # This model will store data on what task to perform
    # Run an infinite while loop to query the database table and
    # fetch the next unprocessed record and hand it off to Celery
    # Add in a Node UUID to be ready for multi-node processing,
    # so that we can avoid RabbitMQ and Redis etc.
    # The initial usecase is to have the Perl plugins for MailScanner
    # just store the raw headers + the raw spam report
    # and then we can split it in Python and store the individual parts
    logger.info('Started scheduler')
    with Session(engine) as db:
        # Find the next task to run
        while True:
            time.sleep(1)
            try:
                logger.debug('Checking for new tasks')
                next_task: Task = db.exec(select(Task).where(Task.state == TaskState.PENDING)).first()
                if not next_task:
                    logger.debug('No new tasks found')
                    continue
                # Use importlib to find the task to run
                # Mark the task as started
                next_task.state = TaskState.STARTED
                db.add(next_task)
                db.commit()
                # Execute the task with the payload as arguments
                task_module = importlib.import_module(next_task.module)
                if not hasattr(task_module, next_task.task):
                    next_task.state = TaskState.REJECTED
                    rich.print('[red][bold] %s.%s does not exist!' % (next_task.module, next_task.task))
                    db.add(next_task)
                    db.commit()
                else:
                    # Make sure the task runs within a try/except block so that it does not break the scheduler
                    try:
                        task_exec = getattr(task_module, next_task.task)
                        task_exec(db=db, payload=next_task.payload)
                    # Upon success, mark the task as completed
                        next_task.state = TaskState.SUCCESS
                    except:
                        # Upon an error, register the issue on the task and allow the scheduler to continue on to the next task
                        next_task.state = TaskState.FAILURE
                    finally:
                        db.add(next_task)
                        db.commit()
                
            except KeyboardInterrupt:
                raise typer.Exit(0)
    
    rich.print('Task processing stopped')

