from flask import Flask
from application.config import DevelopmentConfig
from flask_security import SQLAlchemyUserDatastore, Security
from celery.schedules import crontab

from application.instances import cache
from application.api import api
from application.models import db
from application.sec import datastore
from application.workers import celery_init_app
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    api.init_app(app)
    cache.init_app(app)
    app.security = Security(app, datastore)
    
    with app.app_context():
        import application.views
        db.session.rollback()
        cache.clear()
        if not os.path.exists(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")):
            db.create_all()
            from initial_data import upload_initial_data
            upload_initial_data()
    
    app.app_context().push()
    return app

app = create_app()
celery_app=celery_init_app(app)

from application.tasks import daily_reminder
@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
  sender.add_periodic_task(
      crontab(hour=11,minute=2),
      daily_reminder.s(),
    ),

if __name__ == "__main__":
    app.run(debug=False)
