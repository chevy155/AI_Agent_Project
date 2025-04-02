# agents/data_loader.py
import pandas as pd
import yaml
import os

def load_and_prepare_data(config_path="config.yaml"):
    """
    Loads NVIDIA stock data from the CSV specified in the config file,
    performs basic validation and type conversion, and returns a pandas DataFrame.
    """
    print("--- Running Agent 1: Data Loader & Preparer ---")
    try:
        # --- 1. Load Configuration ---
        print(f"Loading configuration from: {config_path}")
        if not os.path.exists(config_path):
            print(f"ERROR: Config file not found at {config_path}")
            return None
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Get data path from config, with a default fallback
        raw_data_path = config.get('data', {}).get('raw_data_path', 'data/raw/nvda_data.csv')
        print(f"Data path from config: {raw_data_path}")

        # --- 2. Load Data ---
        if not os.path.exists(raw_data_path):
            print(f"ERROR: Data file not found at {raw_data_path}")
            return None

        print(f"Attempting to load CSV data from: {raw_data_path}")
        df = pd.read_csv(raw_data_path)
        print(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns.")

        # --- 3. Basic Validation & Preparation ---
        print("Performing basic validation and preparation...")

        # Check for essential columns
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"ERROR: Missing required columns: {missing_cols}")
            print(f"Available columns: {df.columns.tolist()}")
            return None

        # Convert 'Date' column to datetime objects
        try:
            df['Date'] = pd.to_datetime(df['Date'])
        except Exception as e:
            print(f"ERROR: Could not convert 'Date' column to datetime: {e}")
            # Consider returning None or raising error depending on desired strictness
            return None

        # Ensure numeric types for price/volume columns
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        for col in numeric_cols:
            # 'coerce' turns non-numeric values into NaN (Not a Number)
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Optional: Report or handle NaNs introduced during coercion
        if df[numeric_cols].isnull().any().any():
            print("WARNING: Found missing or non-numeric values in price/volume columns.")
            # Strategy could be to drop rows: df.dropna(subset=numeric_cols, inplace=True)
            # Or fill with a value: df[numeric_cols] = df[numeric_cols].fillna(0) # Example: fill with 0
            # Or just report it for now.

        print("Data loaded and basic preparation complete.")
        # (Add more data quality checks here later based on requirements)

        return df

    except FileNotFoundError as e:
        print(f"ERROR: File not found during loading: {e}")
        return None
    except yaml.YAMLError as e:
        print(f"ERROR: Could not parse config file {config_path}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred in data loader: {e}")
        return None

# --- Example Usage ---
# This part allows you to run this script directly for testing
# It will only execute if you run `python agents/data_loader.py` from the root project folder
if __name__ == '__main__':
    # Ensure this path is correct when running from the root 'finance_agents' directory
    config_file_path = 'config.yaml'

    data_frame = load_and_prepare_data(config_path=config_file_path)

    if data_frame is not None:
        print("\n--- Data Sample (First 5 Rows) ---")
        print(data_frame.head())
        print("\n--- Data Info ---")
        data_frame.info()
    else:
        print("\nFailed to load data.")