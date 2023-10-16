import wx
import time
from models import Player
from database import get_session
import game_mechanics

class GameFrame(wx.Frame):
    def __init__(self, parent, title):
        super(GameFrame, self).__init__(parent, title=title, size=(500, 300))

        self.panel = wx.Panel(self)

        self.output_text = wx.StaticText(self.panel, label="Welcome to the Game", pos=(10, 10))
        self.button_create = wx.Button(self.panel, label="Create Player", pos=(10, 50))
        self.button_delete = wx.Button(self.panel, label="Delete Player", pos=(10, 90))
        self.button_display = wx.Button(self.panel, label="Display all Players", pos=(10, 130))
        self.button_find = wx.Button(self.panel, label="Find Player by ID", pos=(10, 170))
        self.button_leaderboard = wx.Button(self.panel, label="Leaderboard", pos=(10, 210))
        self.button_play = wx.Button(self.panel, label="Play Game", pos=(10, 250))
        self.button_exit = wx.Button(self.panel, label="Exit", pos=(10, 290))

        self.Bind(wx.EVT_BUTTON, self.on_create, self.button_create)
        self.Bind(wx.EVT_BUTTON, self.on_delete, self.button_delete)
        self.Bind(wx.EVT_BUTTON, self.on_display, self.button_display)
        self.Bind(wx.EVT_BUTTON, self.on_find, self.button_find)
        self.Bind(wx.EVT_BUTTON, self.on_leaderboard, self.button_leaderboard)
        self.Bind(wx.EVT_BUTTON, self.on_play, self.button_play)
        self.Bind(wx.EVT_BUTTON, self.on_exit, self.button_exit)

    def on_create(self, event):
        session = get_session()
        name = "SamplePlayer"  # Replace with appropriate wx.TextCtrl value
        new_player = Player(name=name)
        session.add(new_player)
        session.commit()
        self.output_text.SetLabel(f"Player {name} created!")
        session.close()

    def on_delete(self, event):
        session = get_session()
        player_id = 1  # Replace with appropriate wx.TextCtrl value
        player = session.query(Player).filter_by(id=player_id).first()

        if not player:
            self.output_text.SetLabel("Player not found!")
            session.close()
            return

        session.delete(player)
        session.commit()
        self.output_text.SetLabel(f"Player {player.name} deleted!")
        session.close()

    def on_display(self, event):
        session = get_session()
        players = session.query(Player).all()
        output = ""
        for player in players:
            output += f"ID: {player.id}, Name: {player.name}, Temperature: {player.temperature}°F, Days Survived: {player.days_survived}\n"
        self.output_text.SetLabel(output)
        session.close()

    def on_find(self, event):
        session = get_session()
        player_id = 1  # Replace with appropriate wx.TextCtrl value
        player = session.query(Player).filter_by(id=player_id).first()

        if not player:
            self.output_text.SetLabel("Player not found!")
            session.close()
            return

        elif not player.alive:
            self.output_text.SetLabel("This player is dead!")
            session.close()
            return

        self.output_text.SetLabel(f"ID: {player.id}, Name: {player.name}, Temperature: {player.temperature}°F, Days Survived: {player.days_survived}")
        session.close()

    def on_leaderboard(self, event):
        session = get_session()
        players = session.query(Player).order_by(Player.days_survived.desc()).all()
        output = "--- Leaderboard ---\n"
        for player in players:
            output += f"{player.name} - Days Survived: {player.days_survived}\n"
        self.output_text.SetLabel(output)
        session.close()

    def on_play(self, event):
        session = get_session()
        player_id = 1  # Replace with appropriate wx.TextCtrl value
        player = session.query(Player).filter_by(id=player_id).first()

        if not player:
            self.output_text.SetLabel("Player not found!")
            session.close()
            return

        elif not player.alive:
            self.output_text.SetLabel("This player is dead!")
            session.close()
            return

    print(f"\nPlaying as {player.name}.")

    while True:
        print("\n--- Game Menu ---")
        print("1. Gather firewood")
        print("2. Burn logs")
        print("3. Burn All logs")
        print("4. Pass the day")
        print("5. Check temperature and logs")
        print("6. Exit game")

        choice = input("Enter your choice: ")

        if choice == '1':
            game_mechanics.gather_logs(player)
            session.commit()

        elif choice == '2':
            game_mechanics.burn_logs(player)
            session.commit()

        elif choice == '3':
            game_mechanics.burn_all_logs(player)
            session.commit()

        elif choice == '4':
            alive = game_mechanics.pass_day(player)
            session.commit()

            if not alive:
                session.commit()
                print("\nYou fall asleep...")
                time.sleep(2)  # Delay for 2 seconds
                print("...only to never wake.")
                print("\nGame over!")
                break

        elif choice == '5':
            print(f"\nTemperature: {player.temperature}°F, Logs: {player.logs}")

        elif choice == '6':
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
