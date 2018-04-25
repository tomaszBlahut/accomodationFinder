from flask_api import FlaskAPI
import db

app = FlaskAPI(__name__)

@app.route('/example/', methods = ['GET'])
def example():
    return {'Hello, ' : 'world!'}
    
@app.route('/shop/', methods = ['GET'])
def getShop():
    return db.execute("SELECT * FROM pite.shop WHERE shop.city='WARSZAWA'")

