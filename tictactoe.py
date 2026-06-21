import tkinter as tk
from tkinter import messagebox


# ИГРОВАЯ ДОСКА
class Board:

    def __init__(self, size):
        self.size = size
        self.grid = [[' ' for i in range(size)] for i in range(size)]

    def set_cell(self, row, col, symbol):
        # Постановка Х/0
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        if self.grid[row][col] != ' ':
            return False
        self.grid[row][col] = symbol
        return True

    def check_winner(self, symbol):
        # Проверка условий победы
        s = self.size
        for i in range(s):
            for j in range(s):
                # горизонталь
                if j + s <= s and all(self.grid[i][j + k] == symbol for k in range(s)):
                    return True
                # вертикаль
                if i + s <= s and all(self.grid[i + k][j] == symbol for k in range(s)):
                    return True
                # диагональ вправо
                if i + s <= s and j + s <= s and all(self.grid[i + k][j + k] == symbol for k in range(s)):
                    return True
                # диагональ влево
                if i + s <= s and j - s + 1 >= 0 and all(self.grid[i + k][j - k] == symbol for k in range(s)):
                    return True
        return False

    def is_full(self):
        # Проверка заполненой доски
        for row in self.grid:
            if ' ' in row:
                return False
        return True

    def clear(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j] = ' '


# ЛОГИКА ИГРЫ 
class Game:


    def __init__(self, size):
        self.board = Board(size)
        self.current_symbol = 'X'
        self.winner = None
        self.draw = False
        self.game_over = False

    def make_move(self, row, col):
        # Реализация ходов
        if self.game_over:
            return 'game_over'

        if not self.board.set_cell(row, col, self.current_symbol):
            return 'error'

        if self.board.check_winner(self.current_symbol):
            self.winner = self.current_symbol
            self.game_over = True
            return 'win'

        if self.board.is_full():
            self.draw = True
            self.game_over = True
            return 'draw'

        self.current_symbol = 'O' if self.current_symbol == 'X' else 'X'
        return 'ok'

    def restart(self, size=None):
        # Новая игра
        if size is not None:
            self.board = Board(size)
        else:
            self.board.clear()
        self.current_symbol = 'X'
        self.winner = None
        self.draw = False
        self.game_over = False


# ---------- ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ----------
class TicTacToeApp:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("КрестикиНолики")

        # Верхняя панель и кнопка старт
        top_frame = tk.Frame(self.window)
        top_frame.pack(pady=5)

        tk.Label(top_frame, text="Размер (от 3 до 25):").pack(side=tk.LEFT, padx=5)
        self.size_entry = tk.Entry(top_frame, width=5)
        self.size_entry.insert(0, "3")
        self.size_entry.pack(side=tk.LEFT, padx=5)

        self.start_btn = tk.Button(top_frame, text="Новая игра", command=self.new_game)
        self.start_btn.pack(side=tk.LEFT, padx=10)

        # Рамка для кнопок поля
        self.board_frame = tk.Frame(self.window)
        self.board_frame.pack(pady=10)

        # Статусная строка
        self.status_label = tk.Label(self.window, text="Введите размер",
        font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.game = None
        self.buttons = []

        self.window.mainloop()

    def new_game(self):
        try:
            size = int(self.size_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Неккоректный ввод")
            return
        if size < 3:
            messagebox.showerror("Ошибка", "Размер должен быть больше 3")
            return
        if size > 25:
            messagebox.showerror("Ошибка", "Максимальный размер поля 25")
            return

        self.game = Game(size)
        self._draw_board()
        self._update_status()

    def _draw_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        size = self.game.board.size
        self.buttons = [[None for i in range(size)] for i in range(size)]

        for r in range(size):
            for c in range(size):
                btn = tk.Button(
                    self.board_frame,
                    text=' ',
                    font=('Arial', 14, 'bold'),
                    width=3,
                    height=1,
                    command=lambda row=r, col=c: self.cell_click(row, col)
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[r][c] = btn

    def cell_click(self, row, col):
        if self.game is None or self.game.game_over:
            return
        result = self.game.make_move(row, col)
        if result == 'error':
            messagebox.showwarning("Недопустимый ход", "Походи в другую клетку")
            return
        elif result == 'game_over':
            return

        symbol = self.game.board.grid[row][col]
        self.buttons[row][col].config(text=symbol)

        self._update_status()

        if result == 'win':
            messagebox.showinfo("Победа", f"Выиграли {self.game.winner}")
        elif result == 'draw':
            messagebox.showinfo("Ничья", "Ничья")

    def _update_status(self):
        if self.game is None:
            return
        if self.game.game_over:
            if self.game.winner:
                self.status_label.config(text=f"Игра окончена. Победитель: {self.game.winner}")
            else:
                self.status_label.config(text="Игра окончена. Ничья!")
        else:
            self.status_label.config(text=f"Ходит: {self.game.current_symbol}")


if __name__ == "__main__":
    app = TicTacToeApp()