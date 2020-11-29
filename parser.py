from lexer import Token

# -=Molecules=-
# Statement - an action that may mutate state and doesn't return a value
# Statement -> Identifier [Type Expression] Assign Expression | Function Expression+
# Expression - an action that may mutate state that does return a value
# Expression -> (Identifier | Constant | Expression Arrow Expression | Function Expression | Identifier [Type Expression] Assign Expression) [Expression]
## Matter - An assignable piece of state (open to new mutable data in the future)
## Matter -> Identifier
# Function - A list of statements
# Function -> Statement+
#
# -=Atoms=-
# Type - Defines type of matter
# Assign - Defines assigning to matter
# Identifier - An string representing matter
# Arrow - Defines a function type
# Constant - Defines a well defined single value
# 
# -=Conventions=-
# Conventions for tree transform function:
#   curr_node is always the deepest node needed to be satisfied
#   token is the recognised token object with associated value

class ParseNode:
    def __init__(self, name, value, parent, children):
        self.name = name
        self.value = value
        self.parent = parent
        self.children = children

        for child in children:
            child.parent = self

    def __repr__(self, depth=0):
        out = ('\t' * depth) + 'ParseNode(name=\'' + self.name + '\', value=' + str(self.value) + ', parent=\'' + (self.parent.name if self.parent else 'None') + '\', children=' + str(len(self.children)) + ')\n'

        for child in self.children:
            out += child.__repr__(depth+1)

        return out

def proc_function_open(token, curr_node):
    new_node = ParseNode('function', None, curr_node, []) 
    
    curr_node.parent.children.append(new_node)

    return new_node

def proc_open_curlybrace(token, curr_node):
    new_node = ParseNode('object', None, curr_node, [])
    
    curr_node.parent.children.append(new_node)

    return new_node

def proc_close_curlybrace(token, curr_node):
    if curr_node.parent:
        if curr_node.parent.name == 'function' or curr_node.parent.name == 'object':
            return curr_node.parent
        else:
            pass #Syntax Error
    else:
        pass #Syntax Error
            
def proc_open_parenthesis(token, curr_node):
    new_node = ParseNode('parenthesis', None, curr_node, [])

    return new_node

def proc_close_parenthesis(token, curr_node):
    if curr_node.parent:
        if curr_node.parent.name == 'parenthesis':
            return curr_node.parent
        else:
            pass #Syntax Error
    else:
        pass #Syntax Error

def proc_open_squarebrace(token, curr_node):
    new_node = ParseNode('list', None, curr_node.parent, [])

    curr_node.parent.children.append(new_node)

    return new_node

def proc_close_squarebrace(token, curr_node):
    if curr_node.parent:
        if curr_node.parent.name == 'list':
            return curr_node.parent
        else:
            pass #Syntax Error
    else:
        pass #Syntax Error

def proc_open_anglebrace(token, curr_node):
    new_node = ParseNode('set', None, curr_node.parent, [])

    curr_node.parent.children.append(new_node)
    
    return new_node

def proc_close_anglebrace(token, curr_node):
    if curr_node.parent:
        if curr_node.parent.name == 'set':
            return curr_node.parent
        else:
            pass #Syntax Error
    else:
        pass #Syntax Error

def proc_colon(token, curr_node):
    new_node = ParseNode('type', None, curr_node.parent, [])

    curr_node.parent.children.append(new_node)

    return new_node

def proc_equals(token, curr_node):
    new_node = ParseNode('assign', None, curr_node.parent, [])

    curr_node.parent.children.append(new_node)
    
    return new_node
  
def proc_comma(token, curr_node):
    new_node = ParseNode('seperator', None, curr_node.parent, [])

    curr_node.parent.children.append(new_node)

    return new_node

def proc_dot(token, curr_node):
    new_node = ParseNode('access', None, curr_node, [])

    curr_node.children.append(new_node)

    return new_node

def proc_semicolon(token, curr_node):
    explore_node = curr_node
    
    while explore_node != None:
        if explore_node.name == 'statement':
            parent_node = explore_node.parent

            if parent_node:
                return parent_node
            else:
                quit(1) #Syntax Error

        explore_node = explore_node.parent

    quit(1) #Syntax Error

def proc_function_arrow(token, curr_node):
    if curr_node.name == 'expression':
        new_node = ParseNode('function_arrow', None, curr_node, [])

        curr_node.children.append(new_node)

        return curr_node
    else:
        quit(1) #Syntax Error

def proc_decimal(token, curr_node):
    if curr_node == 'expression' and curr_node.children == []:
        curr_node.children.append(ParseNode('constant', ('decimal', float(token.value)), curr_node, []))

        return curr_node
    else:
        quit(1) #Syntax Error

def proc_integer(token, curr_node):
    if curr_node == 'expression' and curr_node.children == []:
        curr_node.children.append(ParseNode('constant', ('integer', int(token.value)), curr_node, []))

        return curr_node
    else:
        quit(1) #Syntax Error

def proc_identitifier(token, curr_node):
    if curr_node.name == 'statement' and curr_node.children == []:
        new_node = ParseNode('identifier', str(token.value), curr_node, [])

        curr_node.children.append(new_node)

        return curr_node
    else:
        new_node = ParseNode('expression', None, curr_node, [
            ParseNode('identifier', str(token.value), curr_node, [])
        ])

        curr_node.children.append(new_node)

        return new_node
    else:
        quit(1) #Syntax Error

class Parser:
    def __init__(self):
        self.token_map = {
                'function_open': proc_function_open,
                'open_curlybrace': proc_open_curlybrace,
                'close_curlybrace': proc_close_curlybrace,
                'open_parenthesis': proc_open_parenthesis,
                'close_parenthesis': proc_close_parenthesis,
                'open_squarebrace': proc_open_squarebrace,
                'close_squarebrace': proc_close_squarebrace,
                'open_anglebrace': proc_open_anglebrace,
                'close_anglebrace': proc_close_anglebrace,
                'colon': proc_colon,
                'equals': proc_equals,
                'comma': proc_comma,
                'dot': proc_dot,
                'semicolon': proc_semicolon,
                'function_arrow': proc_function_arrow,
                'decimal': proc_decimal,
                'integer': proc_integer,
                'identifier': proc_identitifier}

    #self.verifiers = {
    #    'statement': verify_statement,
    #    'expression': verify_expression,
    #    'matter': verify_matter,
    #    'function': verify_function
    #}

    def parse(self, tokens):
        main_func = ParseNode('function', None, None, [
            ParseNode('statement', None, None, [])
        ])

        curr_node = main_func.children[0].children[0]

        for token in tokens:
            if token.name in self.token_map.keys()
                curr_node = self.token_map[token.name](token, curr_node)
            
            print(token)
            print(tree)

            #if curr_node.name in self.verifiers.keys():
            #    if self.verifiers[curr_node.name]:
            #        curr_node = curr_node.parent            

        return tree
