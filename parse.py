from lark import Lark, Transformer
from state import Integer, Decimal, String, List, Set, Object, Empty, Ellipsis, Variable, Expression, AlgebraicType, FunctionType, Function, Statement, MatterStatement, ExpressionStatement

class TreeTransformer(Transformer):
    def integer(self, values):
        return Integer(int(values[0]))
    
    def decimal(self, values):
        return Decimal(float(values[0]))

    def string(self, values):
        return String(values[0].replace('\'', ''))

    
    def list(self, values):
        return List(values)

    def set(self, values):
        return Set(values)

    def object_definition(self, values):
        out = {
            'name': 'object_definition',
            'identifier': None,
            'type': None,
            'value': None
        }

        for value in values:
            if value['name'] == 'identifier':
                out['identifier'] = value
            elif value['name'] == 'type_definition':
                out['type'] = value['expression']
            elif value['name'] == 'assign_definition':
                out['value'] = value['expression']
            elif value['name'] == 'typeassign_definition':
                out['value'] = value['expression']
                out['type'] = value['expression']


        return out

    def object(self, values):
        return Object(values)

    def empty_value(self, values):
        return Empty()

    def ellipsis_value(self, values):
        return Ellipsis()

    def variable(self, values):
        return Variable(values)

    def name(self, values):
        return values[0].value

    def identifier(self, values):
        return {
                'name': 'identifier',
                'value': values[0]
        }

    def algebraic_type(self, values):
        return AlgebraicType(values)

    def function_type(self, values):
        return FunctionType(values)

    def function_bind(self, values):
        return values[0] if values else None

    def function(self, values):
        return Function(values[0], values[1:])

    def type_definition(self, values):
        return {
            'name': 'type_definition',
            'expression': values[0]
        }

    def assign_definition(self, values):
        return {
            'name': 'assign_definition',
            'expression': values[0]
        }

    def typeassign_definition(self, values):
        return {
            'name': 'typeassign_definition',
            'expression': values[0]
        }

    def expression(self, values):
        return Expression(values)

    def matter_statement(self, values):
        identifier = None
        assign = None
        type = None
        
        for value in values:
            if value['name'] == 'identifier':
                identifier = value['value']
            elif value['name'] == 'type_definition':
                type = value['expression']
            elif value['name'] == 'assign_definition':
                assign = value['expression']
            elif value['name'] == 'typeassign_definition':
                assign = value['expression']
                type = value['expression']

        return MatterStatement(identifier, assign, type)

    def expression_statement(self, values):
        return ExpressionStatement(values[0])

    def start(self, values):
        return values

class Parser:
    def __init__(self):
        self.lark = Lark("""
            start: statement+
            type_definition : _type expression
            assign_definition : _assign expression
            typeassign_definition: _typeassign expression
            matter_statement : (identifier type_definition assign_definition) | (identifier type_definition) | (identifier assign_definition) | (identifier typeassign_definition)
            expression_statement: expression
            ?statement : (matter_statement | expression_statement) _end_statement
            
            algebraic_type : _base_expression (_algebraic_seperator _base_expression)+
            function_type : _base_expression (_function_arrow _base_expression)+
            empty_value : _open_paren _close_paren
            ellipsis_value : "..."
            _base_expression : (empty_value
                | ellipsis_value
                | variable
                | constant
                | function
                | list
                | set 
                | object
                | (_open_paren expression _close_paren))
            expression : (algebraic_type | function_type | _base_expression)+
            function : _open_function statement+ _close_function
            list : _open_list [expression (_seperator expression)*] _close_list
            
            set : _open_set [expression (_seperator expression)*] _close_set
           
            object_definition : (identifier type_definition assign_definition) | (identifier type_definition) | (identifier assign_definition) | (identifier typeassign_definition)
            object : _open_object [object_definition (_seperator object_definition)*] _close_object
            ?constant : integer | decimal | string
            identifier : name
            variable: name (_access name)*
           
            function_bind : name?
            _open_function : "@" function_bind  "{"
            _seperator : ","
            _type : ":"
            _assign : "="
            _typeassign : ":="
            _access: "."
            name : /[_a-zA-Z][_\-a-zA-Z0-9]*/
            _function_arrow : "->"
            _algebraic_seperator : "|"
            integer : /-?\d+/
            decimal : /-?\d+\.\d*/
            string : /\'[^\']*\'/
            _end_statement : ";"
            _close_function : _close_curly_brace
            _open_list : "["
            _close_list : "]"
            _open_set : "<"
            _close_set : ">"
            _open_paren : "("
            _close_paren : ")"
            _open_object : "{"
            _close_object : _close_curly_brace
            _close_curly_brace : "}"
            %import common.WS
            %ignore WS
        """, parser="lalr")

    def parse(self, text):
        return self.lark.parse(text)