# team-api

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
```
 | Column         | Data Type |
 |----------------|-----------|
 | employee_id    | SERIAL    |
 | name           | TEXT      |
 | organization   | TEXT      |
 | skill          | TEXT      |
```
* Create `.env` in root directory and add environment variables there
* Run application using below command:
  * `python app.py`