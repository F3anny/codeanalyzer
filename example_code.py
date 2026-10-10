"""
Example Python file for testing the CodeAnalyzer
"""

import os
import sys
from datetime import datetime

def process_data(data, filter_type="all", include_metadata=True):
    results = []
    for item in data:
        if filter_type == "all" or item.get("type") == filter_type:
            if include_metadata:
                item["processed_at"] = datetime.now().isoformat()
                item["processed_by"] = "codeanalyzer_example"
            results.append(item)
    return results

def complex_function(x, y, z, a, b, c):
    if x > 0:
        if y > 0:
            if z > 0:
                if a > 0:
                    if b > 0:
                        if c > 0:
                            return x + y + z + a + b + c
                        else:
                            return x + y + z + a + b
                    else:
                        return x + y + z + a
                else:
                    return x + y + z
            else:
                return x + y
        else:
            return x
    else:
        return 0

class DataProcessor:
    def __init__(self, config):
        self.config = config
        self.processed_count = 0
    
    def process(self, items):
        for item in items:
            self.processed_count += 1
            yield item
    
    def get_stats(self):
        return {"processed": self.processed_count}

# This is a very long line that exceeds 100 characters and should be flagged by our code analyzer tool
very_long_variable_name_that_makes_this_line_extremely_long = "This line is intentionally very long to test the line length checker"