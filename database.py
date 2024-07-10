import mysql.connector


class db:
    def __init__(self, app):
        self.mydb = mysql.connector.connect(
            host=app.config['MYSQL_DATABASE_HOST'],
            user=app.config['MYSQL_DATABASE_USER'],
            password=app.config['MYSQL_DATABASE_PASSWORD'],
            database=app.config['MYSQL_DATABASE_DB']
        )

    def save_batch(self, batch_id):
        try:
            cursor = self.mydb.cursor()
            query = "INSERT INTO batch (batch_id, current_status) VALUES (%s, %s)"
            value = (batch_id, 'processing')
            cursor.execute(query, value)
            return True
        except Exception as e:
            print(e)
            return False

    def __del__(self):
        self.mydb.close()
