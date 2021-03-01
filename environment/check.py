import typecheck

def check_arg(value, type, context):
    if (isinstance(type, tuple) and not any(typecheck.is_type(value, x, context) for x in type)) or (not isinstance(type, tuple) and not typecheck.is_type(value, type, context)):
        raise typecheck.TypeException('Expected: ' + str(type) + ' but got: ' + str(value))

