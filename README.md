## Getting Started

### Prerequisites
Before you begin, ensure you have met the following requirements:

- Docker is installed

### Initialization
1. Clone the repository:
   ```shell
        git clone git@github.com:abduljabbarbcs/email-vault-backend.git
   ```
2. Navigate to the project directory:
   ```sh
   cd email-vault-backend
   ```
3. Make an .env and .env.secrets file at root level out of .example.env and .env.secrets.example and set the variables

### Project Structure
- At the base level it has necessary files like env, dockerfile, docker-compose.yml, requirements.txt, .gitignore
- Directories it contains are common, flask
- Common directory contains:
    - migration directory which contains all of migrations
    - models
    - repositories
    - dto schemas
    - utils
- flask directory contains:
    - api which contains files for all of the apis
    - email-transmitter which contains config.json
    - middlewares which contain auth for access token verification
    - app.py

## Run using docker
- run command base on your docker version
```docker-compose --env-file .env --env-file .env.secrets up --build -d``` 
   or 
```docker compose --env-file .env --env-file .env.secrets up --build -d```
- It will run the backend and related services in docker
- Now backend is available at port 5000
