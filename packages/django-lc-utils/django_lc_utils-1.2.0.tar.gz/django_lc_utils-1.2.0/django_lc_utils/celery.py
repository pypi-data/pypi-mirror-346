"""This module contains utility functions for interacting with celery.

You should avoid importing application specific modules or classes here, this
should only contain generic libraries that can be used for any app.

"""

from functools import partial
from typing import Callable

from django.db import transaction


def queue_task(task: Callable, on_commit: bool = True, countdown: int = 0, *args, **kwargs) -> None | str:
    """Wrapper for calling celery tasks.  By default, tasks will be executed on commit to ensure that data
    has been persisted to the database.

    Examples:
        The most basic call to celery would look like::

           queue_task(your_task, arg1, arg2, kwarg1=val1, kwarg2=val2)

        Additionally, you can provide some arguments that are typically provided to apply_async, such
        as `countdown` and `queue`.

            queue_task(your_task, arg1, arg2, kwarg1=val1, kwarg2=val2, queue="low_priority_queue", countdown=5)

    Args:
        task (Callable): The function to be called as a celery task
        on_commit (bool): Whether to run this task on commit.  Defaults to `True`, and this is the recommended value.
        countdown (int): How long to wait before running this task (matches celery's `countdown` arg). If no `countdown`
            is provided, the task will be immediately queued.
        *args (tuple): Positional arguments to pass to the celery task.  This replaces passing `args=(arg1, arg2, ...)` to
           `apply_async`
        **kwargs (dict): Keyword arguments to pass to the celery task.  This replaces passing `kwargs={"arg1": val1}`

    Keyword Args:
        queue (str): The name of the queue to send the task to.  If no `queue` is provided, the default task
            queue is used.
    """
    task_kwargs = {}
    if queue := kwargs.pop("queue", None):
        task_kwargs["queue"] = queue

    if on_commit:
        transaction.on_commit(partial(task.apply_async, countdown=countdown, args=args, kwargs=kwargs, **task_kwargs))
        return

    return task.apply_async(countdown=countdown, args=args, kwargs=kwargs, **task_kwargs)
