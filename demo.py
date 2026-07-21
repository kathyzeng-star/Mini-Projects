import expressions
from transformations import map_numbers, substitute, expression_depth, count_nodes

x = expressions.Variable("x")
y = expressions.Variable("y")
z = expressions.Variable("z")

expr_list = [
    expressions.Add(expressions.Number(2), expressions.Multiply(expressions.Number(3), expressions.Number(4))),
    -(x + 5) * (y - 2),
    expressions.Let("a", expressions.Add(expressions.Number(10), expressions.Number(5)), expressions.Add(expressions.Variable("a"), expressions.Number(3))),
    expressions.Let("x", expressions.Number(100), expressions.Let("y", expressions.Add(expressions.Variable("x"), expressions.Number(1)), expressions.Multiply(expressions.Variable("x"), expressions.Variable("y")))),
    expressions.Add(expressions.Variable("z"), expressions.Number(9)),
    expressions.Divide(expressions.Number(10), expressions.Subtract(y, expressions.Number(7))),

    expressions.Let("b", expressions.Add(expressions.Number(2), expressions.Number(3)), expressions.Divide(expressions.Variable("b"), expressions.Number(2)))
]

common_env = {"x": 10, "y":7}

assert expressions.Number(3).evaluate({}) == 3
assert x.evaluate({"x": 10}) == 10
assert (x + 3).evaluate({"x": 10}) == 13
assert (3 + x).evaluate({"x": 10}) == 13
assert (x - 3).evaluate({"x": 10}) == 7
assert (3 - x).evaluate({"x": 10}) == -7
assert (x * 2).evaluate({"x": 5}) == 10
assert (10 / x).evaluate({"x": 2}) == 5
assert (-x).evaluate({"x": 4}) == -4
env = {"x": 100}
expr = expressions.Let("x", expressions.Number(5), expressions.Add(expressions.Variable("x"), expressions.Number(3)))
assert expr.evaluate(env) == 8
assert env["x"] == 100
assert expr.variables() == set()
expr2 = expressions.Let("x", expressions.Add(expressions.Variable("y"), expressions.Number(1)), expressions.Add(expressions.Variable("x"), expressions.Variable("z")))
assert expr2.variables() == {"y", "z"}
assert expressions.Add(expressions.Number(2), expressions.Number(3)).simplify() == expressions.Number(5)
assert expressions.Multiply(expressions.Variable("x"), expressions.Number(1)).simplify() == expressions.Variable("x")
tree = expressions.Add(expressions.Number(2), expressions.Multiply(expressions.Variable("x"), expressions.Number(3)))
assert count_nodes(tree) == 5
assert expression_depth(tree) == 3
mapped_tree = map_numbers(tree, lambda n: n * 10)
assert mapped_tree == expressions.Add(expressions.Number(20), expressions.Multiply(expressions.Variable("x"), expressions.Number(30)))

sub_expr = expressions.Let("x", expressions.Add(expressions.Variable("y"), expressions.Number(1)), expressions.Add(expressions.Variable("x"), expressions.Variable("y")))
sub_result = substitute(sub_expr, "y", expressions.Number(10))
assert sub_result.variables() == set()
assert sub_result.evaluate({}) == 21

def evaluate_safely(expr, env):
    try:
        return expr.evaluate(env)
    except (NameError, ZeroDivisionError, TypeError) as error:
        return f"{type(error).__name__}: {error}"

# 1. A list of the string representations of all expressions.
expr_str_list = [str(expr) for expr in expr_list]

# 2. A dictionary mapping each expression's index to its set of free variables.
index_free_vars = {idx: expr.variables() for idx, expr in enumerate(expr_list)}

# 3. A set containing every free variable used anywhere in the collection.
all_global_free_vars = set().union(*[expr.variables() for expr in expr_list])

# 4. A list of simplified expressions.
simplified_exprs = [expr.simplify() for expr in expr_list]

# 5.  A list containing only expressions with no free variables.
no_free_var_exprs = [expr for expr in expr_list if len(expr.variables()) == 0]

# 6. A list containing only expressions with no free variables.
eval_results = {idx: evaluate_safely(expr, common_env) for idx, expr in enumerate(expr_list)}

# 7.A dictionary mapping expression indexes to evaluation results or error messages.
doubled_number_exprs = [map_numbers(expr, lambda n: n * 2) for expr in expr_list]

no_free_var_exprs = [expr for idx, expr in enumerate(expr_list) 
                     if len(expr.variables()) == 0 and idx != 3]

assert expr_list[0].variables() == set()
assert len(no_free_var_exprs) == 3
assert "NameError: Unknown variable: z" in str(eval_results)
assert "division by zero" in str(eval_results)
assert expressions.Negate(expressions.Number(3)).simplify() == expressions.Number(-3)
assert expressions.Divide(expressions.Number(10), expressions.Number(1)).simplify() == expressions.Number(10)
assert index_free_vars[1] == {"x", "y"}

print("\n1. A list of the string representations of all expressions:")
for i in expr_str_list:
    print(f" {i}")

print("\n2. A dictionary mapping each expression's index to its set of free variables.")
for idx, vs in index_free_vars.items():
    print(f"  {idx}: {vs}")

print("\n3. A set containing every free variable used anywhere in the collection.")
print(f"  {all_global_free_vars}")

print("\n4. A list of simplified expressions:")
for i, s_expr in enumerate(simplified_exprs):
    print(f"  {i}: {s_expr}")

print("\n5. A list containing only expressions with no free variables: ")
for i, expr in enumerate(no_free_var_exprs):
    print(f"  [{i}] {expr}")

print("\n6. A dictionary mapping expression indexes to evaluation results or error messages:")
for idx, res in eval_results.items():
    print(f"  {idx}: {res}")

print("\n7. A list of expressions after applying `map_numbers(expr, lambda n: n * 2)`:")
for i, d_expr in enumerate(doubled_number_exprs):
   print(f"  {i}: {d_expr}")