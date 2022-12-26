import pygame
from network import Network

pygame.font.init()

# set up
WIDTH = 900
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


# main button class
class Button:
    def __init__(self, text, x, y, colour):
        # each button will be uniform
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.width = 150
        self.height = 100

    # draw method
    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("verdana", 36)
        text = font.render(self.text, True, (255, 255, 255))
        # finding centre of the button
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2), self.y + round(self.height / 2)
                        - round(text.get_height() / 2)))

    # check mouse clicked conditions
    def click(self, position):
        x1 = position[0]
        y1 = position[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


# menu button class
class Start:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


# functions
def re_draw_window(win, game, player):
    win.fill((202, 228, 241))

    if not (game.connected()):
        # other player is yet to connect
        font = pygame.font.SysFont("verdana", 40)
        text = font.render("Waiting for the other player to connect", True, (0, 0, 139))
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("verdana", 40)
        text = font.render("Your Move", True, (0, 0, 139))
        win.blit(text, (80, 50))

        text = font.render("Opponent's", True, (0, 0, 139))
        win.blit(text, (560, 50))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.both_went():
            text1 = font.render(move1, True, (0, 0, 139))
            text2 = font.render(move2, True, (0, 0, 139))
        else:
            # check if we need to hide opponents move
            if game.p1_went and player == 0:
                text1 = font.render(move1, True, (0, 102, 102))
            elif game.p1_went:
                text1 = font.render("Ready", True, (0, 102, 102))
            else:
                text1 = font.render("Waiting...", True, (0, 102, 102))

            if game.p2_went and player == 1:
                text2 = font.render(move2, True, (0, 102, 102))
            elif game.p2_went:
                text2 = font.render("Ready", True, (0, 102, 102))
            else:
                text2 = font.render("Waiting...", True, (0, 102, 102))

        # render text on screen
        if player == 1:
            win.blit(text2, (80, 150))
            win.blit(text1, (560, 150))
        else:
            win.blit(text1, (80, 150))
            win.blit(text2, (560, 150))

        for button in buttons:
            button.draw(win)

    pygame.display.update()


buttons = [Button("Rock", 50, 350, (51, 102, 0)), Button("Scissors", 350, 350, (0, 51, 102)),
           Button("Paper", 650, 350, (102, 0, 51))]


def main():
    run = True
    clock = pygame.time.Clock()
    # importing network
    network = Network()
    # return player ID
    player = int(network.get_player())
    print("You are player number: {}".format(player))

    while run:
        clock.tick(60)
        try:
            game = network.send("get")
        except:
            run = False
            print("Could not retrieve game from server - game failed locally")
            break

        if game.both_went():
            # draw player moves
            re_draw_window(window, game, player)
            pygame.time.delay(500)
            try:
                # server resets once both players have picked to reset round
                game = network.send("reset")
            except:
                run = False
                print("Could not retrieve game from server")
                break

            # conditions for win/loss/draw
            font = pygame.font.SysFont("verdana", 50)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Win!", True, (34, 139, 34))
                print("You Win!")
            elif game.winner() == -1:
                text = font.render("Draw!", True, (0, 102, 102))
                print("Draw!")
            else:
                text = font.render("You Lose!", True, (178, 34, 34))
                print("You Lose!")

            # around the middle of the screen
            window.blit(text, (WIDTH / 2 - text.get_width() / 2, 180))
            pygame.display.update()
            # delay during win/loss screen
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(position) and game.connected():
                        if player == 0:
                            if not game.p1_went:
                                # check if player has not made a move
                                # if not, send move to server
                                network.send(button.text)
                        else:
                            if not game.p2_went:
                                # check if player has not made a move
                                # if not, send move to server
                                network.send(button.text)

        re_draw_window(window, game, player)


# main menu function
def menu_screen():
    run = True
    clock = pygame.time.Clock()
    # loading imagine and creating instance
    play_img = pygame.image.load("play.png").convert_alpha()
    play_button = Start(450, 250, play_img, 1)

    # runs main function if button is pressed
    while run:
        clock.tick(60)
        window.fill((202, 228, 241))
        play_button.draw(window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                run = False

    main()


while True:
    menu_screen()
