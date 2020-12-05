import concrete
import math

#TODO
#Add types for Empty and Ellipsis

def is_type(type, value):
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
    elif isinstance(type, concrete.ConcreteList):
        if isinstance(value, concrete.ConcreteList):
            if type.is_infinite() and value.is_infinite():
                return all([is_type(type[i], value[i]) for i in range(math.lcm(type.inf_seq_length(), value.inf_seq_length()))])
            elif not type.is_infinite() and not value.is_infinite():
                if len(type) == len(value):
                    return all([is_type(type[i], value[i]) for i in range(len(type))])
                else:
                    return False
            else:
                return False
        else:
            return False
    elif isinstance(type, concrete.ConcreteSet):
        if isinstance(value, concrete.ConcreteSet):
            return all([any([is_type(y, x) for y in type.value]) for x in value.value])
        else:
            return False
    else:
        return (type == value)
