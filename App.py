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


class EasyMineSweepApp(App):
    game = Game(80)
    easy_layout = GridLayout(cols=10, padding=50)
    end_popup = Popup(title='MineSweep',
                      content=Label(text='Game Over'),
                      size_hint=(None, None),
                      size=(400, 400),
                      pos_hint={'x': 0.375,
                                'y': 0.3})
    over = False

    def build(self):

        l1 = Label(text='Tap once to flag,\ntwice to expose')
        l2 = Label(text='')
        l3 = Label(text='MineSweep')
        l4 = Label(text='Easy Level')
        l5 = Label(text='')
        l6 = Label(text='10 Bombs')

        self.easy_layout.add_widget(l1)
        self.easy_layout.add_widget(l2)
        self.easy_layout.add_widget(l3)
        self.easy_layout.add_widget(l4)
        self.easy_layout.add_widget(l5)
        for i in range(4):
            self.easy_layout.add_widget(Label(text=''))
        self.easy_layout.add_widget(l6)

        btn = []
        for i in range(80):
            btn.append(MyButton(i, 80))
            btn[i].bind(on_press=self.reveal)
            self.easy_layout.add_widget(btn[i])

        for i in range(9):
            self.easy_layout.add_widget(Label(text=''))
        reset_button = Button(text='Menu',
                              on_press=self.return_menu,
                              background_color=[0, 0, 0, 0])
        self.easy_layout.add_widget(reset_button)

        return self.easy_layout

    def reveal(self, instance):
        if not self.over:
            if instance.text == '':
                instance.text = 'FLAGGED'
            else:
                answer = self.game.find_pos(instance.posx, instance.posy)
                if answer == -1:
                    instance.text = 'BOOM!'
                    self.game_over()
                else:
                    instance.text = str(answer)

    def game_over(self):
        self.over = True
        self.end_popup.open()

    def return_menu(self, _):
        self.easy_layout.clear_widgets()
        self.stop()
        MineSweepApp().run()


class MediumMineSweepApp(App):
    game = Game(252)
    medium_layout = GridLayout(cols=18, padding=50)
    end_popup = Popup(title='MineSweep',
                      content=Label(text='Game Over'),
                      size_hint=(None, None),
                      size=(400, 400),
                      pos_hint={'x': 0.375,
                                'y': 0.3})
    over = False
    flag_count = None

    def build(self):

        l1 = Label(text='Tap once to flag,\ntwice to expose')
        l2 = Label(text='')
        l3 = Label(text='')
        l4 = Label(text='MineSweeper')
        l5 = Label(text='')
        l6 = Label(text='Medium Level')
        l7 = Label(text='')
        l8 = Label(text='')
        self.flag_count = Label(text='40')

        self.medium_layout.add_widget(l1)
        self.medium_layout.add_widget(l2)
        self.medium_layout.add_widget(l3)
        self.medium_layout.add_widget(l4)
        self.medium_layout.add_widget(l5)
        self.medium_layout.add_widget(l6)
        self.medium_layout.add_widget(l7)
        self.medium_layout.add_widget(l8)
        for i in range(8):
            self.medium_layout.add_widget(Label(text=''))
        self.medium_layout.add_widget(self.flag_count)
        self.medium_layout.add_widget(Label(text='Bombs'))

        btn = []
        for i in range(252):
            btn.append(MyButton(i, 252))
            btn[i].bind(on_press=self.reveal)
            self.medium_layout.add_widget(btn[i])

        for i in range(8):
            self.medium_layout.add_widget(Label(text=''))
        reset_button = Button(text='Menu',
                              on_press=self.return_menu,
                              background_color=[0, 0, 0, 0])
        self.medium_layout.add_widget(reset_button)

        return self.medium_layout

    def reveal(self, instance):
        if not self.over:
            if instance.text == '':
                instance.text = 'F'
                f_count = int(self.flag_count.text)
                self.flag_count.text = str(f_count - 1)
            else:
                answer = self.game.find_pos(instance.posx, instance.posy)
                if answer == -1:
                    instance.text = 'BOOM!'
                    self.game_over()
                else:
                    instance.text = str(answer)
                    f_count = int(self.flag_count.text)
                    self.flag_count.text = str(f_count + 1)

    def game_over(self):
        self.over = True
        self.end_popup.open()

    def return_menu(self, _):
        self.medium_layout.clear_widgets()
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
            EasyMineSweepApp().run()
        elif event.text == 'Medium':
            MediumMineSweepApp().run()


if __name__ == '__main__':
    MineSweepApp().run()
