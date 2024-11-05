from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def search_hudson_rock(query_type, query):
    base_url = "https://cavalier.hudsonrock.com/api/json/v2/osint-tools/"
    
    if query_type == "email":
        endpoint = f"search-by-email?email={query}"
    elif query_type == "username":
        endpoint = f"search-by-username?username={query}"
    else:
        return {"error": "Invalid query type. Please use 'email' or 'username'."}

    url = base_url + endpoint

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {str(e)}"}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query_type = request.form['query_type']
        query = request.form['query']
        result = search_hudson_rock(query_type, query)
        return render_template('index.html', result=result)
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.json
    query_type = data.get('query_type')
    query = data.get('query')
    result = search_hudson_rock(query_type, query)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)