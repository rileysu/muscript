# usage

# new_queue = mu_queue Integer              ; initialise an empty queue? []
# new_queue = new_queue.push 3              ; now queue = [3]
# new_queue = new_queue.push 5              ; now queue = [3, 5]
# head  = new_queue.pop                     ; value 3
# new_queue = new_queue.push 'hello'        ; "ERROR invalid type"

# implementation
# class variable NO ACCESS -> Array

class mu_queue:
    def __init__