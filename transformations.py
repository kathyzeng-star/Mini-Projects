import expressions

# Create functions refer to Chapter 3
def map_numbers(expr, function):
    """
        Args:
            expr: An expression to evaluate 
            function: expression map to the function
        
        Returns:
            The mapped function
    """
    # relate to higher-order function and using recursion
    if isinstance(expr, expressions.Number):
        return expressions.Number(function(expr.value) )
    
    if isinstance(expr, expressions.Variable):
        return expr
    
    if isinstance(expr, expressions.Negate):
        return expressions.Negate(map_numbers(expr.operand, function) )
    
    if isinstance(expr, expressions.BinaryExpression):
        return type(expr)(map_numbers(expr.left, function), map_numbers(expr.right, function) )
    
    if isinstance(expr, expressions.Let):
        return expressions.Let(expr.name, map_numbers(expr.value_expr, function), map_numbers(expr.body_expr, function))
    
    raise TypeError(f"Malformed expression: {expr}")

def substitute(expr, name, replacement):
    """
        Args:
            expr: An expression to evaluate 
            name: a variable name
            replacement: variable replacement
        
        Returns:
            A let expression
    """
    replacement = expressions.to_expression(replacement)
    # Let subsitution a variable substitute inside a value but not body

    # Base case: consist only a number 
    if isinstance(expr, expressions.Number):
        return expr
    
    # Variable
    if isinstance(expr, expressions.Variable):
        if expr.name == name:
            return replacement
        return expr

    # Negate
    if isinstance(expr, expressions.Negate):
        # Operand is a string 
        return expressions.Negate(substitute(expr.operand, name, replacement) )
    
    # BinaryExpression
    if isinstance(expr, expressions.BinaryExpression):
        return type(expr)(substitute(expr.left, name, replacement),
            substitute(expr.right, name, replacement)  )
    
    # Let: two subcases 
    elif isinstance(expr, expressions.Let):
        # name, value_expr, body_expr 
        new_val = substitute(expr.value_expr, name, replacement)
        # bound name == target name
        if expr.name == name:
            new_body = expr.body_expr

        # bound name != target name
        else:
            new_body = substitute(expr.body_expr, name, replacement)

        return expressions.Let(expr.name, new_val, new_body)

    raise TypeError("An expression cannot be substituted.")

def count_nodes(expr):
    """
        Args:
            expr: An expression to evaluate 
        
        Returns:
            total number of expression nodes 
    """
    # count nodes: operands and operators 

    # Base case: only a number included in an expression 
    if isinstance(expr, expressions.Number) or isinstance(expr, expressions.Variable):
        return 1
    
    if isinstance(expr, expressions.Negate):
        return 1 + count_nodes(expr.operand)
    
    if isinstance(expr, expressions.BinaryExpression):
        return 1 + count_nodes(expr.left) + count_nodes(expr.right)
    
    # name, value_expr, body_expr
    if isinstance(expr, expressions.Let):
        return 1 + count_nodes(expr.value_expr) + count_nodes(expr.body_expr)

    raise TypeError("An expression node cannot be count.")
    
def expression_depth(expr):
    """
        Args:
            expr: An expression to evaluate 
        
        Returns:
            the tree depth
    """
    # Base case: only a number or variable included in an expression
    if isinstance(expr, expressions.Number) or isinstance(expr, expressions.Variable):
        return 1
    
    if isinstance(expr, expressions.Negate):
        return 1 + expression_depth(expr.operand)
    
    if isinstance(expr, expressions.BinaryExpression):
        return 1 + max(expression_depth(expr.left), expression_depth(expr.right))
    
    if isinstance(expr, expressions.Let):
        return 1 + max(expression_depth(expr.value_expr), expression_depth(expr.body_expr))
    
    raise TypeError(f"Expression must be in binary, negation or let form or itself:{expr}")

print()
expr = expressions.Add(expressions.Number(2), expressions.Multiply(expressions.Variable("x"), expressions.Number(3)))

mapped = map_numbers(expr, lambda n: n * 10)
print(mapped) # (20 + (x * 30))

expr = expressions.Let("x", expressions.Add(expressions.Variable("y"), expressions.Number(1)), expressions.Add(expressions.Variable("x"), expressions.Variable("y")))
result = substitute(expr, "y", expressions.Number(10))
print(result) 

expr = expressions.Add(expressions.Number(2), expressions.Multiply(expressions.Variable("x"), expressions.Number(3)))
print(count_nodes(expr)) # 5

print(expression_depth(expressions.Number(3))) 
print(expression_depth(expressions.Add(expressions.Number(1), expressions.Number(2))))

print() 