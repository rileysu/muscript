import unittest
import test.debug
import concrete
import typecheck

class TestDecimals(unittest.TestCase):
    def test_assign(self):
        logs = test.debug.execute_and_get_logs('test/decimals/test_files/assign.mu')

        self.assertEqual(logs, [
            concrete.ConcreteDecimal(1.0),
            concrete.ConcreteDecimal(2.0)
        ])
    
    def test_coalesce(self):
        logs = test.debug.execute_and_get_logs('test/decimals/test_files/coalesce.mu')

        self.assertEqual(logs, [
            concrete.ConcreteDecimal(3.0),
            concrete.ConcreteDecimal(4.0)
        ])

    def test_type(self):    
        logs = test.debug.execute_and_get_logs('test/decimals/test_files/type.mu')

        self.assertEqual(logs, [
            concrete.ConcreteDecimal(1.0)
        ])

    def test_const(self):
        self.assertRaises(typecheck.TypeException, test.debug.execute_and_get_logs, 'test/decimals/test_files/const.mu')

    def test_wrong_type(self):
        self.assertRaises(typecheck.TypeException, test.debug.execute_and_get_logs, 'test/decimals/test_files/wrong_type.mu')
