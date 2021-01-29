import parse
import concrete
import context
import environment

ctx = context.Context(context.Scope({}, {}), is_halted=True)

def generate_logger(logs):
    def mu_log(context, value):
        logs.append(value)
        return concrete.ConcreteEmpty()

    return {
        'log': concrete.ConcreteExternalFunction(ctx, mu_log)
    }, {
        'log': concrete.ConcreteType('ExternalFunction')
    }

def execute_and_get_logs(path):
    logs = []
    
    with open(path, 'r') as f:
        text = f.read()
        tree = parse.Parser().parse(text)
        statements = parse.TreeTransformer().transform(tree)
        logger_values, logger_types = generate_logger(logs)
        execute_ctx = context.Context(context.Scope(environment.init_scope_values | logger_values,
            environment.init_scope_types | logger_types))

        execute_ctx.execute(statements)

    return logs
