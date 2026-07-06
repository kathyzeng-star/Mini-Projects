# Expression.py
# The program builds for simple arithmetic expressions

# Check if the input is a number
from ast import expr
import operator

# Part 1: Write an evaluator for these expressions.
def is_number(express):
    return isinstance(express, (int, float))

# Check if the input includes a variable
def is_variable(express):
    return isinstance(express, str)

def is_binary_expression(express):
    return (isinstance(express, tuple) and len(express) == 3
        and isinstance(express[0], str) )

def apply_operation(operator, left_val, right_val):
    if operator == '+':
        return left_val + right_val
    elif operator == '-':
        return left_val - right_val
    elif operator == '*':
        return left_val * right_val
    elif operator == '/':
        return left_val / right_val
    elif operator == '//':
        return left_val // right_val
    elif operator == '%':
        return left_val % right_val
    else:
        raise ValueError("Invalid operator: {}", operator)
    
def evaluate(express, env):
    if is_number(express):
        return express
    if is_variable(express):
        if express in env:
            return env[express]
        raise NameError("Variable {} not found in environment".format(express))
    
    elif is_let_expression(express):
        return evaluate_let(express, env)
    elif is_binary_expression(express):
        operator, left_expr, right_expr = express
        left_val = evaluate(left_expr, env)
        right_val = evaluate(right_expr, env)
        return apply_operation(operator, left_val, right_val)
    raise TypeError("Invalid expression: {}". format(express))

# Extend the evaluator to support let expressions
def is_let_expression(express):
    return (isinstance(express, tuple) and len(express) == 4
        and express[0] == "let")

def evaluate_let(express, env):
    _, var_name, var_expr, body_expr = express
    var_val = evaluate(var_expr, env)
    new_env = env.copy()
    new_env[var_name] = var_val
    return evaluate(body_expr, new_env)

# Part 2: Mapping over expression trees
def map_nums(express, func):
    if is_number(express):
        return func(express)
    
    if is_variable(express):
        return express
    
    # Perform recursion
    if is_binary_expression(express):
        operator, left_expr, right_expr = express
        return (operator, map_nums(left_expr, func), map_nums(right_expr, func))
    
    raise TypeError(f"Invalid expression: {express}")

# Part 3: Mapping over variables
def map_vars(express, func):
    if is_number(express):
        return express
    
    if is_variable(express):
        return func(express)
    
    if is_binary_expression(express):
        operator, left_expr, right_expr = express
        return (operator, map_vars(left_expr, func), map_vars(right_expr, func))

    raise TypeError(f"Invalid expression: {express}")

# Part 4: Create Environment-based functions with closures
def make_evaluator(env):
    def evaluator(express):
        return evaluate(express, env)
    
    return evaluator

# Assume that the input has nested tuples
def main():
    env = {
        "x": 10,
        "y": 7
    }
    
    # For each input, the lambda function manipulates the values in the tree.
    express = ("*", ("+", "x", 3), ("-", "y", 2))

    print("\nThe original expression tree is", express)
    print("The value of the expression is", evaluate(express, env))

    scale_num = map_nums(express, lambda n: n * 10)
    print("\nNumbers scaled by 10:", scale_num) 
    
    renamed = map_vars(express, lambda name: name.upper())
    print("\nHere are variables raise to the upper case:", renamed) 

    evaluate_with_env = make_evaluator(env)
    print("Evaluating with closure:", evaluate_with_env(express)) 

    env = {"x": 100}
    expr = ("let", "x", 5, ("+", "x", 3))
    print(evaluate(expr, env)) # 8
    print(env["x"]) # 100

    print("\n")

if __name__ == "__main__":
    main()