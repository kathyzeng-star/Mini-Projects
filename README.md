# MiniLang Expression Engine Project README

Project Overview
This project, MiniLang, is a small arithmetic expression language that builds an expression evaluator that represents expressions as objects, evaluates them in lexical environments, performs variable analysis and transformation using recursion, and processes collections of expressions. It covers the material from Chapters 1-4 of the CS 131 course. This project strictly uses the Python standard library, without utilising extended features from any third-party libraries. 

Project Details

Environment Preparation:
Only Python 3 need to be installed on your local system using an IDE of your choice. 
You can verify the installation using the command in the terminal: python --version

Project File Structure:
minilang_project/
- expressions.py
- transformations.py
- demo.py
- README.md

Startup and Execution:
git clone https://github.com/kathyzeng-star/Mini-Projects 
cd minilang_project

Run the demo.py file directly in the project root directory to execute all demonstration cases and assertions:
python demo.py

Core Design Description:
Class Inheritance Architecture
This project adopts an abstract base class-driven layered class structure, where all expressions inherit from the Expression class.
All expressions must implement:
- evaluate(self, env): Completes the evaluation of the expression in a given environment.
- variables(self): Returns the set of all free variables in the expression
- simplify(self): Performs safe simplification on the expression and returns a new expression object

The specific implementation is layered as follows:
- Leaf node classes: Number (numeric constant), Variable (variable reference)
- Binary Expression class: BinaryExpression encapsulates the common logic of the four binary operations: addition, subtraction, multiplication, and division. These subclasses define their corresponding operator symbols and rules.
- Unary negation class: Negate
- Lexical Binding Class: Let non-recursive lexical variable binding)

Behavior of Lexical Let Binding:
The Let statement Let(name, value_expr, body_expr) only follows standard lexical scoping rules:
1. First, evaluate value_expr in the passed original environment.
2. Create a shallow copy of the original environment, and add the new variable binding to this copied environment.
3. Evaluate body_expr in the newly created copied environment. This entire process never modifies the original environment that the caller passes to prevent unexpected environment mutations. The newly bound variables are only visible within the body section, and the value_expr in the definition part cannot access these new bindings to achieve the effect of variable shadowing.

Expression Simplification Rules:

First, all simplification operations will recursively simplify the child nodes, then apply safe simplification rules, and keep the execution behavior consistent throughout the process:
- Numeric constants and variables are returned by themselves
- When a negation operation acts on a numeric constant with the corresponding sign.
- When both operands of any binary operation are numeric constants, the corresponding result constant is calculated directly.
- For addition, expressions like x+0 and 0+x can be directly simplified to x; for subtraction, x-0 can be directly simplified to x.
- For multiplication, expressions like x1 and 1x can be directly simplified to x; for division, x/1 can be directly simplified to x.
- It is forbidden to directly simplify 0 * expr to 0. The execution process of expr must be retained to avoid intercepting possible exceptions thrown in expr.
- For Let bindings, only the value expression and the body expression are simplified respectively, and no internal substitution operation will be performed automatically.

Core Feature List:
Fully supports all required language forms: numeric values, variables, addition, subtraction, multiplication and division operations, unary negation and lexical Let bindings. 
Operator overloading: Supports it to construct expression trees through native Python operators, and automatically converts ordinary int/float values into Number nodes. 
Free variable analysis: It follows the lexical scoping rules to differentiate between bound variables and free variables.

Four recursive transformation functions:
- map_numbers(expr, function): Traverses all numeric nodes and applies the passed mapping function, while keeping the overall structure of the expression the same. 
- substitute(expr, name, replacement): It only replaces the free occurrences of variables and will not modify variables that are shadowed by the outer Let bindings.
- count_nodes(expr): Counts the total number of nodes in the entire expression tree.
- expression_depth(expr): Calculates the hierarchical depth of the expression tree; the depth of a leaf node is 1.

Exception Handling:
Throws TypeError for illegal construction of numeric nodes, ValueError/TypeError for invalid variable names, NameError for unbound variables, and allows the native Python
 ZeroDivisionError to automatically raise for the error.
 Batch expression processing: Supports unified statistics, transformation and safe evaluation operations on any set of expressions.

 
