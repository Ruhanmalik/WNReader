from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/url', methods=['POST'])
def get_url():
    

@app.route("/api/users", methods = ['GET'])
def users():
    return jsonify(
        {
            "users":[
                'Ayaan',
                'Zohair',
                'Fardeen',
                'locking'
            ]
    })
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from Flask!', 'data': [1, 2, 3, 4, 5]})

@app.route('/api/users', methods=['POST'])
def create_user():
    # Handle POST request
    return jsonify({'status': 'success'}) 

@app.route('/')
def home():
    return jsonify({"Message": "Your flask server is running"})
if __name__ == '__main__':
    app.run(debug=True, port=5000)