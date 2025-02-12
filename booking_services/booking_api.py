from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite for simplicity (Change to PostgreSQL if needed)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hellyeah22@localhost/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),
                      nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# POST /users - Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(name=data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added succesfully!"}), 201

# GET /users - Retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name} for user in users])

if __name__ == '__main__':
    app.run(debug=True)