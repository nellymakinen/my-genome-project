# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 17:56:42 2024

@author: nelly
"""

import pandas as pd

def load_and_clean_csv(input_file, output_file):
    """
    Load and clean the SNP CSV file by removing metadata and renaming columns, 
    then save the cleaned data to a new file.
    
    Parameters:
        input_file (str): Path to the input raw CSV file.
        output_file (str): Path to save the cleaned CSV file.
    """
    # Read the file, skipping metadata lines starting with #
    with open(input_file, "r") as f:
        lines = f.readlines()
    data_lines = [line for line in lines if not line.startswith("#")]

    # Save cleaned data to a temporary file or process in memory
    with open(output_file, "w") as f:
        f.writelines(data_lines)
    
    # Load the cleaned CSV into a DataFrame
    snp_data = pd.read_csv(output_file)

    # Rename columns to match the annotation script
    snp_data.rename(columns={
        "RSID": "Identifier",
        "CHROMOSOME": "Chromosome",
        "POSITION": "Position",
        "RESULT": "Genotype"
    }, inplace=True)
    
    # Convert Chromosome and Position to strings (handles mixed types)
    snp_data["Chromosome"] = snp_data["Chromosome"].astype(str)
    snp_data["Position"] = snp_data["Position"].astype(str)
    
    # Remove quotes from Chromosome and Position
    snp_data["Chromosome"] = snp_data["Chromosome"].str.replace('"', '')
    snp_data["Position"] = snp_data["Position"].str.replace('"', '').astype(int)
    
    # Save the cleaned data to a new file
    snp_data.to_csv(output_file, index=False)
    print(f"Cleaned file saved to: {output_file}")


# Example usage
if __name__ == "__main__":
    input_csv = "C:/Users/nelly/Documents/Personligt/rawdnadata.csv"  # Replace with your input file
    output_csv = "C:/Users/nelly/Documents/Personligt/cleaned_snp_file.csv"  # Replace with your desired output file
    load_and_clean_csv(input_csv, output_csv)
