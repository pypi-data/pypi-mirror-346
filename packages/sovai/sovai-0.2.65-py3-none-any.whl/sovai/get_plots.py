# Inside plot/get_plot.py

# --- Top Level Imports (Keep lightweight) ---
from typing import Optional, Union, Tuple, List, Dict
import importlib # Needed for dynamic imports
# Keep pandas/plotly config at top level as they modify global state
import pandas as pd
import plotly.io as pio

# --- Global Settings ---
# Changing the default plotting backend to Plotly
# Ensure pandas is imported before using pd.options
pd.options.plotting.backend = "plotly"
pd.set_option("display.max_columns", None)
# Setting the default theme for Plotly to a dark mode
pio.templates.default = "plotly_dark"


# --- Helper Functions (Potentially moved or kept if simple) ---

def enable_plotly_in_cell():
    # Lazy load IPython and plotly offline here
    try:
        import IPython
        from IPython.display import display, HTML
        from plotly.offline import init_notebook_mode

        display(
            HTML(
                """<script src="/static/components/requirejs/require.js"></script>"""
            )
        )
        init_notebook_mode(connected=False)
    except ImportError:
        print("Warning: IPython or plotly offline not available. Plotly may not render correctly in this environment.")


def _draw_graphs(data: Union[Dict, List[Dict]]):
    """Helper to draw graphs from database results (if structure is consistent)."""
    # Lazy load the actual plotting utility if needed
    from sovai.utils.plot import plotting_data
    # print(data)
    if isinstance(data, list):
        # Assuming structure [{key: plot_data}, {key: plot_data}, ...]
        for plot_dict in data:
             if isinstance(plot_dict, dict):
                  for _, val in plot_dict.items():
                      return plotting_data(val) # Plot first one found
    elif isinstance(data, dict):
        for _, val in data.items():
            return plotting_data(val) # Plot first one found
    else:
         print(f"Warning: _draw_graphs received unexpected data type: {type(data)}")
         return None


def generate_error_message(analysis_type, chart_type, source, verbose):
    """Generates error message, potentially displaying Markdown."""
    # Lazy load display/Markdown here
    try:
         from IPython.display import display, Markdown
         if source == "local":
             # Import sovai.data lazily IF NEEDED here, but it's better if plot() handles data fetching
             # For now, just format the message
             code_snippet = (
                 f"# Ensure sovai is imported, e.g., import sovai as sov\n"
                 f"dataset = sov.data('{analysis_type}/monthly') # Fetch data first\n"
                 f"if dataset is not None and not dataset.empty:\n"
                 f"    sov.plot('{analysis_type}', chart_type='{chart_type}', df=dataset)\n"
                 f"else:\n"
                 f"    print('Failed to fetch data.')"
             )
             message = (
                 f"**Input DataFrame `df` is empty or None.** Please provide a valid DataFrame.\n"
                 f"If you intended to fetch data first, you could use:\n\n"
                 f"```python\n{code_snippet}\n```"
             )
             if verbose:
                 display(Markdown(message))
             return "" # Return empty string as add_text no longer used this way
         else:
             display(Markdown("**An unknown error occurred.**"))
             return ""
    except ImportError:
         print("Warning: IPython.display not found. Cannot display formatted error message.")
         # Return simple text message
         if source == "local":
              return f"Input DataFrame `df` is empty or None. Please fetch data first (e.g., using sov.data(...))."
         else:
              return "An unknown error occurred."


