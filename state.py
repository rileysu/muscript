import concrete

class Value():
    def __init__(self, value):
        self.value = value

    def evaluate(self, context):
        return concrete.Concrete(self.value)

class Integer(Value):
    def evaluate(self, context):
        return concrete.ConcreteInteger(self.value)

class Decimal(Value):
    def evaluate(self, context):
        return concrete.ConcreteDecimal(self.value)

class String(Value):
    def evaluate(self, context):
        return concrete.ConcreteString(self.value)

class List(Value):
    def evaluate(self, context):
        return concrete.ConcreteList(list(map(lambda x: x.evaluate(context), self.value)))

class Set(Value):
    def evaluate(self, context):
        return concrete.ConcreteSet(set(map(lambda x: x.evaluate(context), self.value)))

class Object(Value):
    def __init__(self, values):
        self.values = {}
        self.types = {}

        for definition in values:
            #What if object is referenced in object to assign to?
            self.values[definition['identifier']['value']] = definition['value']
            self.types[definition['identifier']['value']] = definition['type']
    
    def evaluate(self, context):
        values = {}
        types = {}
       
        # Structure types and values for concrete types
        # Give values and types undefined if not defined and otherwise give the value specified
        for key in self.values:
            # Ignore type check until implemented
            if self.values[key]:
                values[key] = self.values[key].evaluate(context)
            else:
                values[key] = concrete.ConcreteUndefined()
            if self.types[key]:
                types[key] = self.types[key].evaluate(context)
            # Otherwise set key to the any type
            else:
                types[key] = concrete.ConcreteUndefined()

        return concrete.ConcreteObject(values, types)

class Empty(Value):
    def __init__(self):
        super().__init__(None)

    def evaluate(self, context):
        return concrete.ConcreteEmpty()

class Ellipsis(Value):
    def __init__(self):
        super().__init__(None)

    def evaluate(self, context):
        return concrete.ConcreteEllipsis()


class Variable(Value):
    def evaluate(self, context):
        if context.get_scope().has_value(self.value[0]):
            #Already evaluated on store
            out = context.get_scope().get_value(self.value[0])

            for name in self.value[1:]:
                out = out.get(name)

            return out
        else:
            quit('Undefined Variable: ' + str(self.value)) #Undeclared identifier

class Expression(Value):
    def __init__(self, values):
        self.value = values

    def evaluate(self, context):
        # Should all be values
        # Multiple expressions need to be coalesced
        
        out = None

        for value in self.value:
            if out:
                out = out.coalesce(context, value.evaluate(context))
            else:
                out = value.evaluate(context)

        return out

class AlgebraicType(Value):
    def __init__(self, values):
        self.values = values

    def evaluate(self, context):
        return concrete.ConcreteAlgebraicType(list(map(lambda x: x.evaluate(context), self.values)))

class FunctionType(Value):
    def evaluate(self, context):
        #TODO
        return None

class Function(Value):
    def __init__(self, bind, statements):
        self.bind = bind
        self.statements = statements
        self.argument = None

    def evaluate(self, context):
            return concrete.ConcreteFunction(context, self.bind, self.statements)

class Statement():
    def __init__(self):
        pass

    def execute(self, context):
        pass

class MatterStatement(Statement):
    def __init__(self, identifier, value, type=None):
        self.identifier = identifier
        self.value = value
        self.type = type

    def execute(self, context):
        if self.value:
            if self.type:
                context.get_scope().set_value_type(self.identifier, self.value.evaluate(context), self.type.evaluate(context))
            else:
                context.get_scope().set_value_type(self.identifier, self.value.evaluate(context), concrete.ConcreteUndefined())
        else:
            if self.type: 
                context.get_scope().set_value_type(self.identifier, concrete.ConcreteUndefined(), self.type.evaluate(context))
            else:
                raise Exception('No value or type specified in statement!')

class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def execute(self, context):
        self.expression.evaluate(context)
