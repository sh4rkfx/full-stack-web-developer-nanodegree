"""Flask Migrate Management Script.

Allow the extension of the database after creation using migrate version
control and history.
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src import app, db

# Migrated Blueprints
from src.products import models as raw_data_models


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def list_models():
    """Fetch list of models."""
    print(type(raw_data_models))


if __name__ == '__main__':
    manager.run()

# **Commands List**
# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade
# python manage.py db downgrade
