# foodborne_illness_database

This repo implemented basic web UIs (homepage and search result page), remote connection to mongodb atlas, and basic queries.

## Setup
1. ```cd``` into the working directory
    ```
    cd foodborne_illness_database 
    ```
2. set up python environment from requirements.txt
    ```
    pip install -r requirements.txt
    ```
3. ```cd``` into WPI folder and start django server
    ```
    cd WPI
    python3.6 manage.py runserver 127.0.0.1:8000
    ```
    
## General Intro
- ```WPI/urls.py```: The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
- ```WPI/core/mongo_models.py```: Using [pymongo](https://www.mongodb.com/compatibility/mongodb-and-django) to interact with MongoDB.
- ```WPI/core/views/*.py```: A view function, or view for short, is a Python function that takes a Web request and returns a Web response. For more information please see: https://docs.djangoproject.com/en/3.2/topics/http/views/
