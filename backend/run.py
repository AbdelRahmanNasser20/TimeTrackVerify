from app import create_app
import os
from dotenv import load_dotenv
from app.models import Employee, Event
from app.extensions import db


# from app import db
load_dotenv()

# Get the configuration name from the environment variable, default to 'development'
config_name = os.getenv('FLASK_ENV', "")
app = create_app(config_name)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Employee': Employee, 'Event': Event, 'app': app}



if __name__ == '__main__':
    debug_mode = os.getenv('DEBUG', 'True') == 'True'        
    # print("WE ARE RUNNING DB:",  app.config['SQLALCHEMY_DATABASE_URI'])        
    app.run(host='0.0.0.0', debug=debug_mode, port=5001)