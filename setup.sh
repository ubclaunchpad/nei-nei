#!/usr/bin/env bash

set -e

PROJECT_ROOT=$( cd $(dirname $0) ; pwd -P )

function join { local IFS="$1"; shift; echo "$*"; }

pushd $PROJECT_ROOT > /dev/null

command -v virtualenv >/dev/null 2>&1 || { echo "Installing virtualenv..."; pip install virtualenv; }
echo "Creating virtual environment..."
virtualenv venv
source venv/bin/activate

echo "Installing project dependencies..."
pip install -r requirements.txt

cd rentmyrez

echo "Migrating database..."
python manage.py makemigrations listings
python manage.py migrate

read -p "Username for Django admin user ($USER): " DJANGO_USER
DJANGO_USER=${DJANGO_USER:-$USER}
while read -s -p "Password for Django admin user: " DJANGO_PASS && [[ -z "$DJANGO_PASS" ]] ; do
  >&2 printf "\n\e[01;31mError: Blank passwords aren't allowed.\e[0m\n"
done
echo
echo "Creating Django admin user..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_USER', '', '$DJANGO_PASS')" | python manage.py shell

echo "Running server..."
python manage.py runserver &
sleep 1

cd ../scripts/api

echo "Requesting authentication token..."
regex="{\"token\":\"([a-zA-Z0-9]+)\"}"
response=$(curl -H "Content-Type: application/json" -X POST -d "{\"username\": \"$DJANGO_USER\", \"password\": \"$DJANGO_PASS\"}" http://localhost:8000/api-token-auth/)
if [[ $response =~ $regex ]]
then
  token="${BASH_REMATCH[1]}"
else
  printf "\n\e[01;31mReceived unexpected response from server: \n\n$response\e[0m\n" >&2
  exit 1
fi

echo "Updating API config file..."
api_replacements[0]='s@\("username": \?\)"[[:alnum:]]\+"@\1"'$DJANGO_USER'"@'
api_replacements[1]='s@\("password": \?\)"[[:alnum:]]\+"@\1"'$DJANGO_PASS'"@'
api_replacements[2]='s@\("token": \?\)"[[:alnum:]]\+"@\1"'$token'"@'
sed -i "$(join \; "${api_replacements[@]}")" config.json

echo "Populating API..."
python pull_listings.py | python populate_api.py

echo "Stopping server."
kill -SIGINT $!

cd ../..

echo "Updating crontab.txt..."
sed -i '1d; s@${PROJECT_ROOT}@'$PROJECT_ROOT'@' crontab.txt

cd scripts/plotting

read -p "Plotly account username: " PLOTLY_USER
read -p "Plotly API key: " PLOTLY_API_KEY
echo "Updating Plotly credentials file..."
plotly_replacements[0]='s@\("username": \?\)"[[:alnum:]]\+"@\1"'PLOTLY_USER'"@'
plotly_replacements[1]='s@\("api_key": \?\)"[[:alnum:]]\+"@\1"'PLOTLY_API_KEY'"@'
sed -i "$(join \; "${plotly_replacements[@]}")" .plotly/.config

cd ../../venv/lib/python2.7/site-packages/plotly/

echo "Patching Plotly library file..."
sed -i 's@\(PLOTLY_DIR\) = \(os\.path\.join(os\.path\.expanduser("~"), "\.plotly")\)@\1 = os\.environ\.get("PLOTLY_DIR", \2)@' files.py

deactivate

popd > /dev/null
