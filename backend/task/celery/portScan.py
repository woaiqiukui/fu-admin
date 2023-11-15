from fuadmin.celery import app

@app.task
def portScan():
    print("portScan")
    return "portScan"