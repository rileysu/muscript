import concrete
import context

import environment.std_lib as std_lib
import environment.control_lib as control_lib
import environment.list_lib as list_lib

def mu_integer_add(context, first_value):
    def load_second_value(context, second_value):
        return concrete.ConcreteInteger(first_value.value + second_value.value)

    return concrete.ConcreteExternalFunction(context, load_second_value)

integer = {
    'add': concrete.ConcreteExternalFunction(context.Context(context.Scope({}, {}), is_halted=True), mu_integer_add)
}

def mu_import(scope, value):
    if isinstance(value, concrete.ConcreteString):
        if value.value == 'std':
            return concrete.ConcreteObject(std_lib.values, std_lib.types)
        elif value.value == 'control':
            return concrete.ConcreteObject(control_lib.values, control_lib.types)
        elif value.value == 'integer':
            return concrete.ConcreteObject(integer, {})
        elif value.value == 'list':
            return concrete.ConcreteObject(list_lib.values, list_lib.types)
        else:
            return concrete.ConcreteEmpty()

init_scope_values = {
    'import': concrete.ConcreteExternalFunction(context.Context(context.Scope({}, {}), is_halted=True), mu_import),
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
    'import': concrete.ConcreteType('ExternalFunction'),
    'Integer': concrete.ConcreteType('Any'),
    'Decimal': concrete.ConcreteType('Any'),
    'String': concrete.ConcreteType('Any'),
    'List': concrete.ConcreteType('Any'),
    'Set': concrete.ConcreteType('Any'),
    'Object': concrete.ConcreteType('Any'),
    'Function': concrete.ConcreteType('Any'),
    'ExternalFunction': concrete.ConcreteType('Any'),
    'Any': concrete.ConcreteType('Any')
}
