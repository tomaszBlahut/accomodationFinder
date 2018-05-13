from flask_api import FlaskAPI
from flask_cors import CORS
import db

app = FlaskAPI(__name__)
CORS(app)


@app.route('/example/', methods=['GET'])
def example():
    return {'Hello, ': 'world!'}


@app.route('/shop/', methods=['GET'])
def get_shop():
    return db.execute("SELECT * FROM pite.shop WHERE shop.city='WARSZAWA'")
