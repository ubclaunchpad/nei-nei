# rent-my-rez
The front page of Vancouver housing!

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
> curl http://localhost:8000/listings/ -o data.json
```

Finally, run the plotting scripts like so:

```bash
> PLOTLY_DIR=.plotly/ python heatmap.py ../data.json
```

To see a list of available options, run

```bash
> python heatmap.py -h
```

##Setup Script
You will find a setup script located under the root project directory called *setup.sh*. You can run the script and it will automatically perform all the setup steps listed above:

```bash
> bash setup.sh

Creating virtual environment...
New python executable in venv/bin/python2.7
Also creating executable in venv/bin/python
Installing setuptools, pip, wheel...done.

Installing project dependencies...
Collecting Django==1.9.7 (from -r requirements.txt (line 1))
  Using cached Django-1.9.7-py2.py3-none-any.whl
Collecting djangorestframework==3.3.3 (from -r requirements.txt (line 2))
  Using cached djangorestframework-3.3.3-py2.py3-none-any.whl
Collecting gevent==1.1.1 (from -r requirements.txt (line 3))
Collecting greenlet==0.4.10 (from -r requirements.txt (line 4))
Collecting grequests==0.3.0 (from -r requirements.txt (line 5))
Collecting numpy==1.11.1 (from -r requirements.txt (line 6))
Collecting pandas==0.18.1 (from -r requirements.txt (line 7))
Collecting plotly==1.12.4 (from -r requirements.txt (line 8))
Collecting python-dateutil==2.5.3 (from -r requirements.txt (line 9))
  Using cached python_dateutil-2.5.3-py2.py3-none-any.whl
Collecting pytz==2016.6.1 (from -r requirements.txt (line 10))
  Using cached pytz-2016.6.1-py2.py3-none-any.whl
Collecting requests==2.10.0 (from -r requirements.txt (line 11))
  Using cached requests-2.10.0-py2.py3-none-any.whl
Collecting six==1.10.0 (from -r requirements.txt (line 12))
  Using cached six-1.10.0-py2.py3-none-any.whl
Requirement already satisfied (use --upgrade to upgrade): wheel==0.24.0 in ./venv/lib/python2.7/site-packages (from -r requirements.txt (line 13))
Installing collected packages: Django, djangorestframework, greenlet, gevent, requests, grequests, numpy, pytz, six, python-dateutil, pandas, plotly
Successfully installed Django-1.9.7 djangorestframework-3.3.3 gevent-1.1.1 greenlet-0.4.10 grequests-0.3.0 numpy-1.11.1 pandas-0.18.1 plotly-1.12.4 python-dateutil-2.5.3 pytz-2016.6.1 requests-2.10.0 six-1.10.0
You are using pip version 7.1.2, however version 8.1.2 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.

Migrating database...
No changes detected in app 'listings'
Operations to perform:
  Apply all migrations: authtoken, sessions, admin, listings, auth, contenttypes
Running migrations:
  Rendering model states... DONE
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying authtoken.0001_initial... OK
  Applying authtoken.0002_auto_20160226_1747... OK
  Applying listings.0001_initial... OK
  Applying sessions.0001_initial... OK
Username for Django admin user (simon):
Password for Django admin user:
Creating Django admin user...
Python 2.7.12 (default, Jun 29 2016, 14:05:02)
[GCC 4.2.1 Compatible Apple LLVM 7.3.0 (clang-703.0.31)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> <User: simon>

>>>
Running server...
Performing system checks...

System check identified no issues (0 silenced).
July 21, 2016 - 18:45:05
Django version 1.9.7, using settings 'rentmyrez.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

Requesting authentication token...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0[21/Jul/2016 18:45:06] "POST /api-token-auth/ HTTP/1.1" 200 52
100    93    0    52  100    41   1458   1149 --:--:-- --:--:-- --:--:--  1529

Updating API config file...

Populating API...
[21/Jul/2016 18:45:09] "POST /listings/ HTTP/1.1" 201 398
[21/Jul/2016 18:45:09] "POST /listings/ HTTP/1.1" 201 387
[21/Jul/2016 18:45:09] "POST /listings/ HTTP/1.1" 201 390
.
. Output truncated for brevity
.

Updating crontab.txt...

Patching Plotly library file...
Plotly account username: simon_zhu
Plotly API key: 9bz47vjp1j

Updating Plotly credentials file...

Generating plots...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:[21/Jul/2016 18:45:31] "GET /listings/ HTTP/1.1" 200 318969
100  311k    0  311k    0     0  1661k      0 --:--:-- --:--:-- --:--:-- 1674k

Exiting.
```

##Front-End
This project is meant to display a map of Vancouver and the statistics of housing in each neighbourhood. To view the front end, run a local server on your computer:
```
python -m SimpleHTTPServer 8080
```
And navigate to http://localhost:8080/rentmyrez/frontend/index.html
