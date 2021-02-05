import unittest
import test.debug
import concrete
import typecheck

class TestIntegers(unittest.TestCase):
    def test_assign(self):
        logs = test.debug.execute_and_get_logs('test/integers/test_files/assign.mu')

        self.assertEqual(logs, [
            concrete.ConcreteInteger(1)
        ])
    
    def test_coalesce(self):
        logs = test.debug.execute_and_get_logs('test/integers/test_files/coalesce.mu')

        self.assertEqual(logs, [
            concrete.ConcreteInteger(3),
            concrete.ConcreteInteger(4)
        ])

    def test_type(self):    
        logs = test.debug.execute_and_get_logs('test/integers/test_files/type.mu')

        self.assertEqual(logs, [
            concrete.ConcreteInteger(1)
        ])

    def test_const(self):
        self.assertRaises(Exception, test.debug.execute_and_get_logs, 'test/integers/test_files/const.mu')

    def test_wrong_type(self):
        self.assertRaises(typecheck.TypeException, test.debug.execute_and_get_logs, 'test/integers/test_files/wrong_type.mu')
