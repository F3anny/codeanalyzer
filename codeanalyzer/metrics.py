"""
Code complexity metrics module
"""

import ast
from typing import Union


class ComplexityMetrics:
    """Calculate various code complexity metrics"""
    
    def calculate_cyclomatic_complexity(self, tree: ast.AST) -> int:
        """Calculate cyclomatic complexity for entire file"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, (ast.And, ast.Or)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
    
    def calculate_function_complexity(self, func_node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity for a specific function"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, (ast.And, ast.Or)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
            elif isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp)):
                complexity += 1
        
        return complexity
    
    def calculate_halstead_metrics(self, tree: ast.AST) -> dict:
        """Calculate Halstead complexity metrics"""
        operators = set()
        operands = set()
        operator_count = 0
        operand_count = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp):
                operators.add(type(node.op).__name__)
                operator_count += 1
            elif isinstance(node, ast.UnaryOp):
                operators.add(type(node.op).__name__)
                operator_count += 1
            elif isinstance(node, ast.Compare):
                for op in node.ops:
                    operators.add(type(op).__name__)
                    operator_count += 1
            elif isinstance(node, ast.Name):
                operands.add(node.id)
                operand_count += 1
            elif isinstance(node, (ast.Constant, ast.Num, ast.Str)):
                operands.add(str(node.value if hasattr(node, 'value') else node.n))
                operand_count += 1
        
        n1 = len(operators)  # Unique operators
        n2 = len(operands)   # Unique operands
        N1 = operator_count  # Total operators
        N2 = operand_count   # Total operands
        
        if n1 == 0 or n2 == 0:
            return {
                'vocabulary': 0,
                'length': 0,
                'difficulty': 0,
                'effort': 0
            }
        
        vocabulary = n1 + n2
        length = N1 + N2
        difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
        effort = difficulty * length
        
        return {
            'vocabulary': vocabulary,
            'length': length,
            'difficulty': round(difficulty, 2),
            'effort': round(effort, 2)
        }
    
    def calculate_maintainability_index(self, tree: ast.AST, lines_of_code: int) -> float:
        """Calculate maintainability index (simplified version)"""
        cyclomatic = self.calculate_cyclomatic_complexity(tree)
        halstead = self.calculate_halstead_metrics(tree)
        
        # Simplified maintainability index formula
        if lines_of_code == 0:
            return 100.0
        
        mi = 171 - 5.2 * (cyclomatic ** 0.23) - 0.23 * (cyclomatic) - 16.2 * (lines_of_code ** 0.5)
        
        # Normalize to 0-100 scale
        mi = max(0, min(100, mi))
        
        return round(mi, 2)