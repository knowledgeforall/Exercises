from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players={1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
         3:{"roundtotal":0,"gametotal":0,"name":""},
        }

global roundNum
roundNum = 1
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""

def readDictionaryFile():
    global dictionary
    # Read dictionary file in from dictionary file location
    dict = open('dictionary.txt', 'r')
    dictionary = dict.readlines()
    dict.close()
    
    # Store each word in a list.
    global dictionaryList
    dictionaryList = []
    for newline in dictionary:
        dictionaryList.append(newline.rstrip())

def readTurnTxtFile():
    global turntext   
    #read in turn intial turn status "message" from file
    turn = open('turntext.txt', 'r')
    turntext = turn.readlines()
    turn.close()

def readFinalRoundTxtFile():
    global finalroundtext   
    #read in turn intial turn status "message" from file
    final = open('finalround.txt', 'r')
    finalround = final.readlines()
    final.close()

def readRoundStatusTxtFile():
    global roundstatus
    # read the round status  the Config roundstatusloc file location
    round = open('roundstatus.txt', 'r')
    roundstatus = round.readlines()
    round.close()
    
def readWheelTxtFile():
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location
    wheel = open('wheeldata.txt', 'r')
    wheellist = wheel.readlines()
    wheel.close()
    
def getPlayerInfo():
    global players
    # read in player names from command prompt input
    count = 1
    while count < 3:
        for name in range (3):
            players[count] = {}
            playerName = str(input("Player {}, please enter your name: ".format (count)))
            players[count]["roundtotal"] = 0
            players[count]["gametotal"] = 0
            players[count]["name"] = playerName
            count = count + 1
    
def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
    global roundNum
        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile()
    wofRoundSetup()
    roundNum = 1
    
def getWord():
    global dictionary
    global roundWord
    global roundUnderscoreWord
    #choose random word from dictionary
    roundWord = random.choice(dictionary).rstrip()
    print(roundWord)
    
    #make a list of the word with underscores instead of letters.
    roundUnderscoreWord = list(roundWord)
    count = 0
    for letter in range(len(roundWord)):
        roundUnderscoreWord[count] = "_"
        count = count + 1
        
    wofTurn(initPlayer)
        
def wofRoundSetup():
    global players
    global blankWord
    global initPlayer
    global roundNum
    global initPlayer

    # Return the starting player number (random)
    initPlayer = random.choice(list(players))

    # Use getWord function to retrieve the word and the underscore word (blankWord)
    getWord()
    blankWord = tuple(roundUnderscoreWord)
    for underscore in blankWord:
        blankWord = print(underscore + " ", end='')
    return initPlayer

def round2Setup():
    global roundNum
    global initPlayer
    
    #add round total to game total
    # Set round total for each player = 0
    count = 1
    for roundtotal in range (3):
        players[count]["gametotal"] = players[count]["gametotal"] + players[count]["roundtotal"]
        players[count]["roundtotal"] = 0
        print("-----------------")
        print("{}, your game total is {}.".format(players[count]["name"], players[count]["gametotal"]))
        print("-----------------")
        count = count + 1
        
    roundNum = roundNum + 1
    if roundNum <= 2:
        
       
        # Return the starting player number (random)
        initPlayer = random.choice(list(players))
        
        # Use getWord function to retrieve the word and the underscore word (blankWord)
        getWord()
        blankWord = tuple(roundUnderscoreWord)
        for underscore in blankWord:
            blankWord = print(underscore + " ", end='')

        getPlayer()
        
    else:
        wofFinalRound()
        
    return initPlayer

def getPlayer():
    global initPlayer
    global stillinTurn
    
    if initPlayer == 1:
        initPlayer = 2
    elif initPlayer == 2:
        initPlayer = 3
    else:
        initPlayer = 1
        
    wofTurn(initPlayer)

def spinWheel(playerNum):
    global wheellist
    global players
    global vowels
    global initPlayer
    global letterguess
    global currentAmount
    global goodGuess
    global randomWheelValue
    randomWheelValueInt = 0
    
    # Get random value for wheellist
    randomWheelValue = random.choice(wheellist)
    randomWheelValue = randomWheelValue.strip()
    
    # Check for bankrupcy, and take action.
    if randomWheelValue == "Bankrupt":
        players[initPlayer]["roundtotal"] = 0
        
    # Check for lose turn
    if randomWheelValue == "Lose A Turn":
        print("Sorry, your turn is over.")
        getPlayer()
           
    # Get amount from wheel if not lose turn or bankruptcy
    if randomWheelValue not in ("Bankrupt", "Lose A Turn"):
        randomWheelValueInt == int(randomWheelValue)
        print("The wheel lands on {}.".format(randomWheelValue))
        stillinTurn = True
        
        # Ask user for letter guess
        letterguess = str(input("Player {}, please enter your letter guess: ".format(initPlayer)))

        # Use guessletter function to see if guess is in word, and return count
        letter = letterguess
        playerNum = initPlayer
        guessletter(letter, playerNum)
        
        # Change player round total if they guess right.
            
        
        return stillinTurn
        
