# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 23:11:05 2024
ALLA MEN EXTRA 6, 11, 16
@author: nelly
"""

import pandas as pd

def calculate_prs(input_file, output_file, weights_file):
    snp_data = pd.read_csv(input_file)
    weights = pd.read_csv(weights_file)  # SNP risk weights from GWAS studies
    prs = []

    for _, row in snp_data.iterrows():
        rsid = row['Identifier']
        genotype = row['Genotype']
        weight = weights[weights['RSID'] == rsid]['Weight'].values
        if weight.size > 0:
            score = sum([float(g) * weight[0] for g in genotype if g.isdigit()])
            prs.append(score)
        else:
            prs.append(0)

    snp_data['PRS'] = prs
    snp_data.to_csv(output_file, index=False)
    print(f"PRS calculation saved to {output_file}")

# Example usage
calculate_prs("annotated_snps.csv", "prs_results.csv", "weights.csv")
