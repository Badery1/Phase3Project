import random
import time
from models import Player, LogGathered
from database import get_session

LOG_GATHERING_OUTCOMES = [0, 1, 2, 3, 4]
DEATH_THRESHOLD = -30
TEMPERATURE_INCREASE_PER_LOG = 2.5

def gather_logs(player):
    session = get_session()

    if player.gathering_attempts <= 0:
        print("You've exhausted all attempts to gather logs today.")
        session.close()
        return

    print("\nGathering firewood...")
    time.sleep(2)

    logs_gathered = random.choice(LOG_GATHERING_OUTCOMES)
    player.logs += logs_gathered
    session.add(LogGathered(player_id=player.id, logs=logs_gathered))
    session.commit()

    if logs_gathered:
        print(f"You gathered {logs_gathered} logs!")
    else:
        print("You couldn't find any logs.")

    player.gathering_attempts -= 1
    if player.gathering_attempts <= 0:
        print("You are too tired to gather more logs.")
    else:
        print(f"You have {player.gathering_attempts} gathering attempts left.")

    session.close()

def burn_logs(player):
    session = get_session()

    print(f"\nYou currently have {player.logs} logs.")
    while True:
        logs_to_burn_input = input("How many logs would you like to burn? ")
        try:
            logs_to_burn = int(logs_to_burn_input)

            if logs_to_burn > player.logs:
                print("\nYou don't have that many logs!")
                continue

            if logs_to_burn < 0:
                print("\nYou cannot burn a negative number of logs!")
                continue

            player.logs -= logs_to_burn
            player.temperature += logs_to_burn * TEMPERATURE_INCREASE_PER_LOG
            session.commit()
            
            print("\nBurning logs...")
            time.sleep(2)
            print(f"\nYou burned {logs_to_burn} logs. Your temperature is now {player.temperature}°F.")
            break
        except ValueError:
            print("\nPlease enter a valid number of logs to burn.")

    session.close()

def burn_all_logs(player):
    session = get_session()

    confirmation = input(f"\nYou currently have {player.logs} logs. Are you sure you want to burn ALL of them? (y/n): ")
    if confirmation.lower() == 'y':
        logs_to_burn = player.logs
        if logs_to_burn == 0:
            print("\nYou don't have any logs to burn!")
            return

        player.logs = 0
        player.temperature += logs_to_burn * TEMPERATURE_INCREASE_PER_LOG
        session.commit()

        print("\nBurning all of your logs...")
        time.sleep(3)
        print(f"\nYou burned ALL your logs! Your temperature is now {player.temperature}°F.")
    elif confirmation.lower() == 'n':
        print("\nFine then. DON'T burn all your logs.")
    else:
        print("\nInvalid Choice.")

    session.close()

def pass_day(player):
    session = get_session()

    print("\nYou sleep through the night...")
    time.sleep(2)

    player.days_survived += 1
    temperature_drop = round(0.5 * (player.days_survived ** 1.2), 2)
    player.temperature = round(player.temperature - temperature_drop, 2)
    
    player.gathering_attempts = 3
    session.commit()

    print(f"\nDay has passed! It's now day {player.days_survived}. The temperature dropped by {temperature_drop}°F.")
    print(f"Your current temperature is: {player.temperature}°F.")
    print(f"You have {player.gathering_attempts} attempts to gather wood today.")

    if player.temperature < DEATH_THRESHOLD:
        player.alive = False
        session.commit()
        print("\nIt's getting dangerously cold!")
        session.close()
        return False

    session.close()
    return True