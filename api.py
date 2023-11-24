from flask import Flask, jsonify

import db

app = Flask(__name__)

@app.route('/<int:qr_id>', methods=['GET'])
def index(qr_id):
    try:
        return db.get_by_id(qr_id)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'status': '1', 'message': error_message}), 400

if __name__ == '__main__':
    app.run(port=5000)
