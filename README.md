# rent-my-rez
The Django REST API and api + plotting scripts


## Available APIs

- [Authentication](rentmyrez/api-docs/authentication.apib)
- [Neighbourhoods](rentmyrez/api-docs/neighbourhoods.apib)
- [Listings](rentmyrez/api-docs/listings.apib)

To render static HTML files for the API Blueprints, first install `aglio` via NPM:

```bash
npm install aglio
```

Then, start generating HTML:

```bash
alias aglio=$(npm bin)/aglio
cd rentmyrez
for resource in api-docs/*
do
  aglio -i $resource -o templates/api-docs/`basename $resource .apib`.html
done
```

## Installation
Create a virtual environment in the root project folder by running

```bash
> virtualenv venv
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

 <pre>
 > curl -H "Content-Type: application/json" -X POST -d "{\"username\": \"<b>${username}</b>\", \"password\": \"<b>${password}</b>\"}" http://localhost:8000/api-token-auth/
 </pre>

 You should get a response similar to the following:

 ```json
 {"token":"b8347a8b4708e22ae835ef73a56ba4a16b6d2b5c"}
 ```

 Replace the `token` field in the `rest_api` section of the config file with your newly generated token.

Once that has been done, you can navigate to the *scripts/api/* directory under the project root and run the scripts using the following commands:

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

##Generating Plots
The project includes scripts for generating plots of the data, which can be found under *scripts/plotting*. You will need to create a [plotly](https://plot.ly/) account before moving on. Once you have created one, copy *scripts/plotting/.plotly/.credentials.sample* to *scripts/plotting/.plotly/.credentials* and fill in the `username` and `api_key` fields.

By default, the first time the **plotly** library is configured, it will create a folder in your home directory containing configuration and credentials files. However, since it is best practice to keep the development environment completely isolated and self-contained, it would be ideal if we could move the folder inside our project and set an environment variable telling **plotly** where it can find the folder. Unfortunately, it seems that this feature is not available out of the box, but it can be easily added with a small change to the source code.

Navigate to the folder containing the **plotly** library source code (if you are using a virtual environment, the folder will be located at *<b>${VIRTUAL\_ENVIRONMENT\_DIR}</b>/lib/python2.7/site-packages/plotly/*, and find the file called *files.py*. Change line 4 to the following:

```python
PLOTLY_DIR = os.environ.get('PLOTLY_DIR', os.path.join(os.path.expanduser("~"), ".plotly"))
```

This tells **plotly** that if the `PLOTLY_DIR` environment variable is set, use that value as the folder location, otherwise default to *~/.plotly/*.

The last step before generating the plots is to actually pull the JSON data from the server:

```bash
> curl http://localhost:8000/listings/ -o data/listings.json --create-dirs
```

Finally, run the plotting scripts like so:

```bash
> mkdir -p plots
> PLOTLY_DIR=.plotly/ python heatmap.py data/listings.json -o plots/heatmap.png
```

To see a list of available options, run

```bash
> python heatmap.py -h
```

##Setup Script
You will find a setup script located under the root project directory called *setup.sh*. You can run the script and it will automatically perform all the setup steps listed above. Make sure that you have first installed at least Python and Pip before running the script.

```bash
> bash setup.sh
.
. Output truncated for brevity
.
```
