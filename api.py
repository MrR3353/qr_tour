from flask import Flask

import db

app = Flask(__name__)


@app.route('/<int:qr_id>', methods=['GET'])
def index(qr_id):
    return db.get_by_id(qr_id)


if __name__ == '__main__':
    app.run(port=5000)


