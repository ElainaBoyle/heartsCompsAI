#Reads each file of the HeartsData folder and makes a SQL table
import psycopg2
import json
import os

trick_number = 0

def read_moves(data):
    global trick_number
    move_dict = []
    if data["type"] == 'play':
        player = data["player"]
        #print("player #" + str(player))
        card = data["card"]
        #print("card played: " + card)
        move_dict = {'player': player, 'card_played' : card}
    
    elif data["type"] == "trick":
        winner = data["winner"]
        move_dict = {'winner': winner, 'trick_number': trick_number}
        trick_number+=1

    if move_dict != []:   
        return move_dict
    return 

#Returns the player that won each hand.  Saves the index with the lowest score
def read_winner(data):  
    index = 0
    winner = None
    past_score = 100
    if(data["type"]=="handOver"):
        print("handOver!")
        print(len(data["scores"]))
        while index < len(data["scores"]):
            if(data["scores"][index] < past_score):
                past_score = data["scores"][index]
                winner = index
            index +=1
        print ("The winner is: " + str(winner))

    return winner


#Returns the hand of the player passed in this specific 
def handParser(dealt_hands, move):
    player_hands = []
    original = 0
    target = 0
    temp_hand = []
    for game in move:
        if(move["type"] == "pass"):
            original = move["from"]
            target = move["to"]

            
            return

    return player_hands


#reads the lines of a JSON file and gathers the move data
def read_json(file_name):
    hand_number = 0
    json_data={}
    print(file_name)
    move_data = []
    with open(file_name, 'r') as f:
        data = json.load(f)
        for game in data:
            #print("reading a new game!")
            hands = []
            global trick_number 
            trick_number = 1
            zero_hand = game["initialDeal"][1]
            print("Player One's hand: " + str(len(zero_hand)))
            dealt_cards = game["initialDeal"]
        
            print(dealt_cards)
            for move in game["moves"]: 
                #To-Do: Figure out what to do with knowledge of the winner, make a hand + trick number header, parse move data for the winner's card played
                #winner: We use it to tell us what hand data to pack 

                winner = read_winner(move)
                if(winner != None):
                    print()
                #print("reading a new set of moves!")
                temp_hands = handParser(dealt_cards, move)
                if(temp_hands!= None):
                    hands.append(temp_hands)

                plays = read_moves(move)
                if (plays!= None):
                    move_data.append(plays)
                    # cont = input("should I continue? ")
                    # if(cont != "y"):
                    #     break
            # Process the JSON data here

    return 

# def generate_deck():
#     card_deck = []
#     card_suits = ["s", "c", "d", "h"]
#     for suit in card_suits:
#         count = 1
#         while count <= 13:
#             card_deck.append(str(count) + suit)
#             count+=1
#     return card_deck

def generate_deck_string():
    card_deck = ""
    type_string = " SERIAL"
    card_suits = ["s", "c", "d", "h"]
    
    for suit in card_suits:
        count = 1
        while count <= 13:
            card_deck += str(count) + suit + type_string + ", "
            count +=1
    return card_deck

def main():
    #Info we need in our table
    #hand/trick number, [where is every card], winning player, card played, [winning player's hand] 
    #0-3: Player Number played card
    #4: In hand winning player's hand
    #5: Unknown
    deck = ['1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', '11s', '12s', '13s', '1c', '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', '10c', '11c', '12c', '13c', '1d', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', '10d', '11d', '12d', '13d', '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h']  
    

    directory = 'HeartsData'
    for filename in os.listdir(directory):
        game_data = read_json(directory + '/'+ filename)
        hand = []
        print(game_data[45])
        print(game_data[49])
        print(len(game_data))
        cont = input("Should I go to the next file? ")
        if(cont != "y"):
            break
    for card in deck:
        if card not in hand:
            
            if card in game_data[0]:
                print
    
    game_num =""

        
  

    # conn = psycopg2.connect(database = "heartsai_data", 
    #                         user = "aicomps", 
    #                         host= 'localhost',
    #                         password = "12345",
    #                         port = 5432)


    # cur = conn.cursor()

    # deck_string = generate_deck_string()

    # queury = "CREATE TABLE heartsai_data(game_num VARCHAR (50) UNIQUE NOT NULL PRIMARY KEY," + deck_string + "course_instructor VARCHAR (100) NOT NULL, topic VARCHAR (20) NOT NULL);"
    # cur.execute(queury)
    # # Make the changes to the database persistent
    # conn.commit()


    # # Close cursor and communication with the database
    # cur.close()
    # conn.close()

if __name__ == '__main__':
	main()