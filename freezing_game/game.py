#This code imports necessary modules and files!
import time
from models import Player
from database import get_session
import game_mechanics
import threading
import pygame  

#The variable audio_file stores the name of the audio file to be played.
audio_file = 'game-music.mp3'

# The play_audio function initializes the mixer, loads the audio file, and plays it in a continuous loop.
def play_audio():
    pygame.mixer.init()  # Initialize the pygame mixer
    pygame.mixer.music.load(audio_file)  # Load the audio file
    pygame.mixer.music.play(-1)  # Play the audio in a loop

#The get_int_input function repeatedly prompts the user for input until an integer value is provided.
def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

#The create_player function prompts the user to create a new player by inputting a name, and it performs validation checks before creating the player.
def create_player():
    session = get_session() # Get a database session
    name = input("\x1b[32m" + "Enter new player name: " + "\x1b[0m")# Prompt for a player's name

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
    new_player = Player(name=name)  # Create a new player object
    session.add(new_player)  # Add the new player to the session
    session.commit()  # Commit the changes to the database
    print(f"\nPlayer {name} created!")
    session.close()  # Close the session

#The delete_player function allows the user to delete a player by providing the player's ID.
def delete_player():
    session = get_session()  # Get a database session
    player_id = get_int_input("\x1b[32m" + "Enter *YOUR* player ID to delete: " + "\x1b[0m")  # Prompt for a player's ID
    player = session.query(Player).filter_by(id=player_id).first()  # Query the database for the player

    # Check if the player does not exist
    if not player:
        print("\nPlayer not found!")
        session.close()
        return

    session.delete(player)  # Delete the player from the database
    session.commit()  # Commit the changes to the database
    print(f"\nPlayer {player.name} deleted!")
    session.close()  # Close the session

#The display_all_players function fetches all players from the database and displays their details.
def display_all_players():
    session = get_session()  # Get a database session
    players = session.query(Player).all()  # Query all players from the database
    for player in players:
        print(f"\n\033[1m\033[92mID:\033[0m {player.id}, \033[1m\033[92mName:\033[0m \033[92m{player.name}\033[0m, \033[1m\033[91mTemperature:\033[0m \033[91m{player.temperature}°F\033[0m, \033[1m\033[94mDays Survived:\033[0m \033[94m{player.days_survived}\033[0m")
        time.sleep(2)  # Sleep for 3 seconds to display each player
    session.close()  # Close the session

#The find_player_by_id function allows the user to find a player by their ID and displays the player's details if found.
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
        print("\n\x1b[33m" + r""" This player is dead!
(_;~)                  (~;_)
(   |                  |   )
 ~', ',    ,''~'',   ,' ,'~
     ', ','       ',' ,'
       ',: {'} {'} :,'
         ;   /^\   ;
          ~\  ~  /~
        ,' ,~~~~~, ',
      ,' ,' ;~~~; ', ',
    ,' ,'    '''    ', ',
  (~  ;               ;  ~)
  (-;_)               (_;-)
                    """ + "\x1b[0m")
        session.close()
        return

    print(f"\n\033[1m\033[92mID:\033[0m {player.id}, \033[1m\033[92mName:\033[0m \033[92m{player.name}\033[0m, \033[1m\033[91mTemperature:\033[0m \033[91m{player.temperature}°F\033[0m, \033[1m\033[94mDays Survived:\033[0m \033[94m{player.days_survived}\033[0m")
    time.sleep(3)
    session.close()

#The leaderboard function fetches all players from the database and displays them in descending order based on the number of days survived.
def leaderboard():
    session = get_session()
    players = session.query(Player).order_by(Player.days_survived.desc()).all()
    print("\n--- Leaderboard ---")
    for player in players:
        print(f"{player.name} - Days Survived: {player.days_survived}")
        time.sleep(2)
    session.close()

#The toggle_cabin_location function toggles the player's location between inside and outside the cabin and displays ASCII art accordingly.
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

    time.sleep(5)

