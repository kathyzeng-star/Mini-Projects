from abc import ABC, abstractmethod

class Expression(ABC):
    @abstractmethod
    def evaluate(self, env):
        pass

    @abstractmethod
    def variables(self):
        pass

    @abstractmethod
    def simplify(self):
        pass
 
    def __add__(self, other):
        return Add(self, to_expression(other) )

    def __radd__(self, other):
        return Add(to_expression(other), self)

    def __sub__(self, other):
        return Subtract(self, to_expression(other))

    def __rsub__(self, other):
        return Subtract(to_expression(other), self)

    def __mul__(self, other):
        return Multiply(self, to_expression(other))

    def __rmul__(self, other):
        return Multiply(to_expression(other), self)

    def __truediv__(self, other):
        return Divide(self, to_expression(other))

    def __rtruediv__(self, other):
        return Divide(to_expression(other), self)

    def __neg__(self):
        return Negate(self)

class Number(Expression):
    def __init__(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be an int or float")
        self.value = value

    def evaluate(self, env):
        return self.value

    def variables(self):
        return set()
    
    def simplify(self):
        return self
    
    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return f"Number({self.value!r})"
    
    def __eq__(self, other):
        if not isinstance(other, Number):
            return NotImplemented
        return self.value == other.value

class Variable(Expression):
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Variable name must be a string.")
        # Must not be in empty variable
        if name == "":
            raise ValueError("Variable name cannot be empty.")
        self.name = name

    def evaluate(self, env):
        if self.name not in env:
            raise NameError(f"Unknown variable: {self.name}")
        return env[self.name]

    def variables(self):
        return {self.name}
    
    def simplify(self):
        return self
    
    def __str__(self):
        return self.name
    def __repr__(self):
        return f"Variable({self.name!r})"
    def __eq__(self, other):
        if not isinstance(other, Variable):
            return NotImplemented
        return self.name == other.name
    
class BinaryExpression(Expression):
    symbol = None
    
    def __init__(self, left, right):  
        self.left = to_expression(left)
        self.right = to_expression(right)

    def evaluate(self, env):
        left_value = self.left.evaluate(env)
        right_value = self.right.evaluate(env)
        return self.apply(left_value, right_value)
    
    def variables(self):
        return self.left.variables() | self.right.variables()

    @abstractmethod
    def apply(self, left_value, right_value):
        pass
    
    def __str__(self):
        return (
            f"({self.left} {self.symbol} {self.right})"
        )
    def __repr__(self):
        return (
            f"{type(self).__name__}"
            f"({self.left!r}, {self.right!r})"
        )

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.left == other.left and self.right == other.right)
    
    def simplify(self):
        # Simplify the Binary Expression
        simplified_left = self.left.simplify()
        simplified_right = self.right.simplify()

        if isinstance(simplified_left, Number) and isinstance(simplified_right, Number):
            value = self.apply(simplified_left.value, simplified_right.value)
            return Number(value)
        return type(self) (simplified_left, simplified_right)

class Add(BinaryExpression):
    symbol = '+'

    def apply(self, left_val, right_val):
        return left_val + right_val
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()

        # Case 1: if a + b then return it
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value + right.value)

        # Case 2: if a = 0, then return b
        if isinstance(left, Number) and left.value == 0:
            return right

        # Case 3: if b = 0, then return a
        if isinstance(right, Number) and right.value == 0:
            return left
        
        return Add(left, right)

class Subtract(BinaryExpression):
    symbol = '-'

    def apply(self, left_val, right_val):
        return left_val - right_val
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()

        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value - right.value)

        if isinstance(right, Number) and right.value == 0:
            return left
        
        return Subtract(left, right)

class Multiply(BinaryExpression):
    symbol = '*'

    def apply(self, left_val, right_val):
        return left_val * right_val
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        # Case 1: if a * b then return it
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value * right.value)

        # Case 2: if a = 0, then return b
        if isinstance(left, Number):
            if left.value == 0:
                return Number(0)
            if left.value == 1:
                return right
            
        # Case 3: if b = 0, then return a
        if isinstance(right, Number):
            if right.value == 0:
                return Number(0)
            if right.value == 1:
                return left
        
        return Multiply(left, right)

