# rent-my-rez
The Django REST API and api + plotting scripts

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
You will notice that at this point, the API is empty since it has not yet been populated. Before running the API population scripts, you will first need to make the following changes to the *config.json* file found under *scripts/api/*. 

1. Replace the `username` and `password` fields in the config file with the ones you used to create the Django admin user in the previous section.
2. Run the following command from the shell, replacing `<username>` and `<password>` with the appropriate values:

 ```bash
 > curl -H "Content-Type: application/json" -X POST -d "{\"username\": \"<username>\", \"password\": \"<password>\"}" http://localhost:8000/api-token-auth/
 ```

 You should get a response similar to the following:

 ```json
 {"token":"b8347a8b4708e22ae835ef73a56ba4a16b6d2b5c"}
 ```

 Replace the `token` field in the `rest_api` section of the config file with your newly generated token.

Once that has been done, you can navigate to the *scripts/api/* directory under the project root and run the scripts using the following command:

```bash
> python pull_listings.py | python populate_api.py
```

After this command runs, if you visit [http://localhost:8000/listings/?limit=100](http://localhost:8000/listings/?limit=100), you should see some new listings.

If you want to save the listings data to a file instead, you can run this command:

```bash
> python pull_listings.py output.json
```

Then, later on you can populate the API directly from the file with:

```bash
> python populate_api.py output.json
```

Finally, to setup a cronjob to run daily and repopulate the API with any new postings, run the following command from the project root (after changing the contents appropriately):

```bash
> crontab crontab.txt
```

##Generating Plots
The project includes scripts for generating plots of the data, which can be found under *scripts/plotting*. You will need to create a [plotly](https://plot.ly/) account before moving on. Once you have created one, open *scripts/plotting/.plotly/.credentials* and fill in the `username` and `api_key` fields.

By default, the first time the **plotly** library is configured, it will create a folder in your home directory containing configuration and credentials files. However, since it is best practice to keep the development environment completely isolated and self-contained, it would be ideal if we could move the folder inside our project and set an environment variable telling **plotly** where it can find the folder. Unfortunately, it seems that this feature is not available out of the box, but it can be easily added with a small change to the source code.

Navigate to the folder containing the **plotly** library source code (if you are using a virtual environment, the folder will be located at *${VIRTUAL\_ENVIRONMENT\_DIR}/lib/python2.7/site-packages/plotly/*, and find the file called *files.py*. Change line 4 to the following:

```python
PLOTLY_DIR = os.environ.get('PLOTLY_DIR', os.path.join(os.path.expanduser("~"), ".plotly"))
```

This tells **plotly** that if the `PLOTLY_DIR` environment variable is set, use that value as the folder location, otherwise default to *~/.plotly/*. 

The last step before generating the plots is to actually pull the JSON data from the server:

```bash
> curl http://localhost:8000/listings/ -o data.json
```

Finally, run the plotting scripts like so:

```bash
> PLOTLY_DIR=.plotly/ python heatmap.py ../data.json
```

##Setup Script
Coming soon...
