# Nei Nei
Rental price analytics for neighbourhoods in Vancouver.

## Available APIs

- [Authentication](api/authentication.apib)
- [Neighbourhoods](api/neighbourhoods.apib)
- [Listings](api/listings.apib)

To render static HTML files for the API Blueprints, first install `aglio` via NPM:

```
npm install aglio
```

Then, start generating HTML:

```
alias aglio=$(npm bin)/aglio
aglio -i api/neighbourhoods.apib -o api/neighbourhoods.html
aglio -i api/listings.apib -o api/listings.html
aglio -i api/authentication.apib -o api/authentication.html
```

## Installation
Create a virtual environment in the root project folder by running

```bash
> virtualenv venv
> source venv/bin/activate
```

Then install the dependencies with:

```bash
> pip install -r requirements.txt
```

The database we are using is SQLite3. Run the following commands from the *rentmyrez/* folder to set up the DB:

```bash
> python manage.py makemigrations listings
> python manage.py migrate
```

To run the Django server, run the following command and head to http://127.0.0.1:8000/ to check it out:

```bash
> python manage.py runserver
```

Before moving on, you should also create a Django admin user with:

```bash
> python manage.py createsuperuser
```

At this point, you will need to migrate the database again by running

```bash
> python manage.py migrate
```

## Populating the API
You will notice that at this point, the API is empty since it has not yet been populated. Before running the API population scripts, you will first need to create a *config.json* file from the template found under *scripts/api/* and make the following changes:

1. Replace the `username` and `password` fields in the config file with the ones you used to create the Django admin user in the previous section.
2. Run the following command from the shell, replacing **`${username}`** and **`${password}`** with the appropriate values:

 > curl -H "Content-Type: application/json" -X POST -d "{\"username\": \"${username}\", \"password\": \"${password}\"}" http://localhost:8000/api-token-auth/

 You should get a response similar to the following:

 ```json
 {"token":"b8347a8b4708e22ae835ef73a56ba4a16b6d2b5c"}
 ```

 Replace the `token` field in the `rest_api` section of the config file with your newly generated token.

Once that has been done, you can navigate to the *scripts/api/* directory under the project root and run the scripts using the following command:

```bash
> python populate_neighbourhoods_api.py
> python populate_listings_api.py
```

After this command runs, if you visit [http://localhost:8000/listings/?limit=100](http://localhost:8000/listings/?limit=100), you should see some new listings. A list of neighbourhoods can also be seen at [http://localhost:8000/neighbourhoods](http://localhost:8000/neighbourhoods).

The API can also be populated from raw data files (samples can be found under the *data/* directory):

```bash
> python populate_neighbourhoods_api.py data/raw_neighbourhoods_data.kml
> python populate_listings_api.py data/raw_listings_data.json
```

Finally, to setup a cronjob to run daily and repopulate the API with any new postings, copy the sample file found under the project root to *crontab.txt*, replace the **`${PROJECT_ROOT}`** placeholder with the appropriate directory path, and run the following command:

```bash
> crontab crontab.txt
```

##Setup Script
You will find a setup script located under the root project directory called *setup.sh*. You can run the script and it will automatically perform all the setup steps listed above. Make sure that you have first installed at least Python, Pip, and Node.js before running the script.

```bash
> bash setup.sh
.
. Output truncated for brevity
.
```

## Run
This project is meant to display a map of Vancouver and the statistics of housing in each neighbourhood. To view the front end, run a local server on your computer from the root folder:
```
python -m SimpleHTTPServer 8080
```
And navigate to http://localhost:8080/frontend/index.html
