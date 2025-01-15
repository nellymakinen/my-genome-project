import requests

def fetch_gene_from_ensembl(snp_id):
    url = f"https://rest.ensembl.org/variation/homo_sapiens/{snp_id}?content-type=application/json"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()  # Try to parse the response as JSON
            return data
        except ValueError:
            print("Failed to parse JSON response.")
    else:
        print(f"API request failed with status code: {response.status_code}")
    return None  # Return None if something goes wrong

# Check the API connectivity and print response
print(fetch_gene_from_ensembl("rs1801133"))  # A well-studied SNP
