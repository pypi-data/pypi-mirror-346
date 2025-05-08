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
