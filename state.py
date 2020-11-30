class Value():
    def __init__(self, value):
        self.value = value

    def coalesce(self, value):
        return value

    def evaluate(self, scope):
        return self.value

class Integer(Value):
    pass

class Decimal(Value):
    pass

class String(Value):
    pass

class List(Value):
    def evaluate(self, scope):
        return list(map(lambda x: x.evaluate(scope), self.value))

class Set(Value):
    def evaluate(self, scope):
        return set(map(lambda x: x.evaluate(scope), self.value))

class Object(Value):
    def __init__(self, values):
        self.values = {}
        for definition in values:
            #What if object is referenced in object to assign to?
            self.values[definition['identifier']['values'][0]] = {
                'value': definition['value'], 
                'type': definition['type']
            }
    
    def evaluate(self, scope):
        out = {}
        for key in self.values:
            #Ignore type check until implemented
            out[key] = self.values[key]

        return out


class Variable(Value):
    def evaluate(self, scope):
        if scope.has_key(self.value[0]):
            #Already evaluated on store
            out = scope.get_key(self.value[0])

            for name in self.value[1:]:
                out = out[name]
        
            return out
        else:
            quit('Undefined Variable: ' + str(self.value)) #Undeclared identifier

class Expression(Value):
    def __init__(self, values):
        self.value = values

    def evaluate(self, scope):
        # Should all be values
        # Multiple expressions need to be coalesced
        
        out = None

        for value in self.value:
            if out:
                out.coalesce(scope, value)
                #Temp stub
                out = value.evaluate(scope)
            else:
                out = value.evaluate(scope)

        return out

class FunctionType(Value):
    def evaluate(self, scope):
        #TODO
        return None

class Function(Value):
    def __init__(self, bind, statements):
        self.bind = bind
        self.statements = statements
        self.argument = None

    def coalesce(self, scope, value):
        print(self.argument)
        if not self.argument:
            self.argument = value
            return self.evaluate(scope)
        else:
            # Too many arguments provided
            # In the end this should coalesce the types
            # For now ill just return the second value
            return value
            

    def evaluate(self, scope):
        if self.argument:
            new_scope = scope.copy()
            new_scope.set_key(self.bind, self.argument.evaluate(scope))
            env = ExecutionEnvironment(scope.copy())
            env.execute(self.statements)
        else:
            return self

class Statement():
    def __init__(self):
        pass

    def execute(self, scope):
        pass

class MatterStatement(Statement):
    def __init__(self, identifier, value, type=None):
        self.identifier = identifier
        self.value = value
        self.type = type

    def execute(self, scope):
        #Fix for assigning to objects
        if self.type:
            scope.set_key(self.identifier[0], self.value.evaluate(scope), self.type.evaluate(scope))
        else:
            scope.set_key(self.identifier[0], self.value.evaluate(scope))

class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def execute(self, scope):
        self.expression.evaluate(scope)

class Matter():
    def __init__(self, value, type):
        self.value = value
        self.type = type

class Scope():
    def __init__(self, init):
        self.map = init

    def get_key(self, key):
        return self.map[key].value

    def get_key_type(self, key):
        return self.map[key].type

    def set_key(self, key, value, type=None):
        self.map[key] = Matter(value, type)

    def has_key(self, key):
        return key in self.map

    def copy(self):
        return Scope(self.map.copy())

class ExecutionEnvironment():
    def __init__(self, scope):
        self.scope = scope

    def execute(self, statements):
        for statement in statements:
            statement.execute(self.scope)

