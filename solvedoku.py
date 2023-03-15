#!/usr/bin/python3
# solvedoku.py
import numpy as np
from typing import Tuple, List
from test_boards import boards_sols


class Board:
    """Represents a Sudoku board"""

    def __init__(self, grid: List[List[int]]) -> None:
        """Initialize a new Board

        Args:
            grid (List[List]): A 9x9 2D array of integers from 1 through 9

        Raises:
            TypeError: If grid has the wrong dimensions, or contains values that are not integers from 1 through 9
        """
        # - Verify grid
        correct = True
        if not isinstance(grid, list):
            correct = False
        elif len(grid) == 9:
            for row in grid:
                if not isinstance(row, list) or len(row) != 9:
                    correct = False
                for col in row:
                    if not (isinstance(col, type(None)) or (isinstance(col, int) and col in range(1, 10))):
                        correct = False
        else:
            correct = False
        if not correct:
            raise TypeError(
                "The given value for 'arr' is not a 9x9 list of integers.")

        # - Original grid, will not be changed through solving
        self.grid_orig: List[List] = np.array(grid).tolist()
        # - Grid, will be changed through solving
        self.grid: List[List] = np.array(grid).tolist()
        # - Number of unsolved tiles
        self.unsolved: int = 9 * 9
        # - Lists of true/false based on what values are contained in rows, columns, and blocks
        self.row_has: List[List[bool]]
        self.col_has: List[List[bool]]
        self.block_has: List[List[bool]]
        self.row_has, self.col_has, self.block_has = self.__gen_row_col_block()
        # - Lists of possibile integers for each tile in the Board
        self.poss: List[List[List[int]]] = np.full((9, 9, 9), np.arange(0, 9)).tolist()

    def __repr__(self) -> str:
        """Represent a board by separating each block with bars,
        such that each 3x3 block is surrounded by the appropriate column and row separators.
        This makes things look more readable like a normal Sudoku board.

        Returns:
            str: The string representation of a Board.
        """
        rbar = '--' * 9 + '-' * (4 * 2 - 1) + '\n'
        s = ''
        for idx, row in enumerate(self.grid):
            if idx % 3 == 0:
                s += rbar
            for idy, col in enumerate(row):
                if idy % 3 == 0:
                    s += '| '
                if isinstance(col, type(None)):
                    s += '- '
                else:
                    s += str(col) + ' '
                if idy == len(row) - 1:
                    s += '|'
            s += '\n'
        s += rbar
        return s

    def __str__(self) -> str:
        """When converted to a string, a Board should be the same as its __repr__ representation.

        Returns:
            str: The string representation of a Board.
        """
        return self.__repr__()

    def poss_tostring(self) -> str:
        """Create a string with the current possibilities/notes with appropriate spacing (by row and column).

        Returns:
            str: The current possibilities/notes as a pretty string.
        """
        poss_str = ""

        col_lengths = []
        for col_num in range(0, 9):
            col_max_len = 0
            for row_num in range(0, 9):
                col_max_len = max(col_max_len, len(self.poss[row_num][col_num]))
            col_lengths.append(col_max_len)

        for row in self.poss:
            for idy, col in enumerate(row):
                spaces_to_add = (col_lengths[idy] - len(col)) * 3
                if len(col) != 0:
                    spaces_to_add += 2
                poss_str += str(col) + ' ' * spaces_to_add
            poss_str += '\n'
        return poss_str

    def __get_block_num(self, idx: int, idy: int) -> int | None:
        """Given a row and column index, will return the block number.

        0 1 2
        3 4 5
        6 7 8

        Args:
            idx (int): row index from 0 through 8
            idy (int): column index from 0 through 8

        Returns:
            int | None: The block number between from 0 through 8, or None if the indices are not within the correct
                        dimensions.
        """
        r0, r1, r2 = range(0, 3), range(3, 6), range(6, 9)
        if idx in r0 and idy in r0:
            return 0
        elif idx in r0 and idy in r1:
            return 1
        elif idx in r0 and idy in r2:
            return 2
        elif idx in r1 and idy in r0:
            return 3
        elif idx in r1 and idy in r1:
            return 4
        elif idx in r1 and idy in r2:
            return 5
        elif idx in r2 and idy in r0:
            return 6
        elif idx in r2 and idy in r1:
            return 7
        elif idx in r2 and idy in r2:
            return 8
        else:
            return None

    def __get_block_range(self, block_num: int) -> Tuple[range, range] | None:
        """Given a block number, will return the ranges for the row and column indices.

        Args:
            block_num (int): The block number from 0 through 8

        Returns:
            Tuple[range, range] | None: A tuple where the first value is the row index range and the second value is
                                        the column index range.
        """
        r0, r1, r2 = range(0, 3), range(3, 6), range(6, 9)
        if block_num == 0:
            return (r0, r0)
        elif block_num == 1:
            return (r0, r1)
        elif block_num == 2:
            return (r0, r2)
        elif block_num == 3:
            return (r1, r0)
        elif block_num == 4:
            return (r1, r1)
        elif block_num == 5:
            return (r1, r2)
        elif block_num == 6:
            return (r2, r0)
        elif block_num == 7:
            return (r2, r1)
        elif block_num == 8:
            return (r2, r2)
        else:
            return None

    def __gen_row_col_block(self) -> Tuple[List[List[bool]], List[List[bool]], List[List[bool]]]:
        """Generate the lists of what each row, column, and block contain.

        Returns:
            Tuple[List[List[bool]], List[List[bool]], List[List[bool]]]: A tuple of lists of what each row, column, and
                block (respectively) contain, represented by a boolean for each value.
        """
        row_has: List[List[bool]] = np.full((9, 9), False)
        col_has: List[List[bool]] = np.full((9, 9), False)
        block_has: List[List[bool]] = np.full((9, 9), False)
        for idx, row in enumerate(self.grid):
            for idy, col in enumerate(row):
                if not isinstance(col, type(None)):
                    idc = col - 1
                    row_has[idx][idc] = True
                    col_has[idy][idc] = True
                    block_has[self.__get_block_num(idx, idy)][idc] = True
                    self.unsolved -= 1
        return (row_has, col_has, block_has)

    def __gen_poss(self, curr_poss: List[List[List[int]]]) -> List[List[List[int]]]:
        """Find the list of possibilities for each tile in the Board. This is similar to notes when solving by hand.

        Args:
            curr_poss (List[List[List[int]]]): The current list of possibilities for each tile.

        Returns:
            List[List[List[int]]]: The new list of possibilities for each tile.
        """
        for idx, row in enumerate(self.grid):
            for idy, col in enumerate(row):
                new_poss = []
                if col is None:
                    for idp, p in enumerate(curr_poss[idx][idy]):
                        if not self.row_has[idx][p] and not self.col_has[idy][p] and \
                                not self.block_has[self.__get_block_num(idx, idy)][p]:
                            new_poss.append(curr_poss[idx][idy][idp])
                curr_poss[idx][idy] = new_poss
                if len(curr_poss[idx][idy]) == 1:
                    self.__set_tile(idx=idx, idy=idy, val=curr_poss[idx][idy][0])
                    curr_poss[idx][idy] = []
        return curr_poss

    def __set_tile(self, idx: int, idy: int, val: int):
        """Set the tile at the given indices to the given value.

        Args:
            idx (int): row index from 0 through 8
            idy (int): column index from 0 through 8
            val (int): value to set the tile to
        """
        self.grid[idx][idy] = val + 1
        self.row_has[idx][val] = True
        self.col_has[idy][val] = True
        self.block_has[self.__get_block_num(idx, idy)][val] = True
        self.poss[idx][idy] = []
        self.unsolved -= 1

    def solve(self) -> None:
        """Find a solution for the Board.

        Raises:
            ValueError: If the Board is unsolveable.
        """
        stuck: int = self.unsolved
        tried_xy_wing: bool = False
        while self.unsolved > 0:
            self.poss = self.__gen_poss(self.poss)
            # - Solve by rows
            for idx, row in enumerate(self.row_has):
                for val in range(0, 9):
                    found = self.__solve_row_col(0, idx, row, val)
                    if found:
                        self.__set_tile(idx=idx, idy=found, val=val)
            # - Solve by columns
            for idy, col in enumerate(self.col_has):
                for val in range(0, 9):
                    found = self.__solve_row_col(1, idy, col, val)
                    if found:
                        self.__set_tile(idx=found, idy=idy, val=val)
            # - Solve by blocks
            for block_num in range(0, 9):
                for val in range(0, 9):
                    found = self.__solve_block(block_num, val)
                    if found:
                        self.__set_tile(idx=found[0], idy=found[1], val=val)
            if self.unsolved == stuck and not tried_xy_wing:
                self.__solve_xy_wing()
                tried_xy_wing = True
            elif self.unsolved == stuck:
                print(f"Possibilities when stuck: \n{self.poss_tostring()}")
                raise ValueError("The given board is unsolvable.")
            else:
                tried_xy_wing = False
            stuck = self.unsolved

    def __solve_row_col(self, which_rc: int, rc_num: int, rc_has: List[List[bool]], val: int) -> int | None:
        """Try to find a placement for a given value in either a row or a column.
        Called by self.solve().

        Args:
            which_rc (int): 0 to look at a row, 1 to look at a column
            rc_num (int): Index of the row or column
            rc_has (List[List[bool]]): List of true/false based on what values are contained in the row or column
            val (int): The value to try to find a placement for
            poss (List[List[List]]): The current list of possibilities for the Board

        Returns:
            int | None: Either the found placement for the value (row or column index), or None
        """
        # - If the value is not already in the row or column..
        if not rc_has[val]:
            found = None
            all_found = []

            # - Generate the poss_group based on whether we are looking at a row or a column
            poss_group = []
            if which_rc:
                for row_num in range(0, 9):
                    poss_group.append(self.poss[row_num][rc_num])
            else:
                poss_group = self.poss[rc_num]

            # - Find tiles for which the value is still possible
            for idx, rc in enumerate(poss_group):
                if val in rc:
                    if found is None:
                        found = idx
                    all_found.append(idx)

            # - If exactly one possible position for the value was found, return that position
            if len(all_found) == 1:
                return found
            # - If more than one possible position for the value was found, try to narrow down the possibilities
            elif len(all_found) > 1:
                # - naked pairs
                all_found_poss = [self.poss[idx][rc_num]for idx in all_found] if which_rc else [
                    self.poss[rc_num][idy] for idy in all_found]
                for idx, x in enumerate(all_found_poss):
                    found_match = [(idx, x)]
                    for idy, y in enumerate(all_found_poss):
                        if idx != idy and x == y:
                            found_match.append((idy, y))
                    if len(found_match) == len(found_match[0][1]):
                        for idz, _ in enumerate(all_found_poss):
                            if idz not in [ind for (ind, _) in found_match]:
                                for val in found_match[0][1]:
                                    try:
                                        if which_rc:
                                            self.poss[all_found[idz]][rc_num].remove(val)
                                        else:
                                            self.poss[rc_num][all_found[idz]].remove(val)
                                    except ValueError:
                                        pass
            # - If found in exactly 2 places, attempt to solve with an X Wing
            if len(all_found) == 2:
                self.__solve_x_wing(which_rc, rc_num, val, all_found)
        return None

    def __solve_block(self, block_num: int, val: int) -> Tuple[int, int] | None:
        """Try to find a placement for a given value in a block.
        Called by self.solve().

        Args:
            block_num (int): The number of the block
            val (int): The value to try to find a placement for

        Returns:
            Tuple[int, int] | None: Either the found placement for the value as a tuple of (row index, column index),
                                    or None
        """
        # - Get the list of booleans showing which values the "block_num" block contains
        block_has = self.block_has[block_num]
        # - If the value is not already in the block..
        if not block_has[val]:
            found = None
            all_found = []
            block_range = self.__get_block_range(block_num)

            # - Find tiles for which the value is still possible
            for idx in block_range[0]:
                for idy in block_range[1]:
                    if val in self.poss[idx][idy]:
                        if found is None:
                            found = (idx, idy)
                        all_found.append((idx, idy))

            # - If exactly one possible position for the value was found, return that position
            if len(all_found) == 1:
                return found
            # - If more than one possible position for the value was found, try to narrow down the possibilities
            elif len(all_found) > 1:
                # - naked pairs
                all_found_poss = [self.poss[idx][idy]
                                  for (idx, idy) in all_found]
                for idx, x in enumerate(all_found_poss):
                    found_match = [(idx, x)]
                    for idy, y in enumerate(all_found_poss):
                        if idx != idy and x == y:
                            found_match.append((idy, y))
                    if len(found_match) == len(found_match[0][1]):
                        for idz, _ in enumerate(all_found_poss):
                            if idz not in [ind for (ind, _) in found_match]:
                                for val in found_match[0][1]:
                                    try:
                                        self.poss[all_found[idz][0]][all_found[idz][1]].remove(val)
                                    except ValueError:
                                        pass
                # - If val is only possible in one row or column of this block, eliminate val from the other block
                # - possibilities in the one row or column
                found_row = all_found[0][0]
                found_col = all_found[0][1]
                for f in all_found[1:]:
                    if f[0] != found_row:
                        found_row = None
                    if f[1] != found_col:
                        found_col = None
                if found_row is not None:
                    keep_cols = [col for (row, col) in all_found]
                    for idy, _ in enumerate(self.poss[found_row]):
                        if idy not in keep_cols:
                            try:
                                self.poss[found_row][idy].remove(val)
                            except ValueError:
                                pass
                if found_col is not None:
                    keep_rows = [row for (row, col) in all_found]
                    for idx, _ in enumerate(self.poss):
                        if idx not in keep_rows:
                            try:
                                self.poss[idx][found_col].remove(val)
                            except ValueError:
                                pass
        return None

    def __solve_x_wing(self, which_rc: int, rc_num: int, val: int, pair: List[int]):
        """Try to eliminate possibilities based on the X Wing strategy.
        If a value exists in exactly 2 places in a row or column ('pair', given), and there exists a second row or
        column in which the value exists in the same two places and only those places, eliminate the value from the
        other tiles in the 2 matching rows or columns.
        Called by self.solve().

        Args:
            which_rc (int): 0 to look at a row, 1 to look at a column
            rc_num (int): Index of the row or column
            val (int): The value to try to eliminate as a possibility
            pair (List[int]): The pair of exactly 2 places at which the value exists in the given row or column.
        """
        # - If working with columns, transpose self.poss
        all_poss_groups = []
        if which_rc:
            all_poss_groups = [list(x) for x in zip(*self.poss)]
        else:
            all_poss_groups = self.poss

        # - For every row or column..
        for idx, rc_poss in enumerate(all_poss_groups):
            # - If the row or column number is not equal to the same row or column that we have already found..
            if idx != rc_num:
                rc_has = self.col_has[idx] if which_rc else self.row_has[idx]

                # - If the value is not already in the row or column..
                if not rc_has[val]:
                    all_found = []

                    # - Find tiles for which the value is still possible
                    for idy, rc in enumerate(rc_poss):
                        if val in rc:
                            all_found.append(idy)

                    # - If found in exactly 2 places..
                    if len(all_found) == 2:
                        # - If the places found are the same as the pair we started with..
                        if all_found[0] == pair[0] and all_found[1] == pair[1]:
                            # - Eliminate the val from the other poss's in the same row or column that are not a part
                            # - of the X Wing
                            for idz, rc_elim_poss in enumerate(all_poss_groups):
                                if idz != idx and idz != rc_num:
                                    for idfound in all_found:
                                        try:
                                            rc_elim_poss[idfound].remove(val)
                                        except ValueError:
                                            pass

    def __solve_xy_wing(self):
        """Try to eliminate possibilities based on the XY Wing strategy.
        Called by self.solve().
        """
        # - Find intersects: tiles with only 2 possibilities
        # - Create an intersects list of [(row index, column index, List of wings)]
        intersects: List[Tuple[int, int, List[Tuple[int, int]]]] = []
        for idx, row in enumerate(self.poss):
            for idy, col in enumerate(row):
                if len(col) == 2:
                    intersects.append((idx, idy, []))

        # - Find the possible wings for each intersect
        for idx, idy, wings in intersects:
            # - The possible wings should be made up of other possible intersects
            for wing_idx, wing_idy, _ in intersects:
                # - A wing cannot be the same tile as the intersect
                if idx != wing_idx or idy != wing_idy:
                    # - A wing has to have the same row, column, or block as the intersect
                    if idx == wing_idx or idy == wing_idy or \
                       self.__get_block_num(idx, idy) == self.__get_block_num(wing_idx, wing_idy):
                        # - A wing cannot have the exact same possibilites as the intersect
                        if self.poss[idx][idy] != self.poss[wing_idx][wing_idy]:
                            # - A wing must have one of the same possibilities as the intersect
                            for val in self.poss[idx][idy]:
                                if val in self.poss[wing_idx][wing_idy]:
                                    wings.append((wing_idx, wing_idy))
                                    break

        # - For each intersect..
        for idx, idy, wings in intersects:
            intersect = self.poss[idx][idy]
            # - For each possible wing of that intersect..
            for wing_row, wing_col in wings:
                wing_poss = self.poss[wing_row][wing_col]
                uncommon = list(set(intersect) ^ set(wing_poss))
                # - Try to find a second wing
                for second_wing_row, second_wing_col in wings:
                    # - The second wing cannot intersect the first wing
                    if wing_row != second_wing_row and wing_col != second_wing_col and \
                        self.__get_block_num(wing_row, wing_col) != self.__get_block_num(second_wing_row,
                                                                                         second_wing_col):
                        second_wing_poss = self.poss[second_wing_row][second_wing_col]
                        # - The values that are only in one of intersect's or the first wing's possibilities,
                        # - but not in both, must be equal to the second wing's possibilities
                        if uncommon == second_wing_poss:
                            # - Remove the common value that both of the wing's have from everywhere that intersects
                            # - both of the wings
                            common = list(set(wing_poss) & set(second_wing_poss))[0]
                            # - Remove where tile intersects one wing's row and the other wing's column
                            try:
                                self.poss[wing_row][second_wing_col].remove(common)
                            except ValueError:
                                pass
                            try:
                                self.poss[second_wing_row][wing_col].remove(common)
                            except ValueError:
                                pass
                            # - Remove where tile intersects one wing's block, and the other wing's row or column
                            for wing_idx, wing_idy, other_idx, other_idy in \
                                [(wing_row, wing_col, second_wing_row, second_wing_col),
                                 (second_wing_row, second_wing_col, wing_row, wing_col)]:
                                block_num = self.__get_block_num(wing_idx, wing_idy)
                                block_range = self.__get_block_range(block_num)
                                for block_idx in block_range[0]:
                                    for block_idy in block_range[1]:
                                        if block_idx == other_idx or block_idy == other_idy:
                                            try:
                                                self.poss[block_idx][block_idy].remove(common)
                                            except ValueError:
                                                pass

    def solve_recurse(self) -> None:
        """Solve the Board recursively (brute force).

        Raises:
            ValueError: If the Board is unsolveable.
        """
        grid = np.array(self.grid_orig)
        grid = self.__solve_recurse_inner(grid)
        if grid is not None:
            self.grid = grid
        else:
            raise ValueError("The given board is unsolvable.")

    def __solve_recurse_inner(self, grid: np.ndarray) -> np.ndarray:
        """Inner method for self.solve_recurse().

        Args:
            grid (np.ndarray): The current grid being solved.

        Returns:
            np.ndarray: The solved grid.
        """
        for idx, row in enumerate(grid):
            for idy, col_val in enumerate(row):
                if col_val is None:
                    col = grid[:, idy]

                    block_num = self.__get_block_num(idx, idy)
                    block_range = self.__get_block_range(block_num)
                    block = grid[np.ix_(
                        block_range[0], block_range[1])].flatten()
                    for val in range(1, 10):
                        if val not in row and val not in col and val not in block:
                            grid[idx][idy] = val
                            if self.__solve_recurse_inner(grid) is not None:
                                return grid
                            else:
                                grid[idx][idy] = None
                    return None
        return grid

    def __count_none(self) -> int:
        """Check how many None values exist in the Board's current grid.

        Returns:
            int: The number of values that are None in the Board's current grid.
        """
        count = 0
        for row in self.grid:
            for col in row:
                if col is None:
                    count += 1
        return count

    def verify_board(self, solution: List[List[int]]) -> Tuple[int, int] | None:
        """Check if the Board's grid is equal to the given solution.

        Args:
            solution (List[List[int]]): Solution array to check the Board's grid against.

        Returns:
            Tuple[int, int] | None: Either a tuple of two integers representing the (row index, column index) of the
                                    first error found, or None if no errors are found.
        """
        for x, row in enumerate(self.grid):
            for y, val in enumerate(row):
                if val is not None and val != solution[x][y]:
                    return (x, y)
        return None


if __name__ == '__main__':
    chosen = -1
    while chosen != 'q':
        options = [i for i, _ in enumerate(boards_sols)]
        chosen = input(f"Choose a number out of {options} (or 'q' to exit): ")
        e = 'You have not entered a valid number from the given options.'
        if chosen == 'q':
            exit(0)
        try:
            chosen = int(chosen)
        except ValueError:
            print(e)
        if chosen not in options:
            raise TypeError(e)

        b = Board(boards_sols[chosen][0])
        bs = boards_sols[chosen][1]

        print('Board:')
        print(b)
        try:
            b.solve()
            # b.solve_recurse()
            print('Solved:')
        except ValueError as e:
            print(e)
            print('Unsolved:')
        print(b)
        v = b.verify_board(bs)
        print(f'Verified: {v if v is not None else True}\n')
