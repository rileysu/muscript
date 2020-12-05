import parser
import execution
import unittest
import environment

class TestInteger(unittest.TestCase):
    def setUp(self):
        with open('test/testfiles/integer.mu') as f:
            text = f.read()

            p = parser.Parser()
            
            self.tree = p.parse(text)
            self.statements = parser.TreeTransformer().transform(self.tree)

            self.scope = execution.Scope(environment.init_scope_values, environment.init_scope_types)
            self.env = execution.ExecutionEnvironment(self.scope)

    def test_integer(self):
        self.env.execute(self.statements)
