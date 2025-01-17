import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import User, Transcription
from app import app, db
import config

app.config.from_object(config.DevelopmentConfig)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
