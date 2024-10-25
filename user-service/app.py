from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from models import db, User
import json

from dotenv import load_dotenv
load_dotenv()
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
redis_client = FlaskRedis(app)

@app.route('/users', methods=['GET'])
def get_users():
    cached_users = redis_client.get('users')
    if cached_users:
        return jsonify(json.loads(cached_users)), 200

    users = User.query.all()
    users_data = [{'id': u.id, 'name': u.name, 'email': u.email, 'phone': u.phone} for u in users]
    
    redis_client.set('users', json.dumps(users_data), ex=60)
    return jsonify(users_data), 200

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'], phone=data.get('phone'))
    
    db.session.add(new_user)
    db.session.commit()
    
    # Invalidate cache
    redis_client.delete('users')
    
    return jsonify({'message': 'User created successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=Config.PORT)
