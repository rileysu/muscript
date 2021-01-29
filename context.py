import concrete
import typecheck

class Scope():
    def __init__(self, values, types):
        self.values = values
        self.types = types

    def get_value(self, key):
        return self.values[key]

    def get_type(self, key):
        return self.types[key]

    def set_value_type(self, key, value, type, context):
        type = self.get_type(key) if (self.has_type(key) and not type) else type
       
        if type:
            typecheck.check_type(value, type, context)

        self.values[key] = value
        self.types[key] = type

    def has_value(self, key):
        return key in self.values

    def has_type(self, key):
        return key in self.types

    def copy(self):
        return Scope(self.values.copy(), self.types.copy())

class Context():
    def __init__(self, scope, is_halted=False, is_returnable=True, parent_object=None):
        self.scope = scope
        self.is_halted = is_halted
        self.is_returnable = is_returnable
        self.return_value = concrete.ConcreteEmpty()
        self.parent_object = parent_object

        def return_function(context, value):
            self.halt()
            self.return_value = value

            return concrete.ConcreteEmpty()

        self.return_function = return_function

        # Init the scope if returnable
        if is_returnable:
            self.scope.set_value_type('return',
                    concrete.ConcreteExternalFunction(self, self.return_function),
                    concrete.ConcreteType('ExternalFunction'),
                    self)

        # Init scope if inside object
        if self.parent_object:
            self.scope.set_value_type('self',
                    self.parent_object,
                    self.parent_object,
                    self)

    def copy(self):
        return Context(self.scope.copy(), self.is_halted, self.is_returnable, self.parent_object)

    def halt(self):
        self.is_halted = True

    def execute(self, statements):
        for statement in statements:
            if self.is_halted:
                break
            else:
                statement.execute(self)

    def create_function_context(self, bind, value, type=concrete.ConcreteUndefined()):
        new_scope = self.scope.copy()
        if bind:
            new_scope.set_value_type(bind, value, type, self)

        return Context(new_scope, is_returnable=True)

    # Apply changed variables to parent context
    def close_function_context(self, context):
        for attribute in self.scope.values:
            if context.scope.has_value(attribute):
                self.scope.set_value_type(attribute, 
                        context.scope.get_value(attribute), 
                        context.scope.get_type(attribute),
                        self)
