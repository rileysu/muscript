import context
import concrete

def mu_list_get(context, list_value):
    def load_index(context, index):
        return list_value[index]

    return concrete.ConcreteExternalFunction(context, load_index)

def mu_list_set(context, list_value):
    def load_value(context, value):
        def load_index(context, index):
            list_copy = list_value.copy()
            list_copy[index] = value

            return list_copy

        return concrete.ConcreteExternalFunction(context, load_index)

    return concrete.ConcreteExternalFunction(context, load_value)

ctx = context.Context(context.Scope({}, {}), is_halted=True)

values = {
    'get': concrete.ConcreteExternalFunction(ctx, mu_list_get),
    'set': concrete.ConcreteExternalFunction(ctx, mu_list_set)
}

types = {
    'get': concrete.ConcreteType('ExternalFunction'),
    'set': concrete.ConcreteType('ExternalFunction')
}
