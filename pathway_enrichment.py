# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 23:06:15 2024
GLÖM INTE CHROM 1 I PHARMA OXÅ
ALLA HÄR
@author: nelly
"""

import pandas as pd
from gprofiler import GProfiler
from tqdm import tqdm
import os
import time
from concurrent.futures import ProcessPoolExecutor

def perform_pathway_enrichment(genes, output_file):
    """
    Perform pathway enrichment analysis for a given list of genes.
    Args:
        genes (list): List of unique genes.
        output_file (str): Path to save the pathway enrichment results.
    """
    gp = GProfiler(return_dataframe=True)

    try:
        # Perform enrichment analysis
        enrichment_results = gp.profile(organism='hsapiens', query=genes)

        # Save results if there are any
        if not enrichment_results.empty:
            enrichment_results.to_csv(output_file, index=False)
            print(f"Pathway enrichment results saved to {output_file}.")
        else:
            print("No significant pathways found for genes in the current dataset.")
    except Exception as e:
        print(f"An error occurred during pathway enrichment: {e}")

def extract_genes_and_analyze(file_path, output_dir):
    """
    Extract genes from a file and perform pathway enrichment analysis.
    Args:
        file_path (str): Path to the SNP file.
        output_dir (str): Directory to save the enrichment results.
    """
    try:
        snp_data = pd.read_csv(file_path)

        if 'Gene' not in snp_data.columns:
            raise ValueError(f"The file {file_path} does not contain a 'Gene' column.")
        
        # Extract unique genes
        genes = snp_data['Gene'].dropna().unique()
        if len(genes) == 0:
            print(f"No genes found in {file_path}. Skipping analysis.")
            return

        # Define output file name
        output_file = os.path.join(output_dir, f"pathway_enrichment_{os.path.basename(file_path)}")

        print(f"Performing pathway enrichment for {len(genes)} genes from {file_path}...")
        perform_pathway_enrichment(genes, output_file)
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

def pathway_enrichment_parallel(input_dir, output_dir):
    """
    Perform pathway enrichment analysis on all files in parallel.
    Args:
        input_dir (str): Path to the directory containing SNP files.
        output_dir (str): Path to save the enrichment results.
    """
    os.makedirs(output_dir, exist_ok=True)

    # List all files in the input directory
    snp_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.csv')]
    print(f"Found {len(snp_files)} files for pathway enrichment analysis.")

    # Use parallel processing
    start_time = time.time()
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(extract_genes_and_analyze, file_path, output_dir)
            for file_path in snp_files
        ]

        # Use tqdm to track progress
        for _ in tqdm(futures, desc="Processing files"):
            pass

    elapsed_time = time.time() - start_time
    print(f"Pathway enrichment completed for all files in {elapsed_time:.2f} seconds ({elapsed_time / 60:.2f} minutes).")

# Example usage
if __name__ == "__main__":
    input_dir = "C:/Users/nelly/Documents/Personligt/annotated_chromosomes"  # Replace with input directory path
    output_dir = "C:/Users/nelly/Documents/Personligt/pathway_enrichment_results"  # Replace with output directory path
    
    pathway_enrichment_parallel(input_dir, output_dir)

