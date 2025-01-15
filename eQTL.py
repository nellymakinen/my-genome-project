# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 23:08:49 2024
Chromosome 19: Highly enriched in regulatory elements and eQTLs, 
particularly in genes influencing expression in the liver and immune system.
Chromosome 1 and 11: Also rich in eQTLs, especially for genes involved 
in metabolic pathways.
Focus on chromosomes with significant hits in expression-related 
tissues from studies like GTEx
@author: nelly
"""

import pandas as pd
import requests
import time

def query_gtex(rsid):
    url = f"https://gtexportal.org/rest/v1/variant/{rsid}/tissueSummary"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        return None

def eqtl_analysis(input_file, output_file):
    snp_data = pd.read_csv(input_file)
    results = []

    for rsid in snp_data['Identifier']:
        eqtl_data = query_gtex(rsid)
        results.append({
            "RSID": rsid,
            "eQTL_Data": eqtl_data if eqtl_data else "No data"
        })
        time.sleep(0.1)

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"eQTL analysis results saved to {output_file}")

# Example usage
eqtl_analysis("annotated_snps.csv", "eqtl_results.csv")
