#!/usr/bin/env python3
import os
import lab
import json
import unittest
import copy

import sys
sys.setrecursionlimit(10000)

TEST_DIRECTORY = os.path.join(os.path.dirname(__file__), 'test_inputs')
DB_DIRECTORY = os.path.join(os.path.dirname(__file__), 'resources/db')

class TestSimplify(unittest.TestCase):
    def test_01(self):
        formula = [[("a", True), ("b", False), ("c", True)], [("a", False)]]
        assignments = {"a": False}
        result = lab.simplify_formula(formula, assignments)
        expected = ([[("b", False), ("c", True)]], False)
        self.assertEqual(result, expected)

    def test_02(self):
        formula = [[("a", True)]]
        assignments = dict()
        result = lab.simplify_formula(formula, assignments)
        expected = ([], True)
        self.assertEqual(result, expected)
        
    def test_03(self):
        formula = [[("a", True)], [("a", False)]]
        assignments = dict()
        result = lab.simplify_formula(formula, assignments)
        expected = (None, False)
        self.assertEqual(result, expected)
             
    def test_04(self):
        formula = [[("a", True), ("b", False), ("c", True)], [("a", True), ("b", True)]]
        assignments = {"a": False}
        result = lab.simplify_formula(formula, assignments)
        expected = ([], True)
        self.assertEqual(result, expected)
        
    def test_05(self):
        formula = [[("a", True), ("b", True), ("c", False)],
                        [("d", False), ("e", True), ("f", False)],
                        [("a", False), ("b", False)],
                        [("a", False), ("d", True)]]
        assignments = {"a": True}
        result = lab.simplify_formula(formula, assignments)
        expected = ([[("e", True), ("f", False)]], True)
        self.assertEqual(result, expected)
        
        
class TestSat(unittest.TestCase):
    def opencase(self, casename):
        with open(os.path.join(TEST_DIRECTORY, casename + ".json")) as f:
            cnf = json.load(f)
            return [[(variable, polarity)
                     for variable, polarity in clause]
                    for clause in cnf]

    def satisfiable(self, casename):
        cnf = self.opencase(casename)
        asgn = lab.satisfying_assignment(copy.deepcopy(cnf))
#        print(asgn)
        self.assertIsNotNone(asgn)

        # Check that every clause has some literal appearing in the assignment.
        self.assertTrue(all(any(variable in asgn and asgn[variable] == polarity
                                for variable, polarity in clause)
                            for clause in cnf))

    def unsatisfiable(self, casename):
        cnf = self.opencase(casename)
        asgn = lab.satisfying_assignment(copy.deepcopy(cnf))
        self.assertIsNone(asgn)

    def get_rules(self):
        rule1 = [[('adam', True), ('erik', True), ('duane', True),
                  ('armando', True), ('tim', True)]]
        rule2 = [[('adam', False), ('erik', False)],
                 [('adam', False), ('duane', False)],
                 [('adam', False), ('armando', False)],
                 [('adam', False), ('tim', False)],
                 [('erik', False), ('duane', False)],
                 [('erik', False), ('armando', False)],
                 [('erik', False), ('tim', False)],
                 [('duane', False), ('armando', False)],
                 [('duane', False), ('tim', False)],
                 [('armando', False), ('tim', False)]]
        rule3 = [[('chocolate', False), ('vanilla', False), ('pickles', False)],
                 [('chocolate', True), ('vanilla', True)],
                 [('chocolate', True), ('pickles', True)],
                 [('vanilla', True), ('pickles', True)]]
        rule4 = [[('adam', False), ('pickles', True)],
                 [('adam', False), ('chocolate', False)],
                 [('adam', False), ('vanilla', False)]]
        rule5 = [[('erik', False), ('duane', True)],
                 [('duane', False), ('erik', True)]]
        rule6 = [[('armando', False), ('chocolate', True)],
                 [('armando', False), ('vanilla', True)],
                 [('armando', False), ('pickles', True)]]
        rules = rule1 + rule2 + rule3 + rule4 + rule5 + rule6
        return rules

    def test_class_example(self):
        rules = self.get_rules()
        asgn = lab.satisfying_assignment(rules)
        self.assertTrue('tim' in asgn and asgn['tim']==True)
        self.assertTrue(all(any(variable in asgn and asgn[variable] == polarity
                                for variable, polarity in clause)
                            for clause in rules))
        
        
    def test_class_example_unsat(self):
        rules = self.get_rules()
        asgn = lab.satisfying_assignment(rules + [[('tim', False)]])
        expected = None
        self.assertEqual(asgn, expected)

    def test_A_10_3_100(self):
        self.unsatisfiable('10_3_100')

    def test_B_20_3_1000(self):
        self.unsatisfiable('20_3_1000')

#    def test_C_100_10_100(self):
#        self.satisfiable('100_10_100') # time 
#
#    def test_D_1000_5_10000(self):
#        self.unsatisfiable('1000_5_10000')
#
#    def test_E_1000_10_1000(self):
#        self.satisfiable('1000_10_1000')
##
#    def test_F_1000_11_1000(self):
#        self.satisfiable('1000_11_1000')

    def test_G_1_0_1(self):
        self.satisfiable('1_0_1')

    def test_H_1_0_1_0(self):
        self.satisfiable('1_0_1_0')

db = [
          [1532, 1532, 617],
          [1532, 4724, 617],
          [2876, 4724, 617],
          [2876, 2876, 617],
          [4724, 4724, 617],
          [1640, 2876, 31932],
          [2876, 2876, 31932],
          [1640, 1640, 31932],
          [1640, 1640, 74881],
          [46866, 1640, 74881],
          [46866, 46866, 74881]
        ]
