import sys
import random
import itertools
import os
import time
from tkinter import *
from PIL import ImageTk, Image

#Setting up the user interface
def initTk(b1Amount, b2Amount, b3Amount, pAmount):
    root.geometry("800x600")
    root.title("Texas Hold'em")

    canvas = Canvas(root, height=600, width=800, bg="#F0F0F0")
    canvas.pack()

    Label(root, text="Bot 1: $"+str(b1Amount), font=("Arial", 16)).place(x=20, y=250)
    Label(root, text="Bot 2: $"+str(b2Amount), font=("Arial", 16)).place(x=350, y=80)
    Label(root, text="Bot 3: $"+str(b3Amount), font=("Arial", 16)).place(x=650, y=250)
    Label(root, text="Player: $"+str(pAmount), font=("Arial", 16)).place(x=350, y=400)
    Label(root, text="community cards", font=("Arial", 16)).place(x=250, y=250)

    root.update()

#Displaying cards
def displayCard(card, X, Y):
    path = card[1:]
    if card[0] == "C":
        path += "_of_clubs.png"
    if card[0] == "H":
        path += "_of_hearts.png"
    if card[0] == "D":
        path += "_of_diamonds.png"
    if card[0] == "S":
        path += "_of_spades.png"
    if card[0] == "B":
        path = "back.png"
    img = ImageTk.PhotoImage(Image.open(path).resize((55, 80)))
    label = Label(root, image = img)
    label.image = img
    label.place(x=X, y=Y)
    root.update()

###Below are the three functions to determine the ranks, to handle the tie situation(same rank), and to get winner.
def rank_determined(card):
    suits = [i[0] for i in card]
    values = [int(i[1:]) for i in card]
    values.sort() # sort the value in order to compare the rank, as the result using list here.

    value_count = [values.count(i) for i in set(values)] 
    # set only includes the unique value, it's more convinient to compare when it comes to pairs, etc.
    value_count.sort() #using sort to avoid mistake that five cards may not come in order.

    if len(set(suits)) == 1: #unique values in a list should be in rank 0, 1, 4.
        if values == [1,10,11,12,13]:
            return 0,[14]
        elif len(set(values)) == 5 and values[-1] - values[0] == 4:
            if 1 in values and 2 in values:
                return 4,samerank(4,card)
            else:
                return 1,samerank(1,card)
        else:
            return 4,samerank(4,card)
    else: #find out the patterns by counting how many same values and different values
        if value_count == [1,1,1,1,1]:
            if values == [1,10,11,12,13]:
                return 5,samerank(5,card)
            elif values[-1] - values[0] == 4:
                if 1 in values and 2 in values:
                    return 9,samerank(9,card)
                else:
                    return 5,samerank(5,card)
            else:
                return 9,samerank(9,card)
        elif value_count == [1,1,3]:
            return 6,samerank(6,card)
        elif value_count == [1,2,2]:
            return 7,samerank(7,card)
        elif value_count == [1,4]:
            return 2,samerank(2,card)
        elif value_count == [2,3]:
            return 3,samerank(3,card)
        elif value_count == [1,1,1,2]:
            return 8,samerank(8,card)
def samerank(rank,card): #if there are same ranks

    values = [int(i[1:]) for i in card]
    values.sort() #also using list here that way easier to modify and sort

    if rank == 1:
        return [values[-1]]
    elif rank == 2:
        playervalue = [i for i in set(values) if values.count(i) == 4] #four cards that have same value, so count is 4
        for i in set(values):
            if values.count(i) == 1: #put the four cards at first place and the last card in the last position
                playervalue.append(i) #using list here is easier to modify the order of cards.
        return playervalue
    elif rank == 3:
        playervalue = [i for i in set(values) if values.count(i) == 3] #same idea in the following
        for i in set(values):
            if values.count(i) == 2:
                playervalue.append(i)
        return playervalue
    elif rank == 4:
        return [sum(values)]
    elif rank == 5:
        if values == [1,10,11,12,13]:
            return [14]
        else:
            return [values[-1]]
    elif rank == 6:
        playervalue = [i for i in set(values) if values.count(i) == 3]
        secvalue = []
        for i in set(values):
            if values.count(i) == 1:
                secvalue.append(i)
        secvalue.sort(reverse = True)
        return playervalue+secvalue
    elif rank == 7:
        playervalue = [i for i in set(values) if values.count(i) == 2]
        playervalue.sort(reverse= True)
        for i in set(values):
            if values.count(i) == 1:
                playervalue.append(i)
        return playervalue
    elif rank == 8:
        playervalue = [i for i in set(values) if values.count(i) == 2]
        secvalue = []
        for i in set(values):
            if values.count(i) == 1:
                secvalue.append(i)
        secvalue.sort(reverse = True)
        return playervalue+secvalue
    else:
        if 1 in values:
            if 2 in values:
                return [100*15 + sum(values)+26] #100* help distinguishes the largest value, the sum will not affect the 100*.
            else:
                return [100*14 + sum(values)+13]
        else:
            return [100*values[-1] + sum(values)]
