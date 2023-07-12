# Documentation

## Base URL
Application will start running at http://localhost:5000/

## Overall description
This web application is intended for my students studying test automation. The application only contains `index.html` and multiple endpoints, which can be used to manipulate data in Postgresql.

# /employees

This endpoint is used to manipulate data in `employees` table

* To fetch all employees in your DB, send GET request to `/employees` endpoint.

Response example:
```
[
    {
        "employeeId": 1,
        "name": "Steven",
        "organization": "IT",
        "role": "Developer"
    },
    {
        "employeeId": 2,
        "name": "Mark",
        "organization": "IT",
        "role": "PM"
    }
]
```
* To fetch single employee in your DB, send GET request to `/employees/<employee_id>` endpoint.

Response example:
```
{
    "employeeId": 2,
    "name": "Mark",
    "organization": "IT",
    "role": "PM"
}
```
* To add more employee to DB, send POST request to `/employees` endpoint.

Request example:
```
{
    "name": "Mary",
    "organization": "IT",
    "role": "QA"
}
```
Response example:
```
{
    "employeeId": 3,
    "name": "Mary",
    "organization": "IT",
    "role": "QA"
}
```

* To update full data for particular employee in DB, send PUT request to `/employees/<employee_id>` endpoint.

Request example:
```
{
    "name": "Jenny",
    "organization": "IT",
    "role": "DevOps"
}
```
Response example:
```
{
    "message": "Employee updated"
}
```

* To update single data for particular employee in DB, send PATCH request to `/employees/<employee_id>` endpoint.

Request example:
```
{
    "role": "Senior DevOps"
}
```
Response example:
```
{
    "message": "Employee updated"
}
```

* To delete employee from DB, send DELETE request to `/employees/<employee_id>` endpoint.

Response example:
```
{
    "message": "Employee deleted"
}
```

## Errors

* In case you are referring to employee ID that is not registered, you will get an error message:
```
{
    "error": "Employee not found"
}
```
* In case you are referring to fields that are not defined, you will get an error message:
```
{
    "message": "No fields to update"
}
```
* In case you are trying to send request without auth token, you will get an error message:
```
{
    "message": "Unauthorized"
}
```