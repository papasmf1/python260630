import random
import tkinter as tk


class BlockBreakerGame:
    WIDTH = 800
    HEIGHT = 600
    PADDLE_WIDTH = 360
    PADDLE_HEIGHT = 16
    PADDLE_SPEED = 24

    BALL_SIZE = 14
    BALL_SPEED = 6

    BRICK_ROWS = 6
    BRICK_COLS = 10
    BRICK_WIDTH = 70
    BRICK_HEIGHT = 24
    BRICK_GAP = 6
    BRICK_TOP_OFFSET = 70

    FPS_MS = 16  # 약 60 FPS

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Block Breaker")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(
            root,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg="#101820",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.score = 0
        self.lives = 3
        self.running = True
        self.paused = False

        self.left_pressed = False
        self.right_pressed = False

        self.paddle = self._create_paddle()
        self.ball = self._create_ball()
        self.ball_dx = random.choice([-1, 1]) * self.BALL_SPEED
        self.ball_dy = -self.BALL_SPEED

        self.bricks = []
        self._create_bricks()

        self.hud_text = self.canvas.create_text(
            12,
            12,
            anchor="nw",
            fill="white",
            font=("Consolas", 14, "bold"),
            text="",
        )
        self.message_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2,
            fill="white",
            font=("Consolas", 28, "bold"),
            text="",
        )

        self._bind_keys()
        self._update_hud()
        self._game_loop()

    def _create_paddle(self):
        x1 = (self.WIDTH - self.PADDLE_WIDTH) // 2
        y1 = self.HEIGHT - 50
        x2 = x1 + self.PADDLE_WIDTH
        y2 = y1 + self.PADDLE_HEIGHT
        return self.canvas.create_rectangle(
            x1, y1, x2, y2, fill="#00d8ff", outline=""
        )

    def _create_ball(self):
        x = self.WIDTH // 2
        y = self.HEIGHT // 2
        r = self.BALL_SIZE // 2
        return self.canvas.create_oval(
            x - r, y - r, x + r, y + r, fill="#ffcc00", outline=""
        )

    def _create_bricks(self):
        colors = ["#ff595e", "#ff924c", "#ffca3a", "#8ac926", "#1982c4", "#6a4c93"]

        total_width = self.BRICK_COLS * self.BRICK_WIDTH + (self.BRICK_COLS - 1) * self.BRICK_GAP
        start_x = (self.WIDTH - total_width) // 2

        for row in range(self.BRICK_ROWS):
            for col in range(self.BRICK_COLS):
                x1 = start_x + col * (self.BRICK_WIDTH + self.BRICK_GAP)
                y1 = self.BRICK_TOP_OFFSET + row * (self.BRICK_HEIGHT + self.BRICK_GAP)
                x2 = x1 + self.BRICK_WIDTH
                y2 = y1 + self.BRICK_HEIGHT

                brick = self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=colors[row % len(colors)],
                    outline="#0b0b0b",
                    width=1,
                )
                self.bricks.append(brick)

    def _bind_keys(self) -> None:
        self.root.bind("<KeyPress-Left>", lambda _e: self._set_left(True))
        self.root.bind("<KeyRelease-Left>", lambda _e: self._set_left(False))
        self.root.bind("<KeyPress-Right>", lambda _e: self._set_right(True))
        self.root.bind("<KeyRelease-Right>", lambda _e: self._set_right(False))

        self.root.bind("<a>", lambda _e: self._set_left(True))
        self.root.bind("<KeyRelease-a>", lambda _e: self._set_left(False))
        self.root.bind("<d>", lambda _e: self._set_right(True))
        self.root.bind("<KeyRelease-d>", lambda _e: self._set_right(False))

        self.root.bind("<p>", lambda _e: self._toggle_pause())
        self.root.bind("<r>", lambda _e: self._restart())

    def _set_left(self, state: bool) -> None:
        self.left_pressed = state

    def _set_right(self, state: bool) -> None:
        self.right_pressed = state

    def _toggle_pause(self) -> None:
        if not self.running:
            return
        self.paused = not self.paused
        if self.paused:
            self._show_message("PAUSED\nPress P to resume")
        else:
            self._show_message("")

    def _update_hud(self) -> None:
        self.canvas.itemconfigure(self.hud_text, text=f"Score: {self.score}   Lives: {self.lives}")

    def _show_message(self, msg: str) -> None:
        self.canvas.itemconfigure(self.message_text, text=msg)

    def _move_paddle(self) -> None:
        paddle_coords = self.canvas.coords(self.paddle)
        if not paddle_coords:
            return

        x1, y1, x2, y2 = paddle_coords
        dx = 0

        if self.left_pressed and not self.right_pressed:
            dx = -self.PADDLE_SPEED
        elif self.right_pressed and not self.left_pressed:
            dx = self.PADDLE_SPEED

        if dx == 0:
            return

        if x1 + dx < 0:
            dx = -x1
        elif x2 + dx > self.WIDTH:
            dx = self.WIDTH - x2

        self.canvas.move(self.paddle, dx, 0)

    def _move_ball(self) -> None:
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        bx1, by1, bx2, by2 = self.canvas.coords(self.ball)

        if bx1 <= 0:
            self.ball_dx = abs(self.ball_dx)
        elif bx2 >= self.WIDTH:
            self.ball_dx = -abs(self.ball_dx)

        if by1 <= 0:
            self.ball_dy = abs(self.ball_dy)

        if by2 >= self.HEIGHT:
            self.lives -= 1
            self._update_hud()
            if self.lives <= 0:
                self.running = False
                self._show_message("GAME OVER\nPress R to restart")
            else:
                self._reset_ball()

    def _reset_ball(self) -> None:
        r = self.BALL_SIZE // 2
        x = self.WIDTH // 2
        y = self.HEIGHT // 2
        self.canvas.coords(self.ball, x - r, y - r, x + r, y + r)
        self.ball_dx = random.choice([-1, 1]) * self.BALL_SPEED
        self.ball_dy = -self.BALL_SPEED

    def _check_paddle_collision(self) -> None:
        bx1, by1, bx2, by2 = self.canvas.coords(self.ball)
        overlaps = self.canvas.find_overlapping(bx1, by1, bx2, by2)

        if self.paddle not in overlaps:
            return

        px1, _py1, px2, _py2 = self.canvas.coords(self.paddle)
        paddle_center = (px1 + px2) / 2
        ball_center = (bx1 + bx2) / 2

        # 패들 중심 대비 충돌 위치에 따라 공의 반사 각도(가로 속도)를 변경한다.
        distance_from_center = (ball_center - paddle_center) / (self.PADDLE_WIDTH / 2)
        self.ball_dx = max(-10, min(10, distance_from_center * 10))
        self.ball_dy = -abs(self.ball_dy)

        # 겹침으로 인한 떨림 방지를 위해 공을 패들 바로 위로 살짝 이동한다.
        self.canvas.move(self.ball, 0, -4)

    def _check_brick_collision(self) -> None:
        if not self.bricks:
            return

        bx1, by1, bx2, by2 = self.canvas.coords(self.ball)
        overlaps = self.canvas.find_overlapping(bx1, by1, bx2, by2)

        hit_brick = None
        for item in overlaps:
            if item in self.bricks:
                hit_brick = item
                break

        if hit_brick is None:
            return

        brick_x1, brick_y1, brick_x2, brick_y2 = self.canvas.coords(hit_brick)

        overlap_left = bx2 - brick_x1
        overlap_right = brick_x2 - bx1
        overlap_top = by2 - brick_y1
        overlap_bottom = brick_y2 - by1

        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap in (overlap_left, overlap_right):
            self.ball_dx *= -1
        else:
            self.ball_dy *= -1

        self.canvas.delete(hit_brick)
        self.bricks.remove(hit_brick)
        self.score += 10
        self._update_hud()

        if not self.bricks:
            self.running = False
            self._show_message("YOU WIN!\nPress R to restart")

    def _restart(self) -> None:
        self.score = 0
        self.lives = 3
        self.running = True
        self.paused = False

        self.canvas.delete("all")

        self.paddle = self._create_paddle()
        self.ball = self._create_ball()
        self.ball_dx = random.choice([-1, 1]) * self.BALL_SPEED
        self.ball_dy = -self.BALL_SPEED

        self.bricks = []
        self._create_bricks()

        self.hud_text = self.canvas.create_text(
            12,
            12,
            anchor="nw",
            fill="white",
            font=("Consolas", 14, "bold"),
            text="",
        )
        self.message_text = self.canvas.create_text(
            self.WIDTH // 2,
            self.HEIGHT // 2,
            fill="white",
            font=("Consolas", 28, "bold"),
            text="",
        )

        self._update_hud()
        self._show_message("")

    def _game_loop(self) -> None:
        if self.running and not self.paused:
            self._move_paddle()
            self._move_ball()
            self._check_paddle_collision()
            self._check_brick_collision()

        self.root.after(self.FPS_MS, self._game_loop)


if __name__ == "__main__":
    root = tk.Tk()
    game = BlockBreakerGame(root)
    root.mainloop()
