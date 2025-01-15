# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 20:14:52 2024

@author: nelly
"""

import pandas as pd
import requests
import time
import os
from tqdm import tqdm


def query_pharmgkb(rsid):
    """Query PharmGKB for pharmacogenomic data of an SNP."""
    url = f"https://api.pharmgkb.org/v1/data/variant/{rsid}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def pharmacogenomics_analysis(input_dir, output_dir):
    """
    Perform pharmacogenomic analysis on all annotated SNP files in a directory.
    
    Args:
        input_dir: Path to the directory containing annotated SNP files (CSV format).
        output_dir: Path to save the pharmacogenomics analysis results.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # List all CSV files in the input directory
    annotated_files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
    print(f"Found {len(annotated_files)} annotated files to process.")
    
    # Start timing the process
    overall_start_time = time.time()
    
    # Process each annotated file
    for file_index, annotated_file in enumerate(annotated_files, start=1):
        print(f"Processing file {file_index}/{len(annotated_files)}: {annotated_file}...")
        
        # Load the annotated SNP file
        input_file_path = os.path.join(input_dir, annotated_file)
        snps = pd.read_csv(input_file_path)
        results = []
        
        # Use tqdm for progress tracking in SNP processing
        for index, rsid in tqdm(enumerate(snps['Identifier'], start=1), total=len(snps), desc=f"Processing SNPs in {annotated_file}"):
            pharmgkb_data = query_pharmgkb(rsid)

            results.append({
                "RSID": rsid,
                "PharmGKB_Data": pharmgkb_data if pharmgkb_data else "No data"
            })
            
            # Add delay to avoid overloading the API
            time.sleep(0.1)

        # Save the results for the current file
        results_df = pd.DataFrame(results)
        output_file_path = os.path.join(output_dir, f"pharmacogenomics_{annotated_file}")
        results_df.to_csv(output_file_path, index=False)
        print(f"Results for {annotated_file} saved to {output_file_path}.")
    
    # Stop timing the process
    overall_end_time = time.time()
    total_elapsed_time = overall_end_time - overall_start_time
    print(f"All files processed. Total runtime: {total_elapsed_time:.2f} seconds ({total_elapsed_time / 60:.2f} minutes).")

# Example usage:
if __name__ == "__main__":
    input_dir = "C:/Users/nelly/Documents/Personligt/annotated_chromosomes"  # Replace with your input directory
    output_dir = "C:/Users/nelly/Documents/Personligt/pharmacogenomics_results"  # Directory for output files
    
    try:
        pharmacogenomics_analysis(input_dir, output_dir)
    except Exception as e:
        print(f"An error occurred: {e}")

