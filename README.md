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
## Run
This project is meant to display a map of Vancouver and the statistics of housing in each neighbourhood. To view the front end, run a local server on your computer:
```
python -m SimpleHTTPServer 8080
```
And navigate to http://localhost:8080/rentmyrez/frontend/index.html

To test out the scraper, go into the `/scraper/` folder and run:
```
python main.py
```
You should see some entries in your database!
