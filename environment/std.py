from execution import Scope
from concrete import ConcreteInteger, ConcreteString, ConcreteList, ConcreteSet, ConcreteEmpty, ConcreteExternalFunction

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



std_values = {
    'print': ConcreteExternalFunction(Scope({}, {}), mu_print),
    'is_equal': ConcreteExternalFunction(Scope({}, {}), mu_is_equal),
    'if': ConcreteExternalFunction(Scope({}, {}), mu_if),
    'for_each': ConcreteExternalFunction(Scope({}, {}), mu_for_each)
}

std_types = {}
