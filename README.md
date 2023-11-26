# Endpoints
- For gettiing endpoint in order managing vendor and their purchase orders, goto 
  `/docs/` which list the endpoints.
- The endpoints are available with prefix `/api/`


# DB Setup
- In order to run dbsqlite set USE_SQLITE = True else False for postgres.
- For postgres, set host,database name, username and password in .env file


# Setup
- Run the following commands to setup user and get the auth token in local
  ```
    python manage.py collectstatic
    python .\manage.py makemigrations vendor
    python .\manage.py migrate
    python .\manage.py createuser anyusername anypassword
  ```
- The above command will output following message
  ```
    User created successfully and token is : c730f36fdd5c7f26b8f6ef00a63da0a71c07492f
  ```
- During docker run, run the following command to get user
  ```
    docker-compose run --rm app python .\manage.py createuser anyusername anypassword
  ```
# Tests
- Run the following command to run the test
  ```
    pytest
  ```

# With docker
- Run the following command to run up the docker. This will run the django app, postgres db server and test app running test cases
```
  docker-compose up -d --build
```

- Run the following to check the log of testcase
```
  docker-compose logs test_app
```