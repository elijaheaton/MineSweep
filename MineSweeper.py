from Game import Game

# Would you like a small or medium sized game?
size = 'small'

if size == 'small':
    game = Game(80)
elif size == 'medium':
    game = Game(252)

if __name__ == '__main__':
    game.display_board()