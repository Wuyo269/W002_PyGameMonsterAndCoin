# ------------------------------------------
# Build in modules
# ------------------------------------------
import random
# ------------------------------------------
# 3rd party modules (installation needed)
# ------------------------------------------
import pygame
# ------------------------------------------
# Custom modules
# ------------------------------------------
None


class Figure():
    def __init__(self, image, pos_x: int, pos_y: int, window_width: int, window_height: int) -> None:
        self.image = image
        self.points = 0
        self.velocity_points = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity = 1
        self.to_left = False
        self.to_right = False
        self.to_up = False
        self.to_down = False
        self.window_width = window_width
        self.window_height = window_height

    def add_points(self, points: int) -> None:
        """
        Increment points and velocity points
        Parameters
        ----------
        points: Number of points to add

        Returns None
        -------
        """
        self.points += points
        self.velocity_points += points

    def reset_velocity_points(self):
        self.velocity_points = 0

    def increment_velocity_by_one(self):
        self.velocity += 1

    def move(self, x, y) -> None:
        """
        Move figure on screen. Make sure that figure does not go out the screen
        Parameters
        ----------
        x: value used to move on x-axis
        y: value used to move on y-axis

        Returns None
        -------
        """
        # Move figure
        self.pos_x += x
        self.pos_y += y

        # Make sure that figure is not outside the screen
        if self.pos_x < 0:
            self.pos_x = 0
        if self.pos_y < 0:
            self.pos_y = 0

        if self.pos_x > (self.window_width - self.image.get_width()):
            self.pos_x = self.window_width - self.image.get_width()
        if self.pos_y > (self.window_height - self.image.get_height()):
            self.pos_y = self.window_height - self.image.get_height()

    def is_blocked(self) -> None:
        """
        Check if figure is blocked. It reaches the screen edge.
        Returns None
        -------
        """
        # set default value
        blocked = False

        # Check every side of the screen
        if (self.pos_x <= 0 or self.pos_x >= (self.window_width - self.image.get_width())
                or self.pos_y <= 0 or self.pos_y >= (self.window_height - self.image.get_height())):
            blocked = True

        return blocked


