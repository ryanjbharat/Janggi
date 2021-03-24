# Interface

import pygame
import JanggiGame

WIDTH = 600
HEIGHT = 666
DIMENSION_ROW = 10
DIMENSION_COLUMN = 9
SQ_SIZE = 66 # 475 / ((9+10)/2)
MAX_FPS = 15 # For animations
BLUE_IMAGES = {}
RED_IMAGES = {}
CODE = {'CA':'Cannon','CH':'Chariot','EL':'Elephant','GE':'General','GU':'Guard','HO':'Horse','SO':'Soldier'}
index_to_row = {0: '1', 1: '2', 2: '3', 3: '4', 4 : '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: '10'}
index_to_column = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7: 'h', 8: 'i'}

def load_images():
    pieces = ['Cannon','Chariot','Elephant','General','Guard','Horse','Soldier']
    for piece in pieces:
        BLUE_IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/Blue_"+piece+".png"), (SQ_SIZE, SQ_SIZE))
        RED_IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/Red_"+piece+".png"),(SQ_SIZE, SQ_SIZE))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    game = JanggiGame.JanggiGame()
    print(game.show_janggi_board())
    load_images()
    running = True
    sq_selected = () # No square selected, keep track of last click of user
    player_clicks = [] # Keep track of player clicks
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                sq_selected = (row, col)
                player_clicks.append(sq_selected)
                valid = game.get_all_valid_moves()
            if len(player_clicks) == 2:
                src_coord = index_to_column[player_clicks[0][1]] + index_to_row[player_clicks[0][0]]
                dst_coord = index_to_column[player_clicks[1][1]] + index_to_row[player_clicks[1][0]]
                print(src_coord, dst_coord)
                print('VALID MOVE?: ' + str(game.make_move(src_coord, dst_coord)))
                print('GAME STATE: ' + game.get_game_state())
                print('TURN: ' + game.get_player_turn())
                print('RED IN CHECK: ' + str(game.get_in_check('RED')))
                print('BLUE IN CHECK: ' + str(game.get_in_check('BLUE')))
                sq_selected = () # Reset user clicks
                player_clicks = []
        if sq_selected:
            draw_game_board(screen,game,valid,sq_selected)
        else:
            draw_game_board(screen, game)
        clock.tick(MAX_FPS)
        pygame.display.flip()

def draw_game_board(screen, game, valid_moves=None, sq_selected=None):
    """ Creates the display """
    draw_tiles(screen) # Draws the tiles
    if sq_selected:
        highlight_tiles(screen, game, valid_moves, sq_selected)
    draw_pieces(screen, game.get_janggi_board()) # draw pieces on top of the squares


def draw_tiles(screen):
    """ Draws the tiles """
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION_ROW):
        for c in range(DIMENSION_COLUMN):
            color = colors[((r+c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for r in range(DIMENSION_ROW):
        for c in range(DIMENSION_COLUMN):
            piece = board[r][c]
            if piece != []:
                piece_name = piece.get_name()
                if piece.get_player() == 'RED':
                    screen.blit(RED_IMAGES[CODE[piece_name]], pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
                if piece.get_player() == 'BLUE':
                    screen.blit(BLUE_IMAGES[CODE[piece_name]],pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


def highlight_tiles(screen, game_object, valid_moves, sq_selected):
    if game_object.get_tile_occupant(sq_selected) != []:
        r,c = sq_selected
        if game_object.get_janggi_board()[r][c].get_player() == game_object.get_player_turn():
            # highlight selected square
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # Transparency value
            s.fill(pygame.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves from that square
            s.fill(pygame.Color('yellow'))
            for move in valid_moves:
                if move.get_src_row() == r and move.get_src_col() == c:
                    screen.blit(s, (move.get_dst_col()*SQ_SIZE, move.get_dst_row()*SQ_SIZE))


if __name__ == "__main__":
    main()

