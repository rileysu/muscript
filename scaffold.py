from lexer import Lexer, Token, TokenClass
#from parser import Parser

token_classes = [TokenClass('@{', 'function_open'),
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
#parser = Parser()

with open('example.mu') as f:
    text = f.read()

    tokens = lexer.parse(text)
    
    for token in tokens:
        print(token)

    #print(parser.parse(tokens))
