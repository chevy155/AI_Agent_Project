# agents/pattern_identifier.py
# Agent 3: Analyzes data with indicators using an LLM and generates a report.

import pandas as pd
import yaml # For reading config file
import os

# LangChain components to interact with the LLM
# Ensure necessary langchain packages are installed (they should be from previous steps)
try:
    from langchain_community.chat_models import ChatOllama
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
except ImportError:
    print("ERROR: Required LangChain components not found. Make sure langchain, langchain-core, langchain-community are installed.")
    # Consider adding instructions to install if needed, although they should be present
    exit() # Exit if core components are missing
except Exception as e:
     print(f"An unexpected error occurred during LangChain import: {e}")
     exit()

# --- Agent 3 Core Function ---

def analyze_patterns_and_report(df_with_indicators: pd.DataFrame, config_path: str = "config.yaml") -> str:
    """
    Analyzes recent stock data with technical indicators using a local LLM
    to identify patterns and generate a summary report.

    Args:
        df_with_indicators: Pandas DataFrame containing stock data AND calculated indicators
                            (output from Agent 2).
        config_path: Path to the configuration file.

    Returns:
        A string containing the LLM-generated analysis report, or an error message.
    """
    print("--- Running Agent 3: Pattern Identifier & Reporter ---")
    try:
        # --- 1. Load Configuration ---
        print(f"Loading configuration from: {config_path}")
        if not os.path.exists(config_path):
            return f"ERROR: Config file not found at {config_path}"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Use a combined key or specific key based on your final agent structure choice
        agent_config = config.get('agents', {}).get('pattern_reporting_agent', {}) # Assuming combined agent
        llm_model_id = agent_config.get('llm_model_id', 'llama3.1:8b') # Default if not in config
        analysis_period = agent_config.get('analysis_period_days', 30) # Default 30 days
        # prompt_template_str = agent_config.get('prompt_template', "Default prompt...") # Option to load from config

        print(f"Using LLM: {llm_model_id}, Analyzing last {analysis_period} days.")

        # --- 2. Prepare Data for LLM ---
        if df_with_indicators is None or df_with_indicators.empty:
            return "ERROR: Received empty or invalid DataFrame for analysis."

        # Select recent data (ensure index is datetime for time-based selection)
        try:
             if isinstance(df_with_indicators.index, pd.DatetimeIndex):
                  recent_data = df_with_indicators.last(f'{analysis_period}D') # Use last N calendar days
             else:
                  # Fallback if index is not datetime (use tail)
                  print("Warning: DataFrame index is not DatetimeIndex, using tail() for recent data.")
                  recent_data = df_with_indicators.tail(analysis_period)
        except Exception as e:
             print(f"Warning: Could not select recent data based on days, using tail(). Error: {e}")
             recent_data = df_with_indicators.tail(analysis_period)


        if recent_data.empty:
            return f"ERROR: No data found within the last {analysis_period} days/rows."

        # Format relevant data as a string for the prompt (use markdown for readability)
        # Select key columns - adjust if indicator names differ from defaults ('SMA_5', 'SMA_20', 'RSI_14')
        relevant_columns = ['Close', 'SMA_5', 'SMA_20', 'RSI_14'] # Check these names match output of Agent 2
        cols_to_format = [col for col in relevant_columns if col in recent_data.columns]
        if not cols_to_format:
             return "ERROR: None of the relevant columns (Close, SMA_5, SMA_20, RSI_14) found in DataFrame."

        # Round data for cleaner prompt display
        data_string = recent_data[cols_to_format].round(2).to_markdown()
        print(f"Formatted data for LLM (first 100 chars): {data_string[:100]}...")


        # --- 3. Define Prompt Template ---
        # This is a starting point - requires prompt engineering for good results!
        prompt_template_str = """
        Role: You are a Technical Analysis Assistant specialized in stock chart patterns.
        Task: Analyze the provided recent stock data table below, which includes Closing Price,
              5-day Simple Moving Average (SMA_5), 20-day Simple Moving Average (SMA_20),
              and 14-day Relative Strength Index (RSI_14).
              Generate a concise analysis report focusing ONLY on the following technical signals based SOLELY on the provided data:
              1.  **SMA Crossover:** Identify the most recent crossover event between SMA_5 and SMA_20, if any. State whether it was a bullish (SMA_5 crossed above SMA_20) or bearish (SMA_5 crossed below SMA_20) signal and the approximate date. If no recent crossover, state that.
              2.  **RSI Level:** Describe the current RSI_14 level based on the last row. Is it indicating overbought (>70), oversold (<30), or neutral conditions? Mention if it recently crossed these thresholds.
              3.  **Price vs. SMAs:** Based on the last row, state whether the closing price is above or below SMA_5 and SMA_20.
              4.  **Overall Summary:** Provide a very brief (1-2 sentence) technical summary based *only* on the signals identified above. Do not give financial advice or predict future prices.

        Strictly adhere to analyzing only the provided data table and the requested signals.

        Recent Data Table (Markdown Format):
        {data_subset}

        Concise Analysis Report:
        """
        prompt = PromptTemplate(
            input_variables=["data_subset"],
            template=prompt_template_str,
        )

        # --- 4. Initialize LLM ---
        # Connect to local Llama 3.1 8B model via Ollama service
        print(f"Initializing ChatOllama with model: {llm_model_id}")
        llm = ChatOllama(model=llm_model_id)

        # --- 5. Create and Run LangChain Chain ---
        # Simple chain: Prompt -> LLM -> String Output
        chain = prompt | llm | StrOutputParser()

        print(f"Agent 3: Sending data (last {len(recent_data)} rows) to LLM for analysis...")
        report = chain.invoke({"data_subset": data_string})
        print("Agent 3: Report generated successfully.")

        return report.strip() # Return stripped report string

    except Exception as e:
        print(f"Agent 3: Error during analysis and reporting: {e}")
        # Consider more specific error handling/logging
        return f"ERROR: Failed to generate report due to an unexpected error: {e}"

