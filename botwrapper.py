import ast
import astunparse

# Your template code
template_code = """
import time
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def wait(cycles):
    while cycles > 0:
        message = None
        while message == None or message['type'] != 'message':
            message = pubsub.get_message()
        if cycles > 1:
            r.publish('bot1', f"wait {message['data'].decode()}")
        cycles -= 1

pubsub = r.pubsub()
pubsub.subscribe('cycle1')

def move():
    wait(2)
    r.publish('bot1', 'move')

def shoot():
    wait(1)
    r.publish('bot1', 'shoot')

def rotate():
    wait(1)
    r.publish('bot1', 'rotate')

while True:
    #INSERT CODE HERE
"""

# The code you want to insert
new_code = """
    # New code to insert
    print("This is the inserted code.")
"""

# Parse the template code into an AST
template_ast = ast.parse(template_code)

# Find the insertion point (specifically a while True: loop)
for node in ast.walk(template_ast):
    if isinstance(node, ast.While):
        # Check if the condition is a Constant node with a value of True
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            # Insert the new code as a new statement in the while loop
            new_code_ast = ast.parse(new_code)
            node.body.insert(0, new_code_ast.body[0])
            break

# Unparse the modified AST back into code
modified_code = astunparse.unparse(template_ast)

print(modified_code)