import re

class Token:
    def __init__(self, value, name):
        self.value = value
        self.name = name

    def __str__(self):
        return 'Token(value=\'' + self.value + '\', name=' + self.name + ')'

class TokenClass:
    def __init__(self, regex, name):
        self.regex = regex
        self.name = name

class Lexer:
    def __init__(self, token_classes, ignore_classes):
        self.token_classes = token_classes
        self.ignore_classes = ignore_classes

    def parse(self, text):
        curr_text = text
        tokens = []

        while len(curr_text) > 0:
            found_match = False

            for token_class in self.token_classes:
                match = re.search('^' + token_class.regex, curr_text)

                if match != None:
                    match_text = match.group(0)

                    tokens.append(Token(match_text, token_class.name))

                    curr_text = curr_text[len(match_text):]
                    found_match = True

            for ignore_class in self.ignore_classes:
                match = re.search('^' + ignore_class.regex, curr_text)

                if match != None:
                    match_text = match.group(0)

                    curr_text = curr_text[len(match_text):]
                    found_match = True

            if not found_match:
                raise Exception('Couldn\'t identify token: ' + curr_text)

        return tokens
