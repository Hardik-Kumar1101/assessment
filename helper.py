import pandas as pd



def validate_csv_file(data_frame):
    for i in data_frame.head(0).columns.values:
        print(i)
    if ['S. No.', 'Product Name', 'Input Image Urls'] in data_frame.head(0).columns.values:
        return True
    else:
        return False


def process_images(url_list):
    for item in url_list:
        print(item.replace('/n',''))


def process_csv(batch_id):
    print("process csv thread started")
    data_frame = pd.read_csv('data_set.csv')
    if validate_csv_file(data_frame):
        process_images(data_frame['Input Image Urls'])
    else:
        return {'status': 'error', 'message': 'Invalid file format.'}
    print("process csv thread end")
