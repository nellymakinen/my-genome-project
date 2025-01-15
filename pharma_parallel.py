# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 22:20:32 2024

@author: nelly
"""

import pandas as pd
import requests
import time
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


def query_pharmgkb(rsid):
    """Query PharmGKB for pharmacogenomic data of an SNP."""
    url = f"https://api.pharmgkb.org/v1/data/variant/{rsid}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def process_file(annotated_file, input_dir, output_dir, chromosomes_to_analyze):
    """
    Process a single annotated file for pharmacogenomic analysis.

    Args:
        annotated_file: Name of the file to process.
        input_dir: Directory containing annotated SNP files.
        output_dir: Directory to save results.
        chromosomes_to_analyze: List of chromosomes to include in the analysis.
    """
    print(f"Processing file: {annotated_file}...")

    # Load the annotated SNP file
    input_file_path = os.path.join(input_dir, annotated_file)
    snps = pd.read_csv(input_file_path)

    # Filter SNPs to only include specific chromosomes
    snps_filtered = snps[snps['Chromosome'].isin(chromosomes_to_analyze)]

    if snps_filtered.empty:
        print(f"No relevant SNPs from chromosomes {chromosomes_to_analyze} in {annotated_file}. Skipping...")
        return  # Skip this file if no relevant SNPs

    print(f"Found {len(snps_filtered)} SNPs from chromosomes {chromosomes_to_analyze} in {annotated_file}.")
    results = []

    # Use tqdm for progress tracking in SNP processing
    for index, rsid in tqdm(
        enumerate(snps_filtered['Identifier'], start=1),
        total=len(snps_filtered),
        desc=f"Processing SNPs in {annotated_file}"
    ):
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


def pharmacogenomics_analysis(input_dir, output_dir, chromosomes_to_analyze):
    """
    Perform pharmacogenomic analysis on SNP files using parallelization.

    Args:
        input_dir: Path to the directory containing annotated SNP files (CSV format).
        output_dir: Path to save the pharmacogenomics analysis results.
        chromosomes_to_analyze: List of chromosomes to include in the analysis.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # List all CSV files in the input directory
    annotated_files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
    print(f"Found {len(annotated_files)} annotated files to process.")

    # Start timing the process
    overall_start_time = time.time()

    # Use ThreadPoolExecutor for parallel file processing
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(process_file, annotated_file, input_dir, output_dir, chromosomes_to_analyze)
            for annotated_file in annotated_files
        ]

        # Wait for all futures to complete
        for future in tqdm(futures, desc="Processing files", total=len(futures)):
            future.result()

    # Stop timing the process
    overall_end_time = time.time()
    total_elapsed_time = overall_end_time - overall_start_time
    print(f"All files processed. Total runtime: {total_elapsed_time:.2f} seconds ({total_elapsed_time / 60:.2f} minutes).")


# Example usage:
if __name__ == "__main__":
    input_dir = "C:/Users/nelly/Documents/Personligt/annotated_chromosomes"  # Replace with your input directory
    output_dir = "C:/Users/nelly/Documents/Personligt/pharmacogenomics_results_1_6"  # Directory for output files
    chromosomes_to_analyze = [1, 6]  # Chromosomes to analyze

    try:
        pharmacogenomics_analysis(input_dir, output_dir, chromosomes_to_analyze)
    except Exception as e:
        print(f"An error occurred: {e}")
