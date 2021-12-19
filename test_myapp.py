import unittest
from myapp import myapp

class TestCalc(unittest.TestCase):
    def setUp(self):
        myapp.testing = True
        self.myapp = myapp.test_client()
    def test_calc(self):
        self.myapp.get('/operation/', query_string=dict(optype='sum', line1='344', line2='452'))

if __name__ == "__main__":
    unittest.main()