import unittest
import test.debug
import concrete
import typecheck

class TestStrings(unittest.TestCase):
    def test_assign(self):
        logs = test.debug.execute_and_get_logs('test/strings/test_files/assign.mu')

        self.assertEqual(logs, [
            concrete.ConcreteString('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`~1!2@3#4$5%6^7&8*9(0)-_=+[{]}\\|;:",<.>/?'),
            concrete.ConcreteString('\''),
            concrete.ConcreteString('abcdef\\')
        ])
    
    def test_coalesce(self):
        logs = test.debug.execute_and_get_logs('test/strings/test_files/coalesce.mu')

        self.assertEqual(logs, [
            concrete.ConcreteString('Hello World!'),
            concrete.ConcreteString('abc')
        ])

    def test_type(self):    
        logs = test.debug.execute_and_get_logs('test/strings/test_files/type.mu')

        self.assertEqual(logs, [
            concrete.ConcreteString('Hello World!')
        ])

    def test_const(self):
        self.assertRaises(Exception, test.debug.execute_and_get_logs, 'test/strings/test_files/const.mu')
    
    def test_wrong_type(self):
        self.assertRaises(typecheck.TypeException, test.debug.execute_and_get_logs, 'test/strings/test_files/wrong_type.mu')
