# 
# import requests
# import time
# 
# def fetch_snp_id_from_ncbi(rsid):
#     """Fetch SNP ID from NCBI dbSNP using E-utilities (esearch)."""
#     url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=snp&term={rsid}&retmode=json"
#     
#     try:
#         # Send the request to dbSNP
#         response = requests.get(url)
#         
#         if response.status_code == 200:
#             data = response.json()
#             print(f"Full response data for {rsid}: {data}")
#             
#             # Check for 'IdList' in the response to get the SNP ID(s)
#             if "esearchresult" in data and "idlist" in data["esearchresult"]:
#                 snp_id_list = data["esearchresult"]["idlist"]
#                 if snp_id_list:
#                     snp_id = snp_id_list[0]  # First SNP ID
#                     print(f"SNP ID for {rsid}: {snp_id}")
#                     return snp_id
#                 else:
#                     print("No SNP IDs found for the rsid.")
#             else:
#                 print("No 'idlist' found in the response.")
#         else:
#             print(f"Error: Received status code {response.status_code}")
#             print(f"Response Text: {response.text}")
#             return None
#             
#     except Exception as e:
#         print(f"Error fetching data for {rsid}: {e}")
#         return None
# 
# def fetch_snp_details_from_ncbi(snp_id):
#     """Fetch detailed SNP information from NCBI dbSNP using E-utilities (esummary)."""
#     url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=snp&id={snp_id}&retmode=json"
#     
#     try:
#         # Send the request to dbSNP using the SNP ID
#         response = requests.get(url)
#         
#         if response.status_code == 200:
#             data = response.json()
#             print(f"Full response data for SNP ID {snp_id}: {data}")
#             
#             genes = data['result'][snp_id]['genes']
#             #print(genes)
#             gene_info = []
#             for gene in data.get('genes', []):  # Only extracting genes part
#                 gene_info.append({
#                     'rsID': rsid,
#                     'gene_symbol': gene.get('name', 'N/A'),
#                     'gene_id': gene.get('gene_id', 'N/A')
#                 })
#                 return gene_info
#             else:
#                 print(f"No SNP details found for SNP ID {snp_id}.")
#                 return None, None
#         else:
#             print(f"Error: Received status code {response.status_code}")
#             print(f"Response Text: {response.text}")
#             return None, None
#             
#     except Exception as e:
#         print(f"Error fetching SNP details for {snp_id}: {e}")
#         return None, None
# 
# def fetch_gene_info_from_ncbi(rsid):
#     """Fetch gene information (name and symbol) for a given SNP using NCBI dbSNP API."""
#     # Step 1: Fetch SNP ID from dbSNP using the rsid
#     snp_id = fetch_snp_id_from_ncbi(rsid)
#     
#     if snp_id:
#         # Step 2: Fetch detailed SNP information using the SNP ID
#         gene_name, gene_symbol = fetch_snp_details_from_ncbi(snp_id)
#         return gene_name, gene_symbol
#     else:
#         print(f"Could not fetch SNP ID for {rsid}.")
#         return None, None
# 
# # Example usage
# if __name__ == "__main__":
#     # Test with an example rsid
#     rsid = "rs1801133"  # Replace with any rsID you want to test
#     gene_name, gene_symbol = fetch_gene_info_from_ncbi(rsid)
#     
#     if gene_name and gene_symbol:
#         print(f"Gene Name: {gene_name}")
#         print(f"Gene Symbol: {gene_symbol}")
#     else:
#         print(f"No gene information found for {rsid}.")
# 
# import csv
# import requests
# import time
# 
# # Function to fetch SNP ID from NCBI dbSNP
# def fetch_snp_id_from_ncbi(rsid):
#     url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=snp&term={rsid}&retmode=json"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             if "esearchresult" in data and "idlist" in data["esearchresult"]:
#                 snp_id_list = data["esearchresult"]["idlist"]
#                 return snp_id_list[0] if snp_id_list else None
#         return None
#     except Exception as e:
#         print(f"Error fetching SNP ID for {rsid}: {e}")
#         return None
# 
# # Function to fetch SNP details from NCBI dbSNP
# def fetch_snp_details_from_ncbi(snp_id):
#     url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=snp&id={snp_id}&retmode=json"
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             genes = data['result'].get(snp_id, {}).get('genes', [])
#             if genes:
#                 return genes[0].get('name', 'None'), genes[0].get('gene_id', 'None')
#         return "None", "None"
#     except Exception as e:
#         print(f"Error fetching SNP details for {snp_id}: {e}")
#         return "None", "None"
# 
# # Function to fetch gene info for an rsID
# def fetch_gene_info_from_ncbi(rsid):
#     snp_id = fetch_snp_id_from_ncbi(rsid)
#     if snp_id:
#         return fetch_snp_details_from_ncbi(snp_id)
#     return "None", "None"
# 
# # Main function to process the CSV file
# def extract_gene_data(input_file, output_file):
#     # Read the input CSV file
#     with open(input_file, mode='r') as infile:
#         reader = csv.DictReader(infile)
#         original_data = list(reader)
# 
#     # Prepare updated data
#     updated_data = []
#     for row in original_data:
#         rsid = row.get('Identifier')  # Assuming the rsID is in a column called 'Identifier'
# 
#         # Fetch gene details from NCBI
#         gene_name, gene_id = fetch_gene_info_from_ncbi(rsid)
# 
#         # Add name and gene_id to the row
#         row['gene_name'] = gene_name
#         row['gene_id'] = gene_id
# 
#         updated_data.append(row)
# 
#     # Write the updated data to a new CSV file
#     with open(output_file, mode='w', newline='') as outfile:
#         fieldnames = list(original_data[0].keys()) + ['gene_name', 'gene_id']
#         writer = csv.DictWriter(outfile, fieldnames=fieldnames)
# 
#         writer.writeheader()
#         writer.writerows(updated_data)
# 
#     print(f"Updated file saved as {output_file}")
# 
# # Example usage
# if __name__ == "__main__":
#     input_file = "C:/Users/nelly/Documents/Personligt/test_snps.csv"  # Replace with your input CSV file path
#     output_file = "C:/Users/nelly/Documents/Personligt/test_snps_results.csv"  # Replace with your desired output file path
#     extract_gene_data(input_file, output_file)

