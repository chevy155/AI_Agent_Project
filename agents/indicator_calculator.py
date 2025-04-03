# agents/indicator_calculator.py
# Agent 2: Calculates technical indicators

import pandas as pd
import pandas_ta as ta # Import the pandas-ta library
import sys # Needed only if using the sys.path logic in test block below, technically optional here

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
        or the original DataFrame if calculation fails or input is invalid.
    """
    print("--- Running Agent 2: Technical Indicator Calculator ---")
    try:
        # --- Input Validation (Basic) ---
        if df is None or not isinstance(df, pd.DataFrame) or df.empty:
            print("Agent 2 Error: Invalid or empty DataFrame received.")
            return None # Return None on bad input
        if 'Close' not in df.columns:
            print("Agent 2 Error: DataFrame must contain a 'Close' column for SMA/RSI.")
            return None # Return None on bad input
        # Add checks for High/Low if explicitly needed by an indicator later
        # if 'High' not in df.columns or 'Low' not in df.columns:
        #   print("Warning: High/Low columns missing, needed for some indicators.")


        # --- Calculate Indicators using pandas_ta ---
        # The '.ta.' accessor applies indicators directly to the DataFrame.
        print("Agent 2: Calculating SMA...")
        df.ta.sma(length=5, append=True)  # Appends column named 'SMA_5'
        # Check if enough data for SMA 20 before calculating
        if len(df) >= 20:
            df.ta.sma(length=20, append=True) # Appends column named 'SMA_20'
        else:
            print("Agent 2 Warning: Insufficient data for SMA_20 calculation.")
            df['SMA_20'] = pd.NA # Add column with NAs if calculation skipped

        # Check if enough data for RSI 14 before calculating (needs length+1 technically for diff)
        print("Agent 2: Calculating RSI...")
        if len(df) >= 15:
            df.ta.rsi(length=14, append=True) # Appends column named 'RSI_14'
        else:
             print("Agent 2 Warning: Insufficient data for RSI_14 calculation.")
             df['RSI_14'] = pd.NA # Add column with NAs if calculation skipped


        # --- Potential Future Indicators ---
        # macd = df.ta.macd(fast=12, slow=26, signal=9, append=True)
        # if macd is None:
        #     print("Warning: Could not calculate MACD, possibly insufficient data.")

        print("Agent 2: Indicator calculation process finished.")

    except Exception as e:
        print(f"Agent 2: Error calculating indicators: {e}")
        return None # Return None on error

    return df

# --- Simple Test Block (For testing only this file's function) ---
if __name__ == '__main__':
    print("="*50)
    print("Running basic standalone test for indicator calculator...")
    print("="*50)
    # Create dummy data sufficient for calculations
    # Needs at least 20 rows for SMA_20, 15 for RSI_14
    data = {
        'Close': [100 + i + (i % 3 - 1) * 2 for i in range(25)] # Generate 25 data points
    }
    test_df = pd.DataFrame(data)

    # Add High/Low if needed by indicators being tested (using Close as approx)
    if 'High' not in test_df.columns: test_df['High'] = test_df['Close']
    if 'Low' not in test_df.columns: test_df['Low'] = test_df['Close']

    print("--- Input Dummy Data (Tail): ---")
    print(test_df.tail())

    # Call the function defined in *this* file
    df_with_indicators = calculate_technical_indicators(test_df.copy())

    if df_with_indicators is not None:
        print("\n--- Test DataFrame with Indicators (Tail): ---")
        print(df_with_indicators.tail())
        print("\n--- Columns Added: ---")
        print(df_with_indicators.columns.tolist())
    else:
        print("\nIndicator calculation failed during standalone test.")

    print("\nStandalone test finished.")
    print("="*50)