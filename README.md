# rent-my-rez
The front-page of Vancouver housing!

## Installation
To install dependencies, run:
```
pip install -r ./requirements.txt
```
The database we are using is SQLite3. Run the following commands from the `/rentmyrez/` folder to set up the DB:
```
python manage.py makemigrations
python manage.py migrate
```
To run the Django server, run the following command and head to http://127.0.0.1:8000/ to check it out:
```
python manage.py runserver
```

## Configuration
The `listings/` directory contains a `config.json` file which contains settings used by `pull_listings.py` and `populate_api.py`. Before you can run these scripts, you will need to edit the `rest_api` section of the file. First, create a Django admin user with:
```
python manage.py createsuperuser
```
Replace the `username` and `password` fields in the config file with the ones you used to create the new admin user. At this point, you will need to migrate the database again by running
```
python manage.py migrate
```
Next, run the following command from the shell, replacing `<username>` and `<password>` with the appropriate values:
```
curl -H "Content-Type: application/json" -X POST -d "{\"username\": \"<username>\", \"password\": \"<password>\"}" http://localhost:8000/api-token-auth/
```
You should get a response similar to the following:
```
{"token":"b8347a8b4708e22ae835ef73a56ba4a16b6d2b5c"}
```

Finally, replace the `token` field in the `rest_api` section of the config file with your newly generated token.

## Populating the API
You will notice that at this point, the API is empty since it has not yet been populated. To populate the API, navigate to the `listings/` folder under the project root and run the scripts using the following command:
```
python pull_listings.py | python populate_api.py
```
After this command runs, if you visit [http://localhost:8000/listings/?limit=100](http://localhost:8000/listings/?limit=100), you should see some new listings.

If you want to save the listings data to a file instead, you can run this command:
```
python pull_listings.py output.json
```
Then, later on you can populate the API directly from the file with:
```
python populate_api.py output.json
```
Finally, to setup a cronjob to run daily and repopulate the API with any new postings, run the following command from the project root (after changing the contents appropriately):
```
crontab crontab.txt
```

## Run
This project is meant to display a map of Vancouver and the statistics of housing in each neighbourhood. To view the front end, run a local server on your computer:
```
python -m SimpleHTTPServer 8080
```
And navigate to http://localhost:8080/rentmyrez/frontend/index.html
