from execution import Scope, ScopeMatter
import concrete
import environment.std

def mu_integer_add(scope, first_value):
    
    def load_second_value(scope, second_value):
        return concrete.ConcreteInteger(first_value.value + second_value.value)

    return concrete.ConcreteExternalFunction(scope, load_second_value)

integer = {
    'add': concrete.ConcreteExternalFunction(Scope({}, {}), mu_integer_add)
}

def mu_import(scope, value):
        if value == 'std':
            return concrete.ConcreteObject(environment.std.table, {})
        elif value == 'integer':
            return concrete.ConcreteObject(integer, {})
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
        'ExternalFunction': concrete.ConcreteType('ExternalFunction')
}

init_scope_types = {}
