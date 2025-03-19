from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify(status="ok"), 200

@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    data = request.get_json()
    return jsonify({"status": "success", "message": "Payment verified"}), 200

if __name__ == '__main__':
    app.run(port=5002)  