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
        minimal: int = 0,
    ):
    """Generate a pandas profiling report for a dataframe.
    
    Args:
        df: A polars or pandas DataFrame
        title: Title of the report
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
    
    # Convert polars DataFrame to pandas if needed
    import pandas as pd
    if hasattr(df, 'to_pandas'):
        # This is a polars DataFrame
        pandas_df = df.to_pandas()
    else:
        # Assume it's already a pandas DataFrame
        pandas_df = df
    
    # Create profiling report based on detail level
    if minimal == 0:
        # Level 0: Absolute minimal report (fastest, smallest file size)
        profile = ProfileReport(
            pandas_df,
            title=title,
            minimal=True,                     # Creates a minimal report
            explorative=False,                # Disable explorative analysis
            samples=None,                     # Don't include sample data
            missing_diagrams=None,           # Disable ALL missing value diagrams
            duplicates=None,                 # Disable duplicate row detection
            correlations={
                "pearson": {"calculate": False},
                "spearman": {"calculate": False},
                "kendall": {"calculate": False},
                "phi_k": {"calculate": False},
                "cramers": {"calculate": False},
            },
            interactions=None,               # Disable computation of interactions
            plot=None,                       # Disable ALL plots completely
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
            samples=None,                     # Don't include sample data
            missing_diagrams={"matrix": True},  # Only include missing matrix
            duplicates={"head": 3},           # Show only first 3 duplicate rows
            correlations={
                "pearson": {"calculate": True},  # Include basic correlation
                "spearman": {"calculate": False},
                "kendall": {"calculate": False},
                "phi_k": {"calculate": False},
                "cramers": {"calculate": False},
            },
            interactions=None,                # Disable interactions
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
        profile = ProfileReport(pandas_df, title=title)  # All default settings
    
    # Save to file
    output_file = title.replace(" ", "_") + ".html"
    profile.to_file(output_file)
    print(f"Profile report saved to {output_file}")
    
    return profile