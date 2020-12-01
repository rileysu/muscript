from execution import ExecutionEnvironment

class Concrete():
    def __init__(self, value):
        self.value = value

    def coalesce(self, scope, value):
        # Fallback to return final value
        # Safe option when provided with no other
        return value

class ConcreteInteger(Concrete):
    pass

class ConcreteDecimal(Concrete):
    pass

class ConcreteString(Concrete):
    def coalesce(self, scope, value):
        return ConcreteString(self.value + str(value.value))

class ConcreteList(Concrete):
    pass

class ConcreteSet(Concrete):
    pass

class ConcreteObject(Concrete):
    pass

class ConcreteFunction(Concrete):
    def __init__(self, bind, statements):
        self.bind = bind
        self.statements = statements

    def coalesce(self, scope, value):
        new_scope = scope.copy()
        new_scope.set_key(self.bind, value)
        env = ExecutionEnvironment(new_scope)
        env.execute(self.statements)

        return new_scope.get_key('out') if new_scope.has_key('out') else ConcreteList([])

class ConcreteExternalFunction(Concrete):
    def coalesce(self, scope, value):
        return ConcreteObject(self.value(value))
