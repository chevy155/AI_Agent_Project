# agents/indicator_calculator.py
# Agent 2: Calculates technical indicators

import pandas as pd
import pandas_ta as ta # Import the pandas-ta library

# --- Agent 2 Core Function ---

def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates technical indicators (SMA5, SMA20, RSI14) using pandas_ta
    and adds them as new columns to the input DataFrame.

    Args:
        df: Pandas DataFrame containing stock data.
            Requires at least a 'Close' column. Assumes standard
            OHLCV columns might be present for other indicators if needed later.

    Returns:
        Pandas DataFrame with calculated indicator columns added,
        or the original DataFrame if calculation fails.
    """
    print("Agent 2: Calculating technical indicators...")
    try:
        # --- Input Validation (Basic) ---
        if not isinstance(df, pd.DataFrame):
            print("Error: Input is not a pandas DataFrame.")
            return df
        if 'Close' not in df.columns:
            print("Error: DataFrame must contain a 'Close' column for SMA/RSI.")
            return df
        # Add checks for High/Low if explicitly needed by an indicator later
        # if 'High' not in df.columns or 'Low' not in df.columns:
        #    print("Warning: High/Low columns missing, needed for some indicators.")


        # --- Calculate Indicators using pandas_ta ---
        # The '.ta.' accessor applies indicators directly to the DataFrame.

        # Simple Moving Averages (SMA)
        print("Calculating SMA...")
        df.ta.sma(length=5, append=True)  # Appends column named 'SMA_5'
        df.ta.sma(length=20, append=True) # Appends column named 'SMA_20'

        # Relative Strength Index (RSI)
        print("Calculating RSI...")
        df.ta.rsi(length=14, append=True) # Appends column named 'RSI_14'

        # --- Potential Future Indicators ---
        # macd = df.ta.macd(fast=12, slow=26, signal=9, append=True)
        # if macd is None:
        #     print("Warning: Could not calculate MACD, possibly insufficient data.")

        print("Agent 2: Indicators calculated successfully.")

    except Exception as e:
        print(f"Agent 2: Error calculating indicators: {e}")
        # Return original df or handle error appropriately

    return df

# --- Test Block for running this script directly ---
# This imports and runs Agent 1 first, then passes the result to Agent 2's function
if __name__ == '__main__':
    print("Running integrated test for Agent 1 -> Agent 2...")

    # --- Step 1: Import and run Agent 1's function ---
    loaded_df = None # Initialize to None
    try:
        # Import the function from the other agent file
        # This assumes data_loader.py is in the same 'agents' directory
        from agents.data_loader import load_and_prepare_data

        # Call Agent 1's function to get the real data
        # It should read config.yaml and load data/raw/nvda_data.csv
        loaded_df = load_and_prepare_data() # Uses default config path

    except ImportError:
        print("ERROR: Could not import 'load_and_prepare_data'. Make sure data_loader.py is in the 'agents' folder.")
    except FileNotFoundError:
        print("ERROR: config.yaml or the data file specified within it was not found.")
    except Exception as e:
        print(f"ERROR during data loading (Agent 1): {e}")


    # --- Step 2: Run Agent 2's function if data loaded successfully ---
    if loaded_df is not None and not loaded_df.empty:
        # Pass the loaded DataFrame (using .copy() is good practice to avoid modifying original)
        # to this script's calculate_technical_indicators function
        df_with_indicators = calculate_technical_indicators(loaded_df.copy())

        print("\n--- DataFrame with Indicators (Last 5 rows): ---")
        print(df_with_indicators.tail())
        print("\n--- Columns: ---")
        print(df_with_indicators.columns)
    else:
        print("\nSkipping indicator calculation because data loading failed or returned empty DataFrame.")

    print("\nIntegrated test finished.")