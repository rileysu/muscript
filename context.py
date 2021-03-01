import concrete
import typecheck

class ContextVariable():
    def __init__(self, value, type):
        self.value = value
        self.type = type

class Scope():
    def __init__(self, values, types={}):
        self.values = {}

        for key in values:
            self.values[key] = ContextVariable(values[key], 
                    types[key] if key in types else concrete.ConcreteUndefined())

    def get_value(self, key):
        return self.values[key].value

    def get_type(self, key):
        return self.values[key].type

    # Overwrites variables which could be used in previous contexts
    # Copied contexts will not propogate changes to parent contexts
    def set_value_type(self, key, value, type, context):
        if type == None:
            type = self.get_type(key) if self.has_key(key) else concrete.ConcreteUndefined()

        if value == None: 
            value = self.get_value(key) if self.has_key(key) else concrete.ConcreteUndefined()
        
        if value != None and value != None:
            typecheck.check_type(value, type, context)

        self.values[key] = ContextVariable(value, type)

    # Modifies variables which could be used in previous contexts
    # Copied contexts will propagate changes to parent contexts
    def modify_value_type(self, key, value, type, context):
        if not self.has_key(key):
            self.set_value_type(key, value, type, context)
        else:
            if type == None:
                type = self.get_type(key)

            if value == None:
                value = self.get_value(key)

            if value != None and value != None:
                typecheck.check_type(value, type, context)
            
            self.values[key].value = value
            self.values[key].type = type
    
    def has_key(self, key):
        return key in self.values

    def copy(self):
        new_scope = Scope({})
        new_scope.values = self.values.copy()
        return new_scope

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
