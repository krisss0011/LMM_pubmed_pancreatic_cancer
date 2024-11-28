from Bio import Entrez
import os

def download_pubmed_abstracts(query, email, start_year, end_year, max_results_per_year=100, output_folder="text_data"):
    Entrez.email = email

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for year in range(start_year, end_year + 1):
        print(f"Fetching abstracts for the year {year}...")

        # Add year-specific filter to the query
        year_query = f"{query} AND {year}[dp]"

        # Search PubMed
        handle = Entrez.esearch(db="pubmed", term=year_query, retmax=max_results_per_year)
        record = Entrez.read(handle)
        handle.close()

        # Get PubMed IDs for the results
        id_list = record["IdList"]
        if not id_list:
            print(f"No papers found for the year {year}")
            continue

        for pubmed_id in id_list:
            try:
                # Fetch abstract
                abstract_handle = Entrez.efetch(db="pubmed", id=pubmed_id, rettype="abstract", retmode="text")
                abstract = abstract_handle.read()
                abstract_handle.close()

                # Save the abstract as a .txt file
                file_path = os.path.join(output_folder, f"{year}_PMID_{pubmed_id}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(abstract)

                print(f"Saved abstract for PMID {pubmed_id} to {file_path}")
            except Exception as e:
                print(f"Error fetching abstract for PMID {pubmed_id}: {e}")

    print(f"Abstracts saved to folder: {output_folder}")

# Example usage
if __name__ == "__main__":
    # Define the search parameters
    search_term = "pancreatic cancer AND (treatment OR immunotherapy OR biomarkers)"
    user_email = "kristijan1996@gmail.com"
    start_year = 2022
    end_year = 2024
    max_results_per_year = 100

    # Run the function
    download_pubmed_abstracts(
        query=search_term,
        email=user_email,
        start_year=start_year,
        end_year=end_year,
        max_results_per_year=max_results_per_year,
        output_folder="text_data"
    )
