"""
Report generation module
"""

import json
from typing import List, Dict, Any
from datetime import datetime


class ReportGenerator:
    """Generate analysis reports in various formats"""
    
    def __init__(self):
        self.report_data = []
    
    def generate_text_report(self, analysis_results: List[Dict[str, Any]]) -> str:
        """Generate a human-readable text report"""
        report = []
        report.append("=" * 60)
        report.append("CODE ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Files analyzed: {len(analysis_results)}")
        report.append("")
        
        total_lines = 0
        total_functions = 0
        total_classes = 0
        total_issues = 0
        
        for result in analysis_results:
            if 'error' in result:
                report.append(f"❌ ERROR in {result['file_path']}: {result['error']}")
                continue
                
            total_lines += result.get('lines_of_code', 0)
            total_functions += len(result.get('functions', []))
            total_classes += len(result.get('classes', []))
            total_issues += len(result.get('issues', []))
            
            report.append(f"📁 FILE: {result['file_path']}")
            report.append(f"   Lines of code: {result['lines_of_code']}")
            report.append(f"   Functions: {len(result.get('functions', []))}")
            report.append(f"   Classes: {len(result.get('classes', []))}")
            report.append(f"   Complexity: {result.get('complexity', 0)}")
            report.append(f"   Issues found: {len(result.get('issues', []))}")
            
            # Show issues
            issues = result.get('issues', [])
            if issues:
                report.append("   🚨 ISSUES:")
                for issue in issues[:5]:  # Show first 5 issues
                    report.append(f"      Line {issue['line']}: {issue['message']}")
                if len(issues) > 5:
                    report.append(f"      ... and {len(issues) - 5} more issues")
            
            report.append("")
        
        # Summary
        report.append("=" * 60)
        report.append("SUMMARY")
        report.append("=" * 60)
        report.append(f"Total lines of code: {total_lines}")
        report.append(f"Total functions: {total_functions}")
        report.append(f"Total classes: {total_classes}")
        report.append(f"Total issues: {total_issues}")
        
        if total_issues > 0:
            report.append(f"Issues per 100 lines: {round((total_issues / total_lines) * 100, 2) if total_lines > 0 else 0}")
        
        return "\n".join(report)
    
    def generate_json_report(self, analysis_results: List[Dict[str, Any]]) -> str:
        """Generate a JSON report"""
        report_data = {
            "generated_on": datetime.now().isoformat(),
            "files_analyzed": len(analysis_results),
            "summary": self._generate_summary(analysis_results),
            "files": analysis_results
        }
        
        return json.dumps(report_data, indent=2)
    
    def generate_html_report(self, analysis_results: List[Dict[str, Any]]) -> str:
        """Generate an HTML report"""
        summary = self._generate_summary(analysis_results)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Code Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .summary {{ background-color: #e7f3ff; padding: 15px; margin: 20px 0; border-radius: 5px; }}
                .file {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
                .issue {{ background-color: #fff3cd; padding: 5px; margin: 5px 0; border-radius: 3px; }}
                .error {{ background-color: #f8d7da; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                .metric {{ display: inline-block; margin: 10px; padding: 10px; background-color: #f8f9fa; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔍 Code Analysis Report</h1>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Files analyzed: {len(analysis_results)}</p>
            </div>
            
            <div class="summary">
                <h2>📊 Summary</h2>
                <div class="metric">
                    <strong>Lines of Code:</strong> {summary['total_lines']}
                </div>
                <div class="metric">
                    <strong>Functions:</strong> {summary['total_functions']}
                </div>
                <div class="metric">
                    <strong>Classes:</strong> {summary['total_classes']}
                </div>
                <div class="metric">
                    <strong>Issues:</strong> {summary['total_issues']}
                </div>
            </div>
        """
        
        for result in analysis_results:
            if 'error' in result:
                html += f"""
                <div class="error">
                    <h3>❌ Error in {result['file_path']}</h3>
                    <p>{result['error']}</p>
                </div>
                """
                continue
            
            html += f"""
            <div class="file">
                <h3>📁 {result['file_path']}</h3>
                <p><strong>Lines:</strong> {result['lines_of_code']} | 
                   <strong>Functions:</strong> {len(result.get('functions', []))} | 
                   <strong>Classes:</strong> {len(result.get('classes', []))} | 
                   <strong>Complexity:</strong> {result.get('complexity', 0)}</p>
            """
            
            issues = result.get('issues', [])
            if issues:
                html += "<h4>🚨 Issues:</h4>"
                for issue in issues:
                    html += f"""
                    <div class="issue">
                        <strong>Line {issue['line']}:</strong> {issue['message']} 
                        <span style="color: #666;">({issue['type']})</span>
                    </div>
                    """
            
            html += "</div>"
        
        html += """
        </body>
        </html>
        """
        
        return html
    
    def _generate_summary(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, int]:
        """Generate summary statistics"""
        summary = {
            'total_lines': 0,
            'total_functions': 0,
            'total_classes': 0,
            'total_issues': 0,
            'files_with_errors': 0
        }
        
        for result in analysis_results:
            if 'error' in result:
                summary['files_with_errors'] += 1
                continue
                
            summary['total_lines'] += result.get('lines_of_code', 0)
            summary['total_functions'] += len(result.get('functions', []))
            summary['total_classes'] += len(result.get('classes', []))
            summary['total_issues'] += len(result.get('issues', []))
        
        return summary