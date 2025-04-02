# main.py - Main entry point for the finance agents application

import sys
import os
import pandas as pd # Make sure pandas is imported if you handle the df here

# --- Ensure the 'agents' directory can be found ---
# Add project root to the Python path to help with imports
# This makes 'from agents.module import function' work reliably
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# --- End Path Setup ---

# --- Import functions from agent modules ---
try:
    from agents.data_loader import load_and_prepare_data
    from agents.indicator_calculator import calculate_technical_indicators
    # Import other agent functions here later as needed
    # from agents.pattern_identifier import identify_patterns
    # from agents.report_synthesizer import synthesize_report
    print("Successfully imported agent functions.")
except ImportError as e:
    print(f"ERROR: Failed to import agent functions: {e}")
    print("Check file paths, function names, and ensure __init__.py files exist in subdirectories.")
    sys.exit(1) # Exit if imports fail


# --- Main Execution Logic ---
if __name__ == '__main__':
    print("--- Running Main Agent Workflow ---")

    # Step 1: Load data using Agent 1
    print("\nInvoking Agent 1: Data Loader...")
    data_df = load_and_prepare_data() # Uses config.yaml by default

    # Step 2: Calculate indicators using Agent 2
    if data_df is not None:
        print("\nInvoking Agent 2: Indicator Calculator...")
        df_with_indicators = calculate_technical_indicators(data_df.copy()) # Use copy to avoid modifying original

        if df_with_indicators is not None:
            print("\n--- Main Script: DataFrame with Indicators (Tail) ---")
            print(df_with_indicators.tail())
            print("\nSuccessfully ran Agent 1 -> Agent 2 flow.")

            # Step 3: Future - Pass to Agent 3 (Pattern Identifier)
            # print("\nInvoking Agent 3: Pattern Identifier...")
            # patterns = identify_patterns(df_with_indicators)
            # ... etc ...

        else:
            print("\nAgent 2: Indicator calculation failed.")
    else:
        print("\nAgent 1: Data loading failed. Workflow stopped.")

    print("\n--- Main Agent Workflow Finished ---")