# --- Plot Function Mapper ---
# Stores tuples: (relative_module_path_string, function_name_string)
# Use None for module_path if function is defined locally (like _draw_graphs)
# Use '.' for current directory if needed, but relative from package root is better
PLOT_FUNCTION_MAPPER = {
    # (dataset_name, chart_type, source, full_history_flag_or_None) : (module_path, function_name)
    ("breakout", "predictions", "local", True): (".plots.breakout.breakout_plots", "get_predict_breakout_plot_for_ticker"),
    ("breakout", "accuracy", "local", True): (".plots.breakout.breakout_plots", "interactive_plot_display_breakout_accuracy"),
    ("accounting", "balance", "local", False): (".plots.accounting.accounting_plots", "get_balance_sheet_tree_plot_for_ticker"),
    ("accounting", "cashflows", "local", True): (".plots.accounting.accounting_plots", "plot_cash_flows"),
    ("accounting", "assets", "local", True): (".plots.accounting.accounting_plots", "plot_assets"),
    ("ratios", "relative", "local", True): (".plots.ratios.ratios_plots", "plot_ratios_triple"),
    ("ratios", "benchmark", "local", True): (".plots.ratios.ratios_plots", "plot_ratios_benchmark"),
    ("institutional", "flows", "local", True): (".plots.institutional.institutional_plots", "institutional_flows_plot"),
    ("institutional", "prediction", "local", True): (".plots.institutional.institutional_plots", "institutional_flow_predictions_plot"),
    ("insider", "percentile", "local", True): (".plots.insider.insider_plots", "create_parallel_coordinates_plot_single_ticker"),
    ("insider", "flows", "local", True): (".plots.insider.insider_plots", "insider_flows_plot"),
    ("insider", "prediction", "local", True): (".plots.insider.insider_plots", "insider_flow_predictions_plot"),
    ("news", "sentiment", "local", True): (".plots.news.news_plots", "plot_above_sentiment_returns"),
    ("news", "strategy", "local", True): (".plots.news.news_plots", "plot_news_daily"),
    ("news", "analysis", "local", True): (".plots.news.news_plots", "run_dash_news_ts"),
    ("corprisk/risks", "line", "local", True): (".plots.corp_risk.corp_risk_plots", "plotting_corp_risk_line"),
    ("allocation", "line", "local", True): (".plots.allocation.allocation_plots", "create_line_plot_allocation"),
    ("allocation", "stacked", "local", True): (".plots.allocation.allocation_plots", "create_stacked_bar_plot_allocation"),
    ("earnings", "line", "local", True): (".plots.earnings_surprise.earnings_surprise_plots", "create_earnings_surprise_plot"),
    ("earnings", "tree", "local", True): (".plots.earnings_surprise.earnings_surprise_plots", "earnings_tree"),
    ("bankruptcy", "compare", "local", True): (".plots.bankruptcy.bankruptcy_plots", "plot_bankruptcy_monthly_line"),
    ("bankruptcy", "pca_clusters", "local", True): (".plots.bankruptcy.bankruptcy_plots", "plot_pca_clusters"),
    ("bankruptcy", "predictions", "local", True): (".plots.bankruptcy.bankruptcy_plots", "plot_ticker_widget"),

    # Database plots use the local _draw_graphs helper
    ("bankruptcy", "shapley", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "pca", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "line", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "similar", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "facet", "database"): (None, "_draw_graphs"),
    # ("bankruptcy", "shapley", "database"): (None, "_draw_graphs"), # Duplicate key
    ("bankruptcy", "stack", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "box", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "waterfall", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "pca_relation", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "line_relation", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "facet_relation", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "time_global", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "stack_global", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "box_global", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "waterfall_global", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "confusion_global", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "classification_global", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "precision_global", "database"): (None, "_draw_graphs"),
    ("bankruptcy", "lift_global", "database"): (None, "_draw_graphs"),
}


# --- Main Plot Function ---