# --- Test Block for running this script directly ---
# This imports and runs Agent 1, then Agent 2, then passes the result to Agent 3
if __name__ == '__main__':
    print("="*50)
    print("Running Full Pipeline Test: Agent 1 -> Agent 2 -> Agent 3")
    print("="*50)

    # --- Step 1: Run Agent 1 ---
    loaded_df = None
    try:
        # Assuming data_loader.py is correctly implemented and in the same 'agents' folder
        from agents.data_loader import load_and_prepare_data
        loaded_df = load_and_prepare_data() # Uses default config path
    except ImportError:
        print("ERROR: Could not import 'load_and_prepare_data'. Make sure data_loader.py exists in 'agents'.")
        exit()
    except Exception as e:
        print(f"ERROR during Agent 1 execution: {e}")
        loaded_df = None # Ensure it's None if Agent 1 fails

    # --- Step 2: Run Agent 2 ---
    df_with_indicators = None
    if loaded_df is not None and not loaded_df.empty:
        try:
            # Assuming indicator_calculator.py is correctly implemented and in the same 'agents' folder
            from agents.indicator_calculator import calculate_technical_indicators
            df_with_indicators = calculate_technical_indicators(loaded_df.copy())
        except ImportError:
             print("ERROR: Could not import 'calculate_technical_indicators'. Make sure indicator_calculator.py exists in 'agents'.")
             # If Agent 2 fails, df_with_indicators remains None
        except Exception as e:
            print(f"ERROR during Agent 2 execution: {e}")
            # If Agent 2 fails, df_with_indicators remains None

    # --- Step 3: Run Agent 3 ---
    # Check if df_with_indicators was successfully created by Agent 2
    if df_with_indicators is not None and not df_with_indicators.empty:
        # Check if necessary indicator columns exist before calling Agent 3
        required_indicator_cols = ['SMA_5', 'SMA_20', 'RSI_14']
        if all(col in df_with_indicators.columns for col in required_indicator_cols):
            final_report = analyze_patterns_and_report(df_with_indicators)
            print("\n--- Generated Report (Agent 3 Output) ---")
            print(final_report)
            print("--- End of Report ---")
        else:
             print("\nSkipping Agent 3 because required indicator columns (SMA_5, SMA_20, RSI_14) are missing from Agent 2's output.")
    elif loaded_df is None or loaded_df.empty:
         print("\nSkipping Agent 3 because Agent 1 failed.")
    else:
         print("\nSkipping Agent 3 because Agent 2 failed or did not produce indicators.")


    print("\nFull pipeline test finished.")
    print("="*50)