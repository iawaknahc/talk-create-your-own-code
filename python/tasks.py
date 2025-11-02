import secrets

from celery import Celery, group

app = Celery("tasks", broker="redis://localhost:6379/0")


@app.task
def call_an_expensive_api():
    print("calling an expensive API; USD 0.1 / call")
    return 42


@app.task
def call_another_expensive_api():
    print("calling another expensive API; USD 0.2 / call")
    return 42


@app.task(
    bind=True,
    max_retries=3,
    default_retry_delay=1,
    autoretry_for=(ValueError,),
)
def main_task(self):
    if self.request.retries > 0:
        print(
            f"id={self.request.id} starting other tasks in parallel: retry={self.request.retries}"
        )
    else:
        print(f"id={self.request.id} starting other tasks in parallel")
    group(
        call_an_expensive_api.s(),
        call_another_expensive_api.s(),
    )()
    raise ValueError(f"id={self.request.id} failed")
