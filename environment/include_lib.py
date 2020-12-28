import parser
import concrete
import context
import environment
import environment.check as check

def mu_include(_, relative_path):
    check.check_arg(relative_path, concrete.ConcreteType('String'))

    with open(relative_path.value, 'r') as f:
        code = f.read()

        tree = parser.Parser().parse(code)
        statements = parser.TreeTransformer().transform(tree)

        ctx = context.Context(context.Scope(environment.init_scope_values, environment.init_scope_types))

        ctx.execute(statements)
        
        return ctx.return_value

ctx = context.Context(context.Scope({}, {}))

values = {
    'include': concrete.ConcreteExternalFunction(ctx, mu_include)
}

types = {
    'include': concrete.ConcreteType('ExternalFunction')
}
