from Game import Game

# Would you like a small or medium sized game?
size = 'small'

if size == 'small':
    game = Game(80)
elif size == 'medium':
    game = Game(252)

if __name__ == '__main__':
    game.display_board()
    print(game.find_pos(7,9))
    print('\n\n')
    for i in range(10):
        print(i)
    # down four over five