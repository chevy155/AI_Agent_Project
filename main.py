# main.py - Main entry point for the finance agents application

import sys
import os
import pandas as pd # Make sure pandas is imported if you handle the df here
import time         # Optional: for timing execution

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
    from agents.pattern_identifier import analyze_patterns_and_report # Added Agent 3 import
    print("Successfully imported agent functions.")
except ImportError as e:
    print(f"ERROR: Failed to import agent functions: {e}")
    print("Check file paths, function names, and ensure __init__.py files exist in subdirectories.")
    sys.exit(1) # Exit if imports fail
except Exception as e:
    print(f"An unexpected error occurred during import: {e}")
    sys.exit(1)

# --- Main Execution Logic ---
if __name__ == '__main__':
    start_time = time.time()
    print("="*50)
    print("Starting Finance Analysis Pipeline via main.py...")
    print("="*50)

    # Step 1: Load data using Agent 1
    print("\nInvoking Agent 1: Data Loader...")
    data_df = load_and_prepare_data() # Uses config.yaml by default

    # Step 2: Calculate indicators using Agent 2
    df_with_indicators = None # Initialize
    if data_df is not None and not data_df.empty:
        print("\nInvoking Agent 2: Indicator Calculator...")
        df_with_indicators = calculate_technical_indicators(data_df.copy()) # Use copy

        if df_with_indicators is not None and not df_with_indicators.empty:
            # Basic check if indicators were added (can be more robust)
            if 'SMA_5' not in df_with_indicators.columns or 'RSI_14' not in df_with_indicators.columns:
                 print("Pipeline Warning: Agent 2 might not have added expected indicator columns (SMA_5, RSI_14).")
                 # Decide whether to stop or continue
            else:
                 print("\n--- Agent 2 Output Check (DataFrame with Indicators - Tail) ---")
                 print(df_with_indicators.tail())
                 print("\nSuccessfully ran Agent 1 -> Agent 2 flow.")
        else:
            print("\nAgent 2: Indicator calculation failed or returned empty DataFrame.")
            # df_with_indicators remains None
    else:
        print("\nAgent 1: Data loading failed. Workflow stopped before Agent 2.")
        # df_with_indicators remains None

    # Step 3: Analyze and Report using Agent 3
    final_report = None # Initialize
    if df_with_indicators is not None and not df_with_indicators.empty:
        print("\nInvoking Agent 3: Pattern Identifier & Reporter...")
        # Pass the DataFrame *with indicators* from Agent 2 to Agent 3
        final_report = analyze_patterns_and_report(df_with_indicators) # Uses config.yaml by default

        if final_report is None or final_report.startswith("ERROR:"):
            print(f"\nAgent 3 failed or produced an error: {final_report}")
            # Report is None or contains error string
        else:
            print("\n--- Agent 3 Final Report: ---")
            print(final_report)
            print("-----------------------------")
            print("Successfully ran Agent 1 -> Agent 2 -> Agent 3 flow.")

    else:
        print("\nSkipping Agent 3 because previous steps failed or produced no data.")

    # --- Output Final Summary ---
    print("\n" + "="*50)
    print("Final Analysis Report Summary:")
    print(final_report if final_report and not final_report.startswith("ERROR:") else "No valid report generated.")
    print("="*50)
    end_time = time.time()
    print(f"Pipeline finished in {end_time - start_time:.2f} seconds.")
    print("==================================================")