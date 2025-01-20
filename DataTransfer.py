#Reads each file of the HeartsData folder and makes a SQL table
import psycopg2
import json
import os
import random

game_number = -1
conn = psycopg2.connect(database = "heartsai_data", user = "aicomps", host= 'localhost', password = "12345", port = 5432)
cur = conn.cursor()

def read_moves(data, history):
    deck = ['1c', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', '11c', '12c', '13c', '1d', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', '11d', '12d', '13d', '1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', '11s', '12s', '13s', '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h']  
    index = 0
    if data["type"] == 'play':
        player = data["player"]
        card_played = data["card"]
        for card in deck:
            if (card_played == card):
                history[index] = str(player)
            index += 1
    return history

#Returns the player that won each hand.  Saves the index with the lowest score
def read_winners(finalScores):  #finalScores = [{handNumber: x, scores: [a,b,c,d]}]
    winners = []
    for rounds in finalScores:
        player = 0
        best_player = -1
        past_score = 1000
        for score in rounds["scores"]:
            if score <= past_score:
                past_score = score
                best_player = player
            player+=1        
        winners.append(best_player)
    return winners

#Returns the list of all the hands after passing completes 
def hand_parser(dealt_hands, move): 
    initial = dealt_hands.copy()
    player_hands = []
    original = 0
    target = 0
    index = 0
    original = move["from"]
    target = move["to"]
    passed_cards = move["cards"] 
    while index < len(initial):
        temp_hand = []
        #remove the passed cards from the every player's hand but the target
        if(index == original):
            player_num = 0
            while(player_num < 4):
                if(player_num != target):
                    if(passed_cards[0] in initial[player_num]):
                        initial[player_num].remove(passed_cards[0])
                    if(passed_cards[1] in initial[player_num]):
                        initial[player_num].remove(passed_cards[1])
                    if(passed_cards[2] in initial[player_num]):
                        initial[player_num].remove(passed_cards[2])
                player_num +=1
            temp_hand.extend(initial[original])
        #add the passed cards to the target player's hand
        elif(index == target):
            temp_hand.extend(initial[target])
            for card in passed_cards:
                if(card not in temp_hand):
                    temp_hand.append(card)            
        #if no passing is occurring, just copy over the contents of this player's hand
        else:
            temp_hand.extend(initial[index])

        #add the hand we were just modifying to our new list of hands before looping
        player_hands.append(temp_hand)
        
        index+=1  
    return player_hands

#converts the winning hand to a SQL compatible string
def list_to_string(input_list):
    return_string = ""
    for item in input_list:
        return_string += str(item) + ", "
    return return_string[: -2]

#reads the lines of a JSON file and gathers the move data
def read_json(file_name):
    values = ""
    with open(file_name, 'r') as f:
        data = json.load(f)
        global game_number
        for game in data:
            game_number += 1
            hands = []
            id_list =[]
            dealt_cards = game["initialDeal"]
            temp_hands = dealt_cards
            deck_history = [5]*52
            winningPlayers = read_winners(game["finalScores"])
            hand_num = 0
            trump_suit = "NA"
            winner_play = ""
            for move in game["moves"]: #{"type": "pass","from": 0,"to": 1,"cards": ["1d","8c","6c"],"timestamp": "2024-10-20T09:05:56.631Z"}
                if(move["type"] == "handOver"):
                    winning_hand = "["+ list_to_string(hands[winningPlayers[hand_num]]) + "]"
                    deck_history = [5]*52
                    hand_num += 1
                    
                if(hand_num > 0):
                    continue

                if (move["type"] == "play"): 
                    if (trump_suit == None):
                        trump_suit = move["card"][-1:]
                    if(move["player"] == winningPlayers[hand_num]):
                        winner_play = move["card"]
                        if(move["trickPosition"] == 1):
                            trump_suit = "NA"
                #hand stuff
                if(move["type"] == "pass"):
                    temp_hands = hand_parser(temp_hands, move) #eventually gets us to "accurate" hands
                elif(dealt_cards != temp_hands):
                    hands = temp_hands
                while(True):
                    trick_id = generate_ID() +"g#"+ str(game_number) +"\'"
                    if(trick_id not in id_list):
                        id_list.append(trick_id)
                        break
                #History
                deck_history = read_moves(move, deck_history)
                if(move["type"] == "trick"): 
                    winning_hand = "["+ list_to_string(hands[winningPlayers[hand_num]]) + "]"
                    trick_history = list_to_string(deck_history)
                    values += trick_id + ", " + trick_history + ", " + "\'" + trump_suit + "\'" +", "+ str(winningPlayers[hand_num]) + ", " + "\'" + str(winner_play) + "\'" + ", "  +"\'"+ winning_hand +"\'" + "\n"                   
                    update_database(values)
                    if(winner_play in hands[winningPlayers[hand_num]]):
                        hands[winningPlayers[hand_num]].remove(winner_play)
                    values = ""
                    trump_suit = None

    return

#Generates a string representing a deck of cards
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

def generate_ID():
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    sequence = "\'"
    index = 0
    while index < 10:
        letter = random.randint(0,25)
        sequence += alphabet[letter]
        index += 1
    return sequence

def update_database(values):
    global cur
    global conn
    deck = "1c", "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "11c", "12c", "13c", "1d", "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "11d", "12d", "13d", "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "11s", "12s", "13s", "1h", "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "11h", "12h", "13h"
    INSERT = "INSERT INTO heartsai_data (trick_ID, " + generate_deck()+ ", trump_suit, game_winner, card_played, winning_hand)"
    query = INSERT + "VALUES (" + values + ")"
    cur.execute(query)
    conn.commit()
    return
def main():
    #Info we need in our table
    #hand/trick number, [where is every card], winning player, card played, [winning player's hand] 
    #0-3: Player Number played card
    #4: In hand winning player's hand
    #5: Unknown
    global conn
    global cur
    deck_string = generate_deck_string()
    make_table = input("Do you want to create the HeartsAI table? " )
    if(make_table.lower() in ("y", "yes")):
        query = "CREATE TABLE heartsai_data(trick_ID VARCHAR(100), " + deck_string + "trump_suit VARCHAR (5), game_winner SERIAL, card_played VARCHAR (50) NOT NULL, winning_hand VARCHAR (200) NOT NULL);"
        cur.execute(query)
        # Make the changes to the database persistent
        conn.commit()
    fill_table = input("Should I fill the table with game data? ")
    if(fill_table.lower() in ("y", "yes")):
        directory = 'HeartsData'
        for filename in os.listdir(directory): 
            print(filename)
            read_json(directory + '/'+ filename)
        print("I-I... I think we're finished")
    # Close cursor and communication with the database
    cur.close()
    conn.close()

if __name__ == '__main__':
	main()