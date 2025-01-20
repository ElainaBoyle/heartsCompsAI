import psycopg2






def main():
    #Info we need in our table
    #hand/trick number, [where is every card], winning player, card played, [winning player's hand] 
    #0-3: Player Number played card
    #4: In hand winning player's hand # not working but it doesn't matter because you can already get who the winning player is
    #5: Unknown'

    conn = psycopg2.connect(database = "heartsai_data", user = "aicomps", host= 'localhost', password = "12345", port = 5432)
    cur = conn.cursor()

    cur.execute("ALTER TABLE heartsai_data ADD clubs varchar(255);")
    cur.execute("ALTER TABLE heartsai_data ADD diamonds varchar(255);" )
    cur.execute("ALTER TABLE heartsai_data ADD spades varchar(255);" )
    cur.execute("ALTER TABLE heartsai_data ADD hearts varchar(255);" )
    print("columns added")

    cur.execute("SELECT * FROM heartsai_data;")
    frames = cur.fetchall()
    for frame in frames:
        id = frame[0]
        winning_hand = (frame[56])[1:-1].split(", ")
        print(id)
        clubs = 0
        diamonds = 0
        spades = 0
        hearts = 0

        for card in winning_hand:
            #print(card)
            if card[-1:] == 'c':
                clubs += 1
            if card[-1:] == 'd':
                diamonds += 1
            if card[-1:] == 's':
                spades += 1
            if card[-1:] == 'h':
                hearts += 1
        
        suitsQuery = "UPDATE heartsai_data SET clubs = " + str(clubs)\
                        + ", diamonds = '" + str(diamonds)\
                        + "', spades = '" + str(spades)\
                        + "', hearts = '" + str(hearts)\
                        + "' WHERE trick_id = '" +  str(id) + "';"
        print(clubs, diamonds, spades, hearts)
        
        cur.execute(suitsQuery)


    cur.execute("DELETE FROM heartsai_data WHERE card_played like '%%s' AND winning_hand NOT LIKE '%%s%%")
    cur.execute("DELETE FROM heartsai_data WHERE card_played like '%%d' AND winning_hand NOT LIKE '%%d%%")
    cur.execute("DELETE FROM heartsai_data WHERE card_played like '%%c' AND winning_hand NOT LIKE '%%c%%")
    cur.execute("DELETE FROM heartsai_data WHERE card_played like '%%h' AND winning_hand NOT LIKE '%%h%%")

    print("updates completed")
    # Make the changes to the database persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()

if __name__ == '__main__':
	main()