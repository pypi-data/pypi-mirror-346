"""Utility functions for the mlfastflow package."""

def concat_files(folder_path, file_type='csv'):
    """Concatenate all files in a folder and its subfolders.
    
    Args:
        folder_path (str): Path to the folder containing files to concatenate
        file_type (str): File extension to look for ('csv' or 'parquet')
    
    Returns:
        str: Path to the concatenated output file
    """
    import os
    import polars as pl
    from pathlib import Path
    
    # Ensure proper path handling
    file_path = Path(folder_path)
    parent_dir = file_path.parent
    folder_name = file_path.name
    
    # Define output filename at the same level as input folder
    output_file = parent_dir / f"{folder_name}_combined.{file_type}"
    
    # Get all files with the specified extension in the folder and subfolders
    all_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(f".{file_type}"):
                all_files.append(os.path.join(root, file))
    
    if not all_files:
        print(f"No .{file_type} files found in {folder_path}")
        return None
    
    print(f"Found {len(all_files)} .{file_type} files to combine")
    
    # Read and concatenate all files
    dataframes = []
    for file in all_files:
        try:
            if file_type.lower() == 'csv':
                df = pl.read_csv(file)
            elif file_type.lower() == 'parquet':
                df = pl.read_parquet(file)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading file {file}: {str(e)}")
    
    if not dataframes:
        print("No valid dataframes to concatenate")
        return None
    
    # Concatenate all dataframes
    combined_df = pl.concat(dataframes)
    
    # Save the combined dataframe
    if file_type.lower() == 'csv':
        combined_df.write_csv(output_file)
    elif file_type.lower() == 'parquet':
        combined_df.write_parquet(output_file)
    
    print(f"Combined {len(dataframes)} files into {output_file}")
    return str(output_file)


