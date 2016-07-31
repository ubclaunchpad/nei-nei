#!/usr/bin/env bash

set -e

PROJECT_ROOT=$( cd $(dirname $0) ; pwd -P )

function join { local IFS="$1"; shift; echo "$*"; }
function print_error { printf "\n\e[01;31m$@\e[0m\n" >&2; }
function print_progress { printf "\n\e[01;34m$@\e[0m\n"; }
function finish { print_progress "Exiting."; pkill -TERM -P $SERVER_PID 2>/dev/null; }
trap finish EXIT

pushd $PROJECT_ROOT > /dev/null

command -v virtualenv >/dev/null 2>&1 || { print_progress "Installing virtualenv..."; pip install virtualenv; }
print_progress "Creating virtual environment..."
virtualenv venv
source venv/bin/activate

print_progress "Installing project dependencies..."
pip install -r requirements.txt

cd rentmyrez

print_progress "Migrating database..."
python manage.py makemigrations
python manage.py migrate

read -p "Username for Django admin user ($USER): " DJANGO_USER
DJANGO_USER=${DJANGO_USER:-$USER}
while read -s -p "Password for Django admin user: " DJANGO_PASS && [[ -z "$DJANGO_PASS" ]] ; do
  print_error "Error: Blank passwords aren't allowed."
done
print_progress "Creating Django admin user..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_USER', '', '$DJANGO_PASS')" | python manage.py shell

print_progress "Running server..."
python manage.py runserver &
SERVER_PID=$!
sleep 1

cd ../scripts/api

print_progress "Requesting authentication token..."
regex="{\"token\":\"([a-zA-Z0-9]+)\"}"
response=$(curl -H "Content-Type: application/json" -X POST -d "{\"username\": \"$DJANGO_USER\", \"password\": \"$DJANGO_PASS\"}" http://localhost:8000/api-token-auth/)
if [[ $response =~ $regex ]]
then
  token="${BASH_REMATCH[1]}"
else
  print_error "Received unexpected response from server:\n\n$response"
  exit 1
fi

print_progress "Updating API config file..."
cp config{.sample,}.json
api_replacements[0]='s@${username}@'$DJANGO_USER'@'
api_replacements[1]='s@${password}@'$DJANGO_PASS'@'
api_replacements[2]='s@${token}@'$token'@'
sed -i "$(join \; "${api_replacements[@]}")" config.json

print_progress "Populating API..."
python populate_neighbourhoods_api.py
python populate_listings_api.py

cd ../..

print_progress "Updating crontab.txt..."
cp crontab{.sample,}.txt
sed -i '1d; s@${PROJECT_ROOT}@'$PROJECT_ROOT'@' crontab.txt

cd venv/lib/python2.7/site-packages/plotly/

print_progress "Patching Plotly library file..."
sed -i 's@\(PLOTLY_DIR\) = \(os\.path\.join(os\.path\.expanduser("~"), "\.plotly")\)@\1 = os\.environ\.get("PLOTLY_DIR", \2)@' files.py

cd ../../../../../scripts/plotting

read -p "Plotly account username: " PLOTLY_USER
read -p "Plotly API key: " PLOTLY_API_KEY
print_progress "Updating Plotly credentials file..."
cp .plotly/.credentials{.sample,}
plotly_replacements[0]='s@${username}@'$PLOTLY_USER'@'
plotly_replacements[1]='s@${api_key}@'$PLOTLY_API_KEY'@'
sed -i "$(join \; "${plotly_replacements[@]}")" .plotly/.credentials

print_progress "Generating plots..."
curl http://localhost:8000/listings/ -o data.json
PLOTLY_DIR=.plotly/ python heatmap.py data.json -o heatmap.png

popd > /dev/null
