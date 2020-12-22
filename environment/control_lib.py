import concrete
import environment.check as check
import typecheck
import context

def mu_if(context, cond):
    check.check_arg(cond, concrete.ConcreteInteger)

    def then(context, then_func):
        check.check_arg(then_func, concrete.ConcreteFunction)

        def els(context, else_func):
            check.check_arg(else_func, concrete.ConcreteFunction)

            if cond != concrete.ConcreteInteger(0):
                return then_func.coalesce(context, concrete.ConcreteEmpty())
            else:
                return else_func.coalesce(context, concrete.ConcreteEmpty())

        return concrete.ConcreteExternalFunction(context, els)
            
    return concrete.ConcreteExternalFunction(context, then)

def mu_only(context, cond):
    check.check_arg(cond, concrete.ConcreteInteger)

    def then(context, then_func):
        check.check_arg(then_func, concrete.ConcreteFunction)

        if cond != concrete.ConcreteInteger(0):
            return then_func.coalesce(context, concrete.ConcreteEmpty())
        else:
            return concrete.ConcreteEmpty()
            
    return concrete.ConcreteExternalFunction(context, then)

def mu_while(context, cond):
    check.check_arg(cond, concrete.ConcreteInteger)

    def loop(context, func):
        check.check_arg(func, concrete.ConcreteFunction)

        while cond != concrete.ConcreteInteger(0):
            func.coalesce(context, concrete.ConcreteEmpty())

        return concrete.ConcreteEmpty()

    return concrete.ConcreteExternalFunction(context, loop)

def mu_for_each(context, iterable):
    check.check_arg(iterable, [concrete.ConcreteList, concrete.ConcreteSet])
    
    def loop(context, func):
        check.check_arg(func, concrete.ConcreteFunction)

        for element in iterable:
            func.coalesce(context, element)

        return concrete.ConcreteEmpty()

    return concrete.ConcreteExternalFunction(context, loop)

def mu_match(context, value):

    def collect_maps(context, pattern_maps):
        check.check_arg(pattern_maps, concrete.ConcreteList)

        for pattern_map in pattern_maps:
            check.check_arg(pattern_map, concrete.ConcreteList)
            check.check_arg(pattern_map[1], concrete.ConcreteFunction)

            if typecheck.is_type(value, pattern_map[0]):
                return pattern_map[1].coalesce(context, value)

    return concrete.ConcreteExternalFunction(context, collect_maps)

ctx = context.Context(context.Scope({}, {}), is_halted=True)

values = {
    'if': concrete.ConcreteExternalFunction(ctx, mu_if),
    'only': concrete.ConcreteExternalFunction(ctx, mu_only),
    'while': concrete.ConcreteExternalFunction(ctx, mu_while),
    'for_each': concrete.ConcreteExternalFunction(ctx, mu_for_each),
    'match': concrete.ConcreteExternalFunction(ctx, mu_match)
}

types = {
    'if': concrete.ConcreteType('ConcreteExternalFunction'),
    'only': concrete.ConcreteType('ConcreteExternalFunction'),
    'while': concrete.ConcreteType('ConcreteExternalFunction'),
    'for_each': concrete.ConcreteType('ConcreteExternalFunction'),
    'match': concrete.ConcreteType('ConcreteExternalFunction')
}
