def check_arg(value, type):
    if (isinstance(value, tuple) and not any(isinstance(value, x) for x in type)) or not isinstance(value, type):
        raise Exception('Expected ' + str(type) + ' but got ' + str(value))

