import concrete
import environment.check as check
import typecheck
import execution

def mu_if(scope, cond):
    check.check_arg(cond, concrete.ConcreteInteger)

    def then(scope, then_func):
        check.check_arg(then_func, concrete.ConcreteFunction)

        def els(scope, else_func):
            check.check_arg(else_func, concrete.ConcreteFunction)

            if cond != concrete.ConcreteInteger(0):
                return then_func.coalesce(scope, concrete.ConcreteEmpty())
            else:
                return else_func.coalesce(scope, concrete.ConcreteEmpty())

        return concrete.ConcreteExternalFunction(scope, els)
            
    return concrete.ConcreteExternalFunction(scope, then)

def mu_only(scope, cond):
    check.check_arg(cond, concrete.ConcreteInteger)

    def then(scope, then_func):
        check.check_arg(then_func, concrete.ConcreteFunction)

        if cond != concrete.ConcreteInteger(0):
            return then_func.coalesce(scope, concrete.ConcreteEmpty())
        else:
            return concrete.ConcreteEmpty()
            
    return concrete.ConcreteExternalFunction(scope, then)

def mu_while(scope, cond):
    check.check_arg(cond, concrete.ConcreteInteger)

    def loop(scope, func):
        check.check_arg(func, concrete.ConcreteFunction)

        while cond != concrete.ConcreteInteger(0):
            func.coalesce(scope, concrete.ConcreteEmpty())

        return concrete.ConcreteEmpty()

    return concrete.ConcreteExternalFunction(scope, loop)

def mu_for_each(scope, iterable):
    check.check_arg(iterable, [concrete.ConcreteList, concrete.ConcreteSet])
    
    def loop(scope, func):
        check.check_arg(func, concrete.ConcreteFunction)

        for element in iterable:
            func.coalesce(scope, element)

        return concrete.ConcreteEmpty()

    return concrete.ConcreteExternalFunction(scope, loop)

def mu_match(scope, value):

    def collect_maps(scope, pattern_maps):
        check.check_arg(pattern_maps, concrete.ConcreteList)

        for pattern_map in pattern_maps:
            check.check_arg(pattern_map, concrete.ConcreteList)
            check.check_arg(pattern_map[1], concrete.ConcreteFunction)

            if typecheck.is_type(pattern_map[0], value):
                return pattern_map[1].coalesce(scope, value)

    return concrete.ConcreteExternalFunction(scope, collect_maps)

values = {
    'if': concrete.ConcreteExternalFunction(execution.Scope({}, {}), mu_if),
    'only': concrete.ConcreteExternalFunction(execution.Scope({}, {}), mu_only),
    'while': concrete.ConcreteExternalFunction(execution.Scope({}, {}), mu_while),
    'for_each': concrete.ConcreteExternalFunction(execution.Scope({}, {}), mu_for_each),
    'match': concrete.ConcreteExternalFunction(execution.Scope({}, {}), mu_match)
}

types = {
    'if': concrete.ConcreteType('ConcreteExternalFunction'),
    'only': concrete.ConcreteType('ConcreteExternalFunction'),
    'while': concrete.ConcreteType('ConcreteExternalFunction'),
    'for_each': concrete.ConcreteType('ConcreteExternalFunction'),
    'match': concrete.ConcreteType('ConcreteExternalFunction')
}
