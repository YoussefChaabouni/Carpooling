#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 13:02:43 2020

@author: ariabbas
"""

## Our matching algorithm is based on the Hungarian method, which is a
## combinatorial optimization algorithm that solves the assignment problem
## Specifically, we impletemented the Kuhn–Munkres algorithm also called
## the Munkres assignment algorithm.

import sys
import copy
from typing import Union, NewType, Sequence, Tuple, Optional, Callable


# global var

AnyNum = NewType('AnyNum', Union[int, float])
Matrix = NewType('Matrix', Sequence[Sequence[AnyNum]])

# const

class DISALLOWED_OBJ(object):
    pass
DISALLOWED = DISALLOWED_OBJ()
DISALLOWED_PRINTVAL = "D"


class Matching:
    """
    Compute the Kunh-Munkres solution to the matching problem.
    """

    def __init__(self):
        self.C = None
        self.row_covered = []
        self.col_covered = []
        self.n = 0
        self.Z0_r = 0
        self.Z0_c = 0
        self.marked = None
        self.path = None
        
    def pad_matrix(self, matrix: Matrix, pad_value: int=0) -> Matrix:
        max_columns = 0
        total_rows = len(matrix)