# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 17:48:04 2024

@author: nelly
"""

import pandas as pd
import requests
import time

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
def annotate_snps(input_file, output_file):
    """
    Annotates SNPs in a CSV file using the Ensembl REST API.
    
    Parameters:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to save the annotated output CSV file.
    """
    # Load the SNP data
    print("Loading SNP data...")
    snp_data = pd.read_csv(input_file)

    # Ensure required columns are present
    required_columns = {"Identifier", "Chromosome", "Position", "Genotype"}
    if not required_columns.issubset(snp_data.columns):
        raise ValueError(f"Input file must contain columns: {required_columns}")

    # Annotate each SNP
    print("Annotating SNPs...")
    annotations = []
    for index, row in snp_data.iterrows():
        chromosome = str(row["Chromosome"])
        position = int(row["Position"])
        try:
            annotation = query_ensembl(chromosome, position)
        except Exception as e:
            annotation = f"Error: {e}"
        annotations.append(annotation)
        
        # Print progress every 10 SNPs
        if (index + 1) % 10 == 0:
            print(f"Annotated {index + 1}/{len(snp_data)} SNPs...")

        # Avoid overwhelming the API
        time.sleep(0.1)

    # Add annotations to the dataframe
    snp_data["Function"] = annotations

    # Save the annotated data
    print(f"Saving annotated data to {output_file}...")
    snp_data.to_csv(output_file, index=False)
    print("Annotation complete!")

# Run the script
if __name__ == "__main__":
    # Input and output file paths
    input_csv = "C:/Users/nelly/Documents/Personligt/cleaned_snp_file.csv"   # Replace with your input CSV file
    output_csv = "C:7Users/nelly/Documents/Personligt/annotated_snps.csv"  # Replace with your desired output file

    try:
        annotate_snps(input_csv, output_csv)
    except Exception as e:
        print(f"An error occurred: {e}")
