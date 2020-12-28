from parser import Parser, TreeTransformer
from environment import init_scope_values, init_scope_types
import context

parser = Parser()

with open('examples/include.mu') as f:
    text = f.read()

    tree = parser.parse(text)
    statements = TreeTransformer().transform(tree)

    ctx = context.Context(context.Scope(init_scope_values, init_scope_types))

    ctx.execute(statements)

    #for matter in scope.map:
    #    print(matter)
    #    print(scope.map[matter])
