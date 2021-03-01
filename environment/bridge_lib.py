import concrete
import context
import inspect
import environment.check
import importlib

# In progress
# TODO
# Find a way to represent python classes in muscript

def map_mu_to_py(val):
    if isinstance(val, (concrete.ConcreteInteger, 
            concrete.ConcreteDecimal, 
            concrete.ConcreteString)):
        return val.value
    elif isinstance(val, concrete.ConcreteList):
        return tuple( map_mu_to_py(x) for x in val.value )
    elif isinstance(val, concrete.ConcreteSet):
        return set( map_mu_to_py(x) for x in val.value )
    elif isinstance(val, concrete.ConcreteObject):
        return { k:map_mu_to_py(v) for k, v in val.values }
    else:
        raise Exception('Bad type attempted to be mapped to python: ', val)

def map_py_to_mu(val):
    if inspect.isbuiltin(val):
        if isinstance(val, int):
            return concrete.ConcreteInteger(val)
        elif isinstance(val, float):
            return concrete.ConcreteDecimal(val)
        elif isinstance(val, complex):
            return concrete.ConcreteObject({ 
                    'real': val.real, 
                    'imaginary': val.imag 
                }, {
                    'real': concrete.ConcreteType('Decimal'),
                    'imaginary': concrete.ConcreteType('Decimal')
                })
        elif isinstance(val, str):
            return concrete.ConcreteString(val)
        elif isinstance(val, (list, tuple)):
            return concrete.ConcreteList(tuple( map_py_to_mu(x) for x in val ))
        elif isinstance(val, (set, frozenset)):
            return concrete.ConcreteSet(frozenset( map_py_to_mu(x) for x in val ))
        elif isinstance(val, dict):
            return concrete.ConcreteObject({ k:v for k, v in val }, { k:concrete.ConcreteUndefined(), for k, _ in val })
    elif inspect.isclass(val):
        

def mu_bridge_import(context, lib_constring):
    environment.check.check_arg(lib_constring, concrete.ConcreteType('String'), context)

    lib_string = lib_constring.value

    if not lib_string.isalpha():
        raise Exception('Malformed string passed to bridge')

    mod = importlib.import_module(lib_string)

    exec(import_statement)
    # 'mod' is not the imported module
    # This needs to be transoformed by bridge in order to be used as a library
    # Bridge functions should only be passed a list of arguments

    out_functions = {}

    for attr_string in dir(mod):

        attr = getattr(attr_string)
        
        if callable(attr):
            def mu_func(context, args_conlist):
                # args = [pos_args, ..., object]
                environment.check.check_arg(args, concrete.ConcreteType('List'))
                
                args = args_conlist.value[:-1]
                kwargs = args_conlist.value[-1].values
                  
                attr(*args, **kwargs)

            out_functions[func_name] = mu_func
        else:

        
    

    return concrete.ConcreteEmpty()

ctx = context.Context(context.Scope({}, {}), is_halted=True)

values = {
    'print': concrete.ConcreteExternalFunction(ctx, mu_print)
}

types = {
    'print': concrete.ConcreteType('ExternalFunction')
}
