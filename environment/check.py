import typecheck

def check_arg(value, type):
    if (isinstance(value, tuple) and not any(typecheck.is_type(value, type) for x in type)) or not typecheck.is_type(value, type):
        raise Exception('Expected ' + str(type) + ' but got ' + str(value))

