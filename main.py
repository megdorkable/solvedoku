#!/usr/bin/python3
# main.py
import numpy as np
from typing import List
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from solvedoku import Board, BoardGenerator


class Tile(TextInput):
    def __init__(self, notes_tile, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.font_size = min(self.height, self.width) * 0.9
        self.font_name = 'DejaVuSans'
        self.halign = "center"
        self.multiline = False
        self.write_tab = False
        self.input_filter = 'int'
        self.toggle_notes = False
        self.notes_tile = notes_tile

    def insert_text(self, substring, from_undo=False):
        options = [str(x) for x in range(1, 10)]
        if substring in options:
            if not self.readonly:
                self.text = ''
            if self.toggle_notes:
                self.notes_tile.toggle(int(substring) - 1)
            else:
                self.notes_tile.clear()
                return super().insert_text(substring, from_undo=from_undo)

    def resize(self):
        self.font_size = min(self.height, self.width) * 0.7564
        pad = 6
        if self.height > self.width:
            pad += (self.height - self.width) / 2
        self.padding = (6, pad, 6, 6)


class SudokuBlock(GridLayout):
    def __init__(self, tiles: List[List[Tile]], **kwargs):
        super(SudokuBlock, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.tiles: List[List[Tile]] = tiles

        for tile in self.tiles:
            self.add_widget(tile)


class SudokuBoard(GridLayout):
    def __init__(self, notes, **kwargs):
        super(SudokuBoard, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.spacing = 10
        self.tiles: List[List[Tile]] = np.full((9, 9), None)
        self.notes = notes
        self.solution: List[List[int]] = None
        Window.bind(on_resize=self.on_window_resize)

        for idx in range(0, 9):
            for idy in range(0, 9):
                self.tiles[idx][idy] = Tile(self.notes[idx][idy])

        for block_num in range(0, 9):
            idx_range, idy_range = Board.get_block_range(block_num)
            block_tiles = [self.tiles[idx][idy] for idx in idx_range for idy in idy_range]
            self.add_widget(SudokuBlock(block_tiles))

    def on_window_resize(self, window, width, height):
        for row in self.tiles:
            for tile in row:
                tile.resize()

    def set_value(self, idx: int, idy: int, value: int, background_color=None, text_color=None, readonly=False) -> None:
        self.tiles[idx][idy].text = str(value)
        self.tiles[idx][idy].readonly = readonly
        if background_color:
            self.tiles[idx][idy].background_color = background_color
        if text_color:
            self.tiles[idx][idy].foreground_color = text_color

    def get_grid(self) -> List[List[int]]:
        grid = np.array(self.tiles).tolist()
        for idx, row in enumerate(grid):
            for idy, col_val in enumerate(row):
                try:
                    grid[idx][idy] = int(col_val.text)
                except ValueError:
                    grid[idx][idy] = None
        return grid

    def set_grid(self, grid, background_color=None, text_color=None, readonly=False):
        for idx, row in enumerate(grid):
            for idy, col_val in enumerate(row):
                if col_val is None:
                    self.set_value(idx, idy, '', background_color=[1, 1, 1, 1], text_color=[0, 0, 0, 1], readonly=False)
                else:
                    self.set_value(idx, idy, col_val, background_color, text_color,
                                   readonly or self.tiles[idx][idy].readonly)


class Note(Label):
    def __init__(self, **kwargs):
        super(Note, self).__init__(**kwargs)
        self.font_name = 'DejaVuSans'
        self.halign = "center"
        self.color = 'black'
        self.opacity = 0

    def set_note(self, is_visible=True) -> None:
        self.opacity = 1 if is_visible else 0


class NotesTile(GridLayout):
    def __init__(self, **kwargs):
        super(NotesTile, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.notes = []

        for x in range(0, 9):
            self.notes.append(Note(text=str(x + 1)))
            self.add_widget(self.notes[x])

    def clear(self) -> None:
        for val in range(0, 9):
            self.notes[val].set_note(is_visible=False)

    def set(self, val: int, is_visible=True) -> None:
        self.notes[val].set_note(is_visible)

    def set_all(self, tile_poss: List[int]) -> None:
        for val in range(0, 9):
            is_visible = False
            if val in tile_poss:
                is_visible = True
            self.notes[val].set_note(is_visible)

    def toggle(self, val: int) -> None:
        is_visible = False if self.notes[val].opacity == 1 else True
        self.set(val, is_visible)


class NotesBlock(GridLayout):
    def __init__(self, tiles: List[List[NotesTile]], **kwargs):
        super(NotesBlock, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.tiles: List[NotesTile] = tiles

        for tile in self.tiles:
            self.add_widget(tile)


class NotesBoard(GridLayout):
    def __init__(self, **kwargs):
        super(NotesBoard, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        self.spacing = 10
        self.tiles: List[List[NotesTile]] = np.full((9, 9), None)

        for idx in range(0, 9):
            for idy in range(0, 9):
                self.tiles[idx][idy] = NotesTile()

        for block_num in range(0, 9):
            idx_range, idy_range = Board.get_block_range(block_num)
            block_tiles = [self.tiles[idx][idy] for idx in idx_range for idy in idy_range]
            self.add_widget(NotesBlock(block_tiles))

    def set_notes(self, poss: List[List[List[int]]]) -> None:
        for idx, row in enumerate(poss):
            for idy, col_poss in enumerate(row):
                self.tiles[idx][idy].set_all(col_poss)

    def clear_tile(self, idx: int, idy: int):
        self.tiles[idx][idy].clear()

    def clear_notes(self):
        for idx, row in enumerate(self.tiles):
            for idy, _ in enumerate(row):
                self.clear_tile(idx, idy)


class OverlayScreen(Screen):
    def __init__(self, **kwargs):
        super(OverlayScreen, self).__init__(**kwargs)
        self.size = Window.size
        self.notes = NotesBoard()
        self.board = SudokuBoard(self.notes.tiles)

        layout1 = self.notes
        layout2 = self.board

        self.add_widget(layout2)
        self.add_widget(layout1)


class ActButton(Button):
    def __init__(self, **kwargs):
        super(ActButton, self).__init__(**kwargs)
        self.font_name = 'DejaVuSans'
        self.halign = "center"


class ActionRow(BoxLayout):
    def __init__(self, board: SudokuBoard, notes: NotesBoard, **kwargs):
        super(ActionRow, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.board = board
        self.notes = notes

        toggle_notes_btn = ActButton(text="Toggle\nNotes")
        toggle_notes_btn.bind(on_press=self.callback_toggle_notes)

        verify_btn = ActButton(text="Verify")
        verify_btn.bind(on_press=self.callback_verify)

        gen_notes_btn = ActButton(text="Generate\nNotes")
        gen_notes_btn.bind(on_press=self.callback_gen_notes)

        gen_btn = ActButton(text="Generate\nBoard")
        gen_btn.bind(on_press=self.callback_gen)

        solve_btn = ActButton(text="Solve")
        solve_btn.bind(on_press=self.callback_solve)

        reset_btn = ActButton(text="Reset")
        reset_btn.bind(on_press=self.callback_reset)

        clear_btn = ActButton(text="Clear")
        clear_btn.bind(on_press=self.callback_clear)

        self.add_widget(toggle_notes_btn)
        self.add_widget(verify_btn)
        self.add_widget(gen_notes_btn)
        self.add_widget(gen_btn)
        self.add_widget(solve_btn)
        self.add_widget(reset_btn)
        self.add_widget(clear_btn)

    def callback_toggle_notes(self, event) -> None:
        t = 0.7 + 1
        event.background_color = [t - curr for curr in event.background_color]
        for row in self.board.tiles:
            for tile in row:
                tile.toggle_notes = tile.toggle_notes ^ True

    def callback_verify(self, event) -> None:
        try:
            solution = self.board.solution
            b = Board(self.board.get_grid())

            if solution is None:
                b_solved = Board(self.board.get_grid())
                b_solved.solve()
                solution = b_solved.grid

            incorrect = b.verify_board(solution)
            if incorrect:
                for idx, idy in incorrect:
                    self.board.tiles[idx][idy].background_color = [1, 0.12, 0.12, 1]
        except (ValueError, RuntimeError) as e:
            print(e)

    def callback_gen_notes(self, event) -> None:
        b = Board(self.board.get_grid())
        poss = b.gen_poss(b.poss)
        self.notes.set_notes(poss)

    def callback_gen(self, event) -> None:
        grid, solution = BoardGenerator().generate()
        self.board.solution = solution
        self.board.set_grid(grid, background_color=[1, 1, 1, 0.8], text_color=[0.3, 0.3, 0.3, 1.0], readonly=True)
        self.notes.clear_notes()

    def callback_solve(self, event) -> None:
        try:
            solution = self.board.solution

            if solution is None:
                b = Board(self.board.get_grid())
                b.solve()
                solution = b.grid

            self.board.set_grid(solution)
            self.notes.clear_notes()
        except (ValueError, RuntimeError) as e:
            print(e)

    def callback_reset(self, event) -> None:
        for idx, row in enumerate(self.board.tiles):
            for idy, col_val in enumerate(row):
                if not col_val.readonly:
                    self.board.set_value(idx, idy, '', background_color=[1, 1, 1, 1], text_color=[0, 0, 0, 1])
        self.notes.clear_notes()

    def callback_clear(self, event) -> None:
        grid = np.full((9, 9), None)
        self.board.set_grid(grid)
        self.board.solution = None
        self.notes.clear_notes()


class AllElements(GridLayout):
    def __init__(self, **kwargs):
        super(AllElements, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2

        overlay = OverlayScreen(size_hint=(1, 0.9))
        buttons = ActionRow(board=overlay.board, notes=overlay.notes, size_hint=(1, 0.1))

        self.add_widget(overlay)
        self.add_widget(buttons)

        Window.size = (600, 600)


class SudokuApp(App):

    def build(self):
        return AllElements()


if __name__ == '__main__':
    SudokuApp().run()
