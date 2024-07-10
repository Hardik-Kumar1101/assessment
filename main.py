import os.path
from threading import Thread

from _mysql_connector import MySQL
from flask import Flask, request

from database import db
from helper import process_csv

import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'
app.config['FILE_DEFAULT_NAME'] = 'data_set.csv'

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'data'

db = db(app)

# mysql = MySQL.


@app.route('/')
def hello_world():
    return 'Hello World'


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
                # db operation & image processing
                if db.save_batch(batch_id):
                    thread = Thread(target=process_csv, args=(batch_id,))
                    thread.start()
                    return {"status": "success", "message": "File uploaded.", "batchId": batch_id}
                else:
                    return {'status': 'error', 'message': 'batch creation failed.'}
            else:
                return {"status": "error", "message": "File is not csv."}
    else:
        return {"status": "error", "message": "Bad Request"}


if __name__ == '__main__':
    app.run(debug=True)