def guessletter(letter, playerNum): 
    global players
    global blankWord
    global stillinTurn
    global goodGuess
    global vowels
    global vowelGuess
    # parameters:  take in a letter guess and player number
    global letterguess
    global initPlayer
   
    # ensure letter is a consonate.
    vowelGuess = False
    for vowel in vowels:
        if letterguess == vowel:
            vowelGuess = True

    if vowelGuess == True:
        print("That is a vowel. You must choose a consanant")
        goodGuess = False
        
    # Change position of found letter in blankWord to the letter instead of underscore
    if vowelGuess == False:
        goodGuess = False
        for letter in range(len(roundWord)):
            if list(roundWord)[letter] == letterguess:
                roundUnderscoreWord[letter] = letterguess
                # return goodGuess= true if it was a correct guess
                goodGuess = True

    if goodGuess == True:
        print('Correct!')
        # Change player round total if they guess right.
        players[initPlayer]["roundtotal"] = players[initPlayer]["roundtotal"] + int(randomWheelValue)
        wofTurn(initPlayer)
        
    if goodGuess == False:
        print("Sorry, that is not correct.")
        getPlayer()
        
    wofTurn(initPlayer)

    
    return initPlayer

def buyVowel(playerNum):
    global players
    global vowels
    global goodGuess
    vowelChoice = False
    # Take in a player number
    global initPlayer
    # Ensure player has 250 for buying a vowelcost
    enoughCash = True
    vowelGuess = False
    
    if players[initPlayer]["roundtotal"] < 250:
        print("You do not have enough to buy a vowel")
        enoughCash = False
        wofTurn(initPlayer)
    
    while vowelGuess == False:
        if enoughCash == True:
            boughtVowel = str(input("Player {}, please enter the vowel you would like to buy: ".format(initPlayer)))

        # Ensure letter is a vowel
        vowelGuess = True
        for vowel in vowels:
            if boughtVowel == vowel:
                vowelGuess == True
            else:
                vowelGuess == False

        if vowelGuess == True:
            for letter in range(len(roundWord)):
                if list(roundWord)[letter] == boughtVowel:
                    roundUnderscoreWord[letter] = boughtVowel
                    # return goodGuess= true if it was a correct guess
                    vowelChoice = True
                    players[initPlayer]["roundtotal"] = players[initPlayer]["roundtotal"] - 250
        print(''.join(roundUnderscoreWord))
        print("The board is currently showing {} and your round total is {}".format((''.join(roundUnderscoreWord)), players[initPlayer]["roundtotal"]))

        if vowelGuess == False:
            print("Sorry, that is not a vowel. Please try again.")
            getPlayer()
        
    wofTurn(initPlayer)

def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    global roundNum
    
    # Take in player number
    global initPlayer
    
    # Ask for input of the word and check if it is the same as wordguess
    guessWordInput = str(input("Enter your word guess: "))
    
    # Fill in blankList with all letters, instead of underscores if correct
    if guessWordInput == roundWord:
        print("The word {} is correct!".format(roundWord))
        stillinTurn = False
        round2Setup()
        
    else:
        print("Sorry, that is incorrect.")
        getPlayer()

def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players
    global initPlayer
    global roundNum
    global stillinTurn
    
    guessedWord = False
    # take in a player number.
    global initPlayer
    global roundNum
    # use the string.format method to output your status for the round
    if roundNum <= 2:
        print("-----------------")
        print("Round {}".format(roundNum))
        print("{}".format(players[initPlayer]["name"]))
        print("The board is currently showing {} and your round total is {}".format((''.join(roundUnderscoreWord)), players[initPlayer]["roundtotal"]))
        
        # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
        choice = str(input("What would you like to do? Input 'S' for spin, 'B' for buy vowel, or 'G' for guess the word: "))
        
        # Keep doing all turn activity for a player until they guess wrong
        # Do all turn related activity including update roundtotal 
        
        stillinTurn = True
        while stillinTurn:
            # Check to see if the word is solved, and return false if it is,
            if guessedWord == True:
                return False
            # use the string.format method to output your status for the round
            # Get user input S for spin, B for buy a vowel, G for guess the word
                    
            if(choice.strip().upper() == "S"):
                stillinTurn = spinWheel(playerNum)
            elif(choice.strip().upper() == "B"):
                stillinTurn = buyVowel(playerNum)
            elif(choice.upper() == "G"):
                stillinTurn = guessWord(playerNum)
            else:
                print("Not a correct option")
                wofTurn(initPlayer)
            
def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    global playerNum
    initPlayer = wofRoundSetup()
    playerNum = initPlayer
    
    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
        # Use the wofTurn fuction to dive into each players turn until their turn is done.

def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    global finalRound
    finalRound = True
    winplayer = 0
    amount = 0
    # Find highest gametotal player.  They are playing.

count = 1
highScore = 0
winplayer = 0
for score in players:
    score = players[count]["gametotal"]
    if score > highScore:
        highScore = score
        winplayer = count
    count = count + 1

    # Print out instructions for that player and who the player is.
    print("Player {}, you're going to the final round!".format(winplayer))
    print("-----------------")
    print("This is the Final Round!")
    
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    getWord()
    
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    #for loop
    
    finalLetterSet = {'r','s','t','l','n','e'}
    
    for letter in finalLetterSet:
        guessletter(letter, winplayer)
    
    
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    print(roundUnderscoreWord)
    
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    consonantCount = 0
    while consonantCount < 3:
        letterguess = str(input("Enter a consonant: "))
        consonantCount = consonantCount + 1
    letterguess = str(input("Enter a vowel: "))    
    # Print out the current blankWord again
    print(blankWord)
    
    # Get user to guess word
    
    # If they do, add finalprize and gametotal and print out that the player won 

def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()