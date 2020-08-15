from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from Game import Game
import numpy as np


class MyButton(Button):
    def __init__(self, position, size):
        Button.__init__(self)
        self.position = position

        if size == 80:
            self.posx = int(np.floor(position / 10))
            self.posy = position % 10
        elif size == 252:
            self.posx = int(np.floor(position / 18))
            self.posy = position % 18
        elif size == 480:
            self.posx = int(np.floor(position / 24))
            self.posy = position % 24
        else:
            self.posx = 0
            self.posy = 0


def change_color(block):
    t = block.text
    print(t)
    if t == '0':
        c = [0.999, 0.999, 0.999, 0.5]  # Dark Gray
        block.text = '\n'
    elif t == '1':
        c = [0, 0.2, 0.8, 1]  # Dark Blue
    elif t == '2':
        c = [1, 0.4, 0, 1]  # Rust
    elif t == '3':
        c = [0, 0.5, 0, 1]  # Green
    elif t == '4':
        c = [1, 0, 0, 1]  # Red
    elif t == '5':
        c = [0, 1, 1, 1]  # Blue-Green
    elif t == '6':
        c = [0, 0, 1, 1]  # Blue
    elif t == '7':
        c = [1, 1, 0, 1]  # Yellow
    elif t == '8':
        c = [1, 0, 1, 1]  # Magenta
    else:
        c = [0, 0, 0, 1]  # Black
    block.background_color = c


