import concrete
import context

def mu_print(context, value):
    if isinstance(value, concrete.ConcreteMatter):
        print(value.value)
    else:
        print(value)

    return concrete.ConcreteEmpty()

ctx = context.Context(context.Scope({}, {}), is_halted=True)

values = {
    'print': concrete.ConcreteExternalFunction(ctx, mu_print)
}

types = {
    'print': concrete.ConcreteType('ExternalFunction')
}
