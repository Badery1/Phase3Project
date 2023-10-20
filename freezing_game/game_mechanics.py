# Import necessary modules from Python standard library and custom modules.
import random
import time
from models import Player, LogGathered
from database import get_session

# Define a list of possible outcomes for log gathering and set the death threshold and temperature increase per log.
LOG_GATHERING_OUTCOMES = [0, 1, 2, 3, 4]
DEATH_THRESHOLD = -30
TEMPERATURE_INCREASE_PER_LOG = 2.5

# Define a function to gather logs for the player.
def gather_logs(player):
    # Obtain a new session for database operations.
    session = get_session()

    # Check if the player has any gathering attempts left.
    if player.gathering_attempts <= 0:
        print("You've exhausted all attempts to gather logs today.")
        time.sleep(3)
        session.close()
        return

    # Simulate the process of gathering logs.
    print("\nGathering firewood...")
    time.sleep(3)

    # Randomly determine the number of logs gathered and update the player's log count accordingly.
    logs_gathered = random.choice(LOG_GATHERING_OUTCOMES)
    player.logs += logs_gathered

    # Add a log gathering entry to the database and commit the changes.
    session.add(LogGathered(player_id=player.id, logs=logs_gathered))
    session.commit()

    # Provide feedback to the player based on the result of the gathering attempt.
    if logs_gathered:
        print(f"You gathered {logs_gathered} logs!")
        time.sleep(3)
    else:
        print("You couldn't find any logs.")
        time.sleep(3)

    # Update the remaining gathering attempts for the player and provide appropriate messages.
    player.gathering_attempts -= 1
    if player.gathering_attempts <= 0:
        print("You are too tired to gather more logs.")
        time.sleep(3)
    else:
        print(f"You have {player.gathering_attempts} gathering attempts left.")
        time.sleep(3)

    # Close the session after completing the operations.
    session.close()

# Define a function to burn logs for the player, increasing their temperature.
def burn_logs(player):
    # Obtain a new session for database operations.
    session = get_session()

    # Display the current number of logs the player has and initiate the burning process.
    print(f"\nYou currently have {player.logs} logs.")
    time.sleep(3)
    while True:
        logs_to_burn_input = input("How many logs would you like to burn? ")
        time.sleep(3)
        try:
            logs_to_burn = int(logs_to_burn_input)

            # Check if the player has enough logs to burn and if the input is valid.
            if logs_to_burn > player.logs:
                print("\nYou don't have that many logs!")
                time.sleep(3)
                continue

            if logs_to_burn < 0:
                print("\nYou cannot burn a negative number of logs!")
                time.sleep(3)
                continue

            # Update the player's log count and temperature based on the logs burned.
            player.logs -= logs_to_burn
            player.temperature += logs_to_burn * TEMPERATURE_INCREASE_PER_LOG
            session.commit()

            # Simulate the process of burning logs and display the updated temperature.
            print("\nBurning logs...")
            time.sleep(3)
            print(f"\nYou burned {logs_to_burn} logs. Your temperature is now {player.temperature}°F.")
            time.sleep(5)
            break
        except ValueError:
            print("\nPlease enter a valid number of logs to burn.")

    # Close the session after completing the operations.
    session.close()

# Define a function to burn all logs at once for the player, increasing their temperature.
def burn_all_logs(player):
    # Obtain a new session for database operations.
    session = get_session()

    # Ask for confirmation to burn all logs and process the request accordingly.
    confirmation = input(f"\nYou currently have {player.logs} logs. Are you sure you want to burn ALL of them? (y/n): ")
    if confirmation.lower() == 'y':
        logs_to_burn = player.logs
        if logs_to_burn == 0:
            print("\nYou don't have any logs to burn!")
            time.sleep(5)
            return

        # Update the player's log count and temperature when burning all logs.
        player.logs = 0
        player.temperature += logs_to_burn * TEMPERATURE_INCREASE_PER_LOG
        session.commit()

        # Simulate the process of burning all logs and display the updated temperature.
        print("\nBurning all of your logs...")
        time.sleep(3)
        print(f"\nYou burned ALL your logs! Your temperature is now {player.temperature}°F.")
        time.sleep(5)
    elif confirmation.lower() == 'n':
        print("\nFine then. DON'T burn all your logs.")
        time.sleep(3)
    else:
        print("\nInvalid Choice.")
        time.sleep(3)

    # Close the session after completing the operations.
    session.close()

# Define a function to simulate the passage of a day in the game and update player parameters accordingly.
def pass_day(player):
    # Obtain a new session for database operations.
    session = get_session()

    # Simulate the passage of time and update the player's days survived and temperature.
    print("\nYou sleep through the night...")
    time.sleep(3)

    player.days_survived += 1
    temperature_drop = round(0.5 * (player.days_survived ** 1.2), 2)
    player.temperature = round(player.temperature - temperature_drop, 2)

    player.gathering_attempts = 3
    session.commit()

    # Display the updated information about the day, temperature, and gathering attempts.
    print(f"\nDay has passed! It's now day {player.days_survived}. The temperature dropped by {temperature_drop}°F.")
    print(f"Your current temperature is: {player.temperature}°F.")
    print(f"You have {player.gathering_attempts} attempts to gather wood today.")
    time.sleep(5)

    # Check if the player's temperature has dropped below the death threshold and update their status accordingly.
    if player.temperature < DEATH_THRESHOLD:
        player.alive = False
        session.commit()
        print("\nIt's getting dangerously cold!")
        time.sleep(3)
        session.close()
        return False

    # Close the session after completing the operations.
    session.close()
    return True



