from flask_script import Manager
from library import app
from library import db

from library.knowledge.models import Knowledge

manager = Manager(app)

@manager.command
def init():
    try:
        db.create_all()
        print('Database created!')
    except:
        print('Error!')

if __name__ == '__main__':
    manager.run()