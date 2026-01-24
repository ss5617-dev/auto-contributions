# Learning Objective: Visualize and Explore the Abstract Syntax Tree (AST) of Python Code
#
# This tutorial will guide you through understanding the structure of your Python
# code by visualizing its Abstract Syntax Tree (AST). The AST is a hierarchical
# representation of the source code, making it easier to grasp how Python
# interprets and processes your programs. We'll use Python's built-in `ast`
# module and a simple visitor pattern to traverse and print the AST.
#
# Concepts Covered:
# - What is an AST?
# - How to generate an AST from Python code.
# - How to traverse an AST using a visitor pattern.
# - How to interpret common AST node types.

import ast
import inspect

# A simple NodeVisitor subclass to traverse and print AST nodes.
# This class helps us systematically go through each part of the AST.
class ASTPrinter(ast.NodeVisitor):
    def __init__(self, indent=0):
        # 'indent' keeps track of the current depth in the AST,
        # which we use for pretty-printing.
        self.indent = indent

    def generic_visit(self, node):
        # This is a fallback method. If we don't have a specific
        # 'visit_NodeType' method for a given node, this will be called.
        # It prints the node's type and then continues visiting its children.
        print(f"{'  ' * self.indent}{type(node).__name__}")
        self.indent += 1
        # super().generic_visit(node) is the key here. It tells
        # the visitor to continue traversing the children of the current node.
        super().generic_visit(node)
        self.indent -= 1

    # We can define specific visit methods for common node types to
    # provide more detailed information or custom handling.
    # For this tutorial, we'll focus on printing the type,
    # but you could extract variable names, function names, etc. here.

    def visit_Module(self, node):
        # The root of every Python script is a Module.
        print(f"{'  ' * self.indent}{type(node).__name__} (body_count: {len(node.body)})")
        self.indent += 1
        self.generic_visit(node)
        self.indent -= 1

    def visit_FunctionDef(self, node):
        # Represents a function definition.
        print(f"{'  ' * self.indent}{type(node).__name__} (name: {node.name})")
        self.indent += 1
        # We visit the arguments and the body of the function.
        self.generic_visit(node)
        self.indent -= 1

    def visit_Assign(self, node):
        # Represents an assignment statement (e.g., x = 10).
        print(f"{'  ' * self.indent}{type(node).__name__} (targets_count: {len(node.targets)})")
        self.indent += 1
        # We visit the targets (variables on the left) and the value (on the right).
        self.generic_visit(node)
        self.indent -= 1

    def visit_Name(self, node):
        # Represents a variable name or identifier.
        # 'ctx' indicates the context (e.g., Load, Store, Del).
        print(f"{'  ' * self.indent}{type(node).__name__} (id: {node.id}, ctx: {type(node.ctx).__name__})")
        # No need to call generic_visit here as Name nodes are typically leaves.

    def visit_Constant(self, node):
        # Represents literal values like numbers, strings, booleans, None.
        # In older Python versions, this might be ast.Num, ast.Str, etc.
        print(f"{'  ' * self.indent}{type(node).__name__} (value: {repr(node.value)})")
        # No need to call generic_visit here as Constant nodes are leaves.

    def visit_Expr(self, node):
        # Represents an expression statement, often used for function calls or docstrings.
        print(f"{'  ' * self.indent}{type(node).__name__}")
        self.indent += 1
        self.generic_visit(node)
        self.indent -= 1

    def visit_Call(self, node):
        # Represents a function call.
        print(f"{'  ' * self.indent}{type(node).__name__} (func_type: {type(node.func).__name__})")
        self.indent += 1
        # We visit the function being called and its arguments.
        self.generic_visit(node)
        self.indent -= 1

# --- Example Usage ---

# Define a sample Python code string.
sample_code = """
def greet(name):
    message = f"Hello, {name}!"
    print(message)

x = 100
greet("World")
"""

# Inspect the source code of the current module to get a real-world example.
# This is a more dynamic way to get code to analyze.
# We'll exclude the current function definition itself to avoid infinite recursion.
current_module_source = inspect.getsource(inspect.currentframe())
# Get the source code of a function defined within this script.
def example_function_for_ast_demo(a, b):
    result = a + b
    if result > 10:
        print("Large sum!")
    return result

# Let's analyze the 'sample_code' first.
print("--- Analyzing Sample Code String ---")
try:
    # ast.parse() takes a string of Python code and returns its AST.
    tree = ast.parse(sample_code)

    # Create an instance of our ASTPrinter.
    printer = ASTPrinter()

    # The visit() method starts the traversal from the root of the AST.
    printer.visit(tree)
except SyntaxError as e:
    print(f"Syntax error in sample code: {e}")

print("\n--- Analyzing a Function Definition ---")
try:
    # We can also get the AST of a function object directly.
    # inspect.getsource() gets the source code as a string.
    function_source = inspect.getsource(example_function_for_ast_demo)
    function_tree = ast.parse(function_source)

    printer_function = ASTPrinter()
    printer_function.visit(function_tree)
except Exception as e:
    print(f"Error analyzing function: {e}")

# You can extend this ASTPrinter to extract specific information.
# For example, to list all variable assignments:
class VariableAssignmentFinder(ast.NodeVisitor):
    def __init__(self):
        self.assignments = []

    def visit_Assign(self, node):
        # An assignment has targets (left side) and a value (right side).
        for target in node.targets:
            if isinstance(target, ast.Name):
                # If the target is a simple name (variable), record it.
                self.assignments.append(target.id)
        # Continue visiting children in case of nested assignments or expressions.
        self.generic_visit(node)

print("\n--- Finding Variable Assignments ---")
try:
    tree = ast.parse(sample_code)
    finder = VariableAssignmentFinder()
    finder.visit(tree)
    print(f"Variables assigned: {finder.assignments}")
except SyntaxError as e:
    print(f"Syntax error: {e}")

# Now, let's try to find assignments in the example function.
print("\n--- Finding Variable Assignments in Function ---")
try:
    function_source = inspect.getsource(example_function_for_ast_demo)
    function_tree = ast.parse(function_source)
    finder_function = VariableAssignmentFinder()
    finder_function.visit(function_tree)
    print(f"Variables assigned in function: {finder_function.assignments}")
except Exception as e:
    print(f"Error: {e}")