class Divide(BinaryExpression):
    symbol = '/'
    
    def apply(self, left_val, right_val):
        return left_val / right_val
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()

        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value / right.value)

        if isinstance(left, Number):
            if left.value == 0:
                return Number(0)
            
        if isinstance(right, Number):
            if right.value == 0:
                raise ZeroDivisionError("The denominator must not be zero")
            if right.value == 1:
                return left
        
        return Divide(left, right)

def to_expression(value):
    """Only argument is value that convert from integers and floats into Number objects"""
    if isinstance(value, Expression):
        return value
        
    if isinstance(value, (int, float)):
        return Number(value)

    raise TypeError("The value must expect in int, float or expression.")

class Negate(Expression):
    def __init__(self, operand):
        self.operand = to_expression(operand)

    def evaluate(self, env):
        return -self.operand.evaluate(env)

    def variables(self):
        return self.operand.variables()
    
    def simplify(self):
        # Perform recursion to simplify its operand 
        simplify_op = self.operand.simplify()
        # Folds -Number(n) into Number(-n)
        if isinstance(simplify_op, Number):
            return Number(-simplify_op.value)
        return Negate(simplify_op)

    def __str__(self):
        return f"-{self.operand}"
    
    def __repr__(self):
        return f"Negate({self.operand!r})"
    
    def __eq__(self, other):
        if not isinstance(other, Negate):
            return NotImplemented
        return self.operand == other.operand
    
class Let(Expression):
    def __init__(self, name, value_expr, body_expr):
        # raise a TypeError
        if not isinstance(name, str):
            raise TypeError("Let binding name must be a string.")
        
        if name == "":
            raise ValueError("Let binding name cannot be empty.")
        self.name = name
        self.value_expr = to_expression(value_expr)
        self.body_expr = to_expression(body_expr)

    def evaluate(self, env):
        org_env = self.value_expr.evaluate(env)
        copy_env = env.copy()
        copy_env[self.name] = org_env
        return self.body_expr.evaluate(copy_env)

    def variables(self):
        value_var = self.value_expr.variables()
        body_var = self.body_expr.variables()
        return value_var | (body_var - {self.name})
    
    def simplify(self):
        return Let(
            self.name,
            self.value_expr.simplify(),
            self.body_expr.simplify()
        )

    def __str__(self):
        return f"let {self.name} = {self.value_expr} in {self.body_expr}"
    
    def __repr__(self):
        return (f"Let({self.name!r}, "
               f"{self.value_expr}, "
               f"{self.body_expr}")
    
    def __eq__(self, other):
        if not isinstance(other, Let):
            return NotImplemented
        return (self.name == other.name and self.value_expr == other.value_expr 
            and self.body_expr == other.body_expr)

def main():
    x = Variable("x")
    y = Variable("y")

    expr = (x + 3) * (y - 2)

    env = {"x": 10, "y": 7}
    
    print("Expression:")
    print(expr)
    print("Representation:")
    print(repr(expr))
    print("Variables:")
    print(expr.variables())
    print("Evaluation:")
    print(expr.evaluate(env))
    same_expr = Multiply(
    Add(Variable("x"), Number(3)),
    Subtract(Variable("y"), Number(2))
    )
    print("Structurally equal:")
    print(expr == same_expr)
    x = Variable("x")
    expr = -(x + 3)
    print(expr.evaluate({"x": 10})) # -13
    expr = Let(
        "x",
        Number(5),
        Add(Variable("x"), Number(3))
        )
    env = {"x": 100}
    print(expr.evaluate(env)) # 8
    print(env["x"]) # 100
    expr = Let("x", Add(Number(2), Number(3)), Multiply(Add(Variable("x"), 
            Number(1)), Subtract(Variable("y"), Number(2))))
    env = {"x": 100, "y": 7}
           
    print(expr)
    print(expr.evaluate(env))
    print(env["x"])
    print(expr.variables())

    x = Variable("x")
    print((x + 0).simplify()) # x
    print((0 + x).simplify()) # x
    print((x - 0).simplify()) # x
    print()
    print((0*expr).simplify()) # x
    print((x * 1).simplify()) # x
    print((x * 1).simplify()) # x
    print((1 * x).simplify()) # x
    print((x * 0).simplify()) # 0
    print((0 * x).simplify()) # 0
    print((x / 1).simplify()) # x
    print((0/x).simplify()) # 1
    print(-(x / 1).simplify()) # 1

if __name__ == "__main__":
    main()