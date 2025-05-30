import tkinter as tk
from tkinter import messagebox
import math

class Chess:
    """
    Chess logic from the original code
    """
    PIECE_VALUES = {
        'knight': 3, 'bishop': 3,
        'rook': 5, 'queen': 9, 'king': 100
    }

    @staticmethod
    def is_valid_position(row, col):
        return 0 <= row <= 7 and 0 <= col <= 7

    @staticmethod
    def position_to_coords(position):
        if len(position) != 2:
            raise ValueError("Invalid position format")
        col = ord(position[0].lower()) - ord('a')
        row = int(position[1]) - 1
        return row, col

    @staticmethod
    def coords_to_position(row, col):
        return chr(ord('a') + col) + str(row + 1)

    @classmethod
    def get_piece_moves(cls, piece_type, position, color='white'):
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
        return cls._get_rook_moves(row, col) + cls._get_bishop_moves(row, col)

    @classmethod
    def _get_knight_moves(cls, row, col):
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
        possible_moves = cls.get_piece_moves(piece_type, from_pos, color)
        return target_pos in possible_moves


class ChessGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Chess Piece Game")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        self.chess = Chess()
        self.board_pieces = {}  # {(row, col): {'piece': 'queen', 'color': 'white'}}
        self.selected_piece = None
        self.dragging = False
        self.drag_data = {}
        self.piece_buttons = []  # Store button references
        self.dragging_piece = None
        self.drag_start_pos = None
        
        self.setup_start_screen()
    
    def setup_start_screen(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        title_label = tk.Label(self.root, text="Chess Piece Battle", 
                              font=('Arial', 32, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(pady=50)
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="Drag and drop chess pieces onto the board\nSee which pieces can attack each other!", 
                               font=('Arial', 16), 
                               fg='#ecf0f1', bg='#2c3e50')
        instructions.pack(pady=20)
        
        # Start button
        start_btn = tk.Button(self.root, text="START GAME", 
                             font=('Arial', 20, 'bold'),
                             bg='#e74c3c', fg='white',
                             padx=40, pady=15,
                             command=self.start_game)
        start_btn.pack(pady=30)
    
    def start_game(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.setup_game_screen()
    
    def setup_game_screen(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel for pieces
        left_panel = tk.Frame(main_frame, bg='#34495e', width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Title for piece selection
        piece_title = tk.Label(left_panel, text="Chess Pieces", 
                              font=('Arial', 16, 'bold'),
                              fg='white', bg='#34495e')
        piece_title.pack(pady=10)
        
        # Create piece buttons
        self.create_piece_buttons(left_panel)
        
        # Right panel for board and controls
        right_panel = tk.Frame(main_frame, bg='#2c3e50')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Control buttons
        control_frame = tk.Frame(right_panel, bg='#2c3e50')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        analyze_btn = tk.Button(control_frame, text="Analyze Position", 
                               font=('Arial', 12, 'bold'),
                               bg='#3498db', fg='white',
                               command=self.analyze_position)
        analyze_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = tk.Button(control_frame, text="Clear Board", 
                             font=('Arial', 12, 'bold'),
                             bg='#e67e22', fg='white',
                             command=self.clear_board)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        back_btn = tk.Button(control_frame, text="Back to Menu", 
                            font=('Arial', 12, 'bold'),
                            bg='#95a5a6', fg='white',
                            command=self.setup_start_screen)
        back_btn.pack(side=tk.RIGHT)
        
        # Create the chess board
        self.create_board(right_panel)
        
        # Analysis display
        self.analysis_text = tk.Text(right_panel, height=8, width=60,
                                    font=('Courier', 10),
                                    bg='#ecf0f1', fg='#2c3e50')
        self.analysis_text.pack(fill=tk.X, pady=(10, 0))
    
    def create_piece_buttons(self, parent):
        pieces = ['queen', 'rook', 'bishop', 'knight', 'king']
        colors = ['white', 'black']
        
        # Unicode chess symbols
        piece_symbols = {
            'king': {'white': '♔', 'black': '♚'},
            'queen': {'white': '♕', 'black': '♛'},
            'rook': {'white': '♖', 'black': '♜'},
            'bishop': {'white': '♗', 'black': '♝'},
            'knight': {'white': '♘', 'black': '♞'},
        }
        
        for color in colors:
            color_frame = tk.Frame(parent, bg='#34495e')
            color_frame.pack(fill=tk.X, pady=5)
            
            color_label = tk.Label(color_frame, text=f"{color.title()} Pieces", 
                                  font=('Arial', 12, 'bold'),
                                  fg='white' if color == 'white' else '#bdc3c7', 
                                  bg='#34495e')
            color_label.pack()
            
            for piece in pieces:
                symbol = piece_symbols[piece][color]
                btn = tk.Button(color_frame, text=f"{symbol} {piece.title()}", 
                               font=('Arial', 14),
                               bg='white' if color == 'white' else '#2c3e50',
                               fg='black' if color == 'white' else 'white',
                               width=15)
                # Store button reference
                self.piece_buttons.append(btn)
                btn.configure(command=lambda p=piece, c=color, b=btn: self.select_piece(p, c, b))
                # Add drag and drop functionality to buttons
                btn.bind("<Button-1>", lambda e, p=piece, c=color: self.start_drag_from_button(e, p, c))
                btn.bind("<B1-Motion>", self.drag_piece)
                btn.bind("<ButtonRelease-1>", self.drop_piece)
                btn.pack(pady=2)
    
    def select_piece(self, piece, color, button):
        # Reset all button reliefs first
        for btn in self.piece_buttons:
            btn.config(relief='raised')
        
        self.selected_piece = {'piece': piece, 'color': color}
        button.config(relief='sunken')
        print(f"Selected: {color} {piece}")  # Debug feedback
    
    def create_board(self, parent):
        self.board_frame = tk.Frame(parent, bg='#2c3e50')
        self.board_frame.pack()
        
        self.canvas = tk.Canvas(self.board_frame, width=480, height=480, 
                               bg='#ecf0f1', highlightthickness=2, 
                               highlightbackground='#34495e')
        self.canvas.pack()
        
        # Draw the chess board
        self.draw_board()
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # Allow dropping on canvas
        self.canvas.bind("<Motion>", self.on_canvas_motion)
    
    def draw_board(self):
        self.canvas.delete("all")
        
        # Draw squares
        for row in range(8):
            for col in range(8):
                x1, y1 = col * 60, row * 60
                x2, y2 = x1 + 60, y1 + 60
                
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#8b4513")
        
        # Draw pieces
        piece_symbols = {
            'king': {'white': '♔', 'black': '♚'},
            'queen': {'white': '♕', 'black': '♛'},
            'rook': {'white': '♖', 'black': '♜'},
            'bishop': {'white': '♗', 'black': '♝'},
            'knight': {'white': '♘', 'black': '♞'},
        }
        
        for (row, col), piece_info in self.board_pieces.items():
            x, y = col * 60 + 30, row * 60 + 30
            symbol = piece_symbols[piece_info['piece']][piece_info['color']]
            color = 'black' if piece_info['color'] == 'black' else '#2c3e50'
            
            self.canvas.create_text(x, y, text=symbol, font=('Arial', 36), 
                                   fill=color, tags=f"piece_{row}_{col}")
        
        # Draw coordinates
        for i in range(8):
            # Column labels (a-h)
            self.canvas.create_text(i * 60 + 30, 490, text=chr(ord('a') + i), 
                                   font=('Arial', 10), fill='#2c3e50')
            # Row labels (1-8)
            self.canvas.create_text(490, (7-i) * 60 + 30, text=str(i + 1), 
                                   font=('Arial', 10), fill='#2c3e50')
    
    def start_drag_from_button(self, event, piece, color):
        """Start dragging a piece from the button panel"""
        self.dragging_piece = {'piece': piece, 'color': color}
        self.drag_start_pos = (event.x_root, event.y_root)
        self.dragging = True
        
        # Create a temporary label to show what's being dragged
        piece_symbols = {
            'king': {'white': '♔', 'black': '♚'},
            'queen': {'white': '♕', 'black': '♛'},
            'rook': {'white': '♖', 'black': '♜'},
            'bishop': {'white': '♗', 'black': '♝'},
            'knight': {'white': '♘', 'black': '♞'},
        }
        
        if hasattr(self, 'drag_label'):
            self.drag_label.destroy()
        
        self.drag_label = tk.Label(self.root, 
                                  text=piece_symbols[piece][color],
                                  font=('Arial', 36),
                                  fg='red',
                                  bg='white',
                                  relief='raised',
                                  bd=2)
        self.drag_label.place(x=event.x_root - self.root.winfo_rootx(), 
                             y=event.y_root - self.root.winfo_rooty())
        self.drag_label.lift()
    
    def drag_piece(self, event):
        """Update position of dragged piece"""
        if self.dragging and hasattr(self, 'drag_label'):
            self.drag_label.place(x=event.x_root - self.root.winfo_rootx() - 20, 
                                 y=event.y_root - self.root.winfo_rooty() - 20)
    
    def drop_piece(self, event):
        """Handle dropping a piece"""
        if not self.dragging:
            return
            
        # Get canvas coordinates
        canvas_x = event.x_root - self.canvas.winfo_rootx()
        canvas_y = event.y_root - self.canvas.winfo_rooty()
        
        # Check if dropped on canvas
        if (0 <= canvas_x <= self.canvas.winfo_width() and 
            0 <= canvas_y <= self.canvas.winfo_height()):
            
            # Convert to board coordinates
            col = int(canvas_x // 60)
            row = int(canvas_y // 60)
            
            if 0 <= row < 8 and 0 <= col < 8:
                # Place the piece
                self.board_pieces[(row, col)] = self.dragging_piece.copy()
                self.draw_board()
        
        # Clean up
        if hasattr(self, 'drag_label'):
            self.drag_label.destroy()
        self.dragging = False
        self.dragging_piece = None
    
    def on_canvas_click(self, event):
        """Handle clicking on existing pieces on the board"""
        col = event.x // 60
        row = event.y // 60
        
        if 0 <= row < 8 and 0 <= col < 8:
            if (row, col) in self.board_pieces:
                # Start dragging existing piece
                self.dragging_piece = self.board_pieces[(row, col)].copy()
                self.drag_start_board_pos = (row, col)
                self.dragging = True
                
                # Remove piece from board temporarily
                del self.board_pieces[(row, col)]
                self.draw_board()
                
                # Create drag label
                piece_symbols = {
                    'king': {'white': '♔', 'black': '♚'},
                    'queen': {'white': '♕', 'black': '♛'},
                    'rook': {'white': '♖', 'black': '♜'},
                    'bishop': {'white': '♗', 'black': '♝'},
                    'knight': {'white': '♘', 'black': '♞'},
                }
                
                if hasattr(self, 'drag_label'):
                    self.drag_label.destroy()
                
                self.drag_label = tk.Label(self.root, 
                                          text=piece_symbols[self.dragging_piece['piece']][self.dragging_piece['color']],
                                          font=('Arial', 36),
                                          fg='red',
                                          bg='white',
                                          relief='raised',
                                          bd=2)
                self.drag_label.place(x=event.x + self.canvas.winfo_x(), 
                                     y=event.y + self.canvas.winfo_y())
                self.drag_label.lift()
    
    def on_canvas_motion(self, event):
        """Handle mouse motion over canvas"""
        if self.dragging and hasattr(self, 'drag_label'):
            self.drag_label.place(x=event.x + self.canvas.winfo_x() - 20, 
                                 y=event.y + self.canvas.winfo_y() - 20)
    
    def on_drag(self, event):
        """Handle dragging motion"""
        if self.dragging and hasattr(self, 'drag_label'):
            self.drag_label.place(x=event.x + self.canvas.winfo_x() - 20, 
                                 y=event.y + self.canvas.winfo_y() - 20)
    
    def on_release(self, event):
        """Handle mouse release on canvas"""
        if not self.dragging:
            return
            
        col = event.x // 60
        row = event.y // 60
        
        if 0 <= row < 8 and 0 <= col < 8:
            # Place the piece
            self.board_pieces[(row, col)] = self.dragging_piece.copy()
        elif hasattr(self, 'drag_start_board_pos'):
            # Return piece to original position if dropped outside board
            self.board_pieces[self.drag_start_board_pos] = self.dragging_piece.copy()
        
        # Clean up
        if hasattr(self, 'drag_label'):
            self.drag_label.destroy()
        if hasattr(self, 'drag_start_board_pos'):
            delattr(self, 'drag_start_board_pos')
        
        self.dragging = False
        self.dragging_piece = None
        self.draw_board()
    
    def clear_board(self):
        self.board_pieces.clear()
        self.draw_board()
    
    def analyze_position(self):
        if len(self.board_pieces) < 2:
            messagebox.showinfo("Not Enough Pieces", "Place at least 2 pieces on the board to analyze!")
            return
        
        analysis_text = "=== CHESS POSITION ANALYSIS ===\n\n"
        
        # List all pieces
        pieces_by_color = {'white': [], 'black': []}
        for (row, col), piece_info in self.board_pieces.items():
            pos = self.chess.coords_to_position(row, col)
            pieces_by_color[piece_info['color']].append({
                'piece': piece_info['piece'],
                'position': pos,
                'coords': (row, col)
            })
        
        analysis_text += f"White pieces: {len(pieces_by_color['white'])}\n"
        for piece in pieces_by_color['white']:
            analysis_text += f"  {piece['piece'].title()} at {piece['position']}\n"
        
        analysis_text += f"\nBlack pieces: {len(pieces_by_color['black'])}\n"
        for piece in pieces_by_color['black']:
            analysis_text += f"  {piece['piece'].title()} at {piece['position']}\n"
        
        # Analyze attacks
        analysis_text += "\n=== ATTACK ANALYSIS ===\n"
        white_attacks = 0
        black_attacks = 0
        
        for white_piece in pieces_by_color['white']:
            for black_piece in pieces_by_color['black']:
                if self.chess.can_attack(white_piece['piece'], white_piece['position'], 
                                       black_piece['position'], 'white'):
                    analysis_text += f"White {white_piece['piece']} at {white_piece['position']} can attack Black {black_piece['piece']} at {black_piece['position']}\n"
                    white_attacks += 1
        
        for black_piece in pieces_by_color['black']:
            for white_piece in pieces_by_color['white']:
                if self.chess.can_attack(black_piece['piece'], black_piece['position'], 
                                       white_piece['position'], 'black'):
                    analysis_text += f"Black {black_piece['piece']} at {black_piece['position']} can attack White {white_piece['piece']} at {white_piece['position']}\n"
                    black_attacks += 1
        
        if white_attacks == 0 and black_attacks == 0:
            analysis_text += "No pieces can attack each other.\n"
        
        # Calculate material advantage
        white_value = sum(self.chess.PIECE_VALUES[p['piece']] for p in pieces_by_color['white'])
        black_value = sum(self.chess.PIECE_VALUES[p['piece']] for p in pieces_by_color['black'])
        
        analysis_text += f"\n=== MATERIAL COUNT ===\n"
        analysis_text += f"White total value: {white_value}\n"
        analysis_text += f"Black total value: {black_value}\n"
        
        if white_value > black_value:
            analysis_text += f"White has material advantage: +{white_value - black_value}\n"
        elif black_value > white_value:
            analysis_text += f"Black has material advantage: +{black_value - white_value}\n"
        else:
            analysis_text += "Material is equal\n"
        
        # Determine winner
        analysis_text += f"\n=== WINNER PREDICTION ===\n"
        if white_attacks > black_attacks:
            analysis_text += "White has tactical advantage (more attacks)\n"
        elif black_attacks > white_attacks:
            analysis_text += "Black has tactical advantage (more attacks)\n"
        
        if white_value > black_value and white_attacks >= black_attacks:
            analysis_text += "🏆 WHITE IS LIKELY TO WIN\n"
        elif black_value > white_value and black_attacks >= white_attacks:
            analysis_text += "🏆 BLACK IS LIKELY TO WIN\n"
        else:
            analysis_text += "🤝 POSITION IS ROUGHLY EQUAL\n"
        
        # Display analysis
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, analysis_text)


def main():
    root = tk.Tk()
    game = ChessGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
