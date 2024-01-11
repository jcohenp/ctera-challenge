# CTERA Challenge

This repository contains a solution for the CTERA challenge, consisting of containarized application using a flask app as a web router and a postgresql database.

## Project Structure

- **Dockerfile**: used to build the Flask app before to push to the docker registry.
- **app.py**: Used by the Dockerfile to set the web router
- **db_password.txt.gpg**: file containing the password of the postgresql db encrypted using gpg
- **docker-compose.yaml**: The docker-compose.yml file orchestrates the deployment of the Flask API and PostgreSQL database using Docker Compose.
- **requirements.txt**: Used by the Dockerfile to install the necessary dependencies for the flask app
- **.github/workflows/python-app.yml**: githubaction CI/CD pipeline to build and deploy flask-app to docker-registry when a push event is performed on main branch
- **README.md**: This document providing instructions, explanations, and a guide on how to use the repository.

## Action Performed

- **Flask API (`flask-app`)**:

The Flask API serves as the backend for the application. It provides endpoints to manage user data and performs interactions with a PostgreSQL database. Flask App is listening on port 5001.

- **Endpoints:**
    - `/health`: Check if the flask App is able to connect to the postgresql DB
    - `/number_of_tables`: Return the number of tables that exists in the postgresql DB

- **PostgreSQL Database (`postgres-db`)**:

The PostgreSQL database serves as storage for the web router.


- **Docker Compose Configuration:**

Defines services for a web application (`flask-app`) and a database (`postgresql`).

    - Web App
        - Image: `jcohenp/ctera-app:latest`
        - Ports: Host port `5001` to container port `5001`
        - Secrets: Uses `db_password` secret for database access
        - Env Variables: Configuration for app and database connection

    - Database
        - Image: `bitnami/postgresql`
        - Env Variables: Configuration for the db connection

- **.github/worflows/python-app.yaml:**

Define the CI/CD pipeline to build and deploy the new docker image on push event on main branch.

Secrets need to be defined:
    
    - DOCKER_TOKEN: API token to use as password to log in to the docker registry
    - DOCKER_USERNAME: username used to log in to the docker registry
These secrets are defined in: **https://github.com/jcohenp/ctera-challenge/settings/secrets/actions**

## Configuration:

1. **Clone this repository:**

    ```
    git clone https://github.com/jcohenp/ctera-challenge.git
    ```
2. **Build the Docker Image:**

    ```
    docker build -t ctera-app .
    ```
3. **Create a tag:**

    ```
    sudo docker tag <imageID> docker.io/jcohenp/ctera-app
    ```
4. **Push the image in the Docker registry**

    ```
    sudo docker push docker.io/jcohenp/ctera-app
    ```
5. **Decrypt password secret before running the docker-compose up command**:

    ```
    gpg --decrypt db_password.txt.gpg > db_password.txt
    ```
6. **Run the containarized app**

    ```
    docker-compose up
    ```
7. **To turn off the app**

    ```
    docker-compose down
    ```

## POC

1. **curl http://127.0.0.1:5001/health**
    
    ```
    {"container":"flask-app","status":"Healthy!"} - status code: 200
    
    ```

2. **curl http://127.0.0.1:5001/health - case where db container is not reachable**
    ```
    {"container":"flask-app","status":"Unhealthy"} - status code: 503
    
    ```

3. **curl http://127.0.0.1:5001/number_of_tables**

    ```
    {"number_of_tables":"189"} - status code: 200
    
    ```
    
4. **curl http://127.0.0.1:5001/wrong_route**

    ```
    <!doctype html>
    <html lang=en>
    <title>404 Not Found</title>
    <h1>Not Found</h1>
    <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
    ```
