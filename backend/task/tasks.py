from fuadmin.celery import app

@app.task()
def get_task():
  return 'test'