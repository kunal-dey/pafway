from flask import Flask
from flask_jwt_extended import JWTManager

from user.routes import user
from utils.config import SECRET

app = Flask(__name__)
jwt = JWTManager(app)

app.config['SECRET_KEY'] = SECRET
app.config['PROPAGATE_EXCEPTIONS'] = True

app.register_blueprint(user)

if __name__ == '__main__':
    app.run(debug=True, port=5000)