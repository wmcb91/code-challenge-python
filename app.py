from flask import Flask, escape, request, jsonify
import requests


app = Flask(__name__)

@app.route('/hello/')
def hello():
    name = request.args.get('name', 'World')
    return f'Hello, {escape(name)}!'


@app.route('/brandfolders/<brandfolder_slug>', methods=['GET'])
def list_sections(brandfolder_slug):
    api_key = request.headers.get('x-api-key', '')
    url = 'https://brandfolder.com/api/v4/brandfolders'
    headers = {'Authorization': f'Bearer {api_key}'}
    params = {'search': f'slug:"{brandfolder_slug}"', 'include': 'sections'}
    res = requests.get(url, headers=headers, params=params)
    return jsonify(res.json())
