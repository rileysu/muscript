import context
import concrete

def mu_print(context, value):
    #Use the internal repr to display value
    print(str(value))

    return concrete.ConcreteEmpty()

def mu_is_equal(context, first_value):

    def loaded_is_equal(context, second_value):
        return concrete.ConcreteInteger(int(first_value == second_value))

    return concrete.ConcreteExternalFunction(context, loaded_is_equal)

def mu_if(context, cond):

    def load_if_true(context, true_function):
        def load_if_false(context, false_function):
            if cond == 1:
                return true_function.coalesce(context, concrete.ConcreteEmpty())
            else:
                return false_function.coalesce(context, concrete.ConcreteEmpty())

        return concrete.ConcreteExternalFunction(context, load_if_false)
    return concrete.ConcreteExternalFunction(context, load_if_true)

def mu_for_each(context, values):
    if isinstance(values, concrete.ConcreteString) or isinstance(values, concrete.ConcreteList) or isinstance(values, concrete.ConcreteSet):
        def internal_loop(context, x):
            for value in values:
                x.coalesce(context, value)

        return concrete.ConcreteExternalFunction(context, internal_loop)

    else:
        print('bad')

        return concrete.ConcreteEmpty()

ctx = context.Context(context.Scope({}, {}), is_halted=True)

values = {
    'print': concrete.ConcreteExternalFunction(ctx, mu_print),
    'is_equal': concrete.ConcreteExternalFunction(ctx, mu_is_equal),
    'if': concrete.ConcreteExternalFunction(ctx, mu_if),
    'for_each': concrete.ConcreteExternalFunction(ctx, mu_for_each)
}

types = {
    'print': concrete.ConcreteType('ExternalFunction'),
    'is_equal': concrete.ConcreteType('ExternalFunction'),
    'if': concrete.ConcreteType('ExternalFunction'),
    'for_each': concrete.ConcreteType('ExternalFunction')
}
