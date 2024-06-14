from api import app
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
#scheduler.add_job(func='print_date_time', trigger="interval", seconds=60)
#scheduler.add_job(func='print_date_time')
scheduler.start()
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
