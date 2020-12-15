from execution import Scope, ScopeMatter
import concrete

import environment.std_lib as std_lib
import environment.list_lib as list_lib

def mu_integer_add(scope, first_value):
    def load_second_value(scope, second_value):
        return concrete.ConcreteInteger(first_value.value + second_value.value)

    return concrete.ConcreteExternalFunction(scope, load_second_value)

integer = {
    'add': concrete.ConcreteExternalFunction(Scope({}, {}), mu_integer_add)
}

def mu_import(scope, value):
    if isinstance(value, concrete.ConcreteString):
        if value.value == 'std':
            return concrete.ConcreteObject(std_lib.values, std_lib.types)
        elif value.value == 'integer':
            return concrete.ConcreteObject(integer, {})
        elif value.value == 'list':
            return concrete.ConcreteObject(list_lib.values, list_lib.types)
        else:
            return concrete.ConcreteEmpty()

init_scope_values = {
        'import': concrete.ConcreteExternalFunction(Scope({}, {}), mu_import),
        'Integer': concrete.ConcreteType('Integer'),
        'Decimal': concrete.ConcreteType('Decimal'),
        'String': concrete.ConcreteType('String'),
        'List': concrete.ConcreteType('List'),
        'Set': concrete.ConcreteType('Set'),
        'Object': concrete.ConcreteType('Object'),
        'Function': concrete.ConcreteType('Function'),
        'ExternalFunction': concrete.ConcreteType('ExternalFunction'),
        'Any': concrete.ConcreteType('Any')
}

init_scope_types = {
    'import': concrete.ConcreteType('ExternalFunction')
}
