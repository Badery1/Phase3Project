import time
from models import Player
from database import get_session
import game_mechanics
import threading
import pygame
import pyfiglet  


audio_file = 'game-music.mp3'

# Create a function to play audio in a separate thread
def play_audio():
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play(-1)

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
        print("\x1b[37m" + r""" This player is dead!
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

    time.sleep(5)

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
          *    *  *   *   *       *     *   *  *  *     *   *       *   * 
 *     *    *   *   *    *   *    **   *  *    *___ *   *  (******)   * *
*   **    *  **    *       *     *    *  *    /    /  * (*******)  *
*   *      *    *   *   *   *   *   *   *    / \  / *    (******)   * 
\  *      *  *     *    *   *   *   *   *   /   \/  *    *   *  *
 \  *      *      *   *  *  *   *   *   *  |    /  *   .**.     * 
  `*.  *  *   *   *  *   *    *   *  *  *   \  /\    /___ \.*.   
     \ *    *   *   *   *   *   *    *       \/ \\ * |. .|/`*'  *_
     |*     *   *   *   *   *   *    * *   *    (_) __\-/__  * .'
      \    * *  *   *   *   *   *     *  *   *  |\\  \:/  )  /
       \*  *  *  *   *  *   *   *     *   * *    \V\\  :/ / * |
        |   *   *   *   *   *   *   *    **   * `*'\\_/ /)  /
         \    *  *  *   *   *   *     * *  * *   * ((_)/_) /
         |* *   *   *   *   *   *   *   *   * * *  \ \\  / |
         | *    *   *   *   *   *   *    *  *    * |  |  | /
          | *   *   *   *   *    *  *  *  *    *   |__|__| |
           _______________________________________(___V___)'
                    """ + "\x1b[0m")
        time.sleep(5)
        print("\n\x1b[32m" + r""" As the blizzard clears momentarily, you see it - a cabin. With no other shelter in sight, you decide to take refuge. This, is where you will survive.   
                                                         /\
                                               ___      /%%\
                                              |_I_|     /%%\
                   __________________/',______|I_I|____/%%%%\/\
                  /\'.__.'.__.'.__.'/\/_\'.__.'.__.'.__\%%%%/%%\
                 /%%\_.'.__.'.__.'./\/_ _\_.'.__.'.__.'.\MICHAEL\
                /%%%%\.__.'.__.'._/\/|_|_|\.__.'.__.'.__.\%/%%%%\   
                /%%%%\_.'.__.'.__.\/_|_|_|_\'.__.'.__.'.__\%%%%%%\                  
               /%%%%%%\____________________________________\%%%%%%\
              /%%%%%%%%\]== _ _ _ ============______======]%%%%%%%\
              /%%%%%%%/\]==|_|_|_|============|////|======]%%%%%%%%\
           __/%%%%%%%/%%\==|_|_|_|============|////|======]%%%%%%%%\
            /%%%%%%%/%%%%\====================|&///|======]%%%%%%%%%\
            /%%%%%%%/%%%%\====================|////|======]^^^^^^^^^^
           /%%%%%%%/%%%%%%\===================|////|======]  _ - _ -
            /%%%%%%%/%%%%%%\"""""""""""""""""""'===='"""""""
           ^^^^^^^/%%%%%%%%\   _ -   _ -              _-
                  ^^^^^^^^^^
                    """ + "\x1b[0m")
        time.sleep(5)
        print("\n\x1b[36m" + r""" The door creaks as you enter, the gusting wind dying down behind you. The cabin is cold, almost as cold as the outside. You'll need to find firewood to burn if you're to have any hope of surviving this icy nightmare.
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
        print("\n\x1b[38;5;46m" + r"""
  _   _                 _                               _             
 | | | | _____      __ | |_ ___    ___ _   _ _ ____   _(___   _____ _ 
 | |_| |/ _ \ \ /\ / / | __/ _ \  / __| | | | '__\ \ / | \ \ / / _ (_)
 |  _  | (_) \ V  V /  | || (_) | \__ | |_| | |   \ V /| |\ V |  __/_ 
 |_| |_|\___/ \_/\_/    \__\___/  |___/\__,_|_|    \_/ |_| \_/ \___(_)
        """ + "\x1b[0m")
        time.sleep(5)
        print("\n\x1b[36m" + r""" The temperature drops each day.
______________________
|   ^F     _    ^C   |
|  100    | |    40  |
|   90    | |    30  |
|   80    | |    25  |
|   70    | |    20  |
|   60    | |    15  |
|   50    | |    10  |
|   40    | |     5  |
|   30    | |     0  |
|   20    | |    -5  |
|   10    | |   -10  |  Now                      
|    0    |_|   -20  |    That's cold!            
|  -10    |*|   -25  |
|  -20    |*|   -30  |
|  -30    |*|   -35  |
|        '***`       |
|       (*****)      |
|        `---'       |
|____________________|

                    """ + "\x1b[0m")
        time.sleep(5)
        print("\033[93m" + r""" Gather firewood outside to keep warm.
                  ___                                                                
                 /___\                                                 
                (|0 0|)                                                    
             ___/{\U/}\_____/vvv                                                
            | / \ {~}    / _|_P|                                                 
            |  /\  ~   /_/   ||                                                 
            | _| (____)      ||                       
             \_]/______\  /\_||_/\ 
                _\_||_/_ |] _||_ [|            
               (_,_||_,_) \/ [] \/
        """ + "\033[0m")
        time.sleep(5)
        print("\n\x1b[32m" + r""" You have a limited number of attempts to gather wood each day.
               ,@@@@@@@,
       ,,,.   ,@@@@@@/@@,  .oo8888o.
    ,&%%&%&&%,@@@@@/@@@@@@,8888\88/8o
   ,%&\%&&%&&%,@@@\@@@/@@@88\88888/88'
   %&&%&%&/%&&%@@\@@/ /@@@88888\88888'
   %&&%/ %&%%&&@@\ V /@@' `88\8 `/88'
   `&%\ ` /%&'    |.|        \ '|8'
       |o|        | |         | |
       |.|        | |         | |
    \\/ ._\//_/__/  ,\_//__\\/.  \_//__/_
        """ + "\033[0m")              
        time.sleep(5)
        print("\033[91m" + r""" Once inside the cabin, burn the wood to increase temperature.
                                    ,---------,
                                    |E'''|'''Y|
                                    ||   |   ||
                                    ||===A===||
                                    ||   |   ||
                                    |K.__|__.L|
                                    '---------'
            _________________________
             -__LLLLLLLLLLLLLLLLL__-
              \|#/#############\#|/
              \|##/           \##|/
              \|#|  )  ) ( ) ) |#|/
              \|#|  ( ( ()((   |#|/
              \|#|   /\__\_(-  |#|/
 _____________\|#| _(\/L/(\/)_ |#|/_____________
              \|#|-.J.O.E.-.-.-|#|/         
               '''             ''' 
        """ + "\033[0m")
        time.sleep(5)
        print("\x1b[38;5;94m" + r""" With those thoughts, you prepare yourself for the challenging days ahead.
            _                             _
           | |                           | |
         =H| |========mn=======nm========| |H=
           |_|        ( \     / )        |_|
                       \ )(")( /
                       ( /\_/\ )
                        \     /
                         )=O=(
                        /  _  \
                       /__/ \__\
                       | |   | |
                       |_|   |_|
                       (_)   (_)
============================================================
        """ + "\x1b[0m")
        time.sleep(5)

        # print(f"\nPlaying as {player.name}.")
        name_ascii = pyfiglet.figlet_format(player.name)
        playing_as_ascii = pyfiglet.figlet_format("Playing as:")
        print("\x1b[38;5;207m" + f"\n{playing_as_ascii}\n{name_ascii}" + "\x1b[0m")
        
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
                print(f"\n\033[1mTemperature:\033[0m \033[91m{player.temperature}°F\033[0m, \033[1mLogs:\033[0m \033[92m{player.logs}\033[0m")
                time.sleep(5)
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
                print(f"\n\033[1mTemperature:\033[0m \033[91m{player.temperature}°F\033[0m, \033[1mLogs:\033[0m \033[92m{player.logs}\033[0m")
                time.sleep(5)
            elif choice == '3':
                toggle_cabin_location(player)
                session.commit()
            elif choice == '4':
                break


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
