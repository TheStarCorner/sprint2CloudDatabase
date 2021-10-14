import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)
def initialize_firestore():


    # Setup Google Cloud Key - The json file is obtained by going to
    # Project Settings, Service Accounts, Create Service Account, and then
    # Generate New Private Key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gameproject-c94a1-firebase-adminsdk-bffc2-788c6a95ce.json"
    # Use the application default credentials. The projectID is obtianed
    # by going to Project Settings and then General.
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
    'projectId': 'gameproject-c94a1',
    })
    # Get reference to database
    db = firestore.client()
    return db
def add_game(db):
    # This code below is adding a game to the cloud database (Name, score, hours played, and if the game was finished or not.)
    nameOfGame = input("Enter the name of the game: ")
    hoursPlayed = float(input("How many hours have you played of it?: "))
    gameFinished = input("Did you finish the game? (y/n): " ) in ['Y,','y']
    gameScore = float(input("On a scale from 1-10, what would you rate this game?: "))
    

    # This should check if the game is on the list already or not.
    addedGameCheck = db.collection("games").document(nameOfGame).get()
    data = addedGameCheck.to_dict()
    print(data)

    # Below is a dictionary of all of the values of the game data for the database.
    gameData = {"nameOfGame": nameOfGame,
                "hoursPlayed": hoursPlayed,
                "gameFinished": gameFinished,
                "gameScore": gameScore}
    db.collection("games").document(nameOfGame).set(gameData)

    log_transaction(db, f"You have added the game, {nameOfGame} , with {hoursPlayed} hours played , and you gave it a {gameScore} out of 10.")

def checkGameList(db):
    print("Select Query")
    print("1.) List one game")
    print("2.) List all games")
    print("3.) List all games that are finished")
    print("4.) List all games that are not finished")
    selection = input("> ")

    print()

    if selection == "1":
        # This displays the single game, Splatoon 2
        selections = db.collection("games").document("Splatoon 2").get()
        showSelect = selections.to_dict()
        print(showSelect)

    elif selection == "2":
        #This lists all games from the database. 
        results = db.collection("games").get()
        for result in results:
            show_result = result.to_dict()
            print(show_result)

    elif selection == "3":
        # Displays all finished games
        results = db.collection("games").where("gameFinished", "==", True).get()
        for result in results:
            show_result = result.to_dict()
            print(show_result)

    elif selection == "4":
        # Displays unfinished games
        results = db.collection("games").where("gameFinished", "==", False).get()
        for result in results:
            show_result = result.to_dict()
            print(show_result)

def deleteGame(db):
    # Deletes a single game from the cloud database.
    results = db.collection("games").document("nameOfGame").get()
    print(results)
    delete = input("What game do you want to remove?: ")

    for results in delete:
        db.collection("games").document(delete).delete()
        print(f"You have deleted the game, {delete} from the list.")
        break

def editGame(db):

    # Edits a single game's information in the field section of the database.
    editGameInfo = input("What game do you want to edit?: ")
    editScore = input(f"You have chosen the game {editGameInfo} , what would you score it now?: ")
    print(f"You have changed the score to {editScore} out of 10.")
    print()
    editHours = input(f"How many hours do you have in the game, {editGameInfo}?: ")
    print(f"You now have {editHours} in the game, {editGameInfo}.")
    editedGameInfo = db.collection("games").document(editGameInfo).update({
        "gameScore": editScore,
        "hoursPlayed": editHours
    })

def log_transaction(db, message):
    '''
    Save a message with current timestamp to the log collection in the
    Firestore database.
    '''
    # Logs that you added a game with a specific score and the total amount of hours played.
    data = {"message" : message, "timestamp" : firestore.SERVER_TIMESTAMP}
    db.collection("log").add(data)    

def main():
    db = initialize_firestore()
    print(db)
    choice = None
    while choice != "0":
        print()
        print("0) Exit")
        print("1) Add New Game")
        print("2) Check Game Info")
        print("3) Delete a game from the database")
        print("4) Edit Game Information (Hours Played, Score)")
        choice = input(f"> ")
        print()
        if choice == "1":
            add_game(db)
        elif choice == "2":
            checkGameList(db)
        elif choice == "3":
            deleteGame(db)
        elif choice == "4":
            editGame(db)                        

if __name__ == "__main__":
    main()