#!/usr/bin/env python3
import os
import lab
import json
import unittest
import doctest
from copy import deepcopy

import sys
sys.setrecursionlimit(10000)

TEST_DIRECTORY = os.path.dirname(__file__)

TESTDOC_FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
TESTDOC_SKIP = ["lab", "lab.HyperMinesGame", "lab.HyperMinesGame.dump",
                "lab.HyperMinesGame.from_dict"]


class TestDocTests(unittest.TestCase):
    def test_doctests_run(self):
        """ Checking to see if all lab doctests run successfully """
        results = doctest.testmod(lab, optionflags=TESTDOC_FLAGS, report=False)
        self.assertEqual(results[0], 0)

    def test_all_doc_strings_exist(self):
        """ Checking if docstrings have been written for everything in lab.py """
        tests = doctest.DocTestFinder(exclude_empty=False).find(lab)
        for test in tests:
            if test.name in TESTDOC_SKIP:
                continue
            if not test.docstring:
                self.fail("Oh no, '{}' has no docstring!".format(test.name))

    def test_all_doc_tests_exist(self):
        """ Checking if doctests have been written for everything in lab.py """
        tests = doctest.DocTestFinder(exclude_empty=False).find(lab)
        for test in tests:
            if test.name in TESTDOC_SKIP:
                continue
            if not test.examples:
                self.fail("Oh no, '{}' has no doctests!".format(test.name))

class TestHelpfunc(unittest.TestCase):
    def test_build_init(self):
        result = lab.build_init([3,2], 0)
        expected = [[0,0],
                    [0,0],
                    [0,0]
                    ]
        self.assertEqual(result, expected)
    
    def test_get_value_1(self):
        board = [[1,2,3],
                 [4,5,6]
                ]
        result = lab.get_value([1,1], board)
        expected = 5
        self.assertEqual(result, expected)
        
    def test_get_value_2(self):
        board = [[[1,1],[2,2],[3,3]],
                 [[4,4],[5,5],[6,6]]
                ]
        result = lab.get_value([0,0,0], board)
        expected = 1
        self.assertEqual(result, expected)
        
    def test_replace_value_1(self):
        board = [[1,2,3],
                 [4,5,6]
                ]
        lab.replace_value([1,1], 0, board)
        expected = [[1,2,3],
                    [4,0,6]
                    ]
        self.assertEqual(board, expected)
    
    def test_replace_value_2(self):
        board = [[1,2,3],
                [5,5,5]]                
        lab.replace_value([0,0], 0, board)
        expected = [[0,2,3],
                    [5,5,5]]   
        self.assertEqual(board, expected)
    
    def test_replace_value_3(self):
        board = [[1,2,3]]                
        lab.replace_value([0,1], 0, board)
        expected = [[1,0,3]]
        self.assertEqual(board, expected)
        
    def test_get_neighbors_1(self):
        board = [[1,2,3,4],
                 [5,6,7,8],
                 [9,10,11,12]]                
        result = list(lab.get_neighbors([1,1], [3,4], board))
        expected = [(0, 0),(0, 1),(0, 2),
                     (1, 0),(1, 1),(1, 2),
                     (2, 0),(2, 1),(2, 2)]
        self.assertEqual(result, expected)
        
    def test_get_neighbors_2(self):
        board = [[1,2,3,4],
                 [5,6,7,8],
                 [9,10,11,12]]                
        result = lab.get_neighbors([0,1], [3,4], board)
        expected = ((i,j) for i in range(2) for j in range(3))
        self.assertTrue(all(a==b for a,b in zip(result, expected)))
     
    def test_get_coors(self):
        result = lab.get_coors([3,2])
        expected = ((i,j) for i in range(3) for j in range(2))
        self.assertTrue(all(a==b for a,b in zip(result,expected)))  
        
class TestNewGame(unittest.TestCase):    
    def test_newsmall6dgame(self):
        """ Testing new_game on a small 6-D board """
        with open("test_outputs/test_newsmall6dgame.json") as f:
            expected = json.load(f)
        with open("test_inputs/test_newsmall6dgame.json") as f:
            inputs = json.load(f)
        result = lab.HyperMinesGame(inputs["dimensions"], inputs["bombs"])
        for i in ('dimensions', 'board', 'mask', 'state'):
            self.assertEqual(getattr(result, i), expected[i])


    def test_newlarge4dgame(self):
        """ Testing new_game on a large 4-D board """
        with open("test_outputs/test_newlarge4dgame.json") as f:
            expected = json.load(f)
        with open("test_inputs/test_newlarge4dgame.json") as f:
            inputs = json.load(f)
        result = lab.HyperMinesGame(inputs["dimensions"], inputs["bombs"])
        for i in ('dimensions', 'board', 'mask', 'state'):
            self.assertEqual(getattr(result, i), expected[i])

class TestIntegration(unittest.TestCase):
    def _test_integration(self, n):
        with open("test_outputs/test_integration%s.json" % n) as f:
            expected = json.load(f)
        with open("test_inputs/test_integration%s.json" % n) as f:
            inputs = json.load(f)
        g = lab.HyperMinesGame(inputs['dimensions'], inputs['bombs'])
        for location, results in zip(inputs['digs'], expected):
            squares_revealed, game, rendered, rendered_xray = results
            res = g.dig(location)
            self.assertEqual(res, squares_revealed)
            for i in ('dimensions', 'board', 'mask', 'state'):
                self.assertEqual(getattr(g, i), game[i])
            self.assertEqual(g.render(), rendered)
            self.assertEqual(g.render(True), rendered_xray)

    def test_integration1(self):
        """ dig and render, repeatedly, on a large board"""
        self._test_integration(1)

    def test_integration2(self):
        """ dig and render, repeatedly, on a large board"""
        self._test_integration(2)

    def test_integration3(self):
        """ dig and render, repeatedly, on a large board"""
        self._test_integration(3)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
