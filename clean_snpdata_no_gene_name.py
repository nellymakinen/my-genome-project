import pandas as pd

# Load SNP file
def load_and_clean_snp_file(file_path, output_path):
    # Load data
    snps = pd.read_csv(file_path)

    # Filter out rows with missing gene names
    snps = snps[snps["gene_name"].notnull() & (snps["gene_name"] != "None")]

    # Keep only relevant functional annotations
    relevant_functions = [
        "missense_variant",
        "synonymous_variant",
        "5_prime_UTR_variant",
        "3_prime_UTR_variant",
        "regulatory_region_variant",
        "intron_variant",  # Include introns if they're relevant for splicing
    ]
    snps = snps[snps["Function"].isin(relevant_functions)]

    # Save the cleaned file
    snps.to_csv(output_path, index=False)
    print(f"Cleaned SNP file saved to {output_path}")

# Main function
def main():
    input_file = "your_file.csv"  # Replace with your SNP file path
    output_file = "cleaned_snps.csv"  # Name of the cleaned output file
    load_and_clean_snp_file(input_file, output_file)

if __name__ == "__main__":
    main()


