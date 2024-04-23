import requests
import matplotlib.pyplot as plt
import csv
from typing import Dict, List
from search_terms import SEARCH_TERMS

API_KEY = 'cb3d274f6b959c9b9dfeccf09729d66c'

yearRange = range(2005, 2023)

def get_publication_count(term: str, year: int = None) -> int:
    """
    Function to retrieve the number of publications for a given term in a specific year.

    Args:
        term (str): The search term.
        year (int): The publication year.

    Returns:
        int: The number of publications.
    """
    url: str = 'https://api.elsevier.com/content/search/scopus'
    headers: Dict[str, str] = {'X-ELS-APIKey': API_KEY}
    params: Dict[str, Union[str, int]] = {
        'count': '1'  # We only need to check if there are any results
    }

    if year is None:
        params['query'] = f'ALL("{term}")'
    else:
        params['query'] = f'ALL("{term}") AND PUBYEAR = {year}'

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        data: Dict[str, str] = response.json()
        total_results: int = int(data['search-results']['opensearch:totalResults'])
        print(f"Number of results for '{term}' in {year}: {total_results}")
        return total_results
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data for '{term}' in {year}: {e}")
        return None

def load_cached_data() -> Dict[str, Dict[int, int]]:
    """
    Function to load cached data from CSV file.

    Returns:
        Dict[str, Dict[int, int]]: Dictionary containing cached publication counts.
    """
    publication_counts: Dict[str, Dict[(str|int), int]] = {}
    try:
        with open('publication_counts.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                term = row['Term']
                publication_counts[term] = {}
                publication_counts[term]['Total'] = int(row['Total'])
                for column, count in row.items():
                    if column not in ('Term', 'Total') and count not in ('', None):
                        year = int(column)
                        publication_counts[term][year] = int(count) 
    except FileNotFoundError:
        pass
    return publication_counts

def save_cache(publication_counts: Dict[str, Dict[int, int]]) -> None:
    """
    Function to save the publication counts cache to a CSV file.

    Args:
        publication_counts (Dict[str, Dict[int, int]]): Dictionary containing publication counts.
    """
    sortedItems = sorted(publication_counts.items(), key=lambda item: item[1]["Total"], reverse= True)
    
    with open('publication_counts.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Term'] + ["Total"] + [*yearRange])  # Write header
        for item in sortedItems:
            term = item[0]
            row = [term] + [publication_counts[term]["Total"]] + [publication_counts[term][year] for year in yearRange if year in publication_counts[term]]
            writer.writerow(row)

def main() -> None:
    """
    Main function to fetch publication counts for each term and plot the trend.
    """
    publication_counts: Dict[str, Dict[int, int]] = load_cached_data()

    for term in SEARCH_TERMS:
        if term not in publication_counts or "Total" not in publication_counts[term]:
            total_publication_count = get_publication_count(term)
            publication_counts[term] = {"Total": total_publication_count}
            save_cache(publication_counts)

    for term in SEARCH_TERMS:
        for year in yearRange:
            if year not in publication_counts[term] or publication_counts[term][year] is None:
                if publication_counts[term]["Total"] > 35000 or publication_counts[term]["Total"] == 0:
                    publication_counts[term][year] = None
                    continue
                
                publication_counts[term][year] = get_publication_count(term, year)
                save_cache(publication_counts)

    plot_data = {}
    for term, counts in sorted(publication_counts.items(), key=lambda item: item[1]["Total"], reverse= True):
        if publication_counts[term]["Total"] > 35000 or publication_counts[term]["Total"] < 195:
            continue    
        for year in yearRange:
            if year == "Total":
                continue
            if term not in plot_data:
                plot_data[term] = {}                     
            plot_data[term][year] = publication_counts[term][year]

    plt.figure(figsize=(10, 16))
    for term, counts in plot_data.items():
        years = list(counts.keys())
        counts = list(counts.values())
        linestyle = '-' if list(plot_data.keys()).index(term) < 10 else ':'
        plt.plot(years, counts, label=f'{term}: {publication_counts[term]["Total"]}', linestyle=linestyle)

    plt.title('Number of Publications per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.legend(title='Search Terms Sorted by Mentions in Publication')
    plt.grid(True)
    
    plt.savefig("publication_trend.pdf", bbox_inches="tight")

    plt.show()

if __name__ == "__main__":
    main()