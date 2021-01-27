import concrete
import context
import environment.check as check

import environment.io_lib as io_lib
import environment.control_lib as control_lib
import environment.list_lib as list_lib
import environment.include_lib as include_lib

def mu_import(context, value):
    check.check_arg(value, concrete.ConcreteType('String'), context)

    import_map = {
        'io': concrete.ConcreteObject(io_lib.values, io_lib.types, context),
        'control': concrete.ConcreteObject(control_lib.values, control_lib.types, context),
        'list': concrete.ConcreteObject(list_lib.values, list_lib.types, context)
    }

    if value.value in import_map:
        return import_map[value.value]
    else:
        raise Exception('Could not import the requested library: ' + str(value))


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
} | include_lib.values

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
} | include_lib.types
