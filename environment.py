from execution import Matter, Scope
from concrete import ConcreteInteger, ConcreteString, ConcreteList, ConcreteSet, ConcreteObject, ConcreteEmpty, ConcreteExternalFunction

def mu_print(scope, value):
    # Expecting all concrete types to have a value
    # This is a false assumption but works in most cases
    # A better solution is to allow concrete types to be represented as strings
    print(value.value)

    return ConcreteEmpty()

def mu_is_equal(scope, first_value):
    
    def loaded_is_equal(scope, second_value):
        return ConcreteInteger(int(first_value == second_value))

    return ConcreteExternalFunction(scope, loaded_is_equal)

def mu_if(scope, cond):

    def load_if_true(scope, true_function):
        def load_if_false(scope, false_function):
            if cond == 1:
                return true_function.coalesce(scope)
            else:
                return false_function.coalesce(scope)

        return ConcreteExternalFunction(scope, load_if_false)
    return ConcreteExternalFunction(scope, load_if_true)

def mu_for_each(scope, values):
    if isinstance(values, ConcreteString) or isinstance(values, ConcreteList) or isinstance(values, ConcreteSet):
        def internal_loop(scope, x):
            for value in values:
                x.coalesce(scope, value)

        return ConcreteExternalFunction(scope, internal_loop)

    else:
        print('bad')

        return ConcreteEmpty()



std = {
    'print': Matter(ConcreteExternalFunction(Scope({}), mu_print), None),
    'is_equal': Matter(ConcreteExternalFunction(Scope({}), mu_is_equal), None),
    'if': Matter(ConcreteExternalFunction(Scope({}), mu_if), None),
    'for_each': Matter(ConcreteExternalFunction(Scope({}), mu_for_each), None)
}

#def mu_is_less_than(scope, value):

#def mu_is_less_than_eq(scope, value):

#def mu_is_greater_than(scope, value):

#def mu_is_greater_than_equal(scope, value):

#compare = {
    
#}

def mu_integer_add(scope, first_value):
    
    def load_second_value(scope, second_value):
        return ConcreteInteger(first_value.value + second_value.value)

    return ConcreteExternalFunction(scope, load_second_value)

integer = {
    'add': Matter(ConcreteExternalFunction(Scope({}), mu_integer_add), None)
}

def mu_import(scope, value):
        if value == 'std':
            return ConcreteObject(std)
        elif value == 'integer':
            return ConcreteObject(integer)
        else:
            return ConcreteEmpty()

init_scope = {
        'import': Matter(ConcreteExternalFunction(Scope({}), mu_import), None)
}
