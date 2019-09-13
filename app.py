from flask import Flask, escape, request, jsonify, render_template, redirect
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

@app.route('/ingest', methods=['GET'])
def ingest(msg=None, blob=''):
    return render_template('ingest.html', msg=msg, blob=blob)

@app.route('/ingest/success', methods=['GET'])
def ingest_success():
    print('It worked')
    return render_template('ingest.html', msg='Successfully Ingest Documents')

@app.route('/ingest', methods=['POST'])
def create_assets():
    """
    Accepts a POST request with a JSON body. Makes POST to Brandfolder assets

    TODO: Validate data
    """
    BRANDFOLDER_KEY='pxp6em-11q2fk-1t0s8z'
    BRANDFOLDER_IMAGES_KEY='pxp6em-11q2fk-6cq2mv'
    USER_KEY='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2tleSI6InB4cTdsaS1nNnBpbDQtNnBmZjR1Iiwic3VwZXJ1c2VyIjpmYWxzZX0.A_JyHhzmj4Bm64JeaIAoLOm1c81MnxsXO_UpzYRdGxU'
    
    url = 'https://brandfolder.com/api/v4/brandfolders/{}/assets'.format(BRANDFOLDER_KEY)

    try:
        data = request.json['ingest_data']
        is_json = True
    except:
        data = parse_txt(request.form['ingest_data'])
        is_json = False

    body = {
        'data': data,
        'section_key': BRANDFOLDER_IMAGES_KEY
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {USER_KEY}'
    }

    req = requests.post(url, data=json.dumps(body), headers=headers)
    if is_json:
        return jsonify({
            'status': req.status_code,
            'resp': req.json()
        })

    if req.status_code in [200, 201]:
        return redirect('/ingest/success')
    return redirect('/ingest')

def parse_txt(text):
    unorganized_assets = []
    asset_groups = {}
    splitlines = text.splitlines()
    for i, line in enumerate(splitlines):
        if 'Asset name:' in line:
            name = line.split(':')[1].strip()
            attachments = []
            for j in range(1,4):
                if i + j >= len(splitlines): 
                    break
                if 'attachment name:' in splitlines[i + j].lower():
                    try:
                        attachment_name = splitlines[i + j].split(':')[1].strip()
                    except:
                        attachment_name = ''
                if 'attachment url:' in splitlines[i + j].lower():
                    try:
                        attachment_url = splitlines[i + j].split(':')[1].strip()
                    except:
                        continue
                if 'tags:' in splitlines[i + j].lower():
                    try:
                        tags = splitlines[i + j].split(':')[1].strip().split(', ')
                        tags = [{ 'name': t } for t in tags]
                    except:
                        tags = []

            if name and attachment_url:
                unorganized_assets.append({
                    'name': name,
                    'tags': tags,
                    'attachments': [
                        {
                            'filename': attachment_name,
                            'url': attachment_url
                        }
                    ]
                })

    for unorg_asset in unorganized_assets:
        if unorg_asset['name'] in asset_groups:
            asset_groups[unorg_asset['name']]['attachments'].append(
                unorg_asset['attachments'][0]
            )
        else:
            asset_groups[unorg_asset['name']] = unorg_asset

    assets = [asset for asset in asset_groups.values()]
    return {
        'attributes': assets[:10] # Bad way of limiting to 10 before creating batching
    }
