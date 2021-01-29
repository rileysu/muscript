import concrete
import context

def mu_print(context, value):
    print(value)

    return concrete.ConcreteEmpty()

ctx = context.Context(context.Scope({}, {}), is_halted=True)

values = {
    'print': concrete.ConcreteExternalFunction(ctx, mu_print)
}

types = {
    'print': concrete.ConcreteType('ExternalFunction')
}