5. **Push on master:**

    ```
    Run mr-smithers-excellent/docker-build-push@v6
    Docker image name used for this build: docker.io/***/ctera-app
    Logging into Docker registry docker.io...
    WARNING! Your password will be stored unencrypted in /home/runner/.docker/config.json.
    Configure a credential helper to remove this warning. See
    https://docs.docker.com/engine/reference/commandline/login/#credentials-store
    Building Docker image docker.io/***/ctera-app with tags $(date +%s),latest...
    
    BuildCommand docker build -f Dockerfile -t docker.io/***/ctera-app:$(date +%s) -t docker.io/***/ctera-app:latest .
    #0 building with "default" instance using docker driver
    
    #1 [internal] load .dockerignore
    #1 transferring context: 2B done
    #1 DONE 0.0s
    
    #2 [internal] load build definition from Dockerfile
    #2 transferring dockerfile: 186B done
    #2 DONE 0.0s
    
    #3 [auth] library/python:pull token for registry-1.docker.io
    #3 DONE 0.0s
    
    #4 [internal] load metadata for docker.io/library/python:3.9
    #4 DONE 0.4s
    
    #5 [internal] load build context
    #5 transferring context: 1.76kB done
    #5 DONE 0.0s
    
    #6 [1/5] FROM docker.io/library/python:3.9@sha256:30678bb79d9eeaf98ec0ce83cdcd4d6f5301484ef86873a711e69df2ca77e8ac
    #6 resolve docker.io/library/python:3.9@sha256:30678bb79d9eeaf98ec0ce83cdcd4d6f5301484ef86873a711e69df2ca77e8ac done
    #6 sha256:7a97f6368ea64ce28aa5df12c8a292db5f729f0858dd112579938b295b0c861c 2.85MB / 2.85MB 0.2s done
    #6 sha256:30678bb79d9eeaf98ec0ce83cdcd4d6f5301484ef86873a711e69df2ca77e8ac 1.86kB / 1.86kB done
    #6 sha256:62072a293549fb69041a44936a3ea5cebcbc7195cc532e509fe940175b2f5430 2.01kB / 2.01kB done
    #6 sha256:7fad4bffde2444237b82386b9b704d8ac48a54eee2c992e377a3a28da49b98d3 6.39MB / 6.39MB 0.1s done
    #6 sha256:b85288e0cb16dfd5a0d717d65e0cba46d00c33ce88b772a2b06a5899f88ed0be 244B / 244B 0.1s done
    #6 sha256:edb6b76b75bad04bef16fec848f73e45c0b4522d77cf389baff429081157fa1a 7.51kB / 7.51kB done
    #6 sha256:cd0903c43c21ba3625df928c05a81e32d2d5dc44214e326fafca1957dcdfbfba 14.68MB / 15.82MB 0.2s
    #6 extracting sha256:7fad4bffde2444237b82386b9b704d8ac48a54eee2c992e377a3a28da49b98d3
    #6 sha256:cd0903c43c21ba3625df928c05a81e32d2d5dc44214e326fafca1957dcdfbfba 15.82MB / 15.82MB 0.2s done
    #6 extracting sha256:7fad4bffde2444237b82386b9b704d8ac48a54eee2c992e377a3a28da49b98d3 0.3s done
    #6 extracting sha256:cd0903c43c21ba3625df928c05a81e32d2d5dc44214e326fafca1957dcdfbfba 0.1s
    #6 extracting sha256:cd0903c43c21ba3625df928c05a81e32d2d5dc44214e326fafca1957dcdfbfba 0.4s done
    #6 extracting sha256:b85288e0cb16dfd5a0d717d65e0cba46d00c33ce88b772a2b06a5899f88ed0be done
    #6 extracting sha256:7a97f6368ea64ce28aa5df12c8a292db5f729f0858dd112579938b295b0c861c
    #6 extracting sha256:7a97f6368ea64ce28aa5df12c8a292db5f729f0858dd112579938b295b0c861c 0.2s done
    #6 DONE 1.2s
    
    #7 [2/5] WORKDIR /app
    #7 DONE 0.0s
    
    #8 [3/5] COPY requirements.txt .
    #8 DONE 0.0s
    
    #9 [4/5] RUN pip install --no-cache-dir -r requirements.txt
    #9 2.250 Collecting Flask==3.0.0
    #9 2.293   Downloading flask-3.0.0-py3-none-any.whl (99 kB)
    #9 2.308      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 99.7/99.7 kB 7.7 MB/s eta 0:00:00
    #9 2.488 Collecting psycopg2-binary==2.9.9
    #9 2.499   Downloading psycopg2_binary-2.9.9-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.0 MB)
    #9 2.627      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.0/3.0 MB 23.9 MB/s eta 0:00:00
    #9 2.675 Collecting Werkzeug==3.0.0
    #9 2.684   Downloading werkzeug-3.0.0-py3-none-any.whl (226 kB)
    #9 2.692      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 226.6/226.6 kB 41.8 MB/s eta 0:00:00
    #9 2.737 Collecting docker
    #9 2.754   Downloading docker-7.0.0-py3-none-any.whl (147 kB)
    #9 2.759      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 147.6/147.6 kB 118.8 MB/s eta 0:00:00
    #9 2.848 Collecting importlib-metadata>=3.6.0
    #9 2.856   Downloading importlib_metadata-7.0.1-py3-none-any.whl (23 kB)
    #9 2.889 Collecting click>=8.1.3
    #9 2.896   Downloading click-8.1.7-py3-none-any.whl (97 kB)
    #9 2.899      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 97.9/97.9 kB 192.2 MB/s eta 0:00:00
    #9 2.917 Collecting blinker>=1.6.2
    #9 2.924   Downloading blinker-1.7.0-py3-none-any.whl (13 kB)
    #9 2.952 Collecting Jinja2>=3.1.2
    #9 2.960   Downloading Jinja2-3.1.2-py3-none-any.whl (133 kB)
    #9 2.963      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 133.1/133.1 kB 113.8 MB/s eta 0:00:00
    #9 2.984 Collecting itsdangerous>=2.1.2
    #9 2.991   Downloading itsdangerous-2.1.2-py3-none-any.whl (15 kB)
    #9 3.086 Collecting MarkupSafe>=2.1.1
    #9 3.095   Downloading MarkupSafe-2.1.3-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (25 kB)
    #9 3.156 Collecting urllib3>=1.26.0
    #9 3.163   Downloading urllib3-2.1.0-py3-none-any.whl (104 kB)
    #9 3.166      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 104.6/104.6 kB 192.0 MB/s eta 0:00:00
    #9 3.207 Collecting packaging>=14.0
    #9 3.214   Downloading packaging-23.2-py3-none-any.whl (53 kB)
    #9 3.217      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 53.0/53.0 kB 170.9 MB/s eta 0:00:00
    #9 3.267 Collecting requests>=2.26.0
    #9 3.275   Downloading requests-2.31.0-py3-none-any.whl (62 kB)
    #9 3.277      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 62.6/62.6 kB 168.2 MB/s eta 0:00:00
    #9 3.336 Collecting zipp>=0.5
    #9 3.343   Downloading zipp-3.17.0-py3-none-any.whl (7.4 kB)
    #9 3.527 Collecting charset-normalizer<4,>=2
    #9 3.537   Downloading charset_normalizer-3.3.2-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (142 kB)
    #9 3.540      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 142.3/142.3 kB 119.3 MB/s eta 0:00:00
    #9 3.566 Collecting idna<4,>=2.5
    #9 3.579   Downloading idna-3.6-py3-none-any.whl (61 kB)
    #9 3.581      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 61.6/61.6 kB 186.1 MB/s eta 0:00:00
    #9 3.614 Collecting certifi>=2017.4.17
    #9 3.621   Downloading certifi-2023.11.17-py3-none-any.whl (162 kB)
    #9 3.624      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 162.5/162.5 kB 137.9 MB/s eta 0:00:00
    #9 3.772 Installing collected packages: zipp, urllib3, psycopg2-binary, packaging, MarkupSafe, itsdangerous, idna, click, charset-normalizer, certifi, blinker, Werkzeug, requests, Jinja2, importlib-metadata, Flask, docker
    #9 4.531 Successfully installed Flask-3.0.0 Jinja2-3.1.2 MarkupSafe-2.1.3 Werkzeug-3.0.0 blinker-1.7.0 certifi-2023.11.17 charset-normalizer-3.3.2 click-8.1.7 docker-7.0.0 idna-3.6 importlib-metadata-7.0.1 itsdangerous-2.1.2 packaging-23.2 psycopg2-binary-2.9.9 requests-2.31.0 urllib3-2.1.0 zipp-3.17.0
    #9 4.531 WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
    #9 4.636 
    #9 4.636 [notice] A new release of pip is available: 23.0.1 -> 23.3.2
    #9 4.636 [notice] To update, run: pip install --upgrade pip
    #9 DONE 4.8s
    
    #10 [5/5] COPY app.py .
    #10 DONE 0.0s
    
    #11 exporting to image
    #11 exporting layers
    #11 exporting layers 2.3s done
    #11 writing image sha256:915aa801789b530e1c9b4cb8cf0021cda8161deb2ecd886e0b29fb387ad9d111 done
    #11 naming to docker.io/***/ctera-app:1704819327 done
    #11 naming to docker.io/***/ctera-app:latest done
    #11 DONE 2.3s
    Pushing tags $(date +%s),latest for Docker image docker.io/***/ctera-app...
    The push refers to repository [docker.io/***/ctera-app]
    7688da989b75: Preparing
    23acdecd58c1: Preparing
    a25f08ec2e3b: Preparing
    98157d590f37: Preparing
    6b453b473b14: Preparing
    90c3fd7d657b: Preparing
    6fb1aacdf632: Preparing
    a0814d1f5387: Preparing
    ac7146fb6cf5: Preparing
    209de9f22f2f: Preparing
    777ac9f3cbb2: Preparing
    ae134c61b154: Preparing
    90c3fd7d657b: Waiting
    6fb1aacdf632: Waiting
    a0814d1f5387: Waiting
    ac7146fb6cf5: Waiting
    777ac9f3cbb2: Waiting
    ae134c61b154: Waiting
    209de9f22f2f: Waiting
    6b453b473b14: Layer already exists
    90c3fd7d657b: Layer already exists
    6fb1aacdf632: Layer already exists
    a0814d1f5387: Layer already exists
    ac7146fb6cf5: Layer already exists
    209de9f22f2f: Layer already exists
    777ac9f3cbb2: Layer already exists
    ae134c61b154: Layer already exists
    a25f08ec2e3b: Pushed
    98157d590f37: Pushed
    7688da989b75: Pushed
    23acdecd58c1: Pushed
    1704819327: digest: sha256:28ff9e1084197a44c15b5f5f778f9848ad320a005a0b8295ad2fe1250f6aef3c size: 2838
    7688da989b75: Preparing
    23acdecd58c1: Preparing
    a25f08ec2e3b: Preparing
    98157d590f37: Preparing
    6b453b473b14: Preparing
    90c3fd7d657b: Preparing
    6fb1aacdf632: Preparing
    a0814d1f5387: Preparing
    ac7146fb6cf5: Preparing
    23acdecd58c1: Layer already exists
    a25f08ec2e3b: Layer already exists
    209de9f22f2f: Preparing
    777ac9f3cbb2: Preparing
    98157d590f37: Layer already exists
    ae134c61b154: Preparing
    6b453b473b14: Layer already exists
    90c3fd7d657b: Layer already exists
    a0814d1f5387: Waiting
    6fb1aacdf632: Layer already exists
    777ac9f3cbb2: Layer already exists
    ac7146fb6cf5: Layer already exists
    209de9f22f2f: Layer already exists
    7688da989b75: Layer already exists
    ae134c61b154: Layer already exists
    a0814d1f5387: Layer already exists
    latest: digest: sha256:28ff9e1084197a44c15b5f5f778f9848ad320a005a0b8295ad2fe1250f6aef3c size: 2838
        
    ```
