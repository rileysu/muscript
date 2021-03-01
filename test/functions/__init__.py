import unittest
import test.debug
import concrete
import typecheck

class TestFunctions(unittest.TestCase):
    def test_assign(self):
        logs = test.debug.execute_and_get_logs('test/functions/test_files/assign.mu')
        
        self.assertIsInstance(logs[0], concrete.ConcreteFunction)
        self.assertEqual(logs[1], concrete.ConcreteEmpty())

    def test_coalesce(self):
        logs = test.debug.execute_and_get_logs('test/functions/test_files/coalesce.mu')

        func3 = logs[2]

        self.assertEqual(logs[5:], [
            func3,
            concrete.ConcreteInteger(4)
        ])

    def test_type(self):
        logs = test.debug.execute_and_get_logs('test/functions/test_files/type.mu')

        func_a = logs[0]
        func_b = logs[1]
        func_c = logs[3]

        self.assertEqual(logs, [
            func_a,
            func_b,
            concrete.ConcreteInteger(1),
            func_c,
            concrete.ConcreteInteger(2)
        ])

    def test_closure(self):
        logs = test.debug.execute_and_get_logs('test/functions/test_files/closure.mu')

        self.assertEqual(logs, [
            concrete.ConcreteInteger(1)
        ])

    def test_closure_mutation(self):
        logs = test.debug.execute_and_get_logs('test/functions/test_files/closure_mutation.mu')

        self.assertEqual(logs, [
            concrete.ConcreteInteger(2)
        ])

    def test_closure_hidden_mutation(self):
        logs = test.debug.execute_and_get_logs('test/functions/test_files/closure_hidden_mutation.mu')

        self.assertEqual(logs, [
            concrete.ConcreteInteger(0),
            concrete.ConcreteInteger(1),
            concrete.ConcreteInteger(1),
        ])

    def test_deep_nested_closure_mutation(self):
        logs = test.debug.execute_and_get_logs('test/functions/test_files/deep_nested_closure_mutation.mu')

        self.assertEqual(logs, [
            concrete.ConcreteInteger(1)
        ])

    def test_object_self(self):
        logs = test.debug.execute_and_get_logs('test/functions/test_files/object_self.mu')

        self.assertEqual(logs, [
            concrete.ConcreteInteger(1),
            concrete.ConcreteInteger(0)
        ])

    def test_nested_object_self(self):
        logs = test.debug.execute_and_get_logs('test/functions/test_files/nested_object_self.mu')

        self.assertEqual(logs, [
            concrete.ConcreteInteger(0),
            concrete.ConcreteInteger(1)
        ])

    def test_higher_order(self):
        logs = test.debug.execute_and_get_logs('test/functions/test_files/higher_order.mu')

        self.assertEqual(logs, [
            concrete.ConcreteInteger(1)
        ])

    def test_const(self):
        self.assertRaises(Exception, test.debug.execute_and_get_logs, 'test/functions/test_files/const.mu')

    def test_wrong_arg_type(self):
        self.assertRaises(typecheck.TypeException, test.debug.execute_and_get_logs, 'test/functions/test_files/wrong_type.mu')
    
    def test_wrong_bind_type(self):
        self.assertRaises(typecheck.TypeException, test.debug.execute_and_get_logs, 'test/functions/test_files/wrong_bind_type.mu')
    
    def test_wrong_return_type(self):
        self.assertRaises(typecheck.TypeException, test.debug.execute_and_get_logs, 'test/functions/test_files/wrong_return_type.mu')
