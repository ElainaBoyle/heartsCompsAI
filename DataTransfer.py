#Reads each file of the HeartsData folder and makes a SQL table
import psycopg2
import json
import os
import random

trick_number = 1

def read_moves(data):
    global trick_number
    move_dict = []
    if data["type"] == 'play':
        player = data["player"]
        card = data["card"]
        move_dict = {'player': player, 'card_played' : card}
    elif data["type"] == "trick":
        winner = data["winner"]
        move_dict = {'winner': winner, 'trick_number': trick_number}
        trick_number+=1
    elif data["type"] == "handOver":
        trick_number = 1
    if move_dict != []:   
        return move_dict
    return 

#Returns the player that won each hand.  Saves the index with the lowest score
def read_winner(data):  
    index = 0
    winner = None
    past_score = 100
    if(data["type"]=="handOver"):
        while index < len(data["scores"]):
            if(data["scores"][index] < past_score):
                past_score = data["scores"][index]
                winner = index
            index +=1    
    return winner


#Returns the list of all the hands after passing completes 
def handParser(dealt_hands, move):
    initial = dealt_hands.copy()
    player_hands = []
    original = 0
    target = 0
    index = 0
    if(move["type"] == "pass"):
        original = move["from"]
        target = move["to"]
        passed_cards = move["cards"]
        while index < len(initial):
            temp_hand = []

            #remove the passed cards from the current player's hand
            if(index == original):
                proto_hand = []
                for card in dealt_hands[original]:
                    if(card not in passed_cards):
                        proto_hand.append(card)
                temp_hand.extend(proto_hand)

            #add the passed cards to the target player's hand
            elif(index == target):
                temp_hand.extend(initial[target])
                temp_hand.extend(passed_cards)

            #if no passing is occurring, just copy over the contents of this player's hand
            else:
                temp_hand.extend(initial[index])

            #add the hand we were just modifying to our new list of hands before looping
            player_hands.append(temp_hand)
            
            index+=1  
        return player_hands
    return dealt_hands

#reads the lines of a JSON file and gathers the move data
def read_json(file_name):
    cartridge = []
    move_data = []
    with open(file_name, 'r') as f:
        data = json.load(f)
        for game in data:
            hands = []
            global trick_number 
            trick_number = 1
            dealt_cards = game["initialDeal"]
            temp_hands = dealt_cards
            trick_data = []

            for move in game["moves"]:
                temp_hands = handParser(temp_hands, move)
                if(temp_hands!= None and (dealt_cards != temp_hands)):
                    hands = temp_hands

                plays = read_moves(move)
                winner = read_winner(move)

                if (plays!= None):
                    trick_data.append(plays)
                    #if("winner" in move.keys()):
                    if(move["type"] == "trick"):
                        move_data.append(trick_data)
                        #print("hello")
                        trick_data = []
                if(winner != None):
                    # print("winner is not empty!")
                    cartridge.append({"move_data": move_data, "champion": winner, "hand": hands[winner]})

                    # print(cartridge)
                    # while True:
                    #     cont = input("Want to continue? ")
                    #     if cont == "y":
                    #         break
                    
            # Process the JSON data here
    return cartridge

def generate_deck():
    card_deck = ""
    card_suits = ["c", "d", "s", "h"]
    for suit in card_suits:
        count = 1
        while count <= 13:
            card_deck += "\"" + (str(count) + suit) + "\", "
            count+=1
    card_deck = card_deck[:-2]
    return(card_deck)

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

def generate_ID():
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    sequence = "\'"
    index = 0
    while index < 50:
        letter = random.randint(0,25)
        sequence += alphabet[letter]
        index += 1
    sequence += "\'"
    return sequence

def main():
    #Info we need in our table
    #hand/trick number, [where is every card], winning player, card played, [winning player's hand] 
    #0-3: Player Number played card
    #4: In hand winning player's hand
    #5: Unknown
    generate_deck()
    conn = psycopg2.connect(database = "heartsai_data", user = "aicomps", host= 'localhost', password = "12345", port = 5432)

    cur = conn.cursor()

    deck_string = generate_deck_string()

    query = "CREATE TABLE heartsai_data(trick_ID SERIAL UNIQUE NOT NULL PRIMARY KEY, " + deck_string + "trump_suit VARCHAR (5), game_winner SERIAL, winning_hand VARCHAR (100) NOT NULL);"
    cur.execute(query)
    # Make the changes to the database persistent
    conn.commit()
   
    INSERT = "INSERT INTO heartsai_data (trick_ID, " + generate_deck()+ ", trump_suit, game_winner, winning_hand) "

    
    deck = ['1c', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', '11c', '12c', '13c', '1d', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', '11d', '12d', '13d', '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', '11s', '12s', '13s', '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h']  
    id_list = []
    #trick_num = ""
    trick_num = 0
    directory = 'HeartsData'
    for filename in os.listdir(directory): 
        print(filename)
        cartridge = read_json(directory + '/'+ filename)
        #game_data structure:
        #each index is an entire game, with a full set of tricks.  These games are structured as such:
        #{"move_data": trick_data, "champion": winner, "hand": hands[winner]}
        deck_history = [5]*52
        for game_data in cartridge: #each game: {"move_data": trick_data, "champion": winner, "hand": hands[winner]}
            for trick in game_data["move_data"]: #trick = [{player: x, card_played: x}.....{winner: x, trick_number: x}]
                query ="" + INSERT
                values = "VALUES ("
                for play in trick: #play = {player: x, card_played: x}
                    index = 0
                    if(5 not in deck_history):
                        deck_history = [5]*52
                    for card in deck:
                        if ("card_played" in play.keys()) and (play["card_played"] == card):
                            if(play["player"] == game_data["champion"]):
                                deck_history[index] = 4
                            else:
                                deck_history[index] = play["player"]
                        index += 1
                values += str(trick_num) + ", "
                trick_num+=1
                for item in deck_history: 
                    values += str(item) + ", "
                winning_hand = ""
                for card in game_data["hand"]: 
                    winning_hand += card + ", "
                winning_hand = winning_hand[:-2]
                values += "\'" + trick[0]["card_played"][-1] + "\'" +", "+ str(game_data["champion"]) + ", " + "\'" + winning_hand +"\'" + "); \n"
                query += values
                cur.execute(query)
                # Make the changes to the database persistent
                conn.commit()
                query =""+ INSERT
    print("This is our ID: " + trick_num)



  
    # Close cursor and communication with the database
    cur.close()
    conn.close()

if __name__ == '__main__':
	main()