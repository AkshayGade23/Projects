
import requests
import pandas as pd
import csv
import os
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()
tmdb_api_key = os.getenv('TMDB_API_KEY')

YEARS = range(1950, 2025)
#CSV header based on OMDb movie data fields
CSV_HEADER = [
    'title', 'release_date', 'runtime', 'genres', 'director',
    'writer', 'actors', 'overview', 'language', 'country', 'awards', 'poster_path',
    'ratings', 'imdb_id', 'budget', 'revenue', 'production_companies', 'homepage'
]

#CSV header based on OMDb movie data fields
#directory for CSV files
os.makedirs('./data', exist_ok=True)


#list of movie IDs for a given year
def get_id_list(year, page=1):
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={tmdb_api_key}&primary_release_year={year}&page={page}'
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        raise_on_status=True
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    try:
        response = session.get(url, verify=False)
        response.raise_for_status()  # Will raise HTTPError for bad responses
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Connection error occurred: {conn_err}')
    except requests.exceptions.Timeout as timeout_err:
        print(f'Timeout error occurred: {timeout_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occurred: {req_err}')
    return []


#fetch movie data by ID
def get_data(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}'
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    response = requests.get(url)
    try:
        response = session.get(url, verify=False)
        response.raise_for_status()  # Will raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return response.json()

#movie data to a CSV file
def write_file(file_name, movie_dict):
    with open(file_name, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=movie_dict.keys())
        writer.writerow(movie_dict)

def extract_movie_data(movie_json):
    return {
        "title": movie_json.get("title"),
        "release_date": movie_json.get("release_date"),
        "runtime": movie_json.get("runtime"),
        "genres": ', '.join(genre['name'] for genre in movie_json.get("genres", [])),
        "director": "",  # Placeholder for director, fetch separately if needed
        "writer": "",  # Placeholder for writer, fetch separately if needed
        "actors": "",  # Placeholder for actors, fetch separately if needed
        "overview": movie_json.get("overview"),
        "language": movie_json.get("original_language"),
        "country": ', '.join(movie_json.get("origin_country", [])),
        "awards": "",  # Placeholder for awards, fetch separately if needed
        "poster_path": movie_json.get("poster_path"),
        "ratings": movie_json.get("vote_average"),
        "imdb_id": movie_json.get("imdb_id"),
        "budget": movie_json.get("budget"),
        "revenue": movie_json.get("revenue"),
        "production_companies": ', '.join(company['name'] for company in movie_json.get("production_companies", [])),
        "homepage": movie_json.get("homepage")
    }


for year in YEARS:
    print(f"Fetching data for the year: {year}")
    movie_list = []
    page = 1
    while True:
        ids = get_id_list(year, page)
        if not ids:
            break
        movie_list.extend(ids)
        page += 1

     # Extract unique movie IDs from movie_list
    unique_movie_ids = {movie['id'] for movie in movie_list}

    print(unique_movie_ids)

    # Creating file and writing header
    FILE_NAME = f'./data/{year}_movie_collection_data.csv'

    with open(FILE_NAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADER)
        writer.writeheader()

    # Iterate through the list of IDs to get data
    for movie_id in unique_movie_ids:
        movie_data_json = get_data(movie_id)
        if movie_data_json:
            movie_data = extract_movie_data(movie_data_json)
            write_file(FILE_NAME, movie_data)

    print(f"Data for the year {year} saved to {FILE_NAME}")

print("Data fetching and saving complete.")



