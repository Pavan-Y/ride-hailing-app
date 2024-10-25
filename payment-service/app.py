from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Payment

from dotenv import load_dotenv
load_dotenv()
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

@app.route('/payment', methods=['POST'])
def create_payment():
    data = request.json
    new_payment = Payment(ride_id=data['ride_id'], amount=data['amount'])
    
    db.session.add(new_payment)
    db.session.commit()
    
    return jsonify({'message': 'Payment processed successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=Config.PORT)
