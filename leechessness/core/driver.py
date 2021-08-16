import time

import chess
import mouse
from selenium import webdriver

from core.engine import Engine
from cfg.globals import WEBDRIVER_EXE_PATH, CHESS_COM_LOGIN_LINK, SITE_NOT_SUPPORTED_MESSAGE, CHESS_COM_LINK, STOCKFISH_EXE_PATH
from cfg.board import get_pos
from cfg.credentials import USERNAME, PASSWORD

driver = webdriver.Chrome(executable_path=WEBDRIVER_EXE_PATH)


def move_piece(from_square: str, to_square: str, side: str) -> None:
    """
    Move the piece on the board using the mouse python
    package.
    """

    from_x, from_y = get_pos(side, from_square)
    to_x, to_y = get_pos(side, to_square)

    mouse.drag(from_x, from_y, to_x, to_y, duration=0.5)


def login(username: str, password: str, site: str = CHESS_COM_LINK) -> None:
    """
    Login to the provided site based on the username and password.
    """

    if site == CHESS_COM_LINK:
        driver.get(CHESS_COM_LOGIN_LINK)
        driver.maximize_window()
        driver.find_element_by_id('username').send_keys(username)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_id('login').click()
    else:
        print(SITE_NOT_SUPPORTED_MESSAGE)


def start_game(site: str = CHESS_COM_LINK) -> None:
    """
    Start the first chess match after logging in.
    """

    if site == CHESS_COM_LINK:
        xpath = '/html/body/div[3]/div/div[2]/div/div/div[1]/div[1]/div/button'

        driver.find_element_by_xpath(xpath).click()
    else:
        print(SITE_NOT_SUPPORTED_MESSAGE)


def check_side(site: str = CHESS_COM_LINK) -> str:
    """
    Return the current playing side of the user (white/black).
    """

    if site == CHESS_COM_LINK:
        css_selector = '.clock-white.clock-bottom'
        white = driver.find_elements_by_css_selector(css_selector)

        if len(white) == 0:
            return 'black'
        else:
            return 'white'
    else:
        print(SITE_NOT_SUPPORTED_MESSAGE)

        return 'white'


def start_new_game(site: str = CHESS_COM_LINK) -> None:
    """
    Start a new game after finishing one.
    """

    if site == CHESS_COM_LINK:
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

        play()
    else:
        print(SITE_NOT_SUPPORTED_MESSAGE)


def play(site: str = CHESS_COM_LINK) -> None:
    """
    Play the ongoing chess game.
    """

    if site == CHESS_COM_LINK:
        engine = Engine(STOCKFISH_EXE_PATH)
        engine.new()

        side = check_side()
        moves = 1

        print(f'You are playing {side}')

        if side == 'white':
            to_play = engine.move()
            from_square = chess.square_name(to_play.from_square)
            to_square = chess.square_name(to_play.to_square)

            move_piece(from_square, to_square, side)
            moves = 2

        while True:
            try:
                go_xpath = '/html/body/div[2]/div[2]/div[3]/div'

                driver.find_element_by_xpath(go_xpath)
                start_new_game()

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

            move_piece(from_square, to_square, side)

            if engine.is_checkmate():
                start_new_game()

                return

            moves += 2
    else:
        print(SITE_NOT_SUPPORTED_MESSAGE)


def begin(site: str = CHESS_COM_LINK) -> None:
    """
    Initializes and starts the drivers operations.
    """

    if site == CHESS_COM_LINK:
        login(USERNAME, PASSWORD)
        time.sleep(8)
        start_game()
        time.sleep(5)
        play()
    else:
        print(SITE_NOT_SUPPORTED_MESSAGE)
