from parser import Parser, TreeTransformer
from execution import ExecutionEnvironment, Scope
from environment import init_scope_values, init_scope_types

parser = Parser()

with open('examples/turtle.mu') as f:
    text = f.read()

    tree = parser.parse(text)
    statements = TreeTransformer().transform(tree)

    scope = Scope(init_scope_values, init_scope_types)
    env = ExecutionEnvironment(scope)

    env.execute(statements)

    #for matter in scope.map:
    #    print(matter)
    #    print(scope.map[matter])
