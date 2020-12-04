from execution import Scope, ScopeMatter
from concrete import ConcreteInteger, ConcreteString, ConcreteList, ConcreteSet, ConcreteObject, ConcreteEmpty, ConcreteExternalFunction
import environment.std

def mu_integer_add(scope, first_value):
    
    def load_second_value(scope, second_value):
        return ConcreteInteger(first_value.value + second_value.value)

    return ConcreteExternalFunction(scope, load_second_value)

integer = {
    'add': ScopeMatter(ConcreteExternalFunction(Scope({}), mu_integer_add), None)
}

def mu_import(scope, value):
        if value == 'std':
            return ConcreteObject(environment.std.table)
        elif value == 'integer':
            return ConcreteObject(integer)
        else:
            return ConcreteEmpty()

init_scope = {
        'import': ScopeMatter(ConcreteExternalFunction(Scope({}), mu_import), None)
}
