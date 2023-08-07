# employees-api

A simple app to help my students understand backend development and cover it with automated tests.

# Technical stack
* Python
* Postgres
* Flask

# Quick start

* Clone this repo to your local
* Create and activate virtual env
* Install dependencies:
  * `pip install -r requirements.txt`
* Make sure that your DB prepared with below structure:

Table name: `employees`
```
 | Column         | Data Type |
 |----------------|-----------|
 | employee_id    | SERIAL    |
 | name           | TEXT      |
 | organization   | TEXT      |
 | role           | TEXT      |
```
* To make this code work in your local machine, create `.env` in root directory and add environment variables there as shown in below example:
```
CONNECTION_STRING_DB='your postgresql connection string'
JWT_SECRET_KEY='your secret key'
APP_SUPERUSER='your username'
APP_PASSWORD='your password'
```
* Run application using below command:
  * `python app.py`