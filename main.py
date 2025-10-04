# main.py - Main entry point for the AI Agent Project

import sys
import os
import time

# --- Ensure the 'agents' directory can be found ---
# Add project root to the Python path to help with imports
# This makes 'from agents.module import function' work reliably
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# --- End Path Setup ---

# --- Import functions from agent modules ---
try:
    from agents.weather_agent import get_weather_delmar
    print("Successfully imported weather agent function.")
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
    print("Starting Weather Agent for Del Mar, California...")
    print("="*50)

    # Get weather report for Del Mar, California
    print("\nInvoking Weather Agent...")
    weather_report = get_weather_delmar()

    # Display the weather report
    if weather_report and not weather_report.startswith("ERROR:"):
        print("\n--- Weather Report ---")
        print(weather_report)
        print("Successfully retrieved weather information.")
    else:
        print(f"\nWeather Agent failed or produced an error: {weather_report}")

    # --- Output Final Summary ---
    print("\n" + "="*50)
    print("Weather Report Summary:")
    print(weather_report if weather_report and not weather_report.startswith("ERROR:") else "No valid weather report generated.")
    print("="*50)
    end_time = time.time()
    print(f"Weather agent finished in {end_time - start_time:.2f} seconds.")
    print("==================================================")