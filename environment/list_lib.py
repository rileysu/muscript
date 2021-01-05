import itertools

import context
import environment.check as check
import typecheck
import concrete

# Basic Ops
def mu_list_get(context, list_value):
    check.check_arg(list_value, concrete.ConcreteType('List'))

    def load_index(context, index):
        check.check_arg(index, concrete.ConcreteType('Integer'))
        return list_value[index].copy()

    return concrete.ConcreteExternalFunction(context, load_index)

def mu_list_set(context, list_value):
    check.check_arg(list_value, concrete.ConcreteType('List'))
    
    def load_value(context, value):
        def load_index(context, index):
            check.check_arg(index, concrete.ConcreteType('Integer'))

            list_copy = list_value.copy()
            list_copy[index] = value

            return list_copy

        return concrete.ConcreteExternalFunction(context, load_index)

    return concrete.ConcreteExternalFunction(context, load_value)

def mu_slice(context, list_value):
    check.check_arg(list_value, concrete.ConcreteType('List'))

    def load_slice(context, slice_value):
        check.check_arg(slice_value, concrete.ConcreteList([
            concrete.ConcreteAlgebraicType([concrete.ConcreteType('Integer'), concrete.ConcreteEmpty()]), 
            concrete.ConcreteAlgebraicType([concrete.ConcreteType('Integer'), concrete.ConcreteEmpty()]), 
            concrete.ConcreteAlgebraicType([concrete.ConcreteType('Integer'), concrete.ConcreteEmpty()])]))

        new_slice = slice(
            slice_value[0] if typecheck.is_type(slice_value[0], concrete.ConcreteType('Integer')) else None, 
            slice_value[1] if typecheck.is_type(slice_value[1], concrete.ConcreteType('Integer')) else None, 
            slice_value[2] if typecheck.is_type(slice_value[2], concrete.ConcreteType('Integer')) else None)

        return list_value[new_slice].copy()
        
    return concrete.ConcreteExternalFunction(context, load_slice)

def mu_head(context, list_value):
    check.check_arg(list_value, concrete.ConcreteType('List'))

    return list_value.value[0].copy()

def mu_last(context, list_value):
    check.check_arg(list_value, concrete.ConcreteType('List'))

    return list_value.value[-1].copy()

def mu_init(context, list_value):
    check.check_arg(list_value, concrete.ConcreteType('List'))

    return concrete.ConcreteList(list(list_value.value.copy()[:-1]))

def mu_tail(context, list_value):
    check.check_arg(list_value, concrete.ConcreteType('List'))

    return concrete.ConcreteList(list(list_value.value.copy()[1:]))

def mu_length(context, list_value): 
    check.check_arg(list_value, concrete.ConcreteType('List'))

    return concrete.ConcreteInteger(len(list_value))

# Transformations
def mu_map(context, func):
    check.check_arg(func, concrete.ConcreteType('Function'))

    def load_list(context, list_value):
        check.check_arg(list_value, concrete.ConcreteType('List'))

        return concrete.ConcreteList(list(map(lambda x: func.coalesce(context, x), list_value)))

    return concrete.ConcreteExternalFunction(context, load_list)

def mu_reverse(context, list_value):
    check.check_arg(list_value, concrete.ConcreteType('List'))

    return concrete.ConcreteList(list_value.value.reverse())

# Maybe
# def mu_intersperse(context, list_value):
# def mu_intercalate(context, list_value):

def mu_combinations(context, list_value):
    check.check_arg(list_value, concrete.ConcreteType('List'))

    def load_count(context, count):
        check.check_arg(count, concrete.ConcreteType('Integer'))

        return concrete.ConcreteList(list(itertools.combinations(list_value.copy(), count.value)))

    return concrete.ConcreteExternalFunction(context, load_count)

def mu_permutations(context, list_value):
    check.check_arg(list_value, concrete.ConcreteType('List'))

    def load_count(context, count):
        check.check_arg(count, concrete.ConcreteType('Integer'))

        return concrete.ConcreteList(list(itertools.permutations(list_value.copy(), count.value)))

    return concrete.ConcreteExternalFunction(context, load_count)

# Reduction
def mu_foldl(context, func):

    def load_init(context, init):

        def load_list(context, lst):
            out = init

            for x in lst:
                out = func.coalesce(context, out, x)

            return out

        return concrete.ConcreteExternalFunction(context, load_list)

    return concrete.ConcreteExternalFunction(context, load_init)

ctx = context.Context(context.Scope({}, {}), is_halted=True)

values = {
    'get': concrete.ConcreteExternalFunction(ctx, mu_list_get),
    'set': concrete.ConcreteExternalFunction(ctx, mu_list_set)
}

types = {
    'get': concrete.ConcreteType('ExternalFunction'),
    'set': concrete.ConcreteType('ExternalFunction')
}