import csv
import requests
import time

# Function to fetch SNP ID from NCBI dbSNP
def fetch_snp_id_from_ncbi(rsid):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=snp&term={rsid}&retmode=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "esearchresult" in data and "idlist" in data["esearchresult"]:
                snp_id_list = data["esearchresult"]["idlist"]
                return snp_id_list[0] if snp_id_list else None
        print(f"Could not fetch SNP ID for {rsid}: No data found.")
        return None
    except Exception as e:
        print(f"Error fetching SNP ID for {rsid}: {e}")
        return None

# Function to fetch SNP details from NCBI dbSNP
def fetch_snp_details_from_ncbi(snp_id):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=snp&id={snp_id}&retmode=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            genes = data['result'].get(snp_id, {}).get('genes', [])
            if genes:
                return genes[0].get('name', 'None'), genes[0].get('gene_id', 'None')
        print(f"No gene details found for SNP ID {snp_id}.")
        return "None", "None"
    except Exception as e:
        print(f"Error fetching SNP details for SNP ID {snp_id}: {e}")
        return "None", "None"

# Function to fetch gene info for an rsID
def fetch_gene_info_from_ncbi(rsid):
    snp_id = fetch_snp_id_from_ncbi(rsid)
    if snp_id:
        return fetch_snp_details_from_ncbi(snp_id)
    return "None", "None"

# Main function to process the CSV file
def extract_gene_data(input_file, output_file):
    # Read the input CSV file
    with open(input_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        original_data = list(reader)

    # Check if 'gene_name' and 'gene_id' columns already exist
    existing_columns = reader.fieldnames
    new_columns = []
    if 'gene_name' not in existing_columns:
        new_columns.append('gene_name')
    if 'gene_id' not in existing_columns:
        new_columns.append('gene_id')

    # Prepare updated data
    updated_data = []
    for index, row in enumerate(original_data, start=1):
        rsid = row.get('Identifier')  # Assuming the rsID is in a column called 'Identifier'
        print(f"Processing row {index}/{len(original_data)}: rsID = {rsid}")

        # Fetch gene details from NCBI
        if rsid:
            gene_name, gene_id = fetch_gene_info_from_ncbi(rsid)
            print(f"  Gene Name: {gene_name}, Gene ID: {gene_id}")
        else:
            gene_name, gene_id = "None", "None"
            print(f"  Invalid or missing rsID. Skipping row {index}.")

        # Add name and gene_id to the row
        row['gene_name'] = gene_name
        row['gene_id'] = gene_id

        updated_data.append(row)

    # Write the updated data to a new CSV file
    with open(output_file, mode='w', newline='') as outfile:
        fieldnames = existing_columns + new_columns
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(updated_data)

    print(f"Updated file saved as {output_file}")

# Example usage
if __name__ == "__main__":
    input_file = "C:/Users/nelly/Documents/Personligt/test_snps.csv"  # Replace with your input CSV file path
    output_file = "C:/Users/nelly/Documents/Personligt/test_snps_results.csv"  # Replace with your desired output file path
    extract_gene_data(input_file, output_file)
