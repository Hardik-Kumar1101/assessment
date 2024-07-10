import os.path
from threading import Thread
from flask import Flask, request

from database import db
from helper import process_csv, process_images

import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'
app.config['FILE_DEFAULT_NAME'] = 'data_set.csv'

host = 'localhost'
user = 'root'
password = 'root'
database = 'data'

db = db(host, user, password, database)


# mysql = MySQL.


@app.route('/status', methods=['GET'])
def get_status():
    if request.method == 'GET':
        batch_id = request.args.get('id')
        return db.get_batch(batch_id)
    else:
        return 'Invalid method.'


@app.route('/upload/file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        print("file name ", file.filename)
        if file.filename == '':
            return {"status": "error", "message": "File not found."}
        else:
            if file.filename.find('.csv'):
                folder = str(app.config['UPLOAD_FOLDER'])
                file_name = str(app.config['FILE_DEFAULT_NAME'])
                file.save(os.path.join(folder, file_name))
                batch_id = str(uuid.uuid4()).replace('-', '')

                data = process_csv(batch_id)
                if db.save_batch(batch_id) and data.get("response").get('status') == 'success':
                    thread = Thread(target=process_images, args=(batch_id, data.get('data'), ))
                    thread.start()
                    return data.get("response")
                else:
                    return data.get("response")
            else:
                return {"status": "error", "message": "File is not csv."}
    else:
        return {"status": "error", "message": "Bad Request"}


if __name__ == '__main__':
    app.run(debug=True)
