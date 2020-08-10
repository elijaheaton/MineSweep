from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from Game import Game
import numpy as np


class MyButton(Button):
    def __init__(self, position, size):
        Button.__init__(self)
        self.position = position

        if size == 24:
            self.posx = int(np.floor(position / 6))
            self.posy = position % 6
        elif size == 81:
            self.posx = int(np.floor(position / 9))
            self.posy = position % 9
        else:
            self.posx = 0
            self.posy = 0


class EasyMineSweepApp(App):
    game = Game(24)

    def build(self):

        l1 = Label(text='')
        l2 = Label(text='')
        l3 = Label(text='MineSweeper')
        l4 = Label(text='Easy Level')
        l5 = Label(text='')
        l6 = Label(text='6 Bombs')

        easy_layout = GridLayout(cols=6, padding=50)
        easy_layout.add_widget(l1)
        easy_layout.add_widget(l2)
        easy_layout.add_widget(l3)
        easy_layout.add_widget(l4)
        easy_layout.add_widget(l5)
        easy_layout.add_widget(l6)

        btn = []
        for i in range(24):
            btn.append(MyButton(i, 24))
            btn[i].bind(on_press=self.reveal)
            easy_layout.add_widget(btn[i])

        return easy_layout

    def reveal(self, event):
        answer = self.game.find_pos(event.posx, event.posy)
        if answer == -1:
            event.text = 'BOOM!'
        else:
            event.text = str(answer)


class MineSweepApp(App):

    layout = GridLayout(cols=3, padding=40)

    def build(self):
        self.layout = GridLayout(cols=3, padding=40)

        l1 = Label(text='')
        l2 = Label(text='MineSweeper!')
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


if __name__ == '__main__':
    MineSweepApp().run()
