import psycopg2






def main():
    #Info we need in our table
    #hand/trick number, [where is every card], winning player, card played, [winning player's hand] 
    #0-3: Player Number played card
    #4: In hand winning player's hand # not working but it doesn't matter because you can already get who the winning player is
    #5: Unknown'

    conn = psycopg2.connect(database = "heartsai_data", user = "aicomps", host= 'localhost', password = "12345", port = 5432)
    cur = conn.cursor()

    cur.execute("ALTER TABLE heartsai_data2 ADD clubs varchar(255);")
    cur.execute("ALTER TABLE heartsai_data2 ADD diamonds varchar(255);" )
    cur.execute("ALTER TABLE heartsai_data2 ADD spades varchar(255);" )
    cur.execute("ALTER TABLE heartsai_data2 ADD hearts varchar(255);" )
    print("columns added")

    cur.execute("SELECT * FROM heartsai_data2;")
    frames = cur.fetchall()
    for frame in frames:
        id = frame[0]
        winning_hand = (frame[57])[1:-1].split(", ")
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
        
        suitsQuery = "UPDATE heartsai_data2 SET clubs = " + str(clubs)\
                        + ", diamonds = '" + str(diamonds)\
                        + "', spades = '" + str(spades)\
                        + "', hearts = '" + str(hearts)\
                        + "' WHERE trick_id = '" +  str(id) + "';"
        print(clubs, diamonds, spades, hearts)
        
        cur.execute(suitsQuery)


    cur.execute("DELETE FROM heartsai_data2 WHERE card_played NOT LIKE '%%c' AND trumps_suit LIKE 'c' AND winning_hand LIKE '%%c%%';")
    cur.execute("DELETE FROM heartsai_data2 WHERE card_played NOT LIKE '%%d' AND trumps_suit LIKE 'd' AND winning_hand LIKE '%%d%%';")
    cur.execute("DELETE FROM heartsai_data2 WHERE card_played NOT LIKE '%%s' AND trumps_suit LIKE 's' AND winning_hand LIKE '%%s%%';")
    cur.execute("DELETE FROM heartsai_data2 WHERE card_played NOT LIKE '%%h' AND trumps_suit LIKE 'h' AND winning_hand LIKE '%%h%%';")

    print("updates completed")
    # Make the changes to the database persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()

if __name__ == '__main__':
	main()