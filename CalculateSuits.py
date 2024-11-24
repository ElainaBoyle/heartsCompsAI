'''
adds a column to the database for cardSuits of the winning hand
(cardSuits is an array with a count of each suit e.g 1 club, 5 diamons, 2 spades, 3 hearts)
'''



import psycopg2


def getCardSuits(hand):
    cardSuits = [0,0,0,0]

    for card in hand:
        suit = card[-1:]

        if suit == 'c':
            cardSuits[0] += 1
        if suit == 'd':
            cardSuits[1] += 1
        if suit == 's':
            cardSuits[2] += 1
        if suit == 'h':
            cardSuits[3] += 1
    
    return cardSuits






database = "heartsai_data" 
user = "aicomps"
host= 'localhost'
password = "12345"
port = 5432



conn = psycopg2.connect(database = "heartsai_data", user = "aicomps", host= 'localhost', password = "12345", port = 5432)

cur = conn.cursor()
#adds new column to the table for card suits
cur.execute("ALTER TABLE heartsai_data ADD cardSuits")

#gets all of the IDs and winning hands in tuples
cur.execute('SELECT ID, winning_hand FROM heartsai_data WHERE 1=1')
cases = cur.fetchall

updateString = 'UPDATE heartsai_data SET cardsuits = %s where ID = %s'


#updates the cardSuit column for each case
for case in cases:
    hand = case[1]
    id = case[0]

    cardSuits = getCardSuits(hand.split(', '))
    cur.execute(updateString % (cardSuits, id))

    


# Make the changes to the database persistent
conn.commit() 


# Close cursor and communication with the database
cur.close()
conn.close()