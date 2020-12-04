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
    pass

class ConcreteDecimal(Concrete):
   pass

class ConcreteString(Concrete):
    def coalesce(self, scope, value):
        if isinstance(value, ConcreteString):
            return ConcreteString(self.value + value.value)
        else:
            return value

class ConcreteList(Concrete):
    def __len__(self):
        if ConcreteEllipsis() in self.value:
            return float('inf')
        else:
            return len(self.value)

    def __getitem__(self, arg):
        first_pos = next(i for x, i in enumerate(self.value) if lambda y: y == ConcreteEllipsis())

        if first_pos == 0:
            return ConcreteEmpty()
        else:
            return self.value[arg % first_pos]
        
    def coalesce(self, scope, value):
        if isinstance(value, ConcreteList):
            if len(self) != float('inf') and len(value) != float('inf'):
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

# Dict of strings to ConcreteMatter
class ConcreteObject(Concrete):
    pass

# Exists to easily define and check empty value
# Concrete is already defined as empty
class ConcreteEmpty(Concrete):
    def __init__(self):
        super().__init__(None)


class ConcreteEllipsis(Concrete):
    def __init__(self):
        super().__init__(None)

class ConcreteType(Concrete):
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
        elif self.value == 'Function':
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

    def empty(self):
        return ConcreteFunction(self.scope.copy(), None, [])

    def define(self, value):
        return (self == self.empty() and isinstance(value, ConcreteFunction)) or self == value

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

    def empty(self):
        def empty_func(scope, value):
            return value

        return ConcreteExternalFunction(self.scope.copy(), empty_func)

    def coalesce(self, scope, value=ConcreteEmpty()):
        new_scope = self.scope.copy()
        return self.value(new_scope, value)
