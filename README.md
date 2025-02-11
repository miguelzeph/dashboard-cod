## Dash Cod


## Project

The Pipeline Dashboard is a tool that utilizes the [Codename Pipeline]() to present database results in a user-friendly format. With access to over 117k articles parsed, the dashboard analyzes titles and abstracts from major journals, resulting in approximately 19,000 classified codenames classified as True and False Positives. 

## Installation
Please ensure that you have Python 3.7 and pip installed in your environment. Follow the steps below to set up the package:

1. Verify Python Installation: Open a terminal or command prompt and enter the following command to check if Python 3.7 is installed:

```bash
python3.7 --version
```

2. Verify pip Installation: Enter the following command to check if pip is installed:

```bash
pip3.7 --version
```

3. Clone the Repository: Open a terminal or command prompt and clone the Dash Board repository.

4. Install Dependencies: Use the following command to install all the required dependencies using pip:

```bash
pip3.7 install -r requirements.txt
```

5. Configuration: Create a *config.yml* file in the project directory and specify the necessary configuration parameters as described in the "Configuration" section of this documentation.

```yml
mongo:
  host: ....
  port: 27017
  username: ...
  password: doclib
  authSource: $external # admin
  database: ...
  collection_articles_parsed: pubmedArticles_parsed # collection_synonyms: pubmedArticles_
  collection_articles_codename: pubmedArticles_codename # collection_blacklist: pubmedArticles_synonyms_blacklist

dashboard:
  documents_per_page: 10
  n_statistic_report: 200

flask:
  secret_key: mysecretkey
  session_type: filesystem
  debug: 1
  api_host: 0.0.0.0
  api_port: 5000
```

## Enviroment Variables:

To run the search you need to set the following environment variables:
```bash
# Flask env var
export FLASK_DEBUG=1 # Debug mode (optional)
export FLASK_SECRET_KEY=<your-secret-key>
export FLASK_SESSION_TYPE= filesystem
# DashBoard
export DASHBOARD_DOCUMENTS_PER_PAGE= <number:int>
# Database
export MONGO_USERNAME=<your-username>
export MONGO_PASSWORD=<your-password>
# Bing Search API
# export BING_API_KEY=<bing-api-key> # Moved to other repository
```

## How execute Locally

```bash
cd ./src # Move to src folder
python -m flask --app main.py run # python main.py --config=config.yml # 
```

