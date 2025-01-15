# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 16:58:10 2024

@author: nelly
"""

import pandas as pd
import requests
import time
from multiprocessing import Pool
import numpy as np
#from multiprocessing import set_start_method
#import os

def fetch_gene_from_ensembl(rsid):
    """Fetch the associated gene for a given SNP using Ensembl REST API."""
    url = f"https://rest.ensembl.org/variation/homo_sapiens/{rsid}?content-type=application/json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Extract gene name if available
            if "mappings" in data:
                genes = [mapping.get("gene", "") for mapping in data["mappings"] if mapping.get("gene")]
                return genes[0] if genes else None
        return None
    except Exception as e:
        print(f"Error fetching data for {rsid}: {e}")
        return None

def process_chunk(chunk):
    """Process a chunk of SNP data."""
    chunk['Gene'] = chunk['Identifier'].apply(fetch_gene_from_ensembl)
    return chunk

def annotate_genes_parallel(input_files, output_dir):
    """Annotate multiple files with gene names using limited parallelism."""
    start_time = time.time()
    max_processes = 4  # Limit the number of parallel processes
    
    for input_file in input_files:
        output_file = f"{output_dir}/{input_file.split('/')[-1].replace('.csv', '_annotated.csv')}"
        
        # Load input file
        snp_data = pd.read_csv(input_file)
        
        # Ensure the file contains an 'Identifier' column
        if "Identifier" not in snp_data.columns:
            raise ValueError(f"The input file {input_file} must contain an 'Identifier' column.")
        
        # Split data into chunks for parallel processing
        num_chunks = min(max_processes, len(snp_data))
        chunks = np.array_split(snp_data, num_chunks)
        
        # Process in parallel
        with Pool(max_processes) as pool:
            results = pool.map(process_chunk, chunks)
        
        # Combine results and save
        annotated_data = pd.concat(results)
        annotated_data.to_csv(output_file, index=False)
        print(f"Annotated file saved to {output_file}")
    
    end_time = time.time()
    print(f"All files processed in {end_time - start_time:.2f} seconds.")


if __name__ == '__main__':
    # Example usage
    input_files = [
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_1_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_2_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_3_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_4_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_5_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_6_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_7_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_8_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_9_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_10_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_11_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_12_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_13_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_14_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_15_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_16_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_17_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_18_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_19_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_20_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_21_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_22_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_X_annotated.csv",
        "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_Y_annotated.csv",
    ]
    output_dir = "C:/Users/nelly/Documents/Personligt/annotated_chromosomes/output"
    annotate_genes_parallel(input_files, output_dir)


