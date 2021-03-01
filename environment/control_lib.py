import concrete
import environment.check as check
import typecheck
import context

def mu_if(context, cond):
    check.check_arg(cond, concrete.ConcreteType('Integer'), context)

    def then(context, then_func):
        check.check_arg(then_func, (concrete.ConcreteType('Function'), concrete.ConcreteType('ExternalFunction')), context)

        def els(context, else_func):
            check.check_arg(else_func, (concrete.ConcreteType('Function'), concrete.ConcreteType('ExternalFunction')), context)

            if cond != concrete.ConcreteInteger(0):
                return then_func.coalesce(context, concrete.ConcreteEmpty())
            else:
                return else_func.coalesce(context, concrete.ConcreteEmpty())

        return concrete.ConcreteExternalFunction(context, els)
            
    return concrete.ConcreteExternalFunction(context, then)

def mu_elif(context, cond):
    check.check_arg(cond, concrete.ConcreteType('Integer'), context)

    def then(context, then_func):
        check.check_arg(then_func, (concrete.ConcreteType('Function'), concrete.ConcreteType('ExternalFunction')), context)

        def els(context, else_func):
            check.check_arg(else_func, (concrete.ConcreteType('Function'), concrete.ConcreteType('ExternalFunction')), context)

            if cond != concrete.ConcreteInteger(0):
                return then_func
            else:
                return else_func

        return concrete.ConcreteExternalFunction(context, els)
            
    return concrete.ConcreteExternalFunction(context, then)

def mu_only(context, cond):
    check.check_arg(cond, concrete.ConcreteType('Integer'), context)

    def then(context, then_func):
        check.check_arg(then_func, (concrete.ConcreteType('Function'), concrete.ConcreteType('ExternalFunction')), context)

        if cond != concrete.ConcreteInteger(0):
            return then_func.coalesce(context, concrete.ConcreteEmpty())
        else:
            return concrete.ConcreteEmpty()
            
    return concrete.ConcreteExternalFunction(context, then)

def mu_elonly(context, cond):
    check.check_arg(cond, concrete.ConcreteType('Integer'), context)

    def then(context, then_func):
        check.check_arg(then_func, (concrete.ConcreteType('Function'), concrete.ConcreteType('ExternalFunction')), context)

        def empty_func(context, value):
            return concrete.ConcreteEmpty()

        if cond != concrete.ConcreteInteger(0):
            return then_func
        else:
            return concrete.ConcreteExternalFunction(context, empty_func)
            
    return concrete.ConcreteExternalFunction(context, then)

def mu_while(context, cond):
    check.check_arg(cond, concrete.ConcreteType('Function'), context)

    def loop(context, func):
        check.check_arg(func, concrete.ConcreteType('Function'), context)

        while cond.coalesce(context, concrete.ConcreteEmpty()) != concrete.ConcreteInteger(0):
            func.coalesce(context, concrete.ConcreteEmpty())

        return concrete.ConcreteEmpty()

    return concrete.ConcreteExternalFunction(context, loop)

def mu_for_each(context, iterable):
    check.check_arg(iterable, (concrete.ConcreteType('List'), concrete.ConcreteType('Set')), context)
    
    def loop(context, func):
        check.check_arg(func, concrete.ConcreteType('Function'), context)

        for element in iterable:
            func.coalesce(context, element)

        return concrete.ConcreteEmpty()

    return concrete.ConcreteExternalFunction(context, loop)

def mu_match(context, value):

    def collect_maps(context, pattern_maps):
        check.check_arg(pattern_maps, concrete.ConcreteType('List'), context)

        for pattern_map in pattern_maps:
            check.check_arg(pattern_map, concrete.ConcreteType('List'), context)
            check.check_arg(pattern_map[1], concrete.ConcreteType('Function'), context)

            if typecheck.is_type(value, pattern_map[0], context):
                return pattern_map[1].coalesce(context, value)

    return concrete.ConcreteExternalFunction(context, collect_maps)

ctx = context.Context(context.Scope({}, {}), is_halted=True)

values = {
    'if': concrete.ConcreteExternalFunction(ctx, mu_if),
    'elif': concrete.ConcreteExternalFunction(ctx, mu_elif),
    'only': concrete.ConcreteExternalFunction(ctx, mu_only),
    'elonly': concrete.ConcreteExternalFunction(ctx, mu_elonly),
    'while': concrete.ConcreteExternalFunction(ctx, mu_while),
    'for_each': concrete.ConcreteExternalFunction(ctx, mu_for_each),
    'match': concrete.ConcreteExternalFunction(ctx, mu_match)
}

types = {
    'if': concrete.ConcreteType('ExternalFunction'),
    'elif': concrete.ConcreteType('ExternalFunction'),
    'only': concrete.ConcreteType('ExternalFunction'),
    'elonly': concrete.ConcreteType('ExternalFunction'),
    'while': concrete.ConcreteFunctionType([concrete.ConcreteFunctionType([concrete.ConcreteEmpty(), concrete.ConcreteType('Integer')]), 
        concrete.ConcreteFunctionType([concrete.ConcreteEmpty(), concrete.ConcreteType('Any')]), concrete.ConcreteEmpty]),
    'for_each': concrete.ConcreteType('ExternalFunction'),
    'match': concrete.ConcreteType('ExternalFunction')
}
