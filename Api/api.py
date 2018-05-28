from flask_api import FlaskAPI
from flask_cors import CORS
import dataset

app = FlaskAPI(__name__)
CORS(app)


@app.route('/example/', methods=['GET'])
def example():
    return {'Hello, ': 'world!'}


@app.route('/shop/', methods=['GET'])
def get_shop():
    with dataset.connect('postgresql://postgres:admin@localhost/postgres', 'pite') as database:
        return database['shop'].columns
