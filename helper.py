from threading import Thread
from time import sleep
import asyncio
import pandas as pd
from database import db

host = 'localhost'
user = 'root'
password = 'root'
database = 'data'

db = db(host, user, password, database)


def validate_csv_file(data_frame):
    if ['S. No.', 'Product Name', 'Input Image Urls'] in data_frame.head(0).columns.values:
        return True
    else:
        return False


def compress_image_waiting(n): sleep(n)


def process_images(batch_id, data_frame):
    print("thread started")
    output_images = list()
    counter = 0
    for data in data_frame['Input Image Urls']:
        data = data.replace('\n', '').replace("image", "image-output").replace(',', ',\n')

        for item in data.split(',\n'):
            db.save_process_image(batch_id, item)
            db.update_no_of_processed(batch_id, counter)
            counter += 1
            compress_image_waiting(1000)
            print("image " + str(counter) + ' processing completed')

        output_images.append(data)

    data_frame['Output Image Urls'] = output_images
    for i in data_frame['Output Image Urls']:
        print(i, end='\n')
    print(data_frame)




def process_csv(batch_id):
    data_frame = pd.read_csv('data_set.csv')
    if validate_csv_file(data_frame):
        return {"response": {'status': 'success', 'message': 'processing started.', 'batchId': batch_id},
                "data": data_frame}
    else:
        return {"response": {'status': 'error', 'message': 'Invalid file format.'}, "data": None}
