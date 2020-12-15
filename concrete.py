import math
import state
from execution import ExecutionEnvironment

class Concrete():
    def __init__(self, value):
        self.value = value

    def __eq__(self, value):
        return self.value == value

    def coalesce(self, value):
        # Fallback to return final value
        # Safe option when provided with no other
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
    def coalesce(self, scope, value):
        if isinstance(value, ConcreteString):
            return ConcreteString(self.value + value.value)
        else:
            return value

    def __repr__(self):
        return self.value.__repr__()

class ConcreteList(Concrete):
    def __len__(self):
        return len(self.value)

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

    def coalesce(self, scope, value):
        if isinstance(value, ConcreteList):
            if not (self.is_infinite() or value.is_infinite()):
                return ConcreteList(self.value + value.value)
            else:
                raise Exception('Could not coalesce lists where at least one is infinite')
        else:
            return value
    
    def __iter__(self):
        return iter(self.value)

class ConcreteSet(Concrete):
    def coalesce(self, scope, value):
        if isinstance(value, ConcreteSet):
            return ConcreteSet(self.value + value.value)
        else:
            return value

    def __iter__(self):
        return iter(self.value)

# Dict values and types to concrete objects
class ConcreteObject(Concrete):
    def __init__(self, values, types):
        self.values = values
        self.types = types

    def __repr__(self):
        return '<Object: ' + self.values.__repr__() + ' ' + self.types.__repr__() + '>'

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

class ConcreteType(Concrete):
    def __repr__(self):
        return '<Type: ' + str(self.value) + '>'

    def coalesce(self, scope, value):
        if self.value == 'Integer':
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
            return ConcreteFunction(scope, None, [])
        elif self.value == 'ExternalFunction':
            return ConcreteExternalFunction(scope, lambda scope, value: ConcreteEmpty())
        else:
            raise Exception('Unrecognised type being coalesced: ' + str(self))

class ConcreteFunction(Concrete):
    def __init__(self, scope, bind, statements):
        self.scope = scope
        self.bind = bind
        self.statements = statements

    def __repr__(self):
        return '<Function>'

    def coalesce(self, scope, value=ConcreteEmpty()):
        new_scope = self.scope.copy()
        if self.bind:
            new_scope.set_key(self.bind, value)
        env = ExecutionEnvironment(new_scope)
        
        return_value = ConcreteEmpty()
        def return_function(scope, value):
            nonlocal return_value
            env.halt()
            return_value = value

        new_scope.set_key('return', ConcreteExternalFunction(new_scope, return_function))

        env.execute(self.statements)
        
        return return_value

class ConcreteExternalFunction(Concrete):
    def __init__(self, scope, value):
        self.scope = scope
        super().__init__(value)

    def __repr__(self):
        return '<ExternalFunction>'

    def coalesce(self, scope, value=ConcreteEmpty()):
        new_scope = self.scope.copy()
        return self.value(new_scope, value)