6. **New image is available on docker registry**:

`https://hub.docker.com/repository/docker/jcohenp/ctera-app/general` with latest tag and with with timestamp of current date

## Security

1. **Managing secrets in docker-compose file:**

In docker there are two way to manage secret:
    
    - Using docker secret CLI: than need to initialized docker swarm
    Docker swarm is a container orchestrator, so it is not appropriate for our use case
    - Using secret directly in the docker-compose file that will use a file and put it in our container without exposing the data. The secret files should be decrypted before running docker-compose up

2. **Managing secrets in github action workflow:**

create a secret in github action will not expose the credentials of the docker registry.

3. **Creating user in Dockerfile:**

Creating a user in the Dockerfile that will just have the right to run the flask app is more secure. We dont want to allow root user access on the flask app.

4. **Creating a postgresql user in a db container:**

Creating a user will only give access to the associated db

    ```
    postgres=> \l
                                                           List of databases
       Name    |  Owner   | Encoding | Locale Provider |   Collate   |    Ctype    | ICU Locale | ICU Rules |   Access privileges   
    -----------+----------+----------+-----------------+-------------+-------------+------------+-----------+-----------------------
     postgres  | ctera    | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | =Tc/ctera            +
               |          |          |                 |             |             |            |           | ctera=CTc/ctera
     template0 | postgres | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | =c/postgres          +
               |          |          |                 |             |             |            |           | postgres=CTc/postgres
     template1 | postgres | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | =c/postgres          +
               |          |          |                 |             |             |            |           | postgres=CTc/postgres
    ```
So we can see that the postgres db belong only to the ctera user


## Improvement

1. Add a persistent storage for the db. It is not necessary for this assignment but if you want that your db is persistant you can add a volume in your docker-compose configuration:
    
    ```
    postgres:
    ...
    volumes:
      - /tmp/postgresql:/bitnami/postgresql
    ```
2. Improving security with tls certificate

3. Adding a reverse proxy between clients and flask application

4. Managing Load with container orchestrator (if number of requests is important) 
