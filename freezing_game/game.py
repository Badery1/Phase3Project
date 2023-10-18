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
    name = input("\x1b[32m" + "Enter new player name: " + "\x1b[0m")
    if len(name) <= 2:
            print("\nPlease enter a name with 3 or more letters.")
            session.close()
            return
    elif len(name) > 12:
        print("\nPlease enter a name with 12 letters or less.")
        session.close()
        return
    existing_player = session.query(Player).filter_by(name=name).first()
    if existing_player:
        print(f"\nPlayer named {name} already exists! Please choose a different name.")
        session.close()
        return
    new_player = Player(name=name)
    session.add(new_player)
    session.commit()
    print(f"\nPlayer {name} created!")
    session.close()

def delete_player():
    session = get_session()
    player_id = get_int_input("\x1b[32m" + "Enter *YOUR* player ID to delete: " + "\x1b[0m")
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
    player_id = int(input("\x1b[32m" + "Enter player ID to find: " + "\x1b[0m"))
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
       print("\x1b[31m" + r"""

                                                                                                            _                                        
 \_/ _        |_   _   _.  _|   |_   _.  _ |    o ._ _|_  _    _|_ |_   _          _. ._ ._ _ _|_ |_     _ _|_   _|_ |_   _     _  _. |_  o ._        
  | (_) |_|   | | (/_ (_| (_|   |_) (_| (_ |<   | | | |_ (_)    |_ | | (/_   \/\/ (_| |  | | | |_ | |   (_) |     |_ | | (/_   (_ (_| |_) | | | o o o 
                                                                                                                                                      
 
""" + "\x1b[0m")
        
    else:
        print("\x1b[34m" + r"""
                                                                                                                   
 \_/ _        |_   _   _.  _|    _     _|_   o ._ _|_  _    _|_ |_   _    |_  o _|_ _|_  _  ._    _  _  |  _|       
  | (_) |_|   | | (/_ (_| (_|   (_) |_| |_   | | | |_ (_)    |_ | | (/_   |_) |  |_  |_ (/_ |    (_ (_) | (_| o o o 
                                                                                                                    
""" + "\x1b[0m")

    time.sleep(2)

