import unittest
import test.debug
import concrete
import typecheck

class TestLists(unittest.TestCase):
    def test_assign(self):
        logs = test.debug.execute_and_get_logs('test/lists/test_files/assign.mu')

        self.assertEqual(logs, [
            concrete.ConcreteList([]),
            concrete.ConcreteList([
                concrete.ConcreteInteger(1),
                concrete.ConcreteInteger(2),
                concrete.ConcreteInteger(3)
            ]),
            concrete.ConcreteList([
                concrete.ConcreteInteger(1),
                concrete.ConcreteDecimal(1.0),
                concrete.ConcreteString('a'),
                concrete.ConcreteList([concrete.ConcreteInteger(1)]),
                concrete.ConcreteSet({concrete.ConcreteInteger(1)}),
                concrete.ConcreteObject({
                    'a': concrete.ConcreteInteger(1)
                }, {
                    'a': concrete.ConcreteUndefined()
                })
            ])
        ])
    
    def test_coalesce(self):
        logs = test.debug.execute_and_get_logs('test/lists/test_files/coalesce.mu')

        self.assertEqual(logs, [
            concrete.ConcreteList([
                concrete.ConcreteInteger(1),
                concrete.ConcreteInteger(2),
                concrete.ConcreteInteger(3)
            ]),
            concrete.ConcreteList([
                concrete.ConcreteInteger(1),
                concrete.ConcreteInteger(2),
                concrete.ConcreteInteger(3),
                concrete.ConcreteInteger(4)
            ])
        ])

    def test_const(self):
        self.assertRaises(Exception, test.debug.execute_and_get_logs, 'test/lists/test_files/const.mu')

    def test_type(self):    
        test.debug.execute_and_get_logs('test/lists/test_files/type.mu')

    def test_wrong_type(self):
        self.assertRaises(typecheck.TypeException, test.debug.execute_and_get_logs, 'test/lists/test_files/wrong_type.mu')
