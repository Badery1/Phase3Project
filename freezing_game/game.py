import time
from models import Player
from database import get_session
import game_mechanics

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def create_player():
    session = get_session()
    name = input("Enter player name: ")
    new_player = Player(name=name)
    session.add(new_player)
    session.commit()
    print(f"\nPlayer {name} created!")
    session.close()

def delete_player():
    session = get_session()
    player_id = get_int_input("Enter player ID to delete: ")
    player = session.query(Player).filter_by(id=player_id).first()

    if not player:
        print("\nPlayer not found!")
        session.close()
        return

    session.delete(player)
    session.commit()
    print(f"\nPlayer {player.name} deleted!")
    session.close()

def display_all_players():
    session = get_session()
    players = session.query(Player).all()
    for player in players:
        print(f"ID: {player.id}, Name: {player.name}, Temperature: {player.temperature}°F, Days Survived: {player.days_survived}")
    session.close()

def find_player_by_id():
    session = get_session()
    player_id = int(input("Enter player ID to find: "))
    player = session.query(Player).filter_by(id=player_id).first()

    if not player:
        print("\nPlayer not found!")
        session.close()
        return
    
    elif player.alive == False:
        print("\nThis player is dead!")
        session.close()
        return

    print(f"ID: {player.id}, Name: {player.name}, Temperature: {player.temperature}°F, Days Survived: {player.days_survived}")
    session.close()

def leaderboard():
    session = get_session()
    players = session.query(Player).order_by(Player.days_survived.desc()).all()
    print("\n--- Leaderboard ---")
    for player in players:
        print(f"{player.name} - Days Survived: {player.days_survived}")
    session.close()

def toggle_cabin_location(player):
    player.inside_cabin = not player.inside_cabin
    if player.inside_cabin:
        print("\nYou head back into the warmth the cabin...")
    else:
        print("\nYou head out into the bitter cold...")
    time.sleep(2)

def play_game():
    session = get_session()
    player_id = int(input("\nEnter player ID to play: "))
    player = session.query(Player).filter_by(id=player_id).first()

    if not player:
        print("\nPlayer not found!")
        session.close()
        return

    elif player.alive == False:
        print("\nThis player is dead!")
        session.close()
        return

    print(f"\nPlaying as {player.name}.")
    
    while True:
        if player.inside_cabin:
            print("\nYou are currently inside the cabin.")
            print("\n--- Inside Cabin Menu ---")
            print("1. Burn logs")
            print("2. Burn All logs")
            print("3. Pass the day")
            print("4. Check temperature and logs")
            print("5. Leave cabin")
            print("6. Exit game")
            
        else:
            print("\nYou are currently outside the cabin.")
            print("\n--- Outside Cabin Menu ---")
            print("1. Gather firewood")
            print("2. Check temperature and logs")
            print("3. Enter cabin")
            print("4. Exit game")

        choice = input("Enter your choice: ")

        if player.inside_cabin:
            if choice == '1':
                game_mechanics.burn_logs(player)
                session.commit()
            elif choice == '2':
                game_mechanics.burn_all_logs(player)
                session.commit()
            elif choice == '3':
                alive = game_mechanics.pass_day(player)
                session.commit()

                if not alive:
                    session.commit()
                    print("\nYou fall asleep...")
                    time.sleep(2)
                    print("...only to never wake.")
                    print("\nGame over!")
                    break
            elif choice == '4':
                print(f"\nTemperature: {player.temperature}°F, Logs: {player.logs}")
            elif choice == '5':
                toggle_cabin_location(player)
                session.commit()
            elif choice == '6':
                break

        else:  # outside the cabin
            if choice == '1':
                game_mechanics.gather_logs(player)
                session.commit()
            elif choice == '2':
                print(f"\nTemperature: {player.temperature}°F, Logs: {player.logs}")
            elif choice == '3':
                toggle_cabin_location(player)
                session.commit()
            elif choice == '4':
                break


def main():
    while True:
        print("\n--- Main Menu ---")
        print("1. Create player")
        print("2. Delete player")
        print("3. Display all players")
        print("4. Find player by ID")
        print("5. Leaderboard")
        print("6. Play game")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_player()

        elif choice == '2':
            delete_player()

        elif choice == '3':
            display_all_players()

        elif choice == '4':
            find_player_by_id()

        elif choice == '5':
            leaderboard()

        elif choice == '6':
            play_game()

        elif choice == '7':
            print("\nTill next time!")
            break

if __name__ == "__main__":
    main()