def get_winner(player):
    lowrank = min([i[0] for i in player.values()]) #find the minimun rank
    player = {i[0]:i[1] for i in player.items() if i[1][0] == lowrank} #find the minimum rank from the dictionary
    length = len(player[list(player.keys())[0]][1])
    for i in range(length): #compare each index in a sorted order to check the largest value
        largestvalue = max([p[1][i] for p in player.values()])
        player = {p[0]:p[1] for p in player.items() if p[1][1][i] == largestvalue}

    return list(player.keys())

###For round two, players get their best combination with 5 cards out of 7 cards.
##Using module itertools to see all the possible combinations with 5 cards for each players, and 
#get the best combination for each player that has the highest rank.
def sevencards_determined(card):
    allcases = list(itertools.combinations(card, 5))
    cases = {c:rank_determined(list(c)) for c in allcases}
    return cases[get_winner(cases)[0]]

#This class returns the stats for each round and each game.
class game:

    def __init__(self,numplayer):
        self.numplayer = numplayer
        self.gamerun = True

    def user_input(self,mode,p):
        #falsecommand here is for Assignment 3, you can ignore.
        falsecommand = True
        if mode == "fold/bet":
            print("Hint: Always check your hand cards first!!")
            print("Please choose fold or bet or check(c/f/b): Note:check = c , fold = f , bet = b\n")
            
            # 0 for fold, 1 for bet
            var = IntVar()
            foldBtn = Button(root, bg='#8998D3', text ="Fold", height = 5, width = 15, command = lambda: var.set(0))
            foldBtn.place(x=200, y=400)

            betBtn = Button(root, bg='#8998D3', text ="Bet", height = 5, width = 15, command = lambda: var.set(1))
            betBtn.place(x=500, y=400)

            root.update()
            root.wait_variable(var)

            foldBtn["state"] = "disabled"
            betBtn["state"] = "disabled"
            root.update()

            if var.get() == 0:
                p[1].fold = True
                falsecommand = False
                return p
            else:
                p[1].fold = False
                falsecommand = False
                return p
        elif mode == "betvalue":
            '''
            while falsecommand:
                try:
                    value = int(input("Please input the value that you bet, now you have %s:\n"%(p[1].money-p[1].bet1)))
                    if value <= p[1].money - p[1].bet1:
                        falsecommand = False
                    else:
                        print("You don't have much money poor man.")

                except TypeError:
                    print("please input an integer")
            '''
            #global pop
            pop = Toplevel(root)
            pop.title("Bet Amount")
            pop.geometry("300x150")
            label = Label(pop, text="Please input the value that you bet, \nnow you have $%s:\n"%(p[1].money-p[1].bet1), font=('Aerial', 14))
            label.pack()
            #frame = Frame(pop)
            #frame.pack()
            entry = Entry(pop)
            entry.pack()
            val = IntVar()
            clicked = IntVar()
            clicked.set(0)
            btn = Button(pop, text="ok", command=lambda: clicked.set(1))
            btn.pack()
            pop.update()
            pop.wait_variable(clicked)
            root.wait_variable(clicked)
            val.set(entry.get())
            pop.destroy()
            return val.get()
        elif mode == "continue":
            '''
            while falsecommand:
                command = input("You want to continue the game?? Yes or No(Y/N):\n")
                if command == "Y" or command == 'y':
                    return True
                elif command == "N" or command == 'n':
                    return False
                else:
                    print("please choose the right command : Y = continue , N = game stop")
            '''
            Label(root, fg="red", text="You want to continue the game??", font=("Arial", 16)).place(x=360, y=20)

            # 0 for no, 1 for yes
            var = IntVar()
            foldBtn = Button(root, bg='#8998D3', text ="No", command = lambda: var.set(0))
            foldBtn.place(x=700, y=20)

            betBtn = Button(root, bg='#8998D3', text ="Yes", command = lambda: var.set(1))
            betBtn.place(x=750, y=20)

            root.update()
            root.wait_variable(var)

            if var.get() == 1:
                return True
            else:
                return False

    #Starting the game and processing each round and print the final results(The final winner and the money he received).
    def game_start(self):
        self.players = {}
        round = 0
        u = player("u")
        self.players["User"] = u
        for j in range(self.numplayer):
            p = player("b")
            self.players["Bot %s"%(j+1)] = p
        while self.gamerun:
            self.community = community()
            self.deck = deck()
            os.system('cls||clear')
            #User-interface
            img = ImageTk.PhotoImage(Image.open("curtain.png").resize((800, 600)))
            label = Label(root, image = img)
            label.image = img
            label.place(x=0, y=0)
            root.update()

            print("-----------Game %s Start------------"%(round+1))
            Label(root, text="Game %s\t"%(round+1), font=("Arial", 24)).place(x=20, y=20)
            root.update()

            self.round_1()
            time.sleep(2)
            self.round_2()
            self.round2_result()
            time.sleep(1)
            round += 1
            for p in self.players.items():
                p[1].cards = []
                p[1].bet1 = 0
                if p[1].state == "u" and p[1].out == True:
                    self.gamerun = False
                    print('You broke.!!! You broke.!!! You broke.!!!')
            if self.gamerun:
                self.gamerun = self.user_input("continue",1)
        print("-----------GAME ENDS-----------")
        maxmoney = max([p[1].money for p in self.players.items()])
        bigwin = [p[0] for p in self.players.items() if p[1].money == maxmoney]
        print("The winner of the entire game is %s." %bigwin)
        print("He has $%s." %maxmoney)
        
    #Round 1 includes two different random cards for each players, and three random cards for community cards.
    def round_1(self):
        print("-----------Round 1-----------")
        Label(root, text="Round 1", font=("Arial", 24)).place(x=160, y=20)
        root.update()

        botIdx = 1
        for p in self.players.items():
            if p[1].state == "u":
                print("%s: drawing"%p[0])
                for j in range(2):
                    cardDrawn = self.deck.draw()
                    displayCard(cardDrawn, 350+j*70, 430)
                    p[1].cards.append(cardDrawn)
                    time.sleep(0.5)
                print("Done !")
            elif p[1].state == "b":
                #When players do not choose to fold or they still have money to play. They will receive two hand cards.
                p[1].fold = False
                if p[1].out == False:
                    print("%s: drawing"%p[0])
                    for j in range(2):
                        cardDrawn = self.deck.draw()
                        if botIdx == 1:
                            displayCard("B", 20+j*70, 280)
                        if botIdx == 2:
                            displayCard("B", 350+j*70, 110)
                        if botIdx == 3:
                            displayCard("B", 650+j*70, 280)
                        p[1].cards.append(cardDrawn)
                        time.sleep(0.5)
                    botIdx += 1
                    print("Done !")
                    ###print("%s:%s"%(p[0],p[1].cards))
                #Otherwise they are out.
                else:
                    print("%s:%s"%(p[0]," OUT"))
                #Showing three community cards in the first round of each game.
        print("\nCommunity Cards: ")
        for i in range(3):
            time.sleep(0.5)
            card = self.deck.draw()
            displayCard(card, 230+i*70, 280)
            self.community.cards.append(card)
            print(card)
        print("\n")
        print("----------- Waiting for fold/bet/check -----------")
        
        for p in self.players.items():
            #Players will choose to fold if they do not meet the threshold.
            if p[1].state == "u":
                p = self.user_input("fold/bet",p)
            elif p[1].state == "b":
                if p[1].out == False:
                    p[1].rank = rank_determined(p[1].cards + self.community.cards)
                    if p[1].rank[0] > p[1].threshold:
                        p[1].fold = True

        #Conditions for bet.       
        playerAction = ""
        botsAction = []
        for p in self.players.items():
            if p[1].state == 'u':
                if p[1].out == False and p[1].fold == False:
                    p[1].bet1 = self.user_input("betvalue",p)
                    os.system('cls||clear')
                    print("----------- Round 1 table state -----------")
                    print("%s: bet $%s "%(p[0],p[1].bet1))
                    playerAction = "%s: bet $%s "%(p[0],p[1].bet1)
                elif p[1].out == False and p[1].fold == True:
                    os.system('cls||clear')
                    print("----------- Round 1 table state -----------")
                    print("You FOLD")
                    playerAction = "You FOLD           "
                    p[1].bet1 = 0
                else:
                    os.system('cls||clear')
                    print("----------- Round 1 table state -----------")
                    print("You BROKE")
                    playerAction = "You BROKE          "
            elif p[1].state == 'b':
                if p[1].out == False and p[1].fold == False:
                    p[1].bet1 = p[1].threshold - p[1].rank[0] +1
                    print("%s: bet $%s "%(p[0],p[1].bet1))
                    botsAction.append("%s: bet $%s "%(p[0],p[1].bet1))
                elif p[1].out == False and p[1].fold == True:
                    print("%s:%s"%(p[0]," FOLD"))
                    botsAction.append("%s:%s"%(p[0]," FOLD"))
                    p[1].bet1 = 0
                else:
                    print("%s:%s"%(p[0]," BROKE"))
                    botsAction.append("%s:%s"%(p[0]," BROKE"))
        if playerAction[0] == "U":
            Label(root, text=playerAction[6:], font=("Arial", 16)).place(x=350, y=520)
        else:
            Label(root, text=playerAction, font=("Arial", 16)).place(x=350, y=520)
        for bot in botsAction:
            if bot[4] == "1":
                Label(root, text=bot[7:], font=("Arial", 16)).place(x=20, y=370)
            elif bot[4] == "2":
                Label(root, text=bot[7:], font=("Arial", 16)).place(x=350, y=200)
            elif bot[4] == "3":
                Label(root, text=bot[7:], font=("Arial", 16)).place(x=650, y=370)
        root.update()

    # Round two will generate two new random cards for each players, and add two random cards to the previous community cards.
    def round_2(self):
        print("-----------Round 2-----------")
        Label(root, text="Round 2", font=("Arial", 24)).place(x=160, y=20)
        root.update()

        #Adding extra two community cards.
        print("Drawing...")
        for i in range(2):
            time.sleep(1)
            card = self.deck.draw()
            displayCard(card, 440+i*70, 280)
            self.community.cards.append(card)
        print("Community Cards: %s"%self.community.cards)
        
        #The condition for if the players still have money but choose to fold.
        for p in self.players.items():
            time.sleep(0.5)
            if p[1].state == "u":
                p[1].rank = sevencards_determined(p[1].cards + self.community.cards)
                if p[1].fold == False:
                    self.user_input("fold/bet",p)
            elif p[1].state == "b":
                if p[1].out == False:
                    p[1].rank = sevencards_determined(p[1].cards + self.community.cards)
                    if p[1].rank[0] > p[1].threshold:
                        p[1].fold = True
        self.winner = get_winner({p[0]:p[1].rank for p in self.players.items() if p[1].out == False and p[1].fold == False})
        
        #Conditions for bet.
        playerAction = ""
        botsAction = []
        for p in self.players.items():
            if p[1].state == "u":
                if p[1].out == False and p[1].fold == False:
                    p[1].bet2 = self.user_input("betvalue",p)
                    os.system('cls||clear')
                    print("----------- Round 2 table state -----------")
                    if p[1].bet1+p[1].bet2 < p[1].money:
                        print("%s: bet $%s "%(p[0],p[1].bet1+p[1].bet2))
                        playerAction = "bet $%s "%(p[1].bet1+p[1].bet2)
                    else:
                        print("%s: all in "%p[0])
                        playerAction = "all in        "
                elif p[1].out == False and p[1].fold == True:
                    os.system('cls||clear')
                    print("----------- Round 2 table state -----------")
                    print("%s:%s"%(p[0]," FOLD"))
                    playerAction = "FOLD              "
                    p[1].bet2 = 0
                else:
                    os.system('cls||clear')
                    print("----------- Round 2 table state -----------")
                    print("%s:%s"%(p[0]," BROKE"))
                    playerAction = "BROKE             "
            elif p[1].state == "b":
                if p[1].out == False and p[1].fold == False:
                    p[1].bet2 = p[1].threshold - p[1].rank[0] +1
                    print("%s: bet $%s "%(p[0],p[1].bet2))
                    botsAction.append("%s: bet $%s "%(p[0],p[1].bet2))
                elif p[1].out == False and p[1].fold == True:
                    print("%s:%s"%(p[0]," FOLD"))
                    botsAction.append("%s:%s"%(p[0]," FOLD"))
                    p[1].bet2 = 0
                else:
                    print("%s:%s"%(p[0]," BROKE"))
                    botsAction.append("%s:%s"%(p[0]," BROKE"))
        Label(root, text=playerAction, font=("Arial", 16)).place(x=350, y=520)
        for bot in botsAction:
            if bot[4] == "1":
                Label(root, text=bot[7:], font=("Arial", 16)).place(x=20, y=370)
            elif bot[4] == "2":
                Label(root, text=bot[7:], font=("Arial", 16)).place(x=350, y=200)
            elif bot[4] == "3":
                Label(root, text=bot[7:], font=("Arial", 16)).place(x=650, y=370)
        root.update()

    #Final results: who wins the game, how much money does each player get.
    def round2_result(self):
        print("-----------Game Result-----------")
        print("Winner: %s" %self.winner)
        bonus = 0
        for winner in self.winner:
            if winner[0] == "U":
                #player is winner
                Label(root, bg="green", text="WINNER", font=("Arial", 24)).place(x=350, y=430)
            else:
                if winner[4] == "1":
                    #Bot 1 is winner
                    Label(root, bg="green", text="WINNER", font=("Arial", 24)).place(x=20, y=280)
                if winner[4] == "2":
                    #Bot 2 is winner
                    Label(root, bg="green", text="WINNER", font=("Arial", 24)).place(x=350, y=110)
                if winner[4] == "3":
                    #Bot 3 is winner
                    Label(root, bg="green", text="WINNER", font=("Arial", 24)).place(x=650, y=280)
        root.update()

        for p in self.players.items():
            if p[0] not in self.winner:
                if p[1].bet1 + p[1].bet2 >= p[1].money:
                    bonus += p[1].money
                    p[1].money = 0
                    p[1].out = True
                else:
                    ### Subtract the amount from those who lose
                    p[1].money -= p[1].bet1 + p[1].bet2
                    ### Update the total money
                    bonus += p[1].bet1 + p[1].bet2

        ### Winner receives money from other players who lose.
        for h in self.winner:
            self.players[h].money += bonus/len(self.winner)
        money = []
        for p in self.players.items():
            print("%s: $%s "%(p[0],p[1].money))
            money.append("%s: $%s "%(p[0],p[1].money))
        for p in money:
            if p[0] == "U":
                Label(root, text="Player: $"+p[7:], font=("Arial", 16)).place(x=350, y=400)
            else:
                if p[4] == "1":
                    Label(root, text=p+"   ", font=("Arial", 16)).place(x=20, y=250)
                if p[4] == "2":
                    Label(root, text=p+"   ", font=("Arial", 16)).place(x=350, y=80)
                if p[4] == "3":
                    Label(root, text=p+"   ", font=("Arial", 16)).place(x=650, y=250)
        root.update()

