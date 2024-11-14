import psycopg2
from Deck import Deck
import random

def main():

        conn = psycopg2.connect(database = "mock_data", 
                                user = "aicomps", 
                                host= 'localhost',
                                password = "12345",
                                port = 5432)


        cur = conn.cursor()

        #create a table
        cur.execute("""CREATE TABLE mock_data(
                ID SERIAL PRIMARY KEY, Trump, myHand SET, myCardSuits Set, nextMove)""")


        #import some mock games
        inputString = """INSERT INTO mock_data (ID, Trump, myHand, myCardSuits, nextMove) VALUES(%s)"""
        arrayOfMockGames = []

        for x in range(100):
                string = '' + x + ', c, (), (),' + ''


                deck = Deck()
	        deck.shuffle()
                i = 0
		for x in range(13):
			self.players[i % len(self.players)].addCard(self.deck.deal())
			i += 1








                arrayOfMockGames[x] = string
        for game in arrayOfMockGames:
                cur.execute(inputString, game)


        # Make the changes to the database persistent
        conn.commit()
        # Close cursor and communication with the database
        cur.close()
        conn.close()