class TestHelp(unittest.TestCase):
    def test_adj(self):
        adj, actors = lab.make_adj(db)
        expe_adj = {1532:[4724],
                    4724:[1532,2876],
                    2876:[4724,1640],
                    1640:[2876,46866],
                    46866:[1640]
                }
        expe_actors = [1532, 4724, 2876, 1640, 46866]
        self.assertEqual(adj, expe_adj)
        self.assertEqual(actors, expe_actors)
    
    def test_maker(self):
        actors = [1532, 4724, 2876, 1640, 46866]
        K = 3
        ind_dict, ind_L = lab.make_vars_for_actors(actors, K)
       
        expe = {1532: [('1532_0', True), ('1532_1', True), ('1532_2', True)],
                4724: [('4724_0', True), ('4724_1', True), ('4724_2', True)],
                2876: [('2876_0', True), ('2876_1', True), ('2876_2', True)],
                1640: [('1640_0', True), ('1640_1', True), ('1640_2', True)], 
                46866: [('46866_0', True), ('46866_1', True), ('46866_2', True)]}
#        print(ind_L)
        self.assertEqual(ind_dict, expe)
        
    def test_all_sets(self):
        indic = [('1532_0', True), ('1532_1', True), ('1532_2', True)]
        res = lab.get_all_sets(indic)
#        print(list(res))
#        for i in res:
#            print(list(i))
    def test_rem(self):
        indic = [('1532_0', True), ('1532_1', True), ('1532_2', True)]
        res = lab.get_rem_sets(indic)
        
#        expe = [[('1532_1', True), ('1532_2', True), ('1532_0', False)], 
#                 [('1532_0', True), ('1532_2', True), ('1532_1', False)], 
#                 [('1532_0', True), ('1532_1', True), ('1532_2', False)]]
#        self.assertEqual(res, expe)
#        print(res)
        
    def test_const1(self):
        actors = [1532, 4724, 2876, 1640, 46866]
        ind_dict = {1532: [('1532_0', True), ('1532_1', True), ('1532_2', True)],
                4724: [('4724_0', True), ('4724_1', True), ('4724_2', True)],
                2876: [('2876_0', True), ('2876_1', True), ('2876_2', True)],
                1640: [('1640_0', True), ('1640_1', True), ('1640_2', True)], 
                46866: [('46866_0', True), ('46866_1', True), ('46866_2', True)]}
        res = lab.make_one_manager_constraints(actors, ind_dict)
#        print(res)
        
    def test_const2(self):
        adj = {1532:[4724],
                4724:[1532,2876],
                2876:[4724,1640],
                1640:[2876,46866],
                46866:[1640]}
        actors = [1532, 4724, 2876, 1640, 46866]
        ind_dict = {1532: [('1532_0', True), ('1532_1', True), ('1532_2', True)],
                4724: [('4724_0', True), ('4724_1', True), ('4724_2', True)],
                2876: [('2876_0', True), ('2876_1', True), ('2876_2', True)],
                1640: [('1640_0', True), ('1640_1', True), ('1640_2', True)], 
                46866: [('46866_0', True), ('46866_1', True), ('46866_2', True)]}
        res = lab.make_different_constraints(adj, ind_dict, actors)
#        self.assertTrue(len(res)==15)
#        print(res)
    
class TestActorManager(unittest.TestCase):
    def expect_sat(self, casename, K):
        with open(os.path.join(DB_DIRECTORY, casename + ".json")) as f:
            database = json.load(f)
        sol = lab.managers_for_actors(K, database)
        if sol is None:
            return False
        return lab.check_solution(sol, K, database)

    def expect_unsat(self, casename, K):
        with open(os.path.join(DB_DIRECTORY, casename + ".json")) as f:
            database = json.load(f)
        sol = lab.managers_for_actors(K, database)
        return sol is None

    def test_01_tiny(self):
        sol = self.expect_sat('00_original_tiny', 4)
        self.assertTrue(sol)

    def test_01_tiny_unsat(self):
        sol = self.expect_unsat('00_original_tiny', 1)
        self.assertTrue(sol)
#
#    def test_01_chunks_smaller(self):
#        sol = self.expect_sat('01_chunks_smaller', 10)
#        self.assertTrue(sol)

#    def test_01_chunks_smaller_unsat(self):
#        sol = self.expect_unsat('01_chunks_smaller', 3)
#        self.assertTrue(sol)
#
#    def test_01_chunks_smaller2(self):
#        sol = self.expect_sat('01_chunks_smaller2', 10)
#        self.assertTrue(sol)
#
#    def test_01_chunks_smaller2_unsat(self):
#        sol = self.expect_unsat('01_chunks_smaller2', 3)
#        self.assertTrue(sol)
#
#
#    def test_split_chunks_smaller_0(self):
#        sol = self.expect_sat('split_chunks_smaller_0', 10)
#        self.assertTrue(sol)

    def test_split_chunks_smaller_0_unsat(self):
        sol = self.expect_unsat('split_chunks_smaller_0', 3)
        self.assertTrue(sol)
#
#    def test_split_chunks_smaller_1(self):
#        sol = self.expect_sat('split_chunks_smaller_1', 10)
#        self.assertTrue(sol)
#
    def test_split_chunks_smaller_1_unsat(self):
        sol = self.expect_unsat('split_chunks_smaller_1', 3)
        self.assertTrue(sol)

#    def test_split_chunks_smaller_2(self):
#        sol = self.expect_sat('split_chunks_smaller_2', 10)
#        self.assertTrue(sol)

    def test_split_chunks_smaller_2_unsat(self):
        sol = self.expect_unsat('split_chunks_smaller_2', 1)
        self.assertTrue(sol)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
