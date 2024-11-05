import requests
import json
import argparse
import csv
import os
from datetime import datetime

def search_hudson_rock(query_type, query):
    base_url = "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/"
    
    if query_type == "email":
        endpoint = f"search-by-email?email={query}"
    elif query_type == "username":
        endpoint = f"search-by-username?username={query}"
    else:
        print("Invalid query type. Please use '-email' or '-username'.")
        return None

    url = base_url + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def save_to_csv(data, query_type, query):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{query_type}_{query}_{timestamp}.csv"
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Query Type', 'Query', 'Result'])
        writer.writerow([query_type, query, json.dumps(data)])
    
    print(f"Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Search Hudson Rock API for email or username")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-email", help="Search by email")
    group.add_argument("-username", help="Search by username")
    parser.add_argument("-o", "--output", choices=['console', 'csv'], default='console', help="Output format (default: console)")
    
    args = parser.parse_args()

    if args.email:
        query_type = "email"
        query = args.email
    elif args.username:
        query_type = "username"
        query = args.username

    result = search_hudson_rock(query_type, query)
    
    if result:
        if args.output == 'console':
            print(json.dumps(result, indent=2))
        elif args.output == 'csv':
            save_to_csv(result, query_type, query)

if __name__ == "__main__":
    main()
