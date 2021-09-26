import time
from abc import ABC, abstractmethod

import chess
import mouse
from selenium import webdriver

from core.engine import Engine
from cfg.globals import WEBDRIVER_EXE_PATH, CHESS_COM_LOGIN_LINK, STOCKFISH_EXE_PATH
from cfg.board import get_pos
from cfg.credentials import USERNAME, PASSWORD

driver = webdriver.Chrome(executable_path=WEBDRIVER_EXE_PATH)


class ChessDriver(ABC):

    @abstractmethod
    def move_piece(self, from_square: str, to_square: str, side: str):
        pass

    @abstractmethod
    def login(self, username: str, password: str):
        pass

    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def check_side(self) -> str:
        pass

    @abstractmethod
    def start_new_game(self):
        pass

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def begin(self):
        pass


class ChessComDriver(ChessDriver):

    def move_piece(self, from_square: str, to_square: str, side: str):
        """
        Move the piece on the board using the mouse python
        package.
        """

        from_x, from_y = get_pos(side, from_square)
        to_x, to_y = get_pos(side, to_square)

        mouse.drag(from_x, from_y, to_x, to_y, duration=0.5)

    def login(self, username: str, password: str):
        """
        Login to the provided site based on the username and password.
        """

        driver.get(CHESS_COM_LOGIN_LINK)
        driver.maximize_window()
        driver.find_element_by_id('username').send_keys(username)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_id('login').click()

    def start_game(self):
        """
        Start the first chess match after logging in.
        """

        xpath = '/html/body/div[3]/div/div[2]/div/div/div[1]/div[1]/div/button'

        driver.find_element_by_xpath(xpath).click()

    def check_side(self) -> str:
        """
        Return the current playing side of the user (white/black).
        """

        css_selector = '.clock-white.clock-bottom'
        white = driver.find_elements_by_css_selector(css_selector)

        if len(white) == 0:
            return 'black'
        else:
            return 'white'

    def start_new_game(self):
        """
        Start a new game after finishing one.
        """

        time.sleep(1)

        xpath = '/html/body/div[3]/div/div[2]/div/div[5]/div[1]/button[2]'
        driver.find_element_by_xpath(xpath).click()

        while True:
            try:
                connectivity_xpath = '/html/body/div[2]/div[1]/div/div[2]/div/div[2]'
                driver.find_element_by_xpath(connectivity_xpath)

                break
            except:
                continue

        self.play()

    def play(self):
        """
        Play the ongoing chess game.
        """

        engine = Engine(STOCKFISH_EXE_PATH)
        engine.new()

        side = self.check_side()
        moves = 1

        print(f'You are playing {side}')

        if side == 'white':
            to_play = engine.move()
            from_square = chess.square_name(to_play.from_square)
            to_square = chess.square_name(to_play.to_square)

            self.move_piece(from_square, to_square, side)
            moves = 2

        while True:
            try:
                go_xpath = '/html/body/div[2]/div[2]/div[3]/div'

                driver.find_element_by_xpath(go_xpath)
                self.start_new_game()

                return
            except:
                pass

            move = None
            if side == 'white':
                try:
                    selector = f'div[data-ply="{moves}"]'
                    element = driver.find_element_by_css_selector(selector)
                    move = element.text

                    print(move)
                except:
                    time.sleep(1)
                    continue
            else:
                try:
                    selector = f'div[data-ply="{moves}"]'
                    element = driver.find_element_by_css_selector(selector)
                    move = element.text

                    print(move)
                except:
                    time.sleep(1)
                    continue

            to_play = engine.move(move)
            from_square = chess.square_name(to_play.from_square)
            to_square = chess.square_name(to_play.to_square)

            self.move_piece(from_square, to_square, side)

            if engine.is_checkmate():
                self.start_new_game()

                return

            moves += 2

    def begin(self):
        """
        Initializes and starts the drivers operations.
        """

        self.login(USERNAME, PASSWORD)
        time.sleep(8)
        self.start_game()
        time.sleep(5)
        self.play()
