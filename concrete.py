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
        return ConcreteString(self.value + str(value.value))

class ConcreteList(Concrete):
    def __iter__(self):
        return iter(self.value)

class ConcreteSet(Concrete):
    def __iter__(self):
        return iter(self.value)

class ConcreteObject(Concrete):
    pass

class ConcreteEmpty(Concrete):
    def __init__(self, value=None):
        super().__init__(value)

class ConcreteFunction(Concrete):
    def __init__(self, scope, bind, statements):
        self.scope = scope
        self.bind = bind
        self.statements = statements

    def coalesce(self, scope, value=ConcreteEmpty()):
        new_scope = self.scope.copy()
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

    def coalesce(self, scope, value=None):
        new_scope = self.scope.copy()
        return self.value(new_scope, value)
