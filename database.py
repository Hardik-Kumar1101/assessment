from mysql.connector.aio import connect


class db:
    mydb = connect()
    
    async def connect(self, host, user, password, database):
        self.mydb = await connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    async def save_batch(self, batch_id):
        try:
            cursor = await self.mydb.cursor()
            query = "INSERT INTO batch (batch_id, current_status, final_status) VALUES (%s, %s, %s)"
            value = (batch_id, 'processing', 'pending')
            await cursor.execute(query, value)
            await self.mydb.commit()
            return True
        except Exception as e:
            print(e)
            return False

    async def get_batch(self, batch_id):
        try:
            curses = await self.mydb.cursor()
            query = f"SELECT * FROM batch WHERE batch_id = '{batch_id}'"
            await curses.execute(query)
            return curses.fetchall()
        except Exception as e:
            print(e)
            return "Something went wrong."

    async def save_process_image(self, batch_id, image_uri):
        try:
            cursor = await self.mydb.cursor()
            query = "INSERT INTO process_image (batch_id, image_url) VALUES (%s, %s)"
            value = (batch_id, image_uri)
            await cursor.execute(query, value)
            await self.mydb.commit()
            return True
        except Exception as e:
            print(e)
            return False

    async def update_no_of_processed(self, batch_id, no):
        try:
            cursor = await self.mydb.cursor()
            query = "UPDATE batch SET no_of_processed = %s WHERE batch_id = %s"
            value = (no, batch_id)
            await cursor.execute(query, value)
            await self.mydb.commit()
            return True
        except Exception as e:
            print(e)
            return False

    async def update_final_status(self, batch_id):
        try:
            cursor = await self.mydb.cursor()
            query = "UPDATE batch SET final_status = %s WHERE batch_id = %s"
            value = ('completed', batch_id)
            await cursor.execute(query, value)
            await self.mydb.commit()
            return True
        except Exception as e:
            print(e)
            return False

