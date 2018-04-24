from flask_api import FlaskAPI

app = FlaskAPI(__name__)


@app.route('/example/', methods = ['GET'])
def example():
    return {'Hello, ' : 'world!'}
    