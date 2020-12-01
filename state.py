from concrete import Concrete, ConcreteInteger, ConcreteDecimal, ConcreteString, ConcreteList, ConcreteSet, ConcreteObject, ConcreteFunction

class Value():
    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return Concrete(self.value)

class Integer(Value):
    def evaluate(self, scope):
        return ConcreteInteger(self.value)

class Decimal(Value):
    def evaluate(self, scope):
        return ConcreteDecimal(self.value)

class String(Value):
    def evaluate(self, scope):
        return ConcreteString(self.value)

class List(Value):
    def evaluate(self, scope):
        return ConcreteList(list(map(lambda x: x.evaluate(scope), self.value)))

class Set(Value):
    def evaluate(self, scope):
        return ConcreteSet(set(map(lambda x: x.evaluate(scope), self.value)))

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

        return ConcreteObject(out)


class Variable(Value):
    def evaluate(self, scope):
        if scope.has_key(self.value[0]):
            #Already evaluated on store
            out = scope.get_key(self.value[0])

            for name in self.value[1:]:
                #Quick hack since objects use Matter
                out = out.value[name].value

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
                out = out.coalesce(scope, value.evaluate(scope))
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

    def evaluate(self, scope):
            return ConcreteFunction(self.bind, self.statements)

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