###This class is for setting up players, the money they have, how much they bet, hand cards and their corresponding ranks.
## Setting up the initial conditions for "Fold"(Below the threshold and will quit the current game) and "BROKE"
# (Quit the entire game) are False.
class player:
    def __init__(self,state):
        self.state = state
        self.cards = []
        self.money = 10
        self.bet1 = 0
        self.bet2 = 0
        self.rank = 0
        self.out = False
        self.fold = False
        self.threshold = random.randint(7,9) ### random threshold between 7 to 9.

#This class is for setting up the community cards.
class community:
    def __init__(self):
        self.cards = []

#This class is for setting up a deck of cards and randomly draw the cards.
class deck:

    def __init__(self):
        suit = ["C","S","H","D"]
        value = [str(i) for i in range(1,14)]
        self.cards = [a+b for a in suit for b in value]
        
    def draw(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card

#All the user interactions
def gamecommand():
    #User mode
    args = sys.argv
    args = args[1:]
    if len(args) == 0:
        print("please pass an command: you have the following option:\n")
        print("------- 1. User mode #python ***.py -u # --------")
        print("------- 2. File mode #python ***.py -f # --------")
    else:
        args_list = [a for a in args]
        if "-u" in args_list:
            try:
                if args_list.index("-p") == 1:
                    try:
                        botnum = args_list[2]
                        usergame = game(int(botnum))
                        usergame.game_start()
                    except IndexError:
                        print("please pass an correct command, you have the following option:\n")
                        print("------- 1. User mode #python ***.py -u -p (number of bots)# -------")
                        print("------- example: python ***.py -u -p 3 -------")
                        print("------- 2. File mode #python ***.py -f -i path_to_test_cases_directory -------")  
                        print("------- example: python ***.py -f -i /Users/yanlin/Desktop/PA3/test_cases -------")  
            except ValueError:
                print("please pass an correct command, you have the following option:\n")
                print("------- 1. User mode #python ***.py -u -p (number of bots)# -------")
                print("------- example: python ***.py -u -p 3 -------")
                print("------- 2. File mode #python ***.py -f -i path_to_test_cases_directory -------")  
                print("------- example: python ***.py -f -i /Users/yanlin/Desktop/PA3/test_cases -------")  
        #File mode (This is not related to the GUI)                  
        elif "-f" in args_list:
            if "-i" in args_list:
                if len(args_list) == 3:
                    filedict = {}
                    for root, dirs, files in os.walk(args_list[2], topdown=False):
                        for name in files:
                                if name.find(".txt") != -1:
                                    filepath = os.path.join(root, name)
                                    with open(filepath) as f:
                                        contents = f.readlines()
                                        for i in range(len(contents)):
                                            contents[i] = contents[i][:-1].split(",")
                                        contents = {c[0]:rank_determined(c[1:]) for c in contents}
                                    filedict[name] = contents

                    testresult = {}
                    for test in filedict.items():
                        testresult[test[0]] = get_winner(test[1])[0]

                    with open('test_results.txt') as f:
                        result_contents = f.readlines()
                        passes = 0
                        for i in range(len(result_contents)):
                            time.sleep(0.2)
                            result_contents[i] = result_contents[i][:-1].split(",")
                            if testresult[result_contents[i][0]] == result_contents[i][1]:
                                passes += 1
                            else:
                                print("%s not pass!"%result_contents[i][0])
                                print("Code winner: ",testresult[result_contents[i][0]]," Actual winner:",result_contents[i][1])
                        print("Pass rate is: %s"%((passes/len(result_contents))*100) + '%')
                        print("The number of tests passed are %s"%passes + ", Total Tests = 51")

            elif "-i" not in args_list:
                raise ValueError("Please check if \'-i\' is in the command.")
        else:
            print("please pass an correct command, you have the following option:\n")
            print("------- 1. User mode #python ***.py -u -p (number of bots)# -------")
            print("------- example: python ***.py -u -p 3 -------")
            print("------- 2. File mode #python ***.py -f -i path_to_test_cases_directory -------")  
            print("------- example: python ***.py -f -i /Users/yanlin/Desktop/PA3/test_cases -------")

if __name__ == "__main__":
    root = Tk()
    initTk(10, 10, 10, 10)
    gamecommand()

