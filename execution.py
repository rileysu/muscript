import typecheck

class ScopeMatter():
    def __init__(self, values, types):
        self.values = values
        self.types = types

class Scope():
    def __init__(self, values, types):
        self.values = values
        self.types = types

    def get_key(self, key):
        return self.values[key]

    def get_key_type(self, key):
        return self.types[key]

    def set_key(self, key, value, type):
        type = self.get_key_type(key) if self.has_key_type(key) else type
        
        if type:
            if not typecheck.is_type(type, value):
                raise Exception('Type exception: ' + str(value) + ' -> ' + str(type))

        self.values[key] = value
        self.types[key] = type

    def has_key(self, key):
        return key in self.values

    def has_key_type(self, key):
        return key in self.types

    def copy(self):
        return Scope(self.values.copy(), self.types.copy())

class ExecutionEnvironment():
    def __init__(self, scope):
        self.scope = scope
        self.is_halted = False

    def halt(self):
        self.is_halted = True

    def execute(self, statements):
        for statement in statements:
            if self.is_halted:
                break
            else:
                statement.execute(self.scope)
