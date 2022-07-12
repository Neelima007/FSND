# FSND-Capstone-Project

This project is the final project of the Udacity Full Stack Developer Nano Degree Program. The goal of this project is to deploy a Flask application with Heroku/PostgreSQL and enable Role Based Authentication and roles-based access control (RBAC) with Auth0 (third-party authentication systems).

So, I decided to implement The Casting Agency model a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Getting Started

### Installing Dependencies



#### Virtual Enviornment

I recommend working within a virtual environment whenever using Python for projects. This keeps dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for the platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
$ pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Running the server

first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
$ source setup.sh
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run
```

Sourcing `setup.sh` sets some environment variables used by the app.

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to use the this file to find the application.

## Models:

- **Movies** model defined with attributes title and release date
- **Actors** model defined with attributes name, age and gender

You can find the models in `models.py` file. Local Postgres **DATABASE** details are available in `setup.sh` file for reference.

## Endpoints:

GET /actors 
GET /movies
POST /actors
POST /movies
DELETE /actors/<int:id>
DELETE /movies/<int:id>
PATCH /actors/<int:id>
PATCH /movies/<int:id>

```



## Auth0 Setup:


**Roles**: All 3 roles have been defined in Auth0 and following permissions as shown for each role below are also defined in Auth0.

- **Casting Assistant
    get /actors 
    get /movies

- **Casting Director
  _ get /actors 
    get /movies
    POST /actors
    DELETE /actors/<int:id>
    DELETE /movies/<int:id>
    PATCH /actors/<int:id>
    PATCH /movies/<int:id>

- **Executive Producer
    GET /actors 
    GET /movies
    POST /actors
    POST /movies
    DELETE /actors/<int:id>
    DELETE /movies/<int:id>
    PATCH /actors/<int:id>
    PATCH /movies/<int:id>
  _ 
## Deployment Details:

- App is deployed to [Heroku](https://harsh-casting-agency.herokuapp.com/ "Heroku").
- Heroku Postgres **DATABASE** details are available in `setup.sh` file for reference.

Use the above stated endpoints and append to this link above to execute the app either thru CURL or Postman.
For example:

```bash
All the details and requests are provided in postman collection .Add the authentication and run the requests.
.

## Testing:

We can run our entire test case by running the following command at command line

$ python test_app.py
```

### Thank You!
