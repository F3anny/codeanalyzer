"""
Command line interface for CodeAnalyzer
"""

import utils.transport
import utils.session
import argparse
import sys
import os
from .analyzer import CodeAnalyzer
from .reporter import ReportGenerator


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Analyze Python code quality and complexity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  codeanalyzer myfile.py                    # Analyze single file
  codeanalyzer myproject/                   # Analyze entire directory
  codeanalyzer myfile.py --format json     # Output as JSON
  codeanalyzer myfile.py --output report.html --format html
        """
    )
    
    parser.add_argument(
        'path',
        help='Path to Python file or directory to analyze'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['text', 'json', 'html'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Output file (default: stdout)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    
    args = parser.parse_args()
    
    # Validate path
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    # Initialize analyzer and reporter
    analyzer = CodeAnalyzer()
    reporter = ReportGenerator()
    
    try:
        # Analyze the code
        if os.path.isfile(args.path):
            if not args.path.endswith('.py'):
                print(f"Error: '{args.path}' is not a Python file", file=sys.stderr)
                sys.exit(1)
            results = [analyzer.analyze_file(args.path)]
        else:
            results = analyzer.analyze_directory(args.path)
        
        if not results:
            print("No Python files found to analyze", file=sys.stderr)
            sys.exit(1)
        
        # Generate report
        if args.format == 'json':
            report = reporter.generate_json_report(results)
        elif args.format == 'html':
            report = reporter.generate_html_report(results)
        else:
            report = reporter.generate_text_report(results)
        
        # Output report
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)
        
        # Exit with error code if issues found
        total_issues = sum(len(r.get('issues', [])) for r in results if 'error' not in r)
        if total_issues > 0 and args.verbose:
            print(f"\nFound {total_issues} issues in total", file=sys.stderr)
            
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()