from execution import Matter
from concrete import ConcreteExternalFunction

def mu_print(value):
    # Expecting all concrete types to have a value
    # This is a false assumption but works in most cases
    print(value.value)

std = {
        'print': Matter(ConcreteExternalFunction(mu_print), None)
}

def mu_import(value):
        return std

init_scope = {
        'import': Matter(ConcreteExternalFunction(mu_import), None)
}
