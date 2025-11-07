from celery import Celery, group

app = Celery(
    "tasks", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0"
)


@app.task
def call_an_expensive_api():
    print("calling an expensive API; USD 0.1 / call")
    return 42


@app.task
def call_another_expensive_api():
    print("calling another expensive API; USD 0.2 / call")
    return 42


@app.task
def main_task():
    group(
        call_an_expensive_api.s(),
        call_another_expensive_api.s(),
    )()
    raise ValueError("for some reason we always fail here")
