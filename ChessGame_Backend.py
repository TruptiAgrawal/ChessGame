class Chess:
    """
    1. Encapsulates the core rules mechanics of chess piece movements and attacks.
    2. It abstracts the logic needed to determine valid moves and attack possibilities for different piece types.
    3. Defines the behavior of each piece according to chess rules.
    """

    PIECE_VALUES = {'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 100}

    @staticmethod
    def is_valid_position(row, col):
        """Check if position is within chess board bounds."""
        return 0 <= row <= 7 and 0 <= col <= 7

    @staticmethod
    def position_to_coords(position):
        """Convert chess notation (e.g., 'e4') to row, col coordinates."""
        if len(position) != 2:
            raise ValueError("Invalid position format")
        col = ord(position[0].lower()) - ord('a')
        row = int(position[1]) - 1
        return row, col

    @staticmethod
    def coords_to_position(row, col):
        """Convert row, col coordinates to chess notation."""
        return chr(ord('a') + col) + str(row + 1)

    @classmethod
    def get_piece_moves(cls, piece_type, position, color='white'):
        """Get all possible moves for a piece at given position."""
        row, col = cls.position_to_coords(position)
        piece_type = piece_type.lower()

        moves = []

        if piece_type == 'rook':
            moves = cls._get_rook_moves(row, col)
        elif piece_type == 'bishop':
            moves = cls._get_bishop_moves(row, col)
        elif piece_type == 'queen':
            moves = cls._get_queen_moves(row, col)
        elif piece_type == 'knight':
            moves = cls._get_knight_moves(row, col)
        elif piece_type == 'king':
            moves = cls._get_king_moves(row, col)

        return [cls.coords_to_position(r, c) for r, c in moves if cls.is_valid_position(r, c)]

    @classmethod
    def _get_rook_moves(cls, row, col):
        """Get rook moves (horizontal and vertical)."""
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if cls.is_valid_position(new_row, new_col):
                    moves.append((new_row, new_col))
                else:
                    break

        return moves

    @classmethod
    def _get_bishop_moves(cls, row, col):
        """Get bishop moves (diagonal)."""
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dr, dc in directions:
            for i in range(1, 8):
                new_row, new_col = row + dr * i, col + dc * i
                if cls.is_valid_position(new_row, new_col):
                    moves.append((new_row, new_col))
                else:
                    break

        return moves

    @classmethod
    def _get_queen_moves(cls, row, col):
        """Get queen moves (combination of rook and bishop)."""
        return cls._get_rook_moves(row, col) + cls._get_bishop_moves(row, col)

    @classmethod
    def _get_knight_moves(cls, row, col):
        """Get knight moves (L-shaped)."""
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]

        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if cls.is_valid_position(new_row, new_col):
                moves.append((new_row, new_col))

        return moves

    @classmethod
    def _get_king_moves(cls, row, col):
        """Get king moves (one square in any direction)."""
        moves = []
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if cls.is_valid_position(new_row, new_col):
                moves.append((new_row, new_col))

        return moves

    @classmethod
    def can_attack(cls, piece_type, from_pos, target_pos, color='white'):
        """Check if a piece can attack a target position."""
        possible_moves = cls.get_piece_moves(piece_type, from_pos, color)
        return target_pos in possible_moves


class MyChessGame:
    """
    1. Specific scenario involving two chess pieces on the board.
    2. Manages the state of the game (black and white pieces' types and positions).
    3. Uses the Chess class to evaluate whether one piece can attack the other.
    4. Determines which piece has a higher likelihood of winning and provides possible moves accordingly.
    """

    def __init__(self, white_piece, white_pos, black_piece, black_pos):
        """Initialize game with two pieces."""
        self.white_piece = white_piece.lower()
        self.white_pos = white_pos.lower()
        self.black_piece = black_piece.lower()
        self.black_pos = black_pos.lower()
        self.chess = Chess()

    def can_white_attack_black(self):
        """Check if white piece can attack black piece."""
        return self.chess.can_attack(self.white_piece, self.white_pos, self.black_pos, 'white')

    def can_black_attack_white(self):
        """Check if black piece can attack white piece."""
        return self.chess.can_attack(self.black_piece, self.black_pos, self.white_pos, 'black')

    def get_white_moves(self):
        """Get all possible moves for white piece."""
        return self.chess.get_piece_moves(self.white_piece, self.white_pos, 'white')

    def get_black_moves(self):
        """Get all possible moves for black piece."""
        return self.chess.get_piece_moves(self.black_piece, self.black_pos, 'black')

    def determine_winner(self):
        """Determine winner based on attack potential and piece values."""
        white_value = Chess.PIECE_VALUES[self.white_piece]
        black_value = Chess.PIECE_VALUES[self.black_piece]

        white_can_attack = self.can_white_attack_black()
        black_can_attack = self.can_black_attack_white()

        # If only one can attack, they win
        if white_can_attack and not black_can_attack:
            return f"white {self.white_piece} wins"
        if black_can_attack and not white_can_attack:
            return f"black {self.black_piece} wins"

        # Otherwise, higher value piece wins
        if white_value > black_value:
            return f"white {self.white_piece} wins"
        elif black_value > white_value:
            return f"black {self.black_piece} wins"
        else:
            return "draw"

    def print_winner(self):
        """Print the winner."""
        print(self.determine_winner())


# Example usage
if __name__ == "__main__":
    # Create a game with a white queen at e4 and black knight at f6
    game = MyChessGame("Queen", "e4", "Knight", "f6")
    game.print_winner()

    game2 = MyChessGame("Rook", "a1", "Bishop", "h8")
    game2.print_winner()

    game3 = MyChessGame("Knight", "b1", "Bishop", "c8")
    game3.print_winner()
