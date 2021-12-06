
# To-do lists

This is a project to create and manage To-do lists made with Django Rest Framework. This project only have the API.

## Installation

If you have docker and docker-compose, start the project with:

```bash
docker-compose up
```
Or, install python, and
```bash
pip install -r requirements.txt
python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
```
And the project will be running on port 8000
## Features

Inside screenshots folder you can see available routes, like create user, lists, and tasks, view the logged in user lists, tasks, and more.
The lists and tasks created can only be seen by their creator.
##
This is my first project with Django, created to learn how to interact with authentication, permissions and validation of data.
## Author

- [@ramonhentges](https://github.com/ramonhentges)

