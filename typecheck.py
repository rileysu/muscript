import concrete
import math

class TypeException(Exception):
    pass

def is_type(value, type, context):
    if isinstance(type, concrete.ConcreteUndefined) or isinstance(value, concrete.ConcreteUndefined):
        return True
    elif isinstance(value, concrete.ConcreteMatter):
        return is_type(value.value, type, context)
    elif isinstance(type, concrete.ConcreteType):
        if type.value == 'Integer':
            return isinstance(value, concrete.ConcreteInteger)
        elif type.value == 'Decimal':
            return isinstance(value, concrete.ConcreteDecimal)
        elif type.value == 'String':
            return isinstance(value, concrete.ConcreteString)
        elif type.value == 'List':
            return isinstance(value, concrete.ConcreteList)
        elif type.value == 'Set':
            return isinstance(value, concrete.ConcreteSet)
        elif type.value == 'Object':
            return isinstance(value, concrete.ConcreteObject)
        elif type.value == 'Function':
            return isinstance(value, concrete.ConcreteFunction)
        elif type.value == 'ExternalFunction':
            return isinstance(value, concrete.ConcreteExternalFunction)
        elif type.value == 'Any':
            return True
    elif isinstance(type, concrete.ConcreteList):
        if isinstance(value, concrete.ConcreteList):
            # Handle case for both infinite lists
            # Min length to compare is the lcm of the lengths of the infinite sequence
            if type.is_infinite() and value.is_infinite():
                return all(is_type(value[i], type[i], context) for i in range(math.lcm(type.inf_seq_length(), value.inf_seq_length())))
            # Handle case where list type is constantly sized
            # A constantly sized list type indicates the value must be of the same length
            elif not type.is_infinite() and not value.is_infinite():
                if len(type) == len(value):
                    return all(is_type(value[i], type[i], context) for i in range(len(type)))
                else:
                    return False
            # Handle case of arbitrary length list type
            # This takes place when the type is infinite and the second is not
            elif type.is_infinite() and not value.is_infinite():
                return all(is_type(value[i], type[i], context) for i in range(len(value)))
            else:
                return False
        else:
            return False
    elif isinstance(type, concrete.ConcreteSet):
        if isinstance(value, concrete.ConcreteSet):
            return all(any(is_type(x, y, context) for y in type.value) for x in value.value)
        else:
            return False
    elif isinstance(type, concrete.ConcreteObject):
        if isinstance(value, concrete.ConcreteObject):
            # Each attribute's type in the type object corresponds with the attributes value in the value object
            return all((attribute in value.values and is_type(value.values[attribute], type.types[attribute], context)) for attribute in type.types)
        else:
            return False
    elif isinstance(type, concrete.ConcreteMatter):
        return is_type(value, type.value, context)
    elif isinstance(type, concrete.ConcreteAlgebraicType):
        return any(is_type(value, x, context) for x in type.value)
    elif isinstance(type, concrete.ConcreteSelfReference):
        return is_type(value, context.scope.get_value(type.value), context)
    elif isinstance(type, concrete.ConcreteFunctionType):
        return isinstance(value, concrete.ConcreteFunction) or isinstance(value, concrete.ConcreteExternalFunction)
    else:
        #Case will most likely not work
        return (type == value)

def check_type(value, type, context):
    if not is_type(value, type, context):
        raise TypeException('Expected: ' + str(type) + ' but got: ' + str(value))
