"""
Main code analyzer module
"""

import ast
import os
from typing import Dict, List, Any
from .metrics import ComplexityMetrics


class CodeAnalyzer:
    """Main code analyzer class"""
    
    def __init__(self):
        self.metrics = ComplexityMetrics()
        
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            tree = ast.parse(source_code)
            
            analysis = {
                'file_path': file_path,
                'lines_of_code': len(source_code.splitlines()),
                'functions': self._analyze_functions(tree),
                'classes': self._analyze_classes(tree),
                'imports': self._analyze_imports(tree),
                'complexity': self.metrics.calculate_cyclomatic_complexity(tree),
                'issues': self._find_issues(tree, source_code)
            }
            
            return analysis
            
        except Exception as e:
            return {
                'file_path': file_path,
                'error': str(e)
            }
    
    def analyze_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """Analyze all Python files in a directory"""
        results = []
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    analysis = self.analyze_file(file_path)
                    results.append(analysis)
        
        return results
    
    def _analyze_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyze functions in the AST"""
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'line_number': node.lineno,
                    'args_count': len(node.args.args),
                    'has_docstring': ast.get_docstring(node) is not None,
                    'complexity': self.metrics.calculate_function_complexity(node)
                }
                functions.append(func_info)
        
        return functions
    
    def _analyze_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyze classes in the AST"""
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                class_info = {
                    'name': node.name,
                    'line_number': node.lineno,
                    'methods_count': len(methods),
                    'has_docstring': ast.get_docstring(node) is not None,
                }
                classes.append(class_info)
        
        return classes
    
    def _analyze_imports(self, tree: ast.AST) -> List[str]:
        """Analyze imports in the AST"""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")
        
        return imports
    
    def _find_issues(self, tree: ast.AST, source_code: str) -> List[Dict[str, str]]:
        """Find potential code issues"""
        issues = []
        lines = source_code.splitlines()
        
        # Check for long lines
        for i, line in enumerate(lines, 1):
            if len(line) > 100:
                issues.append({
                    'type': 'style',
                    'line': i,
                    'message': f'Line too long ({len(line)} characters)'
                })
        
        # Check for functions without docstrings
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    issues.append({
                        'type': 'documentation',
                        'line': node.lineno,
                        'message': f'Function "{node.name}" missing docstring'
                    })
        
        # Check for high complexity functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self.metrics.calculate_function_complexity(node)
                if complexity > 10:
                    issues.append({
                        'type': 'complexity',
                        'line': node.lineno,
                        'message': f'Function "{node.name}" has high complexity ({complexity})'
                    })
        
        return issues