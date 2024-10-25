from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from config import Config
from models import db, Ride
import json

from dotenv import load_dotenv
load_dotenv()
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

redis_client = FlaskRedis(app)

@app.route('/ride', methods=['GET'])
def get_rides():
    cached_rides = redis_client.get('rides')
    if cached_rides:
        return jsonify(json.loads(cached_rides)), 200

    rides = Ride.query.all()
    rides_data = [{'id': r.id, 'user_id': r.user_id, 'pickup_location': r.pickup_location, 
                   'dropoff_location': r.dropoff_location, 'status': r.status} for r in rides]
    
    redis_client.set('rides', json.dumps(rides_data), ex=60)
    return jsonify(rides_data), 200

@app.route('/ride', methods=['POST'])
def create_ride():
    data = request.json
    new_ride = Ride(user_id=data['user_id'], pickup_location=data['pickup_location'], 
                    dropoff_location=data['dropoff_location'])
    
    db.session.add(new_ride)
    db.session.commit()
    
    redis_client.delete('rides')
    
    return jsonify({'message': 'Ride created successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=Config.PORT)
