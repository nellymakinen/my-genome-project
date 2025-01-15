# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 18:29:34 2024

@author: nelly
"""

import pandas as pd
import requests
import time
import os

# Define a function to query the Ensembl API for SNP annotations
def query_ensembl(chromosome, position):
    """
    Queries the Ensembl REST API for SNP functional annotation.
    
    Parameters:
        chromosome (str): Chromosome number (e.g., "1", "X").
        position (int): Base pair position of the SNP.
        
    Returns:
        str: Annotation result or error message.
    """
    url = f"https://rest.ensembl.org/overlap/region/human/{chromosome}:{position}-{position}?feature=variation"
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    
    if response.ok:
        data = response.json()
        # Extract relevant information
        annotations = []
        for item in data:
            annotations.append(item.get("consequence_type", "Unknown"))
        return "; ".join(set(annotations))  # Return unique annotations
    else:
        return f"Error: {response.status_code}"

# Main script
def annotate_chromosome(chromosome_data, chromosome, output_dir):
    """
    Annotates SNPs for a single chromosome and saves the result to a file.
    
    Parameters:
        chromosome_data (DataFrame): SNP data for the chromosome.
        chromosome (str): Chromosome number or identifier.
        output_dir (str): Directory to save the annotated output files.
    """
    print(f"Annotating SNPs for chromosome {chromosome}...")
    annotations = []

    for index, row in chromosome_data.iterrows():
        position = int(row["Position"])
        try:
            annotation = query_ensembl(chromosome, position)
        except Exception as e:
            annotation = f"Error: {e}"
        annotations.append(annotation)
        
        # Print progress every 10 SNPs
        if (index + 1) % 10 == 0:
            print(f"Chromosome {chromosome}: Annotated {index + 1}/{len(chromosome_data)} SNPs...")

        # Avoid overwhelming the API
        time.sleep(0.1)

    # Add annotations to the dataframe
    chromosome_data["Function"] = annotations

    # Save the annotated data
    output_file = os.path.join(output_dir, f"chromosome_{chromosome}_annotated.csv")
    chromosome_data.to_csv(output_file, index=False)
    print(f"Annotated data for chromosome {chromosome} saved to {output_file}")

def annotate_snps_by_chromosome(input_file, output_dir):
    """
    Annotates SNPs in a CSV file one chromosome at a time and saves separate files.
    
    Parameters:
        input_file (str): Path to the input CSV file.
        output_dir (str): Directory to save the annotated output files.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the SNP data
    print("Loading SNP data...")
    snp_data = pd.read_csv(input_file)

    # Ensure required columns are present
    required_columns = {"Identifier", "Chromosome", "Position", "Genotype"}
    if not required_columns.issubset(snp_data.columns):
        raise ValueError(f"Input file must contain columns: {required_columns}")

    # Process each chromosome separately
    chromosomes = snp_data["Chromosome"].unique()
    for chromosome in chromosomes:
        chromosome_data = snp_data[snp_data["Chromosome"] == chromosome]
        annotate_chromosome(chromosome_data, chromosome, output_dir)

    print("Annotation for all chromosomes complete!")

# Run the script
if __name__ == "__main__":
    # Input and output paths
    input_csv = "C:/Users/nelly/Documents/Personligt/cleaned_snp_file.csv"  # Replace with your input CSV file
    output_dir = "C:/Users/nelly/Documents/Personligt/annotated_chromosomes"  # Directory for output files

    try:
        annotate_snps_by_chromosome(input_csv, output_dir)
    except Exception as e:
        print(f"An error occurred: {e}")
