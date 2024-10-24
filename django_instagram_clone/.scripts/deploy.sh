#!/bin/bash
set -e

echo "Deployment started ..."

# Move to the repo location
cd code-repositories/instagram_clone_final/

# Pull the latest version of the app
git pull origin master
echo "New changes copied to server !"

# Activate Virtual Env
# source seperate_venvs/instagram_clone_venv/bin/activate
# echo "Virtual env 'instagram_clone_venv' Activated !"

# echo "Installing Dependencies..."
# pip install -r requirements.txt --no-input

# echo "Serving Static Files..."
# python manage.py collectstatic --noinput

# echo "Running Database migration"
# python manage.py makemigrations
# python manage.py migrate

# Deactivate Virtual Env
# deactivate
# echo "Virtual env 'mb' Deactivated !"

# Reloading Application So New Changes could reflect on website
pushd miniblog
touch wsgi.py
popd

echo "Deployment Finished!"