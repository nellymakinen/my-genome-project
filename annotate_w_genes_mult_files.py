import os
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

# Main function to process a single CSV file
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
        print(f"Processing row {index}/{len(original_data)} in file {os.path.basename(input_file)}: rsID = {rsid}")

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

# Process all files in a directory
def process_directory(input_dir, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get list of all CSV files in the input directory
    input_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

    for input_file in input_files:
        input_path = os.path.join(input_dir, input_file)
        output_path = os.path.join(output_dir, f"updated_{input_file}")

        print(f"Processing file: {input_file}")
        extract_gene_data(input_path, output_path)

# Example usage
if __name__ == "__main__":
    input_directory = "C:/Users/nelly/Documents/Personligt/annotated_chromosomes"  # Replace with your input directory path
    output_directory = "C:/Users/nelly/Documents/Personligt/annotated_w_gene_name"  # Replace with your output directory path
    process_directory(input_directory, output_directory)
