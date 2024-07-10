import mysql.connector


class db:
    def __init__(self, host, user, password, database):
        self.mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def save_batch(self, batch_id):
        try:
            cursor = self.mydb.cursor()
            query = "INSERT INTO batch (batch_id, current_status, final_status) VALUES (%s, %s, %s)"
            value = (batch_id, 'processing', 'pending')
            cursor.execute(query, value)
            self.mydb.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_batch(self, batch_id):
        try:
            curses = self.mydb.cursor()
            query = f"SELECT * FROM batch WHERE batch_id = '{batch_id}'"
            curses.execute(query)
            return curses.fetchall()
        except Exception as e:
            print(e)
            return "Something went wrong."

    def save_process_image(self, batch_id, image_uri):
        try:
            cursor = self.mydb.cursor()
            query = "INSERT INTO process_image (batch_id, image_url) VALUES (%s, %s)"
            value = (batch_id, image_uri)
            cursor.execute(query, value)
            self.mydb.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def update_no_of_processed(self, batch_id, no):
        try:
            cursor = self.mydb.cursor()
            query = "UPDATE batch SET no_of_processed = %s WHERE batch_id = %s"
            value = (no, batch_id)
            cursor.execute(query, value)
            self.mydb.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def update_final_status(self, batch_id):
        try:
            cursor = self.mydb.cursor()
            query = "UPDATE batch SET final_status = %s WHERE batch_id = %s"
            value = ('completed', batch_id)
            cursor.execute(query, value)
            self.mydb.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def __del__(self):
        self.mydb.close()
