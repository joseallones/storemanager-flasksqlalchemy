import os

from flask import Flask
import warnings
from model import db
from blueprint import blueprint


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "store.db"))


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db.init_app(app)
app.register_blueprint(blueprint, url_prefix='')

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port= 5001)