def play_game():
    session = get_session()
    player_id = int(input("\x1b[32m" + "Enter *YOUR* player ID to play: " + "\x1b[0m"))
    player = session.query(Player).filter_by(id=player_id).first()

    if not player:
        print("\nPlayer not found!")
        session.close()
        return

    elif player.alive == False:
        print("\nThis player is dead!")
        session.close()
        return

    if player.days_survived == 0:
        print("\nThe world as you know it has ended. A violent ice age took the world by storm, and you are left alone stranded at an abandoned campsite.")
        time.sleep(2)
        print("\nAs the blizzard clears momentarily, you see it - an old, abandoned cabin. With no other shelter in sight, you decide to take refuge. This, is where you will survive.")
        time.sleep(3)
        print("\nThe door creaks as you enter, the gusting wind dying down behind you. The cabin is cold, almost as cold as the outside. You'll need to find firewood to burn if you're to have any hope of surviving this icy nightmare.")
        time.sleep(3)
        print("\nHow to survive:")
        print("- The temperature drops each day.")
        print("- Gather firewood outside to keep warm.")
        print("- You have a limited number of attempts to gather wood each day.")
        print("- Once inside the cabin, burn the wood to increase temperature.")
        time.sleep(3)
        print("\nWith those thoughts, you prepare yourself for the challenging days ahead.")
        time.sleep(2)

    print(f"\nPlaying as {player.name}.")
    
    while True:
        if player.inside_cabin:
            print("\033[91m" + """
            You are currently inside the cabin...     
                    |      |        ,---------,
                    J.    .B        |r'''|'''Y|
                   /  *'.*  \       ||   |   ||
                  /          \      ||===|===||
                 /.-       -.-\     ||   |   ||
                / |-|_    _/-/ \    |L.__|__.J|
               /  ())_)  (_()    \  '---------'
            _________________________
             -__LLLLLLLLLLLLLLLLL__-
              \|#/#############\#|/
              \|##/           \##|/
              \|#|  )  ) ( ) ) |#|/
              \|#|  ( ( ()((   |#|/
              \|#|   /\__\_(-  |#|/
 _____________\|#| _(\/L/(\/)_ |#|/_____________
              \|#|-.-.-.-.-.-.-|#|/         
               '''             ''' 
    """ + "\033[0m")
            print("\033[91m" + r"""
  _____           _     _         _____      _     _         __  __                  
 |_   _|         (_)   | |       / ____|    | |   (_)       |  \/  |                 
   | |  _ __  ___ _  __| | ___  | |     __ _| |__  _ _ __   | \  / | ___ _ __  _   _ 
   | | | '_ \/ __| |/ _` |/ _ \ | |    / _` | '_ \| | '_ \  | |\/| |/ _ | '_ \| | | |
  _| |_| | | \__ | | (_| |  __/ | |___| (_| | |_) | | | | | | |  | |  __| | | | |_| |
 |_____|_| |_|___|_|\__,_|\___|  \_____\__,_|_.__/|_|_| |_| |_|  |_|\___|_| |_|\__,_|
        """ + "\033[0m")
            print("\x1b[31m" + "*************************************" + "\x1b[0m")
            print("\x1b[31m" + "*                                   *" + "\x1b[0m")
            print("\x1b[31m" + "* 1. Burn logs                      *" + "\x1b[0m")
            print("\x1b[31m" + "* 2. Burn All logs                  *" + "\x1b[0m")
            print("\x1b[31m" + "* 3. Pass the day                   *" + "\x1b[0m")
            print("\x1b[31m" + "* 4. Check temperature and logs     *" + "\x1b[0m")
            print("\x1b[31m" + "* 5. Leave cabin                    *" + "\x1b[0m")
            print("\x1b[31m" + "* 6. Exit game                      *" + "\x1b[0m")
            print("\x1b[31m" + "*                                   *" + "\x1b[0m")
            print("\x1b[31m" + "*************************************" + "\x1b[0m")
            
        else:
            print("\033[34m" + """
            You are currently outside the cabin...     
      ...   *         * ..   ...                        *
 *      ...        *           *            *
          ...               ...                          *
            ..                            *
    *        ..        *                       *
           __##______              *                      *
  *    *  /  ##  ****                   *
         /        ****               *         *  X   *
   *    /        ******     *                    XXX      *
       /___________*****          *             XXXXX
        |            ***               *       XXXXXXX   X
    *   | ___        |                    *   XXXXXXXX  XXX
  *     | | |   ___  | *       *             XXXXXXXXXXXXXXX
        | |_|   | |  ****             *           X   XXXXXXX
    *********** | | *******      *                X      X
************************************************************
    """ + "\033[0m")
            print("\033[34m" + r"""
   ____        _       _     _         _____      _     _         __  __                  
  / __ \      | |     (_)   | |       / ____|    | |   (_)       |  \/  |                 
 | |  | |_   _| |_ ___ _  __| | ___  | |     __ _| |__  _ _ __   | \  / | ___ _ __  _   _ 
 | |  | | | | | __/ __| |/ _` |/ _ \ | |    / _` | '_ \| | '_ \  | |\/| |/ _ | '_ \| | | |
 | |__| | |_| | |_\__ | | (_| |  __/ | |___| (_| | |_) | | | | | | |  | |  __| | | | |_| |
  \____/ \__,_|\__|___|_|\__,_|\___|  \_____\__,_|_.__/|_|_| |_| |_|  |_|\___|_| |_|\__,_|
        """ + "\033[0m")
            print("\x1b[36m" + "*************************************" + "\x1b[0m")
            print("\x1b[36m" + "*                                   *" + "\x1b[0m")
            print("\x1b[36m" + "* 1. Gather firewood                *" + "\x1b[0m")
            print("\x1b[36m" + "* 2. Check temperature and logs     *" + "\x1b[0m")
            print("\x1b[36m" + "* 3. Enter cabin                    *" + "\x1b[0m")
            print("\x1b[36m" + "* 4. Exit game                      *" + "\x1b[0m")
            print("\x1b[36m" + "*                                   *" + "\x1b[0m")
            print("\x1b[36m" + "*************************************" + "\x1b[0m")

        choice = input("\x1b[32m" + "Enter your choice: " + "\x1b[0m")

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
        print("\x1b[34m" + r"""
   *                         *                       
 (  `                      (  `                      
 )\))(      )  (           )\))(     (           (   
((_)()\  ( /(  )\   (     ((_)()\   ))\  (      ))\  
(_()((_) )(_))((_)  )\ )  (_()((_) /((_) )\ )  /((_) 
|  \/  |((_)_  (_) _(_/(  |  \/  |(_))  _(_/( (_))(  
| |\/| |/ _` | | || ' \)) | |\/| |/ -_)| ' \))| || | 
|_|  |_|\__,_| |_||_||_|  |_|  |_|\___||_||_|  \_,_| 
                                                     

        """ + "\x1b[0m")

        print("\x1b[31m" + "*******************************" + "\x1b[0m")
        print("\x1b[31m" + "* 1. Create player            *" + "\x1b[0m")
        print("\x1b[31m" + "* 2. Delete player            *" + "\x1b[0m")
        print("\x1b[31m" + "* 3. Display all players      *" + "\x1b[0m")
        print("\x1b[31m" + "* 4. Find player by ID        *" + "\x1b[0m")
        print("\x1b[31m" + "* 5. Leaderboard              *" + "\x1b[0m")
        print("\x1b[31m" + "* 6. Play game                *" + "\x1b[0m")
        print("\x1b[31m" + "* 7. Exit                     *" + "\x1b[0m")
        print("\x1b[31m" + "*******************************" + "\x1b[0m")

        choice = input("\x1b[32m" + "Enter your choice: " + "\x1b[0m")

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
