import unittest
import test.debug
import concrete
import typecheck

class TestObjects(unittest.TestCase):
    def test_assign_all_types(self):
        logs = test.debug.execute_and_get_logs('test/objects/test_files/assign_all_types.mu')

        self.assertEqual(logs, [
            concrete.ConcreteObject({
                'int': concrete.ConcreteInteger(1),
                'dec': concrete.ConcreteDecimal(1.1),
                'list': concrete.ConcreteList((
                    concrete.ConcreteInteger(1),
                    concrete.ConcreteInteger(2),
                    concrete.ConcreteInteger(3)
                )),
                'set': concrete.ConcreteSet(frozenset({
                    concrete.ConcreteInteger(1),
                    concrete.ConcreteInteger(2),
                    concrete.ConcreteInteger(3)
                })),
                'object': concrete.ConcreteObject({
                    'a': concrete.ConcreteInteger(1),
                    'b': concrete.ConcreteInteger(2)
                }, {
                    'a': concrete.ConcreteUndefined(),
                    'b': concrete.ConcreteUndefined()
                })
            }, {
                'int': concrete.ConcreteType('Integer'),
                'dec': concrete.ConcreteType('Decimal'),
                'list': concrete.ConcreteType('List'),
                'set': concrete.ConcreteType('Set'),
                'object': concrete.ConcreteType('Object')
            })
        ])

    def test_coalesce(self):
        logs = test.debug.execute_and_get_logs('test/objects/test_files/coalesce.mu')

        self.assertEqual(logs, [
            concrete.ConcreteObject({}, {}),
            concrete.ConcreteObject({
                'a': concrete.ConcreteInteger(1)
            }, {
                'a': concrete.ConcreteUndefined()
            }),
            concrete.ConcreteObject({
                'a': concrete.ConcreteInteger(3),
                'b': concrete.ConcreteInteger(2)
            }, {
                'a': concrete.ConcreteUndefined(),
                'b': concrete.ConcreteUndefined()
            })
        ])

    def test_types(self):
        logs = test.debug.execute_and_get_logs('test/objects/test_files/types.mu')
   
        function = logs[0]

        self.assertEqual(logs, [
            function,
            concrete.ConcreteObject({
                'int': concrete.ConcreteInteger(1),
                'dec': concrete.ConcreteDecimal(1.1),
                'list': concrete.ConcreteList((
                    concrete.ConcreteInteger(1),
                    concrete.ConcreteInteger(2),
                    concrete.ConcreteInteger(3)
                )),
                'fun': function,
                'otherobj': concrete.ConcreteObject({
                    'a': concrete.ConcreteInteger(1),
                    'b': concrete.ConcreteInteger(2)
                }, {
                    'a': concrete.ConcreteUndefined(),
                    'b': concrete.ConcreteUndefined()
                })
            }, {
                'int': concrete.ConcreteUndefined(),
                'dec': concrete.ConcreteUndefined(),
                'list': concrete.ConcreteUndefined(),
                'fun': concrete.ConcreteUndefined(),
                'otherobj': concrete.ConcreteUndefined()
            })
        ])

    def test_wrong_type(self):
        self.assertRaises(typecheck.TypeException, test.debug.execute_and_get_logs, 'test/objects/test_files/wrong_type.mu')

    def test_wrong_nested_type(self):
        self.assertRaises(typecheck.TypeException, test.debug.execute_and_get_logs, 'test/objects/test_files/wrong_nested_type.mu')

    def test_self(self):
        logs = test.debug.execute_and_get_logs('test/objects/test_files/self.mu')

        function = logs[0]

        self.assertEqual(logs, [
            function,
            concrete.ConcreteObject({
                'f': function
            }, {
                'f': concrete.ConcreteUndefined()
            }),
            concrete.ConcreteObject({
                'f': function
            }, {
                'f': concrete.ConcreteUndefined()
            })
        ])
