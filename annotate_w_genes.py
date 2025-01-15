# # -*- coding: utf-8 -*-
# """
# Created on Sat Dec 28 16:58:10 2024
# 
# @author: nelly
# """
# 
# import pandas as pd
# import requests
# import time
# 
# """def fetch_gene_from_ensembl(rsid):
#     #Fetch the associated gene for a given SNP using Ensembl REST API.
#     url = f"https://rest.ensembl.org/variation/homo_sapiens/{rsid}?content-type=application/json"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             # Extract gene name if available
#             if "mappings" in data:
#                 genes = [mapping.get("gene", "") for mapping in data["mappings"] if mapping.get("gene")]
#                 return genes[0] if genes else None
#         return None
#     except Exception as e:
#         print(f"Error fetching data for {rsid}: {e}")
#         return None
# """
# def fetch_gene_from_ensembl(rsid):
#     """Fetch the associated gene for a given SNP using Ensembl REST API."""
#     url = f"https://rest.ensembl.org/variation/homo_sapiens/{rsid}?content-type=application/json"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             print(f"API response for {rsid}: {data}")  # Add this line to inspect the response
#             if "mappings" in data:
#                 genes = [mapping.get("gene", "") for mapping in data["mappings"] if mapping.get("gene")]
#                 return genes[0] if genes else None
#         else:
#             print(f"Failed to fetch data for {rsid}: Status Code {response.status_code}")
#         return None
#     except Exception as e:
#         print(f"Error fetching data for {rsid}: {e}")
#         return None
# 
# def annotate_genes(input_file, output_file):
#     """Annotate the input file with gene names and save to a new CSV."""
#     # Load input file
#     snp_data = pd.read_csv(input_file)
#     
#     # Ensure the file contains an 'Identifier' column
#     if "Identifier" not in snp_data.columns:
#         raise ValueError("The input file must contain an 'Identifier' column.")
# 
#     # Add a new 'Gene' column
#     snp_data['Gene'] = None
#     for idx, rsid in enumerate(snp_data['Identifier']):
#         #print(snp_data['Identifier'])
#         gene = fetch_gene_from_ensembl(rsid)
#         snp_data.at[idx, 'Gene'] = gene
#         print(f"Processed {idx + 1}/{len(snp_data)}: {rsid} -> {gene}")
#         time.sleep(0.1)  # To avoid overloading the API
# 
#     # Save the annotated data
#     snp_data.to_csv(output_file, index=False)
#     print(f"Annotated file saved to {output_file}.")
# 
# # Example usage
# input_file = "C:/Users/nelly/Documents/Personligt/test_snps.csv"  # Replace with your file path
# output_file = "annotated_snps_test.csv"  # Replace with your desired output file path
# annotate_genes(input_file, output_file)

import pandas as pd
import requests
import time

def fetch_gene_from_ensembl(rsid):
    """Fetch the associated gene for a given SNP using Ensembl REST API."""
    url = f"https://rest.ensembl.org/variation/homo_sapiens/{rsid}?content-type=application/json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"API response for {rsid}: {data}")  # Debugging line
            # Check if 'mappings' exist in the data
            if "mappings" in data:
                # Look through mappings for 'gene' information
                for mapping in data["mappings"]:
                    gene_info = mapping.get("gene", {})
                    gene_name = gene_info.get("id", "No gene ID found")
                    gene_symbol = gene_info.get("symbol", "No gene symbol found")
                    if gene_name and gene_symbol:
                        return {"gene_name": gene_symbol, "gene_id": gene_name}
            return None
        else:
            print(f"Failed to fetch data for {rsid}. Status code: {response.status_code}")
        return None
    except Exception as e:
        print(f"Error fetching data for {rsid}: {e}")
        return None

def annotate_genes(input_file, output_file):
    """Annotate the input file with gene names and save to a new CSV."""
    # Load input file
    snp_data = pd.read_csv(input_file)
    
    # Ensure the file contains an 'Identifier' column
    if "Identifier" not in snp_data.columns:
        raise ValueError("The input file must contain an 'Identifier' column.")

    # Add a new 'Gene' column
    snp_data['Gene'] = None
    for idx, rsid in enumerate(snp_data['Identifier']):
        print(snp_data['Identifier'])
        gene_info = fetch_gene_from_ensembl(rsid)
        if gene_info:
            snp_data.at[idx, 'Gene'] = f"{gene_info['gene_name']} ({gene_info['gene_id']})"
        else:
            snp_data.at[idx, 'Gene'] = "Gene information not found"
        print(f"Processed {idx + 1}/{len(snp_data)}: {rsid} -> {snp_data.at[idx, 'Gene']}")
        time.sleep(0.1)  # To avoid overloading the API

    # Save the annotated data
    snp_data.to_csv(output_file, index=False)
    print(f"Annotated file saved to {output_file}.")

# Example usage
input_file = "C:/Users/nelly/Documents/Personligt/test_snps.csv"  # Replace with your file path
output_file = "annotated_snps_test.csv"  # Replace with your desired output file path
annotate_genes(input_file, output_file)

