#cmd 
#pip install pygame 
import random
import tkinter as tk

CELL_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
SIDE_PANEL_WIDTH = 180
WIDTH = BOARD_WIDTH * CELL_SIZE + SIDE_PANEL_WIDTH
HEIGHT = BOARD_HEIGHT * CELL_SIZE
DROP_DELAY_MS = 500
FAST_DROP_DELAY_MS = 50

SHAPES = {
    "I": [
        [[0, 0], [1, 0], [2, 0], [3, 0]],
        [[2, -1], [2, 0], [2, 1], [2, 2]],
    ],
    "O": [
        [[1, 0], [2, 0], [1, 1], [2, 1]],
    ],
    "T": [
        [[1, 0], [0, 1], [1, 1], [2, 1]],
        [[1, 0], [1, 1], [2, 1], [1, 2]],
        [[0, 1], [1, 1], [2, 1], [1, 2]],
        [[1, 0], [0, 1], [1, 1], [1, 2]],
    ],
    "S": [
        [[1, 0], [2, 0], [0, 1], [1, 1]],
        [[1, 0], [1, 1], [2, 1], [2, 2]],
    ],
    "Z": [
        [[0, 0], [1, 0], [1, 1], [2, 1]],
        [[2, 0], [1, 1], [2, 1], [1, 2]],
    ],
    "J": [
        [[0, 0], [0, 1], [1, 1], [2, 1]],
        [[1, 0], [2, 0], [1, 1], [1, 2]],
        [[0, 1], [1, 1], [2, 1], [2, 2]],
        [[1, 0], [1, 1], [0, 2], [1, 2]],
    ],
    "L": [
        [[2, 0], [0, 1], [1, 1], [2, 1]],
        [[1, 0], [1, 1], [1, 2], [2, 2]],
        [[0, 1], [1, 1], [2, 1], [0, 2]],
        [[0, 0], [1, 0], [1, 1], [1, 2]],
    ],
}

COLORS = {
    "I": "#00d9ff",
    "O": "#ffd400",
    "T": "#b85cff",
    "S": "#61e65c",
    "Z": "#ff5a5a",
    "J": "#4f7bff",
    "L": "#ff9b3d",
}


class TetrisGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tetris")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#101418", highlightthickness=0)
        self.canvas.pack()

        self.board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.current_piece = None
        self.next_piece = self.random_piece()
        self.drop_delay = DROP_DELAY_MS

        self.bind_keys()
        self.spawn_piece()
        self.tick()
        self.draw()

    def bind_keys(self) -> None:
        self.root.bind("<Left>", lambda event: self.move(-1, 0))
        self.root.bind("<Right>", lambda event: self.move(1, 0))
        self.root.bind("<Down>", lambda event: self.soft_drop())
        self.root.bind("<Up>", lambda event: self.rotate())
        self.root.bind("<space>", lambda event: self.hard_drop())
        self.root.bind("r", lambda event: self.reset())
        self.root.bind("R", lambda event: self.reset())

    def random_piece(self):
        kind = random.choice(list(SHAPES))
        return {"kind": kind, "rotation": 0, "x": 3, "y": 0}

    def piece_cells(self, piece):
        shape = SHAPES[piece["kind"]][piece["rotation"] % len(SHAPES[piece["kind"]])]
        return [(piece["x"] + dx, piece["y"] + dy) for dx, dy in shape]

    def valid_position(self, piece) -> bool:
        for x, y in self.piece_cells(piece):
            if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                return False
            if y >= 0 and self.board[y][x] is not None:
                return False
        return True

    def spawn_piece(self) -> None:
        self.current_piece = self.next_piece
        self.next_piece = self.random_piece()
        self.current_piece["x"] = 3
        self.current_piece["y"] = 0
        self.current_piece["rotation"] = 0
        if not self.valid_position(self.current_piece):
            self.game_over = True

    def move(self, dx: int, dy: int) -> bool:
        if self.game_over:
            return False
        candidate = dict(self.current_piece)
        candidate["x"] += dx
        candidate["y"] += dy
        if self.valid_position(candidate):
            self.current_piece = candidate
            self.draw()
            return True
        return False

    def rotate(self) -> None:
        if self.game_over:
            return
        candidate = dict(self.current_piece)
        candidate["rotation"] = (candidate["rotation"] + 1) % len(SHAPES[candidate["kind"]])
        for shift_x in (0, -1, 1, -2, 2):
            trial = dict(candidate)
            trial["x"] += shift_x
            if self.valid_position(trial):
                self.current_piece = trial
                self.draw()
                return

    def soft_drop(self) -> None:
        if self.game_over:
            return
        if not self.move(0, 1):
            self.lock_piece()

    def hard_drop(self) -> None:
        if self.game_over:
            return
        while self.move(0, 1):
            self.score += 1
        self.lock_piece()

    def lock_piece(self) -> None:
        for x, y in self.piece_cells(self.current_piece):
            if y >= 0:
                self.board[y][x] = self.current_piece["kind"]
        cleared = self.clear_lines()
        if cleared:
            self.lines += cleared
            self.score += [0, 100, 300, 500, 800][cleared] * self.level
            self.level = 1 + self.lines // 10
            self.drop_delay = max(100, DROP_DELAY_MS - (self.level - 1) * 40)
        self.spawn_piece()
        self.draw()

    def clear_lines(self) -> int:
        new_board = [row for row in self.board if any(cell is None for cell in row)]
        cleared = BOARD_HEIGHT - len(new_board)
        while len(new_board) < BOARD_HEIGHT:
            new_board.insert(0, [None for _ in range(BOARD_WIDTH)])
        self.board = new_board
        return cleared

    def tick(self) -> None:
        if not self.game_over:
            if not self.move(0, 1):
                self.lock_piece()
        self.draw()
        self.root.after(self.drop_delay, self.tick)

    def reset(self) -> None:
        self.board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.drop_delay = DROP_DELAY_MS
        self.next_piece = self.random_piece()
        self.spawn_piece()
        self.draw()

    def draw_block(self, x: int, y: int, color: str) -> None:
        px = x * CELL_SIZE
        py = y * CELL_SIZE
        self.canvas.create_rectangle(px + 1, py + 1, px + CELL_SIZE - 1, py + CELL_SIZE - 1, fill=color, outline="#0b0f12")

    def draw_grid(self) -> None:
        for x in range(BOARD_WIDTH + 1):
            px = x * CELL_SIZE
            self.canvas.create_line(px, 0, px, HEIGHT, fill="#1f2a33")
        for y in range(BOARD_HEIGHT + 1):
            py = y * CELL_SIZE
            self.canvas.create_line(0, py, BOARD_WIDTH * CELL_SIZE, py, fill="#1f2a33")

    def draw_side_panel(self) -> None:
        x0 = BOARD_WIDTH * CELL_SIZE + 20
        self.canvas.create_rectangle(x0 - 10, 0, WIDTH, HEIGHT, fill="#0d1116", outline="")
        self.canvas.create_text(x0, 30, anchor="w", fill="#e6eef7", font=("Arial", 18, "bold"), text="TETRIS")
        self.canvas.create_text(x0, 75, anchor="w", fill="#9fb0c0", font=("Arial", 11), text=f"Score: {self.score}")
        self.canvas.create_text(x0, 100, anchor="w", fill="#9fb0c0", font=("Arial", 11), text=f"Lines: {self.lines}")
        self.canvas.create_text(x0, 125, anchor="w", fill="#9fb0c0", font=("Arial", 11), text=f"Level: {self.level}")
        self.canvas.create_text(x0, 170, anchor="w", fill="#e6eef7", font=("Arial", 12, "bold"), text="Next")
        self.draw_next_piece(x0, 190)
        self.canvas.create_text(
            x0,
            320,
            anchor="w",
            fill="#9fb0c0",
            font=("Arial", 10),
            text="Left/Right: Move\nUp: Rotate\nDown: Soft drop\nSpace: Hard drop\nR: Restart",
            justify="left",
        )
        if self.game_over:
            self.canvas.create_text(
                BOARD_WIDTH * CELL_SIZE / 2,
                HEIGHT / 2,
                fill="#ffffff",
                font=("Arial", 24, "bold"),
                text="GAME OVER\nPress R to restart",
                justify="center",
            )

    def draw_next_piece(self, x0: int, y0: int) -> None:
        preview = self.next_piece
        shape = SHAPES[preview["kind"]][0]
        color = COLORS[preview["kind"]]
        for dx, dy in shape:
            px = x0 + dx * 18
            py = y0 + dy * 18
            self.canvas.create_rectangle(px, py, px + 16, py + 16, fill=color, outline="#0b0f12")

    def draw(self) -> None:
        self.canvas.delete("all")
        self.draw_grid()
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell is not None:
                    self.draw_block(x, y, COLORS[cell])
        if self.current_piece is not None:
            for x, y in self.piece_cells(self.current_piece):
                if y >= 0:
                    self.draw_block(x, y, COLORS[self.current_piece["kind"]])
        self.draw_side_panel()


def main() -> None:
    root = tk.Tk()
    TetrisGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
