# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 23:09:54 2024
CHROMOSOMES 6, 19, 1
@author: nelly
"""

import pandas as pd
import requests
import time

def query_ldlink(rsid):
    url = f"https://ldlink.nci.nih.gov/?var={rsid}&pop=CEU"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        return None

def ld_analysis(input_file, output_file):
    snp_data = pd.read_csv(input_file)
    results = []

    for rsid in snp_data['Identifier']:
        ld_data = query_ldlink(rsid)
        results.append({
            "RSID": rsid,
            "LD_Data": ld_data if ld_data else "No data"
        })
        time.sleep(0.1)

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"LD analysis results saved to {output_file}")

# Example usage
ld_analysis("annotated_snps.csv", "ld_results.csv")
