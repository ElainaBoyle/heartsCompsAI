#Reads each file of the HeartsData folder and makes a SQL table
import psycopg2

conn = psycopg2.connect(database = "thomastothe", user = "thomastothe", host= 'localhost', password = "corgi981phone", port = 5432)
cur = conn.cursor()


#Creates a SQL cstring to be used for table headings representing a deck of cards
def generate_deck_string():
    card_deck = ""
    type_string = " SERIAL"
    card_suits = ["c", "d", "s", "h"]
    for suit in card_suits:
        count = 1
        while count <= 13:
            card_deck += "\"" + str(count) + suit + "\"" + type_string + ", "
            count +=1
    return card_deck



def main():

    global conn
    global cur
    deck_string = generate_deck_string()
    query = "CREATE TABLE wocg_data(trick_ID VARCHAR(100), " + deck_string + "trump_suit VARCHAR (5), high_card VARCHAR (10), trick_score VARCHAR (100), game_winner SERIAL, card_played VARCHAR (50) NOT NULL, winning_hand VARCHAR (200) NOT NULL);"
    cur.execute(query)

    query = "CREATE TABLE heuristics_data(trick_ID VARCHAR(100), " + deck_string + "trump_suit VARCHAR (5), high_card VARCHAR (10), trick_score VARCHAR (100), game_winner SERIAL, card_played VARCHAR (50) NOT NULL, winning_hand VARCHAR (200) NOT NULL);"
    cur.execute(query)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
	main()