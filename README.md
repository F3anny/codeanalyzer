# CodeAnalyzer 🔍

A Python package for analyzing code quality and complexity metrics. Perfect for developers, educators, and students who want to improve their code quality.

## Features

- **Cyclomatic Complexity Analysis** - Measure code complexity
- **Code Quality Issues Detection** - Find potential problems
- **Multiple Output Formats** - Text, JSON, and HTML reports
- **Directory Analysis** - Analyze entire projects
- **Command Line Interface** - Easy to use CLI tool
- **Function & Class Analysis** - Detailed breakdowns

## Installation

```bash
pip install codeanalyzer
```

## Quick Start

### Command Line Usage

```bash
# Analyze a single file
codeanalyzer myfile.py

# Analyze entire directory
codeanalyzer myproject/

# Generate HTML report
codeanalyzer myfile.py --format html --output report.html

# Generate JSON report
codeanalyzer myfile.py --format json
```

### Python API Usage

```python
from codeanalyzer import CodeAnalyzer, ReportGenerator

# Initialize analyzer
analyzer = CodeAnalyzer()

# Analyze a file
result = analyzer.analyze_file('myfile.py')
print(f"Complexity: {result['complexity']}")
print(f"Issues found: {len(result['issues'])}")

# Generate a report
reporter = ReportGenerator()
report = reporter.generate_text_report([result])
print(report)
```

## What it Analyzes

### Code Metrics
- Lines of code
- Number of functions and classes
- Cyclomatic complexity
- Function complexity
- Import analysis

### Code Issues
- Long lines (>100 characters)
- Missing docstrings
- High complexity functions
- Style violations

### Report Formats
- **Text**: Human-readable console output
- **JSON**: Machine-readable data format
- **HTML**: Beautiful web-based reports

## Example Output

```
==============================================================
CODE ANALYSIS REPORT
==============================================================
Generated on: 2024-01-15 14:30:25
Files analyzed: 1

📁 FILE: example.py
   Lines of code: 45
   Functions: 3
   Classes: 1
   Complexity: 8
   Issues found: 2
   🚨 ISSUES:
      Line 23: Function "process_data" missing docstring
      Line 31: Line too long (105 characters)

==============================================================
SUMMARY
==============================================================
Total lines of code: 45
Total functions: 3
Total classes: 1
Total issues: 2
```

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Author

Created with ❤️ for the Python community