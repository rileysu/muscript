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
        return concrete.ConcreteList(tuple(map(lambda x: x.evaluate(context), self.value)))

class Set(Value):
    def evaluate(self, context):
        return concrete.ConcreteSet(frozenset(map(lambda x: x.evaluate(context), self.value)))

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

        # Ensure changes don't carry up to previous contexts
        new_context = context.copy()
        
        # Structure types and values for concrete types
        # Give values and types undefined if not defined and otherwise give the value specified
        # Resolve values and types to ensure matter isn't transferred unknowingly
        for key in self.values:
            # Ignore type check until implemented
            if self.values[key]:
                values[key] = self.values[key].evaluate(new_context).resolve()
            else:
                values[key] = concrete.ConcreteUndefined()
            if self.types[key]:
                types[key] = self.types[key].evaluate(new_context).resolve()
            # Otherwise set key to the any type
            else:
                types[key] = concrete.ConcreteUndefined()

        return_object = concrete.ConcreteObject(values, types, context)
        new_context.parent_object = return_object

        return return_object

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
        if context.scope.has_key(self.value[0]):

            type = context.scope.get_type(self.value[0])
            
            #Already evaluated on store
            value = context.scope.get_value(self.value[0])

            for name in self.value[1:]:
                type = value.get_type(name)
                value = value.get(name)

            return concrete.ConcreteMatter(value, type)
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
                # Ensures that expressions with multiple values coalescing don't return as matter
                out.resolve()
            else:
                # If the expression only contains one value it can be returned as matter since
                # something like functions should still type check regardless of whether they are in
                # parenthesis or not
                out = value.evaluate(context)

        return out

class AlgebraicType(Value):
    def evaluate(self, context):
        return concrete.ConcreteAlgebraicType(list(map(lambda x: x.evaluate(context).resolve(), self.value)))

class FunctionType(Value):
    def evaluate(self, context):
        #Needs to additionally handle the case of generic types
        return concrete.ConcreteFunctionType(list(map(lambda x: x.evaluate(context).resolve(), self.value)))

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
    def __init__(self, identifier, value, type):
        self.identifier = identifier
        self.value = value
        self.type = type

    def execute(self, context):
        # Modify context so algebraic types can self reference 
        # Matter Statements can't be nested so this should be fine
        if isinstance(self.value, Expression) and isinstance(self.value.value[-1], AlgebraicType):
            context.scope.set_value_type(self.identifier, concrete.ConcreteSelfReference(self.identifier), None, context)

        if self.value:
            if self.type:
                context.scope.modify_value_type(self.identifier, self.value.evaluate(context), self.type.evaluate(context), context)
            else:
                context.scope.modify_value_type(self.identifier, self.value.evaluate(context), None, context)
        else:
            if self.type: 
                context.scope.modify_value_type(self.identifier, None, self.type.evaluate(context), context)
            else:
                raise Exception('No value or type specified in statement!')

class ExpressionStatement(Statement):
    def __init__(self, expression):
        self.expression = expression

    def execute(self, context):
        self.expression.evaluate(context)
