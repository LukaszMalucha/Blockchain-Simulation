import os
# import env

from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
from flask_restful import Api

from resources.user import UserRegister, UserLogin, UserLogout, login_manager
from models.blockchain import Blockchain, block_mining, bits_to_target

# Settings
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DEBUG'] = False
api = Api(app)

Bootstrap(app)
login_manager.init_app(app)

# Register Resources
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

# Initiate Blockchain:
blockchain = Blockchain()


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    """Homepage"""
    return render_template("dashboard.html")


@app.route('/mine_block', methods=['POST'])
def mine_block():
    """Mine a Block"""
    response = block_mining(blockchain)
    return jsonify(response), 200


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    """Add transaction to the next block"""
    index = blockchain.add_transaction(request.form['sender'], request.form['receiver'], request.form['amount'])
    response = {'message': "Transaction will be added to Block #{0}".format(index)}
    return jsonify(response), 200


@app.route('/validation_check', methods=['POST'])
def validation_check():
    """Check if Blockchain was not tampered"""
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'Blockchain is valid',
                    'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
    else:
        response = {'error': 'There are errors in the Blockchain',
                    'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/converter', methods=['POST'])
def converter():
    bits = int(request.form['bits'], 16)
    response = bits_to_target(bits)
    return jsonify(response), 200

# Error Handlers
@app.errorhandler(404)
def error404(error):
    return render_template('404.html')


@app.errorhandler(500)
def error500(error):
    return render_template('500.html')


## APP INITIATION

if __name__ == '__main__':
    from db import db

    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    # app.run(debug=True)

# Docker
    app.run(host='0.0.0.0')

# Heroku
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
