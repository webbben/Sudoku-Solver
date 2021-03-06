import unittest

def TestFactory(module):

    class TestA3(unittest.TestCase):

        def __init__(self, test):
            super(TestA3,self).__init__(test)

            #bind module functions to tester class
            self.Board = module.Board
            self.Solver = module.Solver

        #################################
        # Board.makeMove
        #################################

        def test_makeMove(self):

            b = self.Board("testBoard_singletonsOnly.csv")

            b.makeMove((0,0), 3)
            self.assertSequenceEqual({3,7,4,8,1,9}, b.valsInCols[0])
            self.assertSequenceEqual({3, 4, 5}, b.valsInRows[0])
            self.assertSequenceEqual({2,3,4,5,7,8,9}, b.valsInBoxes[0])
            self.assertNotIn((0,0), b.unSolved)
            self.assertEqual(b.board[(0,0)], 3)

            b.makeMove((8, 8), 1)
            self.assertSequenceEqual({1,2,3,4,6,7}, b.valsInCols[8])
            self.assertSequenceEqual({1,6,9}, b.valsInRows[8])
            self.assertSequenceEqual({1,2,3,4,5,6,9}, b.valsInBoxes[8])
            self.assertNotIn((8, 8), b.unSolved)
            self.assertEqual(b.board[(8, 8)], 1)

            b.makeMove((4, 4), 5)
            self.assertSequenceEqual({1, 4, 5}, b.valsInCols[4])
            self.assertSequenceEqual({2,3,4,5,6,7,8}, b.valsInRows[4])
            self.assertSequenceEqual({8,1,4,5,6}, b.valsInBoxes[4])
            self.assertNotIn((4,4), b.unSolved)
            self.assertEqual(b.board[(4,4)], 5)

        #################################
        # Board.removeMove
        #################################

        def test_removeMove(self):

            b = self.Board("testBoard_med.csv")

            b.removeMove((0, 0), 5)
            self.assertSequenceEqual({8,3}, b.valsInCols[0])
            self.assertSequenceEqual({9,2,4,7}, b.valsInRows[0])
            self.assertSequenceEqual({8,7}, b.valsInBoxes[0])
            self.assertIn((0, 0), b.unSolved)
            self.assertNotIn((0,0), b.board)

            b.removeMove((5, 3), 8)
            self.assertSequenceEqual({2,4,6}, b.valsInCols[3])
            self.assertSequenceEqual({9, 3,4}, b.valsInRows[5])
            self.assertSequenceEqual({5}, b.valsInBoxes[4])
            self.assertIn((5, 3), b.unSolved)
            self.assertNotIn((5, 3), b.board)

            b.removeMove((8, 8), 2)
            self.assertSequenceEqual({6,7}, b.valsInCols[8])
            self.assertSequenceEqual({8,3,6,7}, b.valsInRows[8])
            self.assertSequenceEqual({8,6}, b.valsInBoxes[8])
            self.assertIn((8, 8), b.unSolved)
            self.assertNotIn((8, 8), b.board)


        #################################
        # Board.isValidMove
        #################################
        def test_isValidMove(self):
            b = self.Board("testBoard_med.csv")

            self.assertFalse(b.isValidMove((1, 2), 5))
            self.assertFalse(b.isValidMove((1, 2), 8))
            self.assertFalse(b.isValidMove((1, 2), 9))
            self.assertFalse(b.isValidMove((4, 3), 5))
            self.assertFalse(b.isValidMove((8, 4), 5))
            self.assertFalse(b.isValidMove((6, 4), 4))
            self.assertFalse(b.isValidMove((8, 8), 8))


            self.assertTrue(b.isValidMove((0, 8), 1))
            self.assertTrue(b.isValidMove((4, 1), 5))
            self.assertTrue(b.isValidMove((4, 8), 5))
            self.assertTrue(b.isValidMove((6, 8), 1))
            self.assertTrue(b.isValidMove((6, 8), 3))


        #################################
        # Board.getMostConstrainedUnsolvedSpace
        #################################
        def test_getMostConstrainedUnsolvedSpace(self):

            a = self.Board("testBoard_singletonsOnly.csv")
            a_space = a.getMostConstrainedUnsolvedSpace()
            self.assertIn(a_space, [(4, 0), (3, 6), (2, 2)])


            b = self.Board("testBoard_med.csv")
            b_space = b.getMostConstrainedUnsolvedSpace()
<<<<<<< HEAD
            #self.assertIn(b_space, [(8,2), (0,6)])
=======
            self.assertIn(b_space, [(3, 0), (5, 6), (8, 0), (5, 8), (3, 2), (8, 2), (3, 1), (5, 7), (4, 3), (8, 4)])
>>>>>>> bd9d1fd8e0b3143037a27b2fbbd1f9178d8bca00

            c = self.Board("testBoard_hard.csv")
            c_space = c.getMostConstrainedUnsolvedSpace()
            self.assertIn(c_space, [(3, 2)])

            d = self.Board("testBoard_dastardly.csv")
            d_space = d.getMostConstrainedUnsolvedSpace()
            self.assertIn(d_space, [(1, 0)])


        # #################################
        # # Solver.solve
        # #################################
        def test_solve_easy(self):

            a = self.Solver("testBoard_singletonsOnly.csv")
            a_solved = self.Board("testBoard_singletonsOnly_solution.csv")
            self.assertDictEqual(a.board.board, a_solved.board)

        def test_solve_med(self):
            b = self.Solver("testBoard_med.csv")
            b_solved = self.Board("testBoard_med_solution.csv")
            self.assertDictEqual(b.board.board, b_solved.board)

        def test_solve_hard(self):
            c = self.Solver("testBoard_hard.csv")
            c_solved = self.Board("testBoard_hard_solution.csv")
            self.assertDictEqual(c.board.board, c_solved.board)

        def test_solve_dastardly(self):
            d = self.Solver("testBoard_dastardly.csv")
            d_solved = self.Board("testBoard_dastardly_solution.csv")
            self.assertDictEqual(d.board.board, d_solved.board)



    return TestA3


if __name__ == "__main__":

    #CHANGE THE IMPORT TO BE THE MAIN FILE NAME (i.e., a1)
    mod = __import__("a3_solution")

    unittest.TextTestRunner(verbosity=0).run(
        unittest.TestLoader()
            .loadTestsFromTestCase(testCaseClass=TestFactory(mod)))

