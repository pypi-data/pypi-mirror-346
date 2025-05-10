"""Utility functions for the mlfastflow package."""

def concat_files(folder_path, file_type='csv', add_source_column=False):
    """Concatenate all files in a folder and its subfolders.
    
    Args:
        folder_path (str): Path to the folder containing files to concatenate
        file_type (str): File extension to look for ('csv' or 'parquet')
        add_source_column (bool): If True, adds a 'SOURCE' column with the filename
    
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
                
            # Add source column if requested
            if add_source_column:
                # Extract just the filename without path
                filename = os.path.basename(file)
                # Add the SOURCE column with the filename
                df = df.with_columns(pl.lit(filename).alias("SOURCE"))
                
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
        minimal: bool = True,
    ):
    """Generate a pandas profiling report for a dataframe.
    
    Args:
        df: A polars or pandas DataFrame
        title: Title of the report
        output_path: Directory path where the HTML report will be saved.
            If None, saves to current directory
        minimal: Whether to generate a minimal report (faster) or a complete report
        
    Returns:
        ProfileReport object
    """
    # Import ProfileReport from ydata-profiling
    try:
        from ydata_profiling import ProfileReport
    except ImportError:
        raise ImportError("Please install ydata-profiling: pip install ydata-profiling")
    
    # Import required modules
    import pandas as pd
    import os
    import warnings
    
    # Suppress irrelevant warnings
    warnings.filterwarnings("ignore", message=".*IProgress not found.*")
    
    # Disable promotional banners
    os.environ["YDATA_PROFILING_DISABLE_PREMIUM_BANNER"] = "1"
    
    # Convert to pandas DataFrame if necessary
    if hasattr(df, 'to_pandas'):
        # This is a polars DataFrame
        pandas_df = df.to_pandas()
    else:
        # Assume it's already a pandas DataFrame
        pandas_df = df
    
    # Check for empty DataFrame
    if len(pandas_df) == 0:
        print("Warning: Cannot profile an empty DataFrame")
        return None
    
    # Create the profiling report
    profile = ProfileReport(
        pandas_df,
        title=title,
        minimal=minimal,  # Simple toggle between minimal and complete report
    )
    
    # Create filename from title
    filename = title.replace(" ", "_") + ".html"
    
    # Determine full output path
    if output_path is not None:
        # Ensure output_path exists
        os.makedirs(output_path, exist_ok=True)
        # Combine directory path with filename
        full_path = os.path.join(output_path, filename)
    else:
        # Use current directory if no output_path provided
        full_path = filename
    
    # Try to save the report
    try:
        profile.to_file(full_path)
        print(f"Profile report saved to {full_path}")
    except Exception as e:
        print(f"Error saving profile report: {str(e)}")
        print("This may happen with problematic data. Try with different data or parameters.")
    
    # Create a non-displaying wrapper to prevent showing in Jupyter
    class NoDisplayProfileReport:
        def __init__(self, profile_report):
            self._profile = profile_report
            
        def to_file(self, *args, **kwargs):
            return self._profile.to_file(*args, **kwargs)
            
        # Block the _repr_html_ method that causes automatic display in Jupyter
        def _repr_html_(self):
            return None
            
        # Provide access to other methods of the original profile
        def __getattr__(self, name):
            return getattr(self._profile, name)
            
    return NoDisplayProfileReport(profile)