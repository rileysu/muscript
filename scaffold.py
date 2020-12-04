from lexer import Lexer, Token, TokenClass
from parser import Parser, TreeTransformer
from execution import ExecutionEnvironment, Scope
from environment import init_scope
#from parser import Parser

token_classes = [TokenClass('@{', 'open_function'),
        TokenClass('\\{', 'open_curlybrace'),
        TokenClass('\\}', 'close_curlybrace'),
        TokenClass('\\(', 'open_parenthesis'),
        TokenClass('\\)', 'close_parenthesis'),
        TokenClass('\\[', 'open_squarebrace'),
        TokenClass('\\]', 'close_squarebrace'),
        TokenClass('<', 'open_anglebrace'),
        TokenClass('>', 'close_anglebrace'),
        TokenClass(':', 'colon'),
        TokenClass('=', 'equals'),
        TokenClass(',', 'comma'),
        TokenClass('\\.', 'dot'),
        TokenClass(';', 'semicolon'),
        TokenClass('->', 'function_arrow'),
        TokenClass('\\d+\\.\\d*', 'decimal'),
        TokenClass('\\d+', 'integer'),
        TokenClass('[a-zA-Z_]\\w*', 'identifier')]

ignore_classes = [TokenClass('\\s', 'whitespace')]

lexer = Lexer(token_classes, ignore_classes)
parser = Parser()

with open('example2.mu') as f:
    text = f.read()

    tree = parser.parse(text)
    statements = TreeTransformer().transform(tree)

    scope = Scope(init_scope)
    env = ExecutionEnvironment(scope)

    env.execute(statements)

    #for matter in scope.map:
    #    print(matter)
    #    print(scope.map[matter])