class PlayMineSweep(App):
    def __init__(self, number_tiles):
        super().__init__()
        self.game = Game(number_tiles)
        self.number_tiles = number_tiles
        if number_tiles == 80:
            self.header_spaces = 2
            self.number_cols = 10
            self.number_rows = 8
            self.number_bombs = 10
            self.difficulty = 'Easy'
            self.neighbors = ((-1, -1, -11), (-1, 0, -10),
                              (-1, 1, -9), (0, -1, -1),
                              (0, 1, 1), (1, -1, 9),
                              (1, 0, 10), (1, 1, 11))
        elif number_tiles == 252:
            self.header_spaces = 6
            self.number_cols = 18
            self.number_rows = 14
            self.number_bombs = 40
            self.difficulty = 'Medium'
            self.neighbors = ((-1, -1, -19), (-1, 0, -18),
                              (-1, 1, -17), (0, -1, -1),
                              (0, 1, 1), (1, -1, 17),
                              (1, 0, 18), (1, 1, 19))
        elif number_tiles == 480:
            self.header_spaces = 9
            self.number_cols = 24
            self.number_rows = 20
            self.number_bombs = 99
            self.difficulty = 'Hard'
            self.neighbors = ((-1, -1, -25), (-1, 0, -24),
                              (-1, 1, -23), (0, -1, -1),
                              (0, 1, 1), (1, -1, 23),
                              (1, 0, 24), (1, 1, 25))
        else:
            return

        self.layout = GridLayout(cols=self.number_cols, padding=50)
        self.end_label = Label(text='Game Over')
        self.end_popup = None
        self.over = False
        self.flag_count = None
        self.btn = []

    def build(self):
        self.title = 'MineSweep'

        l1 = Label(text='Tap once to flag,')
        l2 = Label(text='twice to expose')
        l3 = Label(text='MineSweeper')
        l4 = Label(text='%s Level' % self.difficulty)
        self.flag_count = Label(text=str(self.number_bombs))
        l5 = Label(text='Bombs')

        self.layout.add_widget(l1)
        self.layout.add_widget(l2)
        for i in range(self.header_spaces):
            self.layout.add_widget(Label())
        self.layout.add_widget(l3)
        self.layout.add_widget(l4)
        for i in range(self.header_spaces):
            self.layout.add_widget(Label())
        self.layout.add_widget(self.flag_count)
        self.layout.add_widget(l5)

        for i in range(self.number_tiles):
            self.btn.append(MyButton(i, self.number_tiles))
            self.btn[i].bind(on_press=self.reveal)
            self.layout.add_widget(self.btn[i])

        for i in range(self.number_cols - 1):
            self.layout.add_widget(Label(text=''))
        menu = Button(text='Menu',
                      on_press=self.return_menu,
                      background_color=[0, 0, 0, 0])
        self.layout.add_widget(menu)

        return self.layout

    def reveal(self, instance):
        if not self.over:
            f_count = int(self.flag_count.text)
            if instance.text == '' and instance.text != '\n':
                instance.text = 'F'
                self.flag_count.text = str(f_count - 1)
            else:
                answer = self.game.find_pos(instance.posx, instance.posy)
                if answer == -1:
                    instance.text = '!'
                    self.game_over()
                else:
                    instance.text = str(answer)
                    change_color(instance)
                    if not answer:
                        self.zero_recursion(instance.position)
                    self.flag_count.text = str(f_count + 1)

                    if self.detect_win():
                        self.win()

    def zero_recursion(self, index):
        # Find all neighbors if instance is a zero
        if self.btn[index].text == '\n':
            for x in self.neighbors:
                check_box = (x[0] + self.btn[index].posx, x[1] + self.btn[index].posy)
                # Now let's check that check_box is on the board
                if check_box[0] in range(self.number_rows):
                    if check_box[1] in range(self.number_cols):
                        if self.btn[index + x[2]].text == '':
                            # First reveal the instance of MyButton()
                            # Right now, we have to reveal twice
                            for _ in range(2):
                                self.reveal(self.btn[index + x[2]])
                            # Then, if the instance is a zero, do the recursion
                            if self.btn[index + x[2]].text == '\n':
                                self.zero_recursion(index + x[2])

    def game_over(self):
        self.over = True
        for block in self.btn:
            check = self.game.find_pos(block.posx, block.posy)
            if check == -1:
                if block.text == 'F':
                    block.text = 'B'
                else:
                    block.text = 'b'
        self.make_end_popup()
        self.end_popup.open()

    def detect_win(self):
        win = False
        for block in self.btn:
            check = self.game.find_pos(block.posx, block.posy)
            if check == -1 or (check != -1 and block.text != ''):
                win = True
            else:
                win = False
                break
        return win

    def win(self):
        self.over = True
        self.end_label = Label(text='You Won!!')
        self.make_end_popup()
        self.end_popup.open()

    def make_end_popup(self):
        self.end_popup = Popup(title='MineSweep',
                               content=self.end_label,
                               size_hint=(None, None),
                               size=(400, 400),
                               pos_hint={'x': 0.375,
                                         'y': 0.3})

    def return_menu(self, _):
        self.layout.clear_widgets()
        self.stop()
        MineSweepApp().run()


class MineSweepApp(App):

    layout = GridLayout(cols=3, padding=40)

    def build(self):
        self.title = 'MineSweep'
        self.layout = GridLayout(cols=3, padding=40)

        l1 = Label(text='')
        l2 = Label(text='Mine Sweeper!')
        l3 = Label(text='')

        easy = Button(text='Easy')
        medium = Button(text='Medium')
        hard = Button(text='Hard')

        easy.bind(on_press=self.choose_level)
        medium.bind(on_press=self.choose_level)
        hard.bind(on_press=self.choose_level)

        self.layout.add_widget(l1)
        self.layout.add_widget(l2)
        self.layout.add_widget(l3)
        self.layout.add_widget(easy)
        self.layout.add_widget(medium)
        self.layout.add_widget(hard)
        return self.layout

    def choose_level(self, event):
        self.layout.clear_widgets()
        if event.text == 'Easy':
            PlayMineSweep(80).run()
        elif event.text == 'Medium':
            PlayMineSweep(252).run()
        elif event.text == 'Hard':
            PlayMineSweep(480).run()
        else:
            print('Error. Not a button option.')


if __name__ == '__main__':
    MineSweepApp().run()
