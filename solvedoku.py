#!/usr/bin/python3
# solvedoku.py
import numpy
from typing import Tuple, List
from test_boards import boards_sols


class Board:
    def __init__(self, arr: list) -> None:
        correct_dims = True

        if not isinstance(arr, list):
            correct_dims = False
        elif len(arr) == 9:
            for row in arr:
                if len(row) != 9:
                    correct_dims = False
                for col in row:
                    if not isinstance(col, (int, type(None))):
                        correct_dims = False
        else:
            correct_dims = False
        if not correct_dims:
            raise TypeError(
                "The given value for 'arr' is not a 9x9 list of integers.")

        self.inp_arr = arr
        self.sol_arr = arr
        self.unsolved = 9 * 9
        self.row, self.col, self.block = self.__gen_row_col_block()

    def __repr__(self) -> str:
        rbar = '--' * 9 + '-' * (4 * 2 - 1) + '\n'
        s = ''
        for idx, row in enumerate(self.sol_arr):
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
        return self.__repr__()

    def __get_block_num(self, idx: int, idy: int) -> int | None:
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
        row_has = numpy.full((9, 9), False)
        col_has = numpy.full((9, 9), False)
        block_has = numpy.full((9, 9), False)
        for idx, row in enumerate(self.inp_arr):
            for idy, col in enumerate(row):
                if not isinstance(col, type(None)):
                    idc = col - 1
                    row_has[idx][idc] = True
                    col_has[idy][idc] = True
                    block_has[self.__get_block_num(idx, idy)][idc] = True
                    self.unsolved -= 1
        return (row_has, col_has, block_has)

    def solve(self) -> None:
        stuck = self.unsolved
        poss = numpy.full((9, 9, 9), numpy.arange(0, 9)).tolist()
        while self.unsolved > 0:
            poss = self.__solve_poss(poss)
            for idx, row in enumerate(self.row):
                for val in range(0, 9):
                    found = self.__solve_row(idx, row, val, poss)
                    if found:
                        self.__set_tile(idx=idx, idy=found, val=val)
                        poss[idx][found] = []
            for idy, col in enumerate(self.col):
                for val in range(0, 9):
                    found = self.__solve_col(idy, col, val, poss)
                    if found:
                        self.__set_tile(idx=found, idy=idy, val=val)
                        poss[found][idy] = []
            for block_num in range(0, 9):
                for val in range(0, 9):
                    found = self.__solve_block(block_num, val, poss)
                    if found:
                        self.__set_tile(idx=found[0], idy=found[1], val=val)
                        poss[found[0]][found[1]] = []
            if self.unsolved == stuck:
                raise ValueError("The given board is unsolvable.")
            stuck = self.unsolved

    def __count_none(self):
        count = 0
        for row in self.sol_arr:
            for col in row:
                if col is None:
                    count += 1
        return count

    def __set_tile(self, idx: int, idy: int, val: int):
        self.sol_arr[idx][idy] = val + 1
        self.row[idx][val] = True
        self.col[idy][val] = True
        self.block[self.__get_block_num(idx, idy)][val] = True
        self.unsolved -= 1

    def __solve_poss(self, curr_poss: List[List[List]]) -> List[List[List]]:
        for idx, row in enumerate(self.sol_arr):
            for idy, col in enumerate(row):
                new_poss = []
                if col is None:
                    for idp, p in enumerate(curr_poss[idx][idy]):
                        if not self.row[idx][p] and not self.col[idy][p] and \
                                not self.block[self.__get_block_num(idx, idy)][p]:
                            new_poss.append(curr_poss[idx][idy][idp])
                curr_poss[idx][idy] = new_poss
                if len(curr_poss[idx][idy]) == 1:
                    self.__set_tile(idx=idx, idy=idy,
                                    val=curr_poss[idx][idy][0])
                    curr_poss[idx][idy] = []
        return curr_poss

    def __solve_row(self, row_num: int, row: List[List], val: int, poss_group: List[List[List]]) -> int | None:
        if not row[val]:
            found = None
            all_found = []
            for idy, col in enumerate(poss_group[row_num]):
                if val in col:
                    if found is None:
                        found = idy
                    all_found.append(idy)
            if len(all_found) == 1:
                return found
            elif len(all_found) > 1:
                # naked pairs
                all_found_poss = [poss_group[row_num][idy]
                                  for idy in all_found]
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
                                        poss_group[row_num][
                                            all_found[idz]].remove(val)
                                    except ValueError:
                                        pass
        return None

    def __solve_col(self, col_num: int, col: List[List], val: int, poss_group: List[List[List]]) -> int | None:
        if not col[val]:
            found = None
            all_found = []
            column_poss = []
            for row in range(0, 9):
                column_poss.append(poss_group[row][col_num])
            for idx, row in enumerate(column_poss):
                if val in row:
                    if found is None:
                        found = idx
                    all_found.append(idx)
            if len(all_found) == 1:
                return found
            elif len(all_found) > 1:
                # naked pairs
                all_found_poss = [poss_group[idx][col_num]
                                  for idx in all_found]
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
                                        poss_group[all_found[idz]][
                                            col_num].remove(val)
                                    except ValueError:
                                        pass
        return None

    def __solve_block(self, block_num: int, val: int, poss_group: List[List[List]]) -> Tuple[int, int] | None:
        block = self.block[block_num]
        if not block[val]:
            found = None
            all_found = []
            block_range = self.__get_block_range(block_num)
            for idx in block_range[0]:
                for idy in block_range[1]:
                    if val in poss_group[idx][idy]:
                        if found is None:
                            found = (idx, idy)
                        all_found.append((idx, idy))
            if len(all_found) == 1:
                return found
            elif len(all_found) > 1:
                # naked pairs
                all_found_poss = [poss_group[idx][idy]
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
                                        poss_group[all_found[idz][0]
                                                   ][all_found[idz][1]].remove(val)
                                    except ValueError:
                                        pass
                # if val is only possible in one row or column of this block, eliminate val from the other block poss's
                found_row = all_found[0][0]
                found_col = all_found[0][1]
                for f in all_found[1:]:
                    if f[0] != found_row:
                        found_row = None
                    if f[1] != found_col:
                        found_col = None
                if found_row is not None:
                    keep_cols = [col for (row, col) in all_found]
                    for idy, _ in enumerate(poss_group[found_row]):
                        if idy not in keep_cols:
                            try:
                                poss_group[found_row][idy].remove(val)
                            except ValueError:
                                pass
                if found_col is not None:
                    keep_rows = [row for (row, col) in all_found]
                    for idx, _ in enumerate(poss_group):
                        if idx not in keep_rows:
                            try:
                                poss_group[idx][found_col].remove(val)
                            except ValueError:
                                pass
        return None

    def solve_recurse(self) -> None:
        grid = numpy.array(self.inp_arr)
        grid = self.__solve_recurse_inner(grid)
        if grid is not None:
            self.sol_arr = grid
        else:
            raise ValueError("The given board is unsolvable.")

    def __solve_recurse_inner(self, grid: numpy.ndarray) -> numpy.ndarray:
        for idx, row in enumerate(grid):
            for idy, col_val in enumerate(row):
                if col_val is None:
                    col = grid[:, idy]

                    block_num = self.__get_block_num(idx, idy)
                    block_range = self.__get_block_range(block_num)
                    block = grid[numpy.ix_(
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

    def verify_board(self, solution: List[List]) -> Tuple | None:
        for x, row in enumerate(self.sol_arr):
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
