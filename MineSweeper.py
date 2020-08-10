from Game import Game

# Would you like a small or medium sized game?
size = 'small'

if size == 'small':
    game = Game(24)
elif size == 'medium':
    game = Game(81)

if __name__ == '__main__':
    game.display_board()
    print(game.find_pos(1,4))