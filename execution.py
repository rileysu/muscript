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