def plot(
    dataset_name,
    chart_type=None,
    df=None,
    tickers: Optional[List[str]] = None,
    ticker: Optional[List[str]] = None, # Allow single ticker string too? Handled below.
    verbose=False,
    purge_cache=False,
    **kwargs,
):
    """
    Generates plots based on dataset name and chart type.
    Lazily loads required plotting modules.
    """
    # Lazy load data function from main package IF NEEDED
    # This assumes 'sovai.data' is accessible when plot is called
    from sovai import data as sovai_data

    # Handle single ticker string
    if isinstance(ticker, str):
        tickers = [ticker]
    elif isinstance(tickers, str):
        tickers = [tickers]

    # Enable plotly rendering in notebook cell if possible
    enable_plotly_in_cell()

    # --- Find the Plotting Function Info ---
    plot_info = None
    source = None
    full_history = None

    # Combine tickers/ticker for lookup consistency if needed
    lookup_tickers = tickers # Use the potentially updated list

    key_local_4 = (dataset_name, chart_type, "local", True)
    key_local_3 = (dataset_name, chart_type, "local", False) # Handle False case if exists
    key_db_3 = (dataset_name, chart_type, "database")

    if key_local_4 in PLOT_FUNCTION_MAPPER:
        source = "local"
        full_history = True
        plot_info = PLOT_FUNCTION_MAPPER[key_local_4]
    elif key_local_3 in PLOT_FUNCTION_MAPPER:
         source = "local"
         full_history = False
         plot_info = PLOT_FUNCTION_MAPPER[key_local_3]
    elif key_db_3 in PLOT_FUNCTION_MAPPER:
        source = "database"
        plot_info = PLOT_FUNCTION_MAPPER[key_db_3]
    else:
         # Try finding keys without the full_history flag for broader local matching if specific flag not found
         key_local_any_hist = (dataset_name, chart_type, "local")
         possible_keys = [k for k in PLOT_FUNCTION_MAPPER if k[:3] == key_local_any_hist]
         if possible_keys:
              # Default to first found if multiple match (e.g., True/False flag only difference)
              matched_key = possible_keys[0]
              source = "local"
              full_history = matched_key[3] # Get the flag from the key itself
              plot_info = PLOT_FUNCTION_MAPPER[matched_key]
         else:
              raise ValueError(f"Plotting function for dataset='{dataset_name}' with chart_type='{chart_type}' not found.")


    module_path, function_name = plot_info

    # --- Get the actual plotting function ---
    plot_function = None
    if module_path: # If it's one of the external plot modules
        try:
            # Dynamically import the module relative to the current package ('sovai.plot')
            # Assumes this file (get_plots.py) is inside a package named 'sovai.plot'
            imported_module = importlib.import_module(module_path, package=__package__)
            plot_function = getattr(imported_module, function_name)
        except ImportError as e:
            raise ImportError(f"Could not import plotting module '{module_path}' relative to {__package__}: {e}")
        except AttributeError:
            raise AttributeError(f"Function '{function_name}' not found in module '{module_path}'.")
    elif function_name == "_draw_graphs": # Handle local helper
        plot_function = _draw_graphs
    else:
         # Should not happen if mapper is correct
         raise ValueError(f"Invalid plot_info found in mapper: {plot_info}")


    # --- Execute based on source ---
    if source == "local":
        data_to_plot = df
        if df is None or df.empty: # Check if the DataFrame is None or empty
            error_msg_context = generate_error_message(dataset_name, chart_type, source, verbose)
            print(f"Warning: Input DataFrame 'df' is None or empty. Attempting to fetch data... {error_msg_context}")
            try:
                 # Use the lazy-loaded sovai_data function
                 data_to_plot = sovai_data(dataset_name, tickers=lookup_tickers, full_history=full_history)
                 if data_to_plot is None or data_to_plot.empty:
                       print(f"Failed to fetch data for {dataset_name}. Cannot generate plot.")
                       return None
            except Exception as e:
                 print(f"Error fetching data for {dataset_name}: {e}")
                 return None

        # Call the dynamically loaded plotting function
        try:
            # Pass tickers argument explicitly if the plot function might need it
            # Adjust based on specific plot function signatures if necessary
            if lookup_tickers is not None:
                 return plot_function(data_to_plot, tickers=lookup_tickers, **kwargs)
            else:
                 return plot_function(data_to_plot, **kwargs)
        except Exception as e:
            print(f"Error calling plot function '{function_name}' for local data: {e}")
            # Optionally re-raise or return None
            raise e


    elif source == "database":
        # Retrieve datasets from the data function
        # Assuming sovai_data handles the /charts endpoint correctly
        try:
            datasets = sovai_data(
                dataset_name + "/charts",
                chart=chart_type,
                tickers=lookup_tickers,
                purge_cache=purge_cache,
                **kwargs,
            )
        except Exception as e:
             print(f"Error fetching database chart data for {dataset_name}: {e}")
             return None


        if datasets is None:
            print(f"Failed to retrieve data for {dataset_name} with chart type {chart_type} and tickers {lookup_tickers}")
            return None

        # Call the plotting function (_draw_graphs or potentially others if mapper changes)
        try:
            if isinstance(datasets, list):
                 # Maybe plot only the first? Or return a list of figures?
                 # For now, plot the first non-empty result if _draw_graphs is used.
                 if plot_function == _draw_graphs:
                      for dataset in datasets:
                           if dataset is not None: # Check if dataset itself is None
                                fig = plot_function(dataset, **kwargs)
                                if fig: return fig # Return the first generated figure
                      return None # Return None if no figures generated
                 else:
                      # If another function handles lists, call it
                      # Or iterate and show? Needs clarification on desired behavior for lists.
                      print("Warning: Received a list of datasets for database source, plotting first.")
                      return plot_function(datasets[0], **kwargs) if datasets else None

            else:
                 # Handle the single dataset case
                 return plot_function(datasets, **kwargs)
        except Exception as e:
             print(f"Error calling plot function '{function_name}' for database data: {e}")
             # Optionally re-raise or return None
             raise e

    else:
        # This case should be prevented by the initial check
        raise ValueError(f"Source '{source}' derived from mapper is not recognized.")