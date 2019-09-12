# Brandfolder Code Challenge - Python

## Objective
### Create a Flask API which takes input data about files and creates assets in Brandfolder.

## Requirements
- Write a Python script to `POST` the data from `input.txt` (in any format of your choice) to your Flask backend at `http://localhost:5000/ingest`
- This script should include information in the `POST` request to tell your application which Brandfolder and section(s) to create the assets in.
- Files with the same asset name should be added as attachments to the same asset, in whichever section is indicated by at least one of them.
- Such assets with multiple attachments should have all of the combined tags from each attachment.
- Missing or blank input data should not be sent to the Brandfolder API when creating/tagging assets.
- The Flask app's `/ingest` endpoint backend should create the assets on Brandfolder in the given section, with their associated tags and return identifying information about the new assets.



## Create virtual environment
`python3 -m venv env`

## Start virtual environment
`source env/bin/activate`

## Install requirements
`pip install -r requirements.txt`

## Start development server
`flask run`

## View in browser
[http://127.0.0.1:5000/hello/](http://127.0.0.1:5000/hello/)

Or with optional `name` parameter.

[http://localhost:5000/hello/?name=Brandfolder](http://localhost:5000/hello/?name=Brandfolder)


## Modify the code
You can add/modify/delete all of the provided code as much as you wish to help you fulfull the requirements.

Changes to the code will be automatically reloaded.

Refer to [Brandfolder docs](https://developers.brandfolder.com/) and [Flask docs](https://flask.palletsprojects.com/en/1.1.x/) for help.

## Ask questions
