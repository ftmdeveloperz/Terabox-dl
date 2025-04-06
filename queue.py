# queue.py

from asyncio import Queue

user_queues = {}
cancel_tasks = {}

def get_user_queue(user_id):
    if user_id not in user_queues:
        user_queues[user_id] = Queue()
    return user_queues[user_id]

def add_to_queue(user_id, task):
    queue = get_user_queue(user_id)
    queue.put_nowait(task)

def get_next_task(user_id):
    queue = get_user_queue(user_id)
    return queue.get()

def task_done(user_id):
    queue = get_user_queue(user_id)
    queue.task_done()

def is_queue_empty(user_id):
    queue = get_user_queue(user_id)
    return queue.empty()

def set_cancel(user_id, value=True):
    cancel_tasks[user_id] = value

def check_cancel(user_id):
    return cancel_tasks.get(user_id, False)

def clear_cancel(user_id):
    cancel_tasks[user_id] = False

def pending_tasks(user_id):
    queue = get_user_queue(user_id)
    return queue.qsize()
