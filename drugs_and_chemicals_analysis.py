import pandas as pd

# Step 1: Load SNP data
def load_snp_data(file_path):
    snps = pd.read_csv(file_path)
    return snps

# Step 2: Match SNPs to known interactions
def match_interactions(snps, drug_db, chemical_db):
    results = []

    for _, row in snps.iterrows():
        rs_id = row["Identifier"]
        gene_name = row["gene_name"]

        # Check drug interactions
        drug_matches = drug_db[drug_db["gene_name"] == gene_name]

        # Check chemical interactions
        chemical_matches = chemical_db[chemical_db["gene_name"] == gene_name]

        results.append({
            "rs_id": rs_id,
            "gene_name": gene_name,
            "function": row["Function"],
            "drug_interactions": drug_matches.to_dict(orient="records"),
            "chemical_interactions": chemical_matches.to_dict(orient="records")
        })

    return results

# Step 3: Generate a report
def generate_report(results, output_file):
    with open(output_file, "w") as f:
        f.write("rs_id,gene_name,function,drug_interactions,chemical_interactions\n")
        for result in results:
            f.write(f"{result['rs_id']},{result['gene_name']},{result['function']},"
                    f"{result['drug_interactions']},{result['chemical_interactions']}\n")

# Main function
def main():
    # Input SNP file and databases
    snp_file = "your_file.csv"  # Replace with your SNP file path
    drug_db_file = "drug_interactions.csv"  # Precompiled drug-gene interaction database
    chemical_db_file = "chemical_interactions.csv"  # Precompiled chemical-gene interaction database
    output_file = "analysis_report.csv"
    
    # Load SNP and interaction databases
    snps = load_snp_data(snp_file)
    drug_db = pd.read_csv(drug_db_file)
    chemical_db = pd.read_csv(chemical_db_file)

    # Match interactions
    results = match_interactions(snps, drug_db, chemical_db)

    # Generate report
    generate_report(results, output_file)
    print(f"Analysis report saved to {output_file}")

if __name__ == "__main__":
    main()
