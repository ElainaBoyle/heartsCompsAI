import psycopg2

def main():

    conn = psycopg2.connect(database = "mock_data", 
                            user = "aicomps", 
                            host= 'localhost',
                            password = "12345",
                            port = 5432)


    cur = conn.cursor()

    cur.execute("""CREATE TABLE mock_data(
            game_num SERIAL PRIMARY KEY,
            course_name VARCHAR (50) UNIQUE NOT NULL,
            course_instructor VARCHAR (100) NOT NULL,
            topic VARCHAR (20) NOT NULL);
            """)
    # Make the changes to the database persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()