import psycopg2

def main():

        conn = psycopg2.connect(database = "mock_data", 
                                user = "aicomps", 
                                host= 'localhost',
                                password = "12345",
                                port = 5432)


        cur = conn.cursor()

        #create a table
        cur.execute("""CREATE TABLE mock_data(
                game_num SERIAL PRIMARY KEY, XXXXXXXX, XXXXXXXX, XXXXXX)""")


        #import some mock games
        inputString = """INSERT INTO mock_data (ID, XXXXXXXXXX,XXXXXXX) VALUES(%s)"""
        arrarOfMockGames = []
        for game in arrarOfMockGames:
                cur.execute(inputString, game)


        # Make the changes to the database persistent
        conn.commit()
        # Close cursor and communication with the database
        cur.close()
        conn.close()