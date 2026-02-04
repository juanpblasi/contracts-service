"""
Report generation module
"""
import json
from datetime import datetime
from typing import Dict


class ReportGenerator:
    """Generate formatted reports from comparison results"""
    
    @staticmethod
    def generate_json_report(comparison_result: Dict, file1_name: str, file2_name: str) -> Dict:
        """
        Generate a comprehensive JSON report
        
        Args:
            comparison_result: Result from ContractComparator
            file1_name: Name of first file
            file2_name: Name of second file
            
        Returns:
            dict: Formatted report
        """
        report = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'file1': file1_name,
                'file2': file2_name,
                'report_version': '1.0'
            },
            'summary': {
                'total_fields': comparison_result['statistics']['total_fields'],
                'matches': comparison_result['statistics']['matches_count'],
                'differences': comparison_result['statistics']['differences_count'],
                'only_in_file1': comparison_result['statistics']['only_in_file1_count'],
                'only_in_file2': comparison_result['statistics']['only_in_file2_count'],
                'match_percentage': comparison_result['statistics']['match_percentage']
            },
            'details': {
                'matches': comparison_result['matches'],
                'differences': comparison_result['differences'],
                'only_in_file1': comparison_result['only_in_file1'],
                'only_in_file2': comparison_result['only_in_file2']
            }
        }
        
        return report
    
    @staticmethod
    def generate_html_report(comparison_result: Dict, file1_name: str, file2_name: str) -> str:
        """
        Generate an HTML report
        
        Args:
            comparison_result: Result from ContractComparator
            file1_name: Name of first file
            file2_name: Name of second file
            
        Returns:
            str: HTML report
        """
        stats = comparison_result['statistics']
        
        html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contract Comparison Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #003E7E 0%, #0066CC 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .summary {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .stat {{
            display: inline-block;
            margin: 10px 20px 10px 0;
            padding: 10px 20px;
            background: #f0f0f0;
            border-radius: 5px;
        }}
        .stat-label {{
            font-weight: bold;
            color: #003E7E;
        }}
        table {{
            width: 100%;
            background: white;
            border-collapse: collapse;
            margin-bottom: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background-color: #003E7E;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{
            background-color: #f9f9f9;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }}
        .badge-match {{
            background-color: #4CAF50;
            color: white;
        }}
        .badge-diff {{
            background-color: #FF9800;
            color: white;
        }}
        .badge-only {{
            background-color: #2196F3;
            color: white;
        }}
        h2 {{
            color: #003E7E;
            border-bottom: 2px solid #003E7E;
            padding-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Contract Comparison Report</h1>
        <p>Comparing: <strong>{file1_name}</strong> vs <strong>{file2_name}</strong></p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <div class="stat">
            <span class="stat-label">Total Fields:</span> {stats['total_fields']}
        </div>
        <div class="stat">
            <span class="stat-label">Matches:</span> {stats['matches_count']} 
            <span class="badge badge-match">✓</span>
        </div>
        <div class="stat">
            <span class="stat-label">Differences:</span> {stats['differences_count']} 
            <span class="badge badge-diff">!</span>
        </div>
        <div class="stat">
            <span class="stat-label">Only in File 1:</span> {stats['only_in_file1_count']}
            <span class="badge badge-only">1</span>
        </div>
        <div class="stat">
            <span class="stat-label">Only in File 2:</span> {stats['only_in_file2_count']}
            <span class="badge badge-only">2</span>
        </div>
        <div class="stat">
            <span class="stat-label">Match Percentage:</span> {stats['match_percentage']}%
        </div>
    </div>
"""
        
        # Differences table
        if comparison_result['differences']:
            html += """
    <h2>Differences Found</h2>
    <table>
        <thead>
            <tr>
                <th>Field</th>
                <th>File 1 Value</th>
                <th>File 2 Value</th>
            </tr>
        </thead>
        <tbody>
"""
            for diff in comparison_result['differences']:
                html += f"""
            <tr>
                <td><strong>{diff['field']}</strong></td>
                <td>{diff['file1_value']}</td>
                <td>{diff['file2_value']}</td>
            </tr>
"""
            html += """
        </tbody>
    </table>
"""
        
        # Fields only in file 1
        if comparison_result['only_in_file1']:
            html += """
    <h2>Fields Only in File 1</h2>
    <table>
        <thead>
            <tr>
                <th>Field</th>
                <th>Value</th>
            </tr>
        </thead>
        <tbody>
"""
            for item in comparison_result['only_in_file1']:
                html += f"""
            <tr>
                <td><strong>{item['field']}</strong></td>
                <td>{item['value']}</td>
            </tr>
"""
            html += """
        </tbody>
    </table>
"""
        
        # Fields only in file 2
        if comparison_result['only_in_file2']:
            html += """
    <h2>Fields Only in File 2</h2>
    <table>
        <thead>
            <tr>
                <th>Field</th>
                <th>Value</th>
            </tr>
        </thead>
        <tbody>
"""
            for item in comparison_result['only_in_file2']:
                html += f"""
            <tr>
                <td><strong>{item['field']}</strong></td>
                <td>{item['value']}</td>
            </tr>
"""
            html += """
        </tbody>
    </table>
"""
        
        html += """
</body>
</html>
"""
        return html
    
    @staticmethod
    def export_to_file(report: Dict, filepath: str, format: str = 'json'):
        """
        Export report to file
        
        Args:
            report: Report data
            filepath: Output file path
            format: Output format ('json' or 'html')
        """
        if format == 'json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
        elif format == 'html':
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
