# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 19:24:02 2024

@author: nelly
"""

import pandas as pd
import requests

def query_pharmgkb(rsid):
    """Query PharmGKB for pharmacogenomic data of an SNP."""
    url = f"https://api.pharmgkb.org/v1/data/variant/{rsid}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def pharmacogenomics_analysis(snp_file):
    """
    Perform pharmacogenomic analysis using PharmGKB.
    Args:
        snp_file: Path to the annotated SNP file (CSV format).
    """
    snps = pd.read_csv(snp_file)
    results = []

    for rsid in snps['Identifier']:
        pharmgkb_data = query_pharmgkb(rsid)

        results.append({
            "RSID": rsid,
            "PharmGKB_Data": pharmgkb_data if pharmgkb_data else "No data"
        })
    
    results_df = pd.DataFrame(results)
    results_df.to_csv("pharmacogenomics_results.csv", index=False)
    print("Pharmacogenomics results saved to 'pharmacogenomics_results.csv'.")

# Example usage:
pharmacogenomics_analysis("C:/Users/nelly/Documents/Personligt/annotated_chromosomes/chromosome_Y_annotated.csv")
