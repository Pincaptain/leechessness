from random import randint

from chess import Board, Move
from chess.engine import SimpleEngine, Limit


class Engine(object):
    """
    A class that represents a chess engine used to make
    moves, keep board state and display changes.
    """

    def __init__(self, engine_path: str) -> None:
        """
        Initialize the engine by specifying the engine path
        and creating the chess board.
        """
        super().__init__()

        self.engine = SimpleEngine.popen_uci(engine_path)
        self.board = Board()

    def new(self) -> None:
        """
        Recreate the chess board to start a new game and
        once recreated display the current board state.
        """

        self.board = Board()

        print(self.board)

    def move(self, move: str = None) -> Move:
        """
        Return an optimal move using the engine based on the 
        last played move and the current board state.
        """

        if move is not None:
            self.board.push_san(move)

        limit = Limit(time=randint(1, 5))
        result = self.engine.play(self.board, limit)

        self.board.push(result.move)

        print(self.board)

        return result.move

    def is_checkmate(self) -> bool:
        """
        Return true if the current board state represents
        a checkmate.
        """

        return self.board.is_checkmate()
