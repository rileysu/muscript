import unittest
import test.debug
import concrete
import typecheck

class TestControl(unittest.TestCase):
    def test_if(self):
        logs = test.debug.execute_and_get_logs('test/control/test_files/if.mu')

        self.assertEqual(logs, [
            concrete.ConcreteInteger(1),
            concrete.ConcreteInteger(1),
            concrete.ConcreteInteger(1),
            concrete.ConcreteInteger(1),
            concrete.ConcreteInteger(1),
            concrete.ConcreteInteger(1)
        ])
    
    def test_only(self):
        logs = test.debug.execute_and_get_logs('test/control/test_files/only.mu')

        self.assertEqual(logs, [
            concrete.ConcreteInteger(1)
        ])

    def test_while(self):    
        logs = test.debug.execute_and_get_logs('test/control/test_files/while.mu')

        self.assertEqual(logs, [
            concrete.ConcreteInteger(0),
            concrete.ConcreteInteger(0),
            concrete.ConcreteInteger(0),
            concrete.ConcreteInteger(0),
            concrete.ConcreteInteger(1)
        ])

    def test_for_each(self):    
        logs = test.debug.execute_and_get_logs('test/control/test_files/for_each.mu')

        # Set will return things in an arbitrary order but this still works
        # If test fails in the future change this so it doesn't depend on order

        self.assertEqual(logs, [
            concrete.ConcreteInteger(1),
            concrete.ConcreteInteger(2),
            concrete.ConcreteInteger(3),
            concrete.ConcreteInteger(4),
            concrete.ConcreteInteger(1),
            concrete.ConcreteInteger(2),
            concrete.ConcreteInteger(3),
            concrete.ConcreteInteger(4)
        ])

    def test_match(self):
        logs = test.debug.execute_and_get_logs('test/control/test_files/match.mu')


        self.assertEqual(logs, [
            concrete.ConcreteInteger(1),
            concrete.ConcreteInteger(1),
            concrete.ConcreteInteger(1),
            concrete.ConcreteInteger(1),
            concrete.ConcreteInteger(1)
        ])
