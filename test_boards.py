#!/usr/bin/python3
# test_boards.py

e0 = [[6, None, None, None, None, 9, None, None, 2],
      [None, 4, 3, 1, None, 2, None, 9, None],
      [2, None, 1, None, None, 8, None, 6, 4],
      [9, None, None, None, None, None, 8, 7, 1],
      [8, None, 5, 7, 2, None, 3, None, None],
      [4, 3, 7, None, None, 1, 2, None, 6],
      [None, 7, None, None, 5, None, 6, None, None],
      [None, None, 6, 9, None, 3, 4, None, None],
      [None, 2, 4, None, None, None, None, None, 5]]

es0 = [[6, 5, 8, 4, 7, 9, 1, 3, 2],
       [7, 4, 3, 1, 6, 2, 5, 9, 8],
       [2, 9, 1, 5, 3, 8, 7, 6, 4],
       [9, 6, 2, 3, 4, 5, 8, 7, 1],
       [8, 1, 5, 7, 2, 6, 3, 4, 9],
       [4, 3, 7, 8, 9, 1, 2, 5, 6],
       [1, 7, 9, 2, 5, 4, 6, 8, 3],
       [5, 8, 6, 9, 1, 3, 4, 2, 7],
       [3, 2, 4, 6, 8, 7, 9, 1, 5]]

e1r = [[6, 1, 3, 4, 5, 9, 7, None, 2],
       [None, 4, 3, 1, None, 2, None, 9, None],
       [2, None, 1, None, None, 8, None, 6, 4],
       [9, None, None, None, None, None, 8, 7, 1],
       [8, None, 5, 7, 2, None, 3, None, None],
       [4, 3, 7, None, None, 1, 2, None, 6],
       [None, 7, None, None, 5, None, 6, None, None],
       [None, None, 6, 9, None, 3, 4, None, None],
       [1, 2, 4, 6, 7, 8, 9, None, 5]]

es1r = [[6, 5, 8, 4, 7, 9, 1, 3, 2],
        [7, 4, 3, 1, 6, 2, 5, 9, 8],
        [2, 9, 1, 5, 3, 8, 7, 6, 4],
        [9, 6, 2, 3, 4, 5, 8, 7, 1],
        [8, 1, 5, 7, 2, 6, 3, 4, 9],
        [4, 3, 7, 8, 9, 1, 2, 5, 6],
        [1, 7, 9, 2, 5, 4, 6, 8, 3],
        [5, 8, 6, 9, 1, 3, 4, 2, 7],
        [3, 2, 4, 6, 8, 7, 9, 1, 1]]

e2 = [[6, None, None, None, None, None, None, None, 4],
      [None, None, 9, None, 8, None, 2, None, 1],
      [None, 3, None, None, None, 9, None, None, None],
      [None, 5, None, 1, None, None, 6, None, 2],
      [None, None, None, None, 6, None, None, 3, None],
      [None, None, 2, None, None, None, None, 4, None],
      [None, None, None, None, None, None, None, 6, None],
      [7, None, None, 5, None, None, None, None, None],
      [None, None, 3, None, 1, None, 8, None, 9]]

es2 = [[6, 2, 8, 7, 5, 1, 3, 9, 4],
       [4, 7, 9, 3, 8, 6, 2, 5, 1],
       [1, 3, 5, 4, 2, 9, 7, 8, 6],
       [9, 5, 4, 1, 3, 8, 6, 7, 2],
       [8, 1, 7, 2, 6, 4, 9, 3, 5],
       [3, 6, 2, 9, 7, 5, 1, 4, 8],
       [2, 9, 1, 8, 4, 3, 5, 6, 7],
       [7, 8, 6, 5, 9, 2, 4, 1, 3],
       [5, 4, 3, 6, 1, 7, 8, 2, 9]]

e3 = [[None, None, None, 6, 5, None, None, 1, None],
      [None, None, 7, None, None, None, None, None, None],
      [8, 2, None, None, None, 9, 3, None, None],
      [None, None, 4, None, None, None, 5, None, None],
      [None, None, 3, None, None, 7, None, None, None],
      [5, 7, None, 9, None, None, None, None, 6],
      [None, None, None, None, 8, None, None, None, 3],
      [9, 5, None, None, None, 2, 8, None, None],
      [4, None, None, None, None, None, None, None, None]]

es3 = [[3, 4, 9, 6, 5, 8, 7, 1, 2],
       [1, 6, 7, 2, 3, 4, 9, 5, 8],
       [8, 2, 5, 7, 1, 9, 3, 6, 4],
       [2, 9, 4, 8, 6, 1, 5, 3, 7],
       [6, 8, 3, 5, 4, 7, 1, 2, 9],
       [5, 7, 1, 9, 2, 3, 4, 8, 6],
       [7, 1, 2, 4, 8, 5, 6, 9, 3],
       [9, 5, 6, 3, 7, 2, 8, 4, 1],
       [4, 3, 8, 1, 9, 6, 2, 7, 5]]

e4 = [[6, None, None, None, None, None, 7, None, None],
      [None, 4, None, None, 3, None, None, 6, 5],
      [None, None, 1, None, None, 8, None, None, None],
      [None, 6, None, None, 5, None, None, 3, 9],
      [4, None, None, 6, None, None, None, None, None],
      [None, None, None, None, None, None, None, 2, None],
      [8, None, None, None, None, 3, None, 9, 7],
      [None, None, None, None, 7, None, 4, None, None],
      [None, 9, None, None, None, None, 2, None, None]]

es4 = [[6, 3, 9, 4, 2, 5, 7, 1, 8],
       [2, 4, 8, 1, 3, 7, 9, 6, 5],
       [5, 7, 1, 9, 6, 8, 3, 4, 2],
       [1, 6, 2, 7, 5, 4, 8, 3, 9],
       [4, 8, 3, 6, 9, 2, 5, 7, 1],
       [9, 5, 7, 3, 8, 1, 6, 2, 4],
       [8, 2, 6, 5, 4, 3, 1, 9, 7],
       [3, 1, 5, 2, 7, 9, 4, 8, 6],
       [7, 9, 4, 8, 1, 6, 2, 5, 3]]

e5 = [[4, None, None, None, None, None, 9, 3, 8],
      [None, 3, 2, None, 9, 4, 1, None, None],
      [None, 9, 5, 3, None, None, 2, 4, None],
      [3, 7, None, 6, None, 9, None, None, 4],
      [5, 2, 9, None, None, 1, 6, 7, 3],
      [6, None, 4, 7, None, 3, None, 9, None],
      [9, 5, 7, None, None, 8, 3, None, None],
      [None, None, 3, 9, None, None, 4, None, None],
      [2, 4, None, None, 3, None, 7, None, 9]]


boards_sols = [(e0, es0), (e1r, es1r), (e2, es2),
               (e3, es3), (e4, es4), (e5, es1r)]
