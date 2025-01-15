# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 23:06:56 2024
CHROM 6, 11, 17, x
@author: nelly
"""

import pandas as pd
import requests
import time

def query_gwas(rsid):
    url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rsid}"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        return None

def disease_associations(input_file, output_file):
    snp_data = pd.read_csv(input_file)
    results = []

    for rsid in snp_data['Identifier']:
        data = query_gwas(rsid)
        results.append({
            "RSID": rsid,
            "GWAS_Data": data if data else "No data"
        })
        time.sleep(0.1)  # Avoid overwhelming the API

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"Disease associations saved to {output_file}")

# Example usage
disease_associations("annotated_snps.csv", "disease_associations.csv")