# The play_game function allows the user to play the game, interacting with game mechanics based on the player's choices.
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
        print("\n\x1b[36m" + r""" The world as you know it has ended. A violent ice age took the world by storm, and you are left alone stranded at an abandoned campsite.
          -    -  -   -   -       -     -   -  -  -     -   -       -   - 
 -     -    -   -   -    -   -    --   -  -    -      -  )   - -
  - -  -    --  -    -       -     -    -  -  /|   )   (     )  -
-   -      -    -   -   -   -   -   -   -    / -  / (  (   -  - (   - 
_  -      -  -     -    -   -   -   -   -   /   \)  -    -   -  -
 \  -      -      -   -  -  -   -   -   -  |   /  -  .--.     - 
  `-.  -  -   -   -  -   -    -   -  -  -   (  /\    /___ \.-.   
     \ -    -   -   -   -   -   -    -       \/ \\ - |. .|/`-'  -_
     |-     -   -   -   -   -   -    - -   -    (_) __\-/__  - .'
      \    - -  -   -   -   -   -     -  -   - | \\  \:/  )  /
       \-  -  -  -   -  -   -   -     -   - -  \ V\\  :/ / - |
        |   -   -   -   -   -   -   -    --   - `-'\\_/ /)  /
         \    -  -  -   -   -   -     - -  - -   - ((_)/_) /
         |- -   -   -   -   -   -   -   -   - - -  \ \\  / |
         | -    -   -   -   -   -   -    -  -    - |  |  | /
          | -   -   -   -   -    -  -  -  -    -   |__|__| |
           _______________________________________(___V___)'
                    """ + "\x1b[0m")
        time.sleep(5)
        print("\n\x1b[32m" + r""" As the blizzard clears momentarily, you see it - a cabin. With no other shelter in sight, you decide to take refuge. This, is where you will survive.
                                                
                                                         /\
                                               ___      /%%\
                                              |_I_|     /%%\
                   __________________/',______|I_I|____/%%%%\/\
                  /\'.__.'.__.'.__.'/\/_\'.__.'.__.'.__\%%%%/%%\
                 /%%\_.'.__.'.__.'./\/_ _\_.'.__.'.__.'.\%%/%%%%\
                /%%%%\.__.'.__.'._/\/|_|_|\.__.'.__.'.__.\%/%%%%\   
                /%%%%\_.'.__.'.__.\/_|_|_|_\'.__.'.__.'.__\%%%%%%\                  
               /%%%%%%\____________________________________\%%%%%%\
              /%%%%%%%%\]== _ _ _ ============______======]%%%%%%%\
              /%%%%%%%/\]==|_|_|_|============|////|======]%%%%%%%%\
             /%%%%%%%/%%\==|_|_|_|============|////|======]%%%%%%%%\
            /%%%%%%%/%%%%\====================|&///|======]%%%%%%%%%\
            /%%%%%%%/%%%%\====================|////|======]^^^^^^^^^^
           /%%%%%%%/%%%%%%\===================|////|======]  _ - _ -
           /%%%%%%%/%%%%%%\"""""""""""""""""""'===='"""""""
           ^^^^^^^/%%%%%%%%\   _ -   _ -              _-
                  ^^^^^^^^^^
                    """ + "\x1b[0m")
        time.sleep(5)
        print("\n\x1b[33m" + r""" The door creaks as you enter, the gusting wind dying down behind you. The cabin is cold, almost as cold as the outside. You'll need to find firewood to burn if you're to have any hope of surviving this icy nightmare.
     /|                  ______________________________________    
    / |                 |                                      | 
   /__|______           |    ...Hello, anyone home?!?!?!?!?.   |     
  |  __  __  |          |______________________________________|    
  | |  ||  | | 
  | |__||__| |        O  
  |  __  __()|/      O   
  | |  ||  | |      o
  | |  ||  | |
  | |__||__| |
  |__________|  
                    """ + "\x1b[0m")
        time.sleep(5)
        print("\nHow to survive:")
        time.sleep(5)
        print("- The temperature drops each day.")
        time.sleep(5)
        print("\n\x1b[32m" + r""" Gather firewood outside to keep warm.
       ___                                                                
      /___\                                                 
     (|0 0|)                                                    
   __/{\U/}\_ ___/vvv                                                
  / \  {~}   / _|_P|                                                 
  | /\  ~   /_/   ||                                                 
  |_| (____)      ||                       
  \_]/______\  /\_||_/\ 
     _\_||_/_ |] _||_ [|            
    (_,_||_,_) \/ [] \/
        """ + "\x1b[0m")
        time.sleep(5)
        print("\n\x1b[32m" + r""" You have a limited number of attempts to gather wood each day.
               ,@@@@@@@,
       ,,,.   ,@@@@@@/@@,  .oo8888o.
    ,&T%L%R&%,@@@@@/@@@@@@,8888\88/8o
   ,E&EY&E%&&%,@@@\@@@/@@@88\88888/88'
   %&L%&%&/%&&%@@\@@/ /@@@88888\88888'
   %&&%/ %&%%&&@@\ V /@@' `88\8 `/88'
   `&%\ ` /%&'    |.|        \ '|8'
       |o|        | |         | |
       |.|        | |         | |
    \\/ ._\//_/__/  ,\_//__\\/.  \_//__/_
        """ + "\033[0m")              
        time.sleep(5)
        print("\033[91m" + r""" Once inside the cabin, burn the wood to increase temperature.
                    |      |        ,---------,
                    |      |        |r'''|'''Y|
                   /        \       ||   |   ||
                  /          \      ||===|===||
                 /            \     ||   |   ||
                /              \    |L.__|__.J|
               /                \   '---------'
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
        time.sleep(5)
        print("\nWith those thoughts, you prepare yourself for the challenging days ahead.")
        time.sleep(5)

        # Print a formatted string with the player's name.
        print(f"\nPlaying as {player.name}.")

        # Convert the player's name to ASCII art format using the pyfiglet library.
        name_ascii = pyfiglet.figlet_format(player.name)

        # Create ASCII art for the phrase "Playing as:" using the pyfiglet library.
        playing_as_ascii = pyfiglet.figlet_format("Playing as:")

        # Print the ASCII art for the phrase "Playing as:" and the player's name in a specific color.
        print("\x1b[38;5;207m" + f"\n{playing_as_ascii}\n{name_ascii}" + "\x1b[0m")

        # Pause the execution for 5 seconds to allow the player to view the ASCII art.
        time.sleep(5)

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
                    time.sleep(5)
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

#The main function is the main entry point of the program. It starts the audio in a separate thread and presents a menu for various actions.
def main():
    audio_thread = threading.Thread(target=play_audio)
    audio_thread.daemon = True
    audio_thread.start()
    while True:
        print("\033[91m" + r"""
   *                         *                       
 (  `                      (  `                      
 )\))(      )  (           )\))(     (           (   
((_)()\  ( /(  )\   (     ((_)()\   ))\  (      ))\  
(_()((_) )(_))((_)  )\ )  (_()((_) /((_) )\ )  /((_) 
|  \/  |((_)_  (_) _(_/(  |  \/  |(_))  _(_/( (_))(  
| |\/| |/ _` | | || ' \)) | |\/| |/ -_)| ' \))| || | 
|_|  |_|\__,_| |_||_||_|  |_|  |_|\___||_||_|  \_,_| 
                                                     

        """ + "\033[0m")
# This Ascii art code creates an infinite loop that continuously prints a stylized ASCII art message in the terminal. 
# The ANSI escape sequence "\033[91m" changes the subsequent text color to red, while the enclosed multiple line raw string represents the ASCII art. 
# The "\033[0m" sequence resets the text color to the default after printing the ASCII art, ensuring that subsequent text remains unaffected by the color change. 
# This kind of code is commonly used to add visual appeal to CLI games and apps.     

        print("\033[34m" + "*******************************" + "\033[0m")
        print("\033[34m" + "* 1. Create player            *" + "\033[0m")
        print("\033[34m" + "* 2. Delete player            *" + "\033[0m")
        print("\033[34m" + "* 3. Display all players      *" + "\033[0m")
        print("\033[34m" + "* 4. Find player by ID        *" + "\033[0m")
        print("\033[34m" + "* 5. Leaderboard              *" + "\033[0m")
        print("\033[34m" + "* 6. Play game                *" + "\033[0m")
        print("\033[34m" + "* 7. Exit                     *" + "\033[0m")
        print("\033[34m" + "*******************************" + "\033[0m")

        choice = input("\x1b[32m" + "Enter your choice: " + "\x1b[0m")

        # Checks if the user's choice is '1'.
        if choice == '1':
            # Calls the 'create_player' function if the condition is met.
            create_player()

        # Checks if the user's choice is '2'.
        elif choice == '2':
            # Calls the 'delete_player' function if the condition is met.
            delete_player()

        # Checks if the user's choice is '3'.
        elif choice == '3':
            # Calls the 'display_all_players' function if the condition is met.
            display_all_players()

        # Checks if the user's choice is '4'.
        elif choice == '4':
            # Calls the 'find_player_by_id' function if the condition is met.
            find_player_by_id()

        # Checks if the user's choice is '5'.
        elif choice == '5':
            # Calls the 'leaderboard' function if the condition is met.
            leaderboard()

        # Checks if the user's choice is '6'.
        elif choice == '6':
            # Calls the 'play_game' function if the condition is met.
            play_game()

        # Checks if the user's choice is '7'.
        elif choice == '7':
            # Prints a farewell message and breaks out of the loop if the condition is met.
            print("\nTill next time!")
            break

# Calls the 'main' function if the script is run as the main program.
if __name__ == "__main__":
    main()
