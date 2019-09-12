from flask import Flask, escape, request, jsonify
import requests
import json

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

@app.route('/ingest', methods=['POST'])
def ingest_assets():
    """
    Accepts a POST request with a JSON body. Makes POST to Brandfolder assets

    TODO: Validate data
    """
    BRANDFOLDER_KEY='pxp6em-11q2fk-1t0s8z'
    BRANDFOLDER_IMAGES_KEY='pxp6em-11q2fk-6cq2mv'
    USER_KEY='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2tleSI6InB4cTdsaS1nNnBpbDQtNnBmZjR1Iiwic3VwZXJ1c2VyIjpmYWxzZX0.A_JyHhzmj4Bm64JeaIAoLOm1c81MnxsXO_UpzYRdGxU'
    
    url = 'https://brandfolder.com/api/v4/brandfolders/{}/assets'.format(BRANDFOLDER_KEY)
    body = {
        "data": request.json['data'],
        "section_key": request.json['section_key']
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(USER_KEY)
    }

    req = requests.post(url, data=json.dumps(body), headers=headers)
    try:
        return jsonify({ 'status': req.status_code, 'msg': req.json() })
    except:
        return jsonify({ 'status': req.status_code})


