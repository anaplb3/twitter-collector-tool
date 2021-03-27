from flask_script import Manager
from flask import Flask
from flask_cors import CORS
import os
from app import blueprint
from apscheduler.schedulers.background import BackgroundScheduler
from tweetcollector.collector import Collector
from tweetcollector.report import Report

 # Config for flask app
app = Flask(__name__)
app.register_blueprint(blueprint)
CORS(app)
app.app_context().push()

cl = Collector()

# Config for cron job
cron = BackgroundScheduler(daemon=True, timezone='America/Sao_Paulo')
cron.add_job(cl.collect(), 'cron', day_of_week=(
    'mon-fri'), minute='0-59/30', hour='7-0')

manager = Manager(app)

cfg = PROD_CFG if os.environ['ENV'] == 'prod' else DEV_CFG

@manager.command
def run():
    cron.start()
    port = cfg["port"]
    app.run(host=cfg["host"], port=port, debug=cfg["debug"])


if __name__ == "__main__":
    manager.run()