class MyGame:
    def __init__(self) -> None:
        pygame.init()

        # game settings
        self.monsters_number = 4
        self.coins_number = 5
        self.points_to_win = 50

        # Game properties
        self.run_game = False
        self.action_per_second = 120
        self.window_height = 640
        self.window_width = 640
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("KaToRga")

        # Prepare Game
        self.images = []
        self.coins = []
        self.monsters = []
        self.load_images()
        self.create_monsters()
        self.create_sprite()

        # Run Game
        self.main_loop()

    def check_events(self) -> None:
        """
        Method contains logic for keys used by user.
        Returns None
        -------
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.sprite.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.sprite.to_right = True
                if event.key == pygame.K_UP:
                    self.sprite.to_up = True
                if event.key == pygame.K_DOWN:
                    self.sprite.to_down = True
                if event.key == pygame.K_F2:
                    self.run_game = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.sprite.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.sprite.to_right = False
                if event.key == pygame.K_UP:
                    self.sprite.to_up = False
                if event.key == pygame.K_DOWN:
                    self.sprite.to_down = False

            if event.type == pygame.QUIT:
                exit()

    def load_images(self) -> None:
        """
        Load images to list
        Returns None
        -------
        """

        for name in ["robot", "monster", "door", "coin"]:
            self.images.append(pygame.image.load(f"{name}.png"))

    def create_sprite(self) -> None:
        """
        Create main character.
        Returns None
        -------
        """
        self.sprite = Figure(self.images[0], self.window_width / 2, self.window_height / 2, self.window_width,
                             self.window_height)

    def create_coins(self) -> None:
        """
        Coins appear randomly in time and space. The max number of coins available in game is restricted by variable 'self.coins_number'.
        Returns None
        -------
        """
        if random.randint(1, 10000) > 9900 and len(self.coins) < self.coins_number:
            x_temp = random.randint(0, self.window_width - self.images[3].get_width())
            y_temp = random.randint(0, self.window_height - self.images[3].get_height())
            self.coins.append(Figure(self.images[3], x_temp, y_temp, self.window_width, self.window_height))

    def create_monsters(self) -> None:
        """
        Create monsters. Monster are located at the beginning of the game away from the main character.
        Set up move direction fo monsters.
        The number of monster in the game is restricted by variable 'self.monsters_number'
        Returns None
        -------
        """
        # Create monsters
        for i in range(self.monsters_number):
            x_temp = random.randint(0, self.window_width - self.images[1].get_width())
            y_temp = random.randint(0, self.window_height - self.images[1].get_height())
            while x_temp in range(int(self.window_width / 2 - 100),
                                  int(self.window_width / 2 + 100)) and y_temp in range(
                int(self.window_height / 2 - 100), int(self.window_height / 2 + 100)):
                x_temp = random.randint(0, self.window_width - self.images[1].get_width())
                y_temp = random.randint(0, self.window_height - self.images[1].get_height())

            self.monsters.append(Figure(self.images[1], x_temp, y_temp, self.window_width, self.window_height))
        # Set up direction for monster
        for m in self.monsters:
            self.set_up_direction(m)

    def set_up_direction(self, figure: Figure) -> None:
        """
        Set up randomly the direction of figure
        Parameters
        ----------
        figure: Figure object

        Returns None
        -------
        """
        # Create random number between 1 and 4
        random_number = random.randint(1, 4)
        # Set up direction
        if random_number == 1:
            figure.to_left = True
            figure.to_right = False
            figure.to_up = False
            figure.to_down = False
        elif random_number == 2:
            figure.to_left = False
            figure.to_right = True
            figure.to_up = False
            figure.to_down = False
        elif random_number == 3:
            figure.to_left = False
            figure.to_right = False
            figure.to_up = True
            figure.to_down = False
        elif random_number == 4:
            figure.to_left = False
            figure.to_right = False
            figure.to_up = False
            figure.to_down = True

    def move(self, figure: Figure, speed: int) -> None:
        """
        Move figure by provided number of pixels
        Parameters
        ----------
        figure: Figure type object
        speed: number of pixels to move

        Returns None
        -------
        """
        if figure.to_right:
            figure.move(speed, 0)
        if figure.to_left:
            figure.move(-speed, 0)
        if figure.to_up:
            figure.move(0, -speed)
        if figure.to_down:
            figure.move(0, speed)

    def move_monsters(self) -> None:
        """
        Move all monsters. Randomly change monster direction.
        Chances for changing direction 50 / 10 000.
        Returns None
        -------
        """
        for m in self.monsters:
            self.move(m, m.velocity)
            if m.is_blocked():
                self.set_up_direction(m)
            if random.randint(1, 10000) > 9950:
                self.set_up_direction(m)

    def gather_coins(self) -> None:
        """
        #Check if coins are touched by main character or monster.
        If figure touch the coin add its points and delete coin
        Returns None
        -------
        """
        self.delete_list = []
        # Loop through every coin
        for c in self.coins:
            # Check if sprite touched the coin
            if self.objects_toched(self.sprite, c):
                self.sprite.add_points(1)
                self.delete_list = [c]
            # Check if monsters touched the coin
            else:
                for m in self.monsters:
                    if self.objects_toched(c, m):
                        m.add_points(1)
                        self.delete_list = [c]

        # Remove coins listed in delete list
        for c in self.delete_list:
            self.coins.remove(c)

    def raise_velocity(self, figure: Figure, points_threshold: int) -> None:
        """
        Check if figure reach a threshold and if yes raise its velocity.
        Parameters
        ----------
        figure: Figure type object
        points_threshold: Threshold points to rais figure velocity

        Returns None
        -------
        """
        if figure.velocity_points >= points_threshold:
            figure.increment_velocity_by_one()
            figure.reset_velocity_points()

    def check_velocity_points(self) -> None:
        """
        Check velocity Points for each figure.
        Returns None
        -------
        """
        self.raise_velocity(self.sprite, 10)
        for m in self.monsters:
            self.raise_velocity(m, 5)

    def objects_toched(self, object_one: Figure, object_two: Figure) -> bool:
        """
        #Check if 2 objects touch each other
        Parameters
        ----------
        object_one: Figure type object
        object_two: Figure type object

        Returns True / False
        -------
        """
        x_object_one_range = range(int(object_one.pos_x), int(object_one.pos_x) + object_one.image.get_width())
        x_object_two_range = range(int(object_two.pos_x), int(object_two.pos_x) + object_two.image.get_width())
        x_object_one_set = set(x_object_one_range)

        y_object_one_range = range(int(object_one.pos_y), int(object_one.pos_y) + object_one.image.get_height())
        y_object_two_range = range(int(object_two.pos_y), int(object_two.pos_y) + object_two.image.get_height())
        y_object_one_set = set(y_object_one_range)

        if len(x_object_one_set.intersection(x_object_two_range)) > 0 and len(
                y_object_one_set.intersection(y_object_two_range)) > 0:
            return True
        else:
            return False

    def end_game(self) -> None:
        """
        If monster touches the main character the game is over.
        Returns None
        -------
        """
        for m in self.monsters:
            if self.objects_toched(m, self.sprite):
                return True
        return False

    def game_solved(self) -> bool:
        """
        If the main character gather sufficient number of points
        Returns None
        -------
        """
        if self.sprite.points >= self.points_to_win:
            return True
        else:
            return False

    def draw_information(self, text: str) -> None:
        """
        Display information on screen
        Parameters
        ----------
        text: Information to display

        Returns None
        -------
        """
        game_text = self.game_font.render(text, True, (255, 0, 0))
        game_text_x = self.window_width / 2 - game_text.get_width() / 2
        game_text_y = self.window_height / 2 - game_text.get_height() / 2
        pygame.draw.rect(self.window, (0, 0, 0),
                         (game_text_x, game_text_y, game_text.get_width(), game_text.get_height()))
        self.window.blit(game_text, (game_text_x, game_text_y))

    def draw_window(self) -> None:
        """
        #Display the game
        Returns None
        -------
        """
        self.window.fill((255, 255, 255))
        if not self.run_game:
            # Display beginning message
            self.draw_information(f"You need to get {self.points_to_win} points. Press F2 to start.")
        elif self.game_solved():
            # Display winning information
            self.draw_information("Congratulations, you won the game!")
        elif self.end_game():
            # Display information about end of game
            self.draw_information(f"Game over! Your points {self.sprite.points}/{self.points_to_win}")
        else:
            # Display main character
            self.window.blit(self.sprite.image, (self.sprite.pos_x, self.sprite.pos_y))
            # Display monsters
            for m in self.monsters:
                self.window.blit(self.images[1], (m.pos_x, m.pos_y))
            # Display coins
            for c in self.coins:
                self.window.blit(c.image, (c.pos_x, c.pos_y))
            # Display information about points
            textsurface = self.game_font.render(f"Points: {self.sprite.points}/ {self.points_to_win}", False,
                                                (0, 0, 0))  # "text", antialias, color
            self.window.blit(textsurface, (500, 10))
        pygame.display.flip()

    def main_loop(self)-> None:
        """
        Run game constantly.
        Returns None
        -------
        """
        while True:
            self.check_events()
            if not self.game_solved() and not self.end_game():
                if self.run_game:
                    self.move(self.sprite, self.sprite.velocity)
                    self.create_coins()
                    self.gather_coins()
                    self.move_monsters()
                    self.check_velocity_points()
                self.draw_window()

                # Perform 60 action per sec
                self.clock.tick(self.action_per_second)


if __name__ == "__main__":
    # Run game
    MyGame()
