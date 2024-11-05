import requests
import json
import sys
import argparse

def search_hudson_rock(query_type, query):
    base_url = "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/"
    
    if query_type == "email":
        endpoint = f"search-by-email?email={query}"
    elif query_type == "username":
        endpoint = f"search-by-username?username={query}"
    else:
        print("Invalid query type. Please use '-email' or '-username'.")
        return

    url = base_url + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        print(json.dumps(data, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Search Hudson Rock API for email or username")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-email", help="Search by email")
    group.add_argument("-username", help="Search by username")
    
    args = parser.parse_args()

    if args.email:
        search_hudson_rock("email", args.email)
    elif args.username:
        search_hudson_rock("username", args.username)

if __name__ == "__main__":
    main()
