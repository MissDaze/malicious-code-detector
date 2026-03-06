#!/usr/bin/env python3
"""
Example: Safe, legitimate code
This demonstrates code that should NOT trigger alerts
"""

import json
import logging
from pathlib import Path

def process_data(input_file: str, output_file: str):
    """Safely process JSON data"""
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Read input file
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        # Process data
        processed = []
        for item in data:
            if isinstance(item, dict) and 'name' in item:
                processed.append({
                    'name': item['name'].upper(),
                    'processed': True
                })
        
        # Write output
        with open(output_file, 'w') as f:
            json.dump(processed, f, indent=2)
        
        logger.info(f"Processed {len(processed)} items")
        return True
    
    except FileNotFoundError:
        logger.error(f"File not found: {input_file}")
        return False
    except json.JSONDecodeError:
        logger.error("Invalid JSON format")
        return False

if __name__ == '__main__':
    process_data('input.json', 'output.json')
