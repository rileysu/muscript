import math
import state
import typecheck

class Concrete():
    def __init__(self, value):
        self.value = value

    def __eq__(self, value):
        return isinstance(value, type(self)) and self.value == value.value

    def __hash__(self):
        return hash(self.value)

    def assimilate(self, context, value):
        return value
    
    def coalesce(self, context, value):
        # Fallback to return final value
        # Safe option when provided with no other
        if isinstance(value, ConcreteUndefined):
            return self
        else:
            return value

class ConcreteInteger(Concrete):
    def __int__(self):
        return self.value

    def __repr__(self):
        return self.value.__repr__()

class ConcreteDecimal(Concrete):
    def __float__(self):
        return self.value

    def __repr__(self):
        return self.value.__repr__()

class ConcreteString(Concrete):
    def coalesce(self, context, value):
        if isinstance(value, ConcreteUndefined):
            return self
        elif isinstance(value, ConcreteString):
            return ConcreteString(self.value + value.value)
        else:
            return value

    def __repr__(self):
        return self.value.__repr__()

class ConcreteList(Concrete):
    def __len__(self):
        return len(self.value)

    def __repr__(self):
        return self.value.__repr__()

    def __getitem__(self, index):
        seq_len = self.inf_seq_length() if self.is_infinite() else len(self.value)

        if seq_len == 0:
            return ConcreteEmpty()
        else:
            return self.value[int(index) % seq_len]

    def __setitem__(self, index, value):
        seq_len = self.inf_seq_length() if self.is_infinite() else len(self.value)

        if seq_len == 0:
            raise Exception('Could not set index in infinite empty list')
        else:
            self.value[int(index) % seq_len] = value

    def copy(self):
        return ConcreteList(self.value.copy())
    
    def is_infinite(self):
        return ConcreteEllipsis() in self.value

    def inf_seq_length(self):
        return next(i for i, x in enumerate(self.value) if x == ConcreteEllipsis())

    def coalesce(self, context, value):
        if isinstance(value, ConcreteUndefined):
            return self
        elif isinstance(value, ConcreteList):
            if not (self.is_infinite() or value.is_infinite()):
                return ConcreteList(self.value.copy() + value.value.copy())
            else:
                raise Exception('Could not coalesce lists where at least one is infinite')
        else:
            return value
    
    def __iter__(self):
        return iter(self.value)

class ConcreteSet(Concrete):
    def __repr__(self):
        return self.value.__repr__()

    def __iter__(self):
        return iter(self.value)
    
    def coalesce(self, context, value):
        if isinstance(value, ConcreteUndefined):
            return self
        elif isinstance(value, ConcreteSet):
            return ConcreteSet(self.value.copy() + value.value.copy())
        else:
            return value

# Dict values and types to concrete objects
class ConcreteObject(Concrete):
    # All values should have a corresponding type when the object is created
    def __init__(self, values, types):
        self.values = values
        self.types = types

        # Check types when we are sure all are initialised
        for attribute in self.values:
            typecheck.check_type(self.values[attribute], self.types[attribute])

    def __eq__(self, value):
        return isinstance(value, type(self)) and self.values == value.values and self.types == value.types

    def __hash__(self):
        return hash((self.values, self.types))

    def __repr__(self):
        return '<Object: ' + self.values.__repr__() + ' ' + self.types.__repr__() + '>'

    def assimilate(self, context, value):
        self.coalesce(context, value)

    def coalesce(self, context, value):
        if isinstance(value, ConcreteUndefined):
            return self
        elif isinstance(value, ConcreteObject):
            values = self.values.copy()
            types = self.types.copy()

            for attribute in value.values:
                if not isinstance(value.values[attribute], ConcreteUndefined):
                    values[attribute] = value.values[attribute]

            for attribute in value.types:
                if not isinstance(value.types[attribute], ConcreteUndefined):
                    types[attribute] = value.types[attribute]

            return ConcreteObject(values, types)
        else:
            return value

    def get(self, key):
        return self.values[key]

    def get_type(self, key):
        return self.types[key]

# Exists to easily define and check empty value
# Concrete is already defined as empty
class ConcreteEmpty(Concrete):
    def __init__(self):
        super().__init__(None)

    def __repr__(self):
        return '<Empty>'


class ConcreteEllipsis(Concrete):
    def __init__(self):
        super().__init__(None)

    def __repr__(self):
        return '<Ellipsis>'

class ConcreteUndefined(Concrete):
    def __init__(self):
        super().__init__(None)

    def __repr__(self):
        return '<Undefined>'

class ConcreteType(Concrete):
    def __repr__(self):
        return '<Type: ' + str(self.value) + '>'

    def coalesce(self, context, value):
        if isinstance(value, ConcreteUndefined):
            return self
        elif self.value == 'Integer':
            if isinstance(value, ConcreteInteger):
                return ConcreteInteger(value.value)
            elif isinstance(value, ConcreteDecimal):
                return ConcreteInteger(int(value.value))
            elif isinstance(value, ConcreteString):
                return ConcreteInteger(int(value.value))
        elif self.value == 'Decimal':
            if isinstance(value, ConcreteInteger):
                return ConcreteDecimal(float(value.value))
            elif isinstance(value, ConcreteDecimal):
                return ConcreteDecimal(value.value)
            elif isinstance(value, ConcreteString):
                return ConcreteDecimal(float(value.value))
        elif self.value == 'String':
            return ConcreteString(str(value))
        elif self.value == 'List':
            return ConcreteList(value)
        elif self.value == 'Set':
            return ConcreteSet(value)
        elif self.value == 'Object':
            #TODO
            return ConcreteObject(value, {})
        elif self.value == 'Function':
            #TODO
            return ConcreteFunction(context, None, [])
        elif self.value == 'ExternalFunction':
            return ConcreteExternalFunction(context, lambda scope, value: ConcreteEmpty())
        else:
            raise Exception('Unrecognised type being coalesced: ' + str(self))

class ConcreteAlgebraicType(Concrete):
    def __repr__(self):
        return '<AlgebraicType: ' + str(self.value) + '>'

class ConcreteFunctionType(Concrete):
    def __getitem__(self, index):
        return self.value[index]

    def __repr__(self):
        return '<FunctionType: ' + str(self.value) + '>'

    def assimilate(self, context, value):
        if isinstance(value, ConcreteFunction):
            value.set_type(self)
        elif isinstance(value, ConcreteExternalFunction):
            value.set_type(self)
        
        return value

class ConcreteFunction(Concrete):
    def __init__(self, context, bind, statements,
            type=ConcreteFunctionType([ConcreteType('Any'), ConcreteType('Any')])):
        self.context = context
        self.bind = bind
        self.statements = statements
        self.type = type

    def __eq__(self, value):
        return isinstance(value, type(self)) and self.statements == value.statements

    def __hash__(self):
        return hash((self.bind, self.statements))

    def __repr__(self):
        return '<Function: ' + str(id(self)) + '>'

    def set_type(self, type):
        self.type = type

    def coalesce(self, context, value=ConcreteEmpty()):
        if isinstance(value, ConcreteUndefined):
            return self

        typecheck.check_type(value, self.type[0])
        
        new_context = self.context.create_function_context(self.bind, value)
        
        new_context.execute(self.statements)

        return_value = new_context.get_return_value()

        self.context.close_function_context(new_context)

        if len(self.type[1:]) > 1:
            if isinstance(return_value, ConcreteFunction) or isinstance(return_value, ConcreteExternalFunction):
                return_value.set_type(self.type[1:])
        else:
            typecheck.check_type(return_value, self.type[-1])

        # Also check if the return is another function and apply correct type signature

        return return_value

class ConcreteExternalFunction(Concrete):
    def __init__(self, context, value, type=ConcreteFunctionType([ConcreteType('Any'), ConcreteType('Any')])):
        self.context = context
        self.value = value
        self.type = type

    def __eq__(self, value):
        return isinstance(value, type(self)) and self.value == value.value

    def __hash__(self):
        return hash(self.context, self.value)

    def __repr__(self):
        return '<ExternalFunction>'

    def set_type(self, type):
        self.type = type

    def coalesce(self, context, value=ConcreteEmpty()):
        if isinstance(value, ConcreteUndefined):
            return self

        new_context = self.context.copy()
        return self.value(new_context, value)
