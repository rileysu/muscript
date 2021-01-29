import typecheck

def check_arg(value, type, context):
    if (isinstance(value, tuple) and not any(typecheck.is_type(value, type, context) for x in type)) or not typecheck.is_type(value, type, context):
        raise typecheck.TypeException('Expected: ' + str(type) + ' but got: ' + str(value))