def profile(
        df,
        title: str = "Pandas Profiling Report",
        output_path: str = None,
        minimal: int = 0,
    ):
    """Generate a pandas profiling report for a dataframe.
    
    Args:
        df: A polars or pandas DataFrame
        title: Title of the report
        output_path: Directory path where the HTML report will be saved.
            If None, uses current directory
        minimal: Controls the size and detail level of the report
            0: Minimal report (fastest, smallest file size)
            1: Basic report (some statistics, no plots)
            2: Intermediate report (basic visualizations)
            3: Full report (all features enabled)
        
    Returns:
        ProfileReport object
    """
    try:
        from pandas_profiling import ProfileReport
    except ImportError:
        try:
            from ydata_profiling import ProfileReport
        except ImportError:
            raise ImportError("Please install either pandas-profiling or ydata-profiling")
    
    # Import necessary modules and configure tqdm to avoid widget warnings
    import pandas as pd
    import numpy as np
    import warnings
    import tqdm
    import os
    
    # Suppress the TqdmWarning about IProgress not found
    warnings.filterwarnings("ignore", category=tqdm.TqdmWarning)
    
    # Disable the promotional banner about upgrading to ydata-sdk
    os.environ["YDATA_PROFILING_DISABLE_SPARK_BANNER"] = "1"
    os.environ["YDATA_PROFILING_DISABLE_PREMIUM_BANNER"] = "1"
    
    # Set tqdm to use the basic text-based progress bar instead of widgets
    tqdm.tqdm.monitor_interval = 0  # Disable the monitor thread
    
    # Convert to pandas DataFrame if necessary
    if hasattr(df, 'to_pandas'):
        # This is a polars DataFrame
        pandas_df = df.to_pandas()
    else:
        # Assume it's already a pandas DataFrame
        pandas_df = df
        
    # Preprocessing to handle problematic data that could cause KeyError
    if len(pandas_df) == 0:
        print("Warning: Empty DataFrame. Adding a dummy row to prevent profiling errors.")
        # Add a dummy row with non-null values
        pandas_df = pd.DataFrame([[1] * len(pandas_df.columns)], columns=pandas_df.columns)
    else:
        # Check each column for all-null values
        all_null_cols = [col for col in pandas_df.columns if pandas_df[col].isnull().all()]
        if all_null_cols:
            print(f"Warning: Found {len(all_null_cols)} column(s) with all null values.")
            print("These columns may cause errors in profiling: {}".format(', '.join(all_null_cols)))
            print("Replacing null values with placeholders to prevent errors.")
            
            # Replace null values with appropriate defaults based on column type
            for col in all_null_cols:
                dtype = pandas_df[col].dtype
                if pd.api.types.is_numeric_dtype(dtype):
                    pandas_df[col] = pandas_df[col].fillna(0)
                elif pd.api.types.is_datetime64_dtype(dtype):
                    pandas_df[col] = pandas_df[col].fillna(pd.Timestamp('2000-01-01'))
                else:
                    pandas_df[col] = pandas_df[col].fillna('unknown')
        
        # Check for columns with only one unique value (causes issues with percentiles)
        single_value_cols = [col for col in pandas_df.columns 
                          if pandas_df[col].nunique() == 1 and pd.api.types.is_numeric_dtype(pandas_df[col].dtype)]
        if single_value_cols:
            print(f"Warning: Found {len(single_value_cols)} numeric column(s) with only one unique value.")
            print("These columns may cause errors in profiling: {}".format(', '.join(single_value_cols)))
            print("Adding tiny variations to these columns to enable quantile calculations.")
            
            # Add tiny variations to enable quantile calculations
            for col in single_value_cols:
                base_value = pandas_df[col].iloc[0]
                # Add very small random variations that won't affect the analysis
                pandas_df[col] = base_value + np.random.normal(0, 0.0000001, size=len(pandas_df))
                
        # Explicitly ensure object columns with mixed types are properly handled
        for col in pandas_df.select_dtypes(include=['object']).columns:
            # If we have mixed numeric and string values, force to string
            if pandas_df[col].apply(lambda x: isinstance(x, (int, float))).any() and \
               pandas_df[col].apply(lambda x: isinstance(x, str)).any():
                pandas_df[col] = pandas_df[col].astype(str)
    
    # Create profiling report based on detail level
    if minimal == 0:
        # Level 0: Absolute minimal report (fastest, smallest file size)
        profile = ProfileReport(
            pandas_df,
            title=title,
            minimal=True,                     # Creates a minimal report
            explorative=False,                # Disable explorative analysis
            samples={},                      # Empty dict instead of None for samples
            missing_diagrams={},            # Empty dict instead of None for missing_diagrams
            duplicates={},                  # Empty dict instead of None for duplicates
            correlations={
                "pearson": {"calculate": False},
                "spearman": {"calculate": False},
                "kendall": {"calculate": False},
                "phi_k": {"calculate": False},
                "cramers": {"calculate": False},
            },
            interactions={},                # Empty dict instead of None for interactions
            plot={},                         # Empty dict instead of None for plot
            html={
                "style": {"full_width": True},
                "minify_html": True,         # Minify the HTML for smaller file size
                "use_local_assets": True,    # Use local assets to avoid CDN
                "inline": True               # Inline all assets for a single file
            },
            vars={
                "num": {"quantiles": [], "chi_squared_threshold": 0.999},  # Minimal numeric analysis
                "cat": {"length": False, "characters": False, "words": False, "cardinality_threshold": 0},
                "image": {"active": False},                                   # Disable image analysis
                "bool": {"active": True},                                     # Keep bool analysis (very lightweight)
                "path": {"active": False}                                     # Disable path variable analysis
            },
            n_obs_unique=1,                    # Only show the first unique value
            n_extreme_obs=1,                   # Only show the first extreme value
            n_freq_table_max=1,               # Only show the first frequency table value
            show_variable_description=False,   # Don't show variable descriptions
        )
    elif minimal == 1:
        # Level 1: Basic report with essential statistics, no plots
        profile = ProfileReport(
            pandas_df,
            title=title,
            minimal=True,                     # Creates a minimal report
            explorative=False,                # Disable explorative analysis
            samples={},                       # Empty dict instead of None
            missing_diagrams={"matrix": True},  # Only include missing matrix
            duplicates={"head": 3},           # Show only first 3 duplicate rows
            correlations={
                "pearson": {"calculate": True},  # Include basic correlation
                "spearman": {"calculate": False},
                "kendall": {"calculate": False},
                "phi_k": {"calculate": False},
                "cramers": {"calculate": False},
            },
            interactions={},                # Empty dict instead of None for interactions
            plot={
                "histogram": {"active": False},
                "correlation": {"active": False},
                "missing": {"active": False},
                "image": {"active": False}
            },
            html={
                "style": {"full_width": True},
                "minify_html": True,
            },
            vars={
                "num": {"quantiles": [0.25, 0.5, 0.75], "chi_squared_threshold": 0.95},
                "cat": {"length": False, "characters": False, "words": False},
                "image": {"active": False},
                "bool": {"active": True},
                "path": {"active": False}
            },
            n_obs_unique=5,                    # Show 5 unique values
            n_extreme_obs=3,                   # Show 3 extreme values
            n_freq_table_max=5,                # Show top 5 frequency values
        )
    elif minimal == 2:
        # Level 2: Intermediate report with basic visualizations
        profile = ProfileReport(
            pandas_df,
            title=title,
            minimal=True,                      # Still use minimal base
            explorative=False,                 # No explorative analysis
            samples={"head": 5, "tail": 5},    # Include sample rows
            missing_diagrams={"matrix": True, "bar": True},  # Include missing matrix and bar
            duplicates={"head": 5},            # Show first 5 duplicate rows
            correlations={
                "pearson": {"calculate": True},   # Include pearson correlation
                "spearman": {"calculate": True},  # Include spearman correlation
                "kendall": {"calculate": False},
                "phi_k": {"calculate": False},
                "cramers": {"calculate": False},
            },
            interactions={"continuous": True},   # Include continuous interactions
            plot={
                "histogram": {"active": True},    # Include histograms
                "correlation": {"active": True},  # Include correlation plot
                "missing": {"active": True},      # Include missing plot
                "image": {"active": False}       # No image plots
            },
            vars={
                "num": {"quantiles": [0.05, 0.25, 0.5, 0.75, 0.95]},
                "cat": {"length": True, "characters": False, "words": False},
                "image": {"active": False},
                "bool": {"active": True},
                "path": {"active": False}
            },
            n_obs_unique=10,  # Show 10 unique values
        )
    elif minimal == 3:
        # Level 3: Full detailed report (slowest, largest file size)
        # Instead of using all defaults, specify parameters to avoid NoneType errors
        profile = ProfileReport(
            pandas_df, 
            title=title,
            # Ensure these parameters are dictionaries, not None
            samples={"head": 10, "tail": 10},
            missing_diagrams={"matrix": True, "bar": True, "heatmap": True, "dendrogram": True},
            duplicates={"head": 10},
            interactions={"continuous": True, "discrete": True},
            correlations={
                "pearson": {"calculate": True},
                "spearman": {"calculate": True},
                "kendall": {"calculate": True},
                "phi_k": {"calculate": True},
                "cramers": {"calculate": True},
            },
            plot={
                "histogram": {"active": True},
                "correlation": {"active": True},
                "missing": {"active": True},
                "image": {"active": True}
            }
        )  # Full featured report
    
    try:
        # Create filename from title
        filename = title.replace(" ", "_") + ".html"
        
        # Determine full output path
        if output_path is not None:
            import os
            # Ensure output_path exists
            os.makedirs(output_path, exist_ok=True)
            # Combine directory path with filename
            full_path = os.path.join(output_path, filename)
        else:
            # Use current directory if no output_path provided
            full_path = filename
        
        try:
            # Save the report to the specified path
            profile.to_file(full_path)
            print(f"Profile report saved to {full_path}")
        except KeyError as e:
            print(f"Error saving profile report: {str(e)}")
            print("This often happens with empty dataframes or columns with all null values.")
            print("Try filtering your dataframe to include only non-null columns or check your data.")
            raise
        
        return profile
    except Exception as e:
        print(f"Unexpected error in profile generation: {str(e)}")
        print("If the error is related to missing quantiles (e.g., '75%'), check for empty columns or all-null values.")
        print("You might need to preprocess your dataframe to handle special cases before profiling.")
        raise