#!/usr/bin/python3
# main.py
import numpy as np
from typing import List
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from solvedoku import Board, BoardGenerator


class Tile(TextInput):
    def __init__(self, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.font_size = min(self.height, self.width) * 0.9
        self.font_name = 'DejaVuSans'
        self.halign = "center"
        self.multiline = False
        self.write_tab = False

    def resize(self):
        self.font_size = min(self.height, self.width) * 0.7564
        pad = 6
        if self.height > self.width:
            pad += (self.height - self.width) / 2
        self.padding = (6, pad, 6, 6)


class SudokuBlock(GridLayout):
    def __init__(self, tiles, **kwargs):
        super(SudokuBlock, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.tiles = tiles

        for tile in self.tiles:
            self.add_widget(tile)


class SudokuBoard(GridLayout):
    def __init__(self, **kwargs):
        super(SudokuBoard, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.tiles = np.full((9, 9), None)
        self.solution = None
        Window.bind(on_resize=self.on_window_resize)

        for idx in range(0, 9):
            for idy in range(0, 9):
                self.tiles[idx][idy] = Tile()

        for block_num in range(0, 9):
            idx_range, idy_range = Board.get_block_range(block_num)
            block_tiles = [self.tiles[idx][idy] for idx in idx_range for idy in idy_range]
            self.add_widget(SudokuBlock(block_tiles))

    def on_window_resize(self, window, width, height):
        for row in self.tiles:
            for tile in row:
                tile.resize()

    def set_value(self, idx: int, idy: int, value: int) -> None:
        self.tiles[idx][idy].text = str(value)

    def get_grid(self) -> List[List[int]]:
        grid = np.array(self.tiles).tolist()
        for idx, row in enumerate(grid):
            for idy, col_val in enumerate(row):
                try:
                    grid[idx][idy] = int(col_val.text)
                except ValueError:
                    grid[idx][idy] = None
        return grid

    def set_grid(self, grid):
        for idx, row in enumerate(grid):
            for idy, col_val in enumerate(row):
                self.set_value(idx, idy, col_val if col_val is not None else '')


class ActionButtons(BoxLayout):
    def __init__(self, board: SudokuBoard, **kwargs):
        super(ActionButtons, self).__init__(**kwargs)

        self.board = board

        gen_btn = Button(text="Generate Random Board")
        gen_btn.bind(on_press=self.callback_gen)

        solve_btn = Button(text="Solve")
        solve_btn.bind(on_press=self.callback_solve)

        clear_btn = Button(text="Clear")
        clear_btn.bind(on_press=self.callback_clear)

        self.add_widget(gen_btn)
        self.add_widget(solve_btn)
        self.add_widget(clear_btn)

    def callback_gen(self, event) -> None:
        grid, solution = BoardGenerator().generate()
        self.board.solution = solution
        self.board.set_grid(grid)

    def callback_solve(self, event) -> None:
        try:
            solution = self.board.solution

            if solution is None:
                b = Board(self.board.get_grid())
                b.solve()
                solution = b.grid

            self.board.set_grid(solution)
        except (ValueError, RuntimeError) as e:
            print(e)

    def callback_clear(self, event) -> None:
        grid = np.full((9, 9), None)
        self.board.set_grid(grid)
        self.board.solution = None


class AllElements(GridLayout):
    def __init__(self, **kwargs):
        super(AllElements, self).__init__(**kwargs)
        # self.height: self.minimum_height
        # self.width = self.height
        self.cols = 1
        self.rows = 2

        board = SudokuBoard(spacing=10)
        buttons = ActionButtons(board=board, orientation='horizontal', spacing=10, size_hint=(1, 0.1))

        self.add_widget(board)
        self.add_widget(buttons)

        Window.size = (600, 600)


class SudokuApp(App):

    def build(self):
        return AllElements()


if __name__ == '__main__':
    SudokuApp().run()
