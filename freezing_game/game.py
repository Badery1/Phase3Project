import wx
import time
from models import Player
from database import get_session
import game_mechanics

class GameApp(wx.App):
    def OnInit(self):
        self.frame = GameFrame(None, title="The Freezing Game!", size=(800, 600))
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

class GameFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(GameFrame, self).__init__(*args, **kw)

        self.session = get_session()

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.text_display = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(400, 300))
        vbox.Add(self.text_display, 1, flag=wx.EXPAND | wx.ALL, border=5)

        button_panel = wx.Panel(panel)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        create_button = wx.Button(button_panel, label='Create Player', size=(100, 30))
        delete_button = wx.Button(button_panel, label='Delete Player', size=(100, 30))
        display_button = wx.Button(button_panel, label='Display Players', size=(100, 30))
        find_button = wx.Button(button_panel, label='Find Player', size=(100, 30))
        leaderboard_button = wx.Button(button_panel, label='Leaderboard', size=(100, 30))
        play_button = wx.Button(button_panel, label='Play Game', size=(100, 30))

        create_button.Bind(wx.EVT_BUTTON, self.create_player)
        delete_button.Bind(wx.EVT_BUTTON, self.delete_player)
        display_button.Bind(wx.EVT_BUTTON, self.display_all_players)
        find_button.Bind(wx.EVT_BUTTON, self.find_player_by_id)
        leaderboard_button.Bind(wx.EVT_BUTTON, self.leaderboard)
        play_button.Bind(wx.EVT_BUTTON, self.play_game)

        hbox.Add(create_button, 0, flag=wx.ALL, border=5)
        hbox.Add(delete_button, 0, flag=wx.ALL, border=5)
        hbox.Add(display_button, 0, flag=wx.ALL, border=5)
        hbox.Add(find_button, 0, flag=wx.ALL, border=5)
        hbox.Add(leaderboard_button, 0, flag=wx.ALL, border=5)
        hbox.Add(play_button, 0, flag=wx.ALL, border=5)

        button_panel.SetSizer(hbox)
        vbox.Add(button_panel, flag=wx.ALIGN_CENTER)

        panel.SetSizer(vbox)

        self.input_field = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.input_field.Bind(wx.EVT_TEXT_ENTER, self.on_input_enter)
        vbox.Add(self.input_field, 0, flag=wx.EXPAND | wx.ALL, border=5)

        self.player = None
        self.init_game()

    def init_game(self):
        self.text_display.AppendText("Welcome to the The Freezing Game!\n")
        self.text_display.AppendText("Use the provided buttons to Play!\n")
        self.text_display.AppendText("Have fun!\n")

    def create_player(self, event):
        name_dlg = wx.TextEntryDialog(self, 'Enter player name:', 'Create Player', '')
        if name_dlg.ShowModal() == wx.ID_OK:
            name = name_dlg.GetValue()
            new_player = Player(name=name)
            self.session.add(new_player)
            self.session.commit()
            self.text_display.AppendText(f"\nPlayer {name} created!\n")
        name_dlg.Destroy()

    def delete_player(self, event):
        player_id_dlg = wx.TextEntryDialog(self, 'Enter player ID to delete:', 'Delete Player', '')
        if player_id_dlg.ShowModal() == wx.ID_OK:
            player_id = int(player_id_dlg.GetValue())
            player = self.session.query(Player).filter_by(id=player_id).first()
            if not player:
                self.text_display.AppendText("\nPlayer not found!\n")
            else:
                self.session.delete(player)
                self.session.commit()
                self.text_display.AppendText(f"\nPlayer {player.name} deleted!\n")
        player_id_dlg.Destroy()

    def display_all_players(self, event):
        players = self.session.query(Player).all()
        for player in players:
            self.text_display.AppendText(f"ID: {player.id}, Name: {player.name}, Temperature: {player.temperature}°F, Days Survived: {player.days_survived}\n")

    def find_player_by_id(self, event):
        player_id_dlg = wx.TextEntryDialog(self, 'Enter player ID to find:', 'Find Player', '')
        if player_id_dlg.ShowModal() == wx.ID_OK:
            player_id = int(player_id_dlg.GetValue())
            player = self.session.query(Player).filter_by(id=player_id).first()
            if not player:
                self.text_display.AppendText("\nPlayer not found!\n")
            elif not player.alive:
                self.text_display.AppendText("\nThis player is dead!\n")
            else:
                self.text_display.AppendText(f"ID: {player.id}, Name: {player.name}, Temperature: {player.temperature}°F, Days Survived: {player.days_survived}\n")
        player_id_dlg.Destroy()

    def leaderboard(self, event):
        players = self.session.query(Player).order_by(Player.days_survived.desc()).all()
        self.text_display.AppendText("\n--- Leaderboard ---\n")
        for player in players:
            self.text_display.AppendText(f"{player.name} - Days Survived: {player.days_survived}\n")

    def play_game(self, event):
        player_id_dlg = wx.TextEntryDialog(self, 'Enter player ID to play:', 'Play Game', '')
        if player_id_dlg.ShowModal() == wx.ID_OK:
            player_id = int(player_id_dlg.GetValue())
            self.player = self.session.query(Player).filter_by(id=player_id).first()
            if not self.player:
                self.text_display.AppendText("\nPlayer not found!\n")
            elif not self.player.alive:
                self.text_display.AppendText("\nThis player is dead!\n")
            else:
                self.play_as_player()
        player_id_dlg.Destroy()

    def play_as_player(self):
        self.text_display.AppendText("The world as you know it has ended. A violent ice age took the world by storm, and you are left alone stranded at an abandoned campsite.\n")
        time.sleep(2)
        self.text_display.AppendText("As the blizzard clears momentarily, you see it - an old, abandoned cabin. With no other shelter in sight, you decide to take refuge. This is where you will survive.\n")
        time.sleep(3)
        self.text_display.AppendText("The door creaks as you enter, the gusting wind dying down behind you. The cabin is cold, almost as cold as the outside. You'll need to find firewood to burn if you're to have any hope of surviving this icy nightmare.\n")
        time.sleep(3)
        self.text_display.AppendText("How to survive:\n")
        self.text_display.AppendText("- The temperature drops each day.\n")
        self.text_display.AppendText("- Gather firewood outside to keep warm.\n")
        self.text_display.AppendText("- You have a limited number of attempts to gather wood each day.\n")
        self.text_display.AppendText("- Once inside the cabin, burn the wood to increase temperature.\n")
        time.sleep(3)
        self.text_display.AppendText("With those thoughts, you prepare yourself for the challenging days ahead.\n")
        time.sleep(2)
        
        while True:
            if self.player.inside_cabin:
                self.text_display.AppendText("\nYou are currently inside the cabin.\n")
                self.text_display.AppendText("\n--- Inside Cabin Menu ---\n")
                self.text_display.AppendText("1. Burn logs\n")
                self.text_display.AppendText("2. Burn All logs\n")
                self.text_display.AppendText("3. Pass the day\n")
                self.text_display.AppendText("4. Check temperature and logs\n")
                self.text_display.AppendText("5. Leave cabin\n")
                self.text_display.AppendText("6. Exit game\n")
            else:
                self.text_display.AppendText("\nYou are currently outside the cabin.\n")
                self.text_display.AppendText("\n--- Outside Cabin Menu ---\n")
                self.text_display.AppendText("1. Gather firewood\n")
                self.text_display.AppendText("2. Check temperature and logs\n")
                self.text_display.AppendText("3. Enter cabin\n")
                self.text_display.AppendText("4. Exit game\n")

            choice_dlg = wx.TextEntryDialog(self, 'Enter your choice:', 'Game Menu', '')
            if choice_dlg.ShowModal() == wx.ID_OK:
                choice = choice_dlg.GetValue()
                if self.player.inside_cabin:
                    if choice == '1':
                        game_mechanics.burn_logs(self.player)
                        self.session.commit()
                    elif choice == '2':
                        game_mechanics.burn_all_logs(self.player)
                        self.session.commit()
                    elif choice == '3':
                        alive = game_mechanics.pass_day(self.player)
                        self.session.commit()

                        if not alive:
                            self.session.commit()
                            self.text_display.AppendText("\nYou fall asleep...\n")
                            time.sleep(2)
                            self.text_display.AppendText("...only to never wake.\n")
                            self.text_display.AppendText("\nGame over!\n")
                            break
                    elif choice == '4':
                        self.text_display.AppendText(f"\nTemperature: {self.player.temperature}°F, Logs: {self.player.logs}\n")
                    elif choice == '5':
                        game_mechanics.toggle_cabin_location(self.player)
                        self.session.commit()
                    elif choice == '6':
                        break
                else:  # outside the cabin
                    if choice == '1':
                        game_mechanics.gather_logs(self.player)
                        self.session.commit()
                    elif choice == '2':
                        self.text_display.AppendText(f"\nTemperature: {self.player.temperature}°F, Logs: {self.player.logs}\n")
                    elif choice == '3':
                        game_mechanics.toggle_cabin_location(self.player)
                        self.session.commit()
                    elif choice == '4':
                        break
            choice_dlg.Destroy()

    def on_input_enter(self, event):
        user_input = self.input_field.GetValue()
        self.text_display.AppendText(f"> {user_input}\n")
        self.input_field.Clear()

if __name__ == '__main__':
    app = GameApp(0)
    app.MainLoop()