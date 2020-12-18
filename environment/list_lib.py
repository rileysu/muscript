import execution
import concrete

def mu_list_get(scope, list_value):
    def load_index(scope, index):
        return list_value[index]

    return concrete.ConcreteExternalFunction(scope, load_index)

def mu_list_set(scope, list_value):
    def load_value(scope, value):
        def load_index(scope, index):
            list_copy = list_value.copy()
            list_copy[index] = value

            return list_copy

        return concrete.ConcreteExternalFunction(scope, load_index)

    return concrete.ConcreteExternalFunction(scope, load_value)

values = {
    'get': concrete.ConcreteExternalFunction(execution.Scope({}, {}), mu_list_get),
    'set': concrete.ConcreteExternalFunction(execution.Scope({}, {}), mu_list_set)
}

types = {
    'get': concrete.ConcreteType('ExternalFunction'),
    'set': concrete.ConcreteType('ExternalFunction')
}
