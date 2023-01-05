# Koor Backend
## Github Repo [🔗](https://github.com/digimonkt/koor-backend/)

![Django](https://img.shields.io/badge/Django-0C4B33?style=for-the-badge&logo=django&logoColor=white)

## Prerequisites
 - Python >= 3.10

## Project Setup
 - ### Clone the Git Repo 
     ```bash
     git clone git@github.com:digimonkt/koor-backend.git
     cd koor-backend
     ```

 - ### Setup a virtual environment
     ```bash
     python -m venv env
     ```
 - ### Activate virtual environment
     ```bash
     .\env\Scripts\Activate.ps1   # for Windows Powershell
     ```
    or
     ```bash
     .\env\Scripts\activate  # for Windows Command Prompt
     ```
    or
     ```bash
     source .\env\Scripts\activate  # for Linux or Unix
     ```

 - ### Installing Pre-requisites
     ```bash
     pip install -r .\requirements.txt
     ```

 - ### Setup `.env` File
    Create .env file add following variables. Detail about the variable based on the Configuration referenced [here](#configuration)
     ```
     DEBUG=True
     DATABASE_URI=postgres://<username>:<password>@<hostname>:<port>/<database-name>
     POSTGRES_CONN_MAX_AGE=600
     SECRET_KEY="<YOUR SECRET KEY HERE>"
     ```
## Configuration
### Local Configuration
- #### DEBUG
    Boolean value (i.e. True or False). You’re certainly developing your project with DEBUG = True, since this enables handy features like full tracebacks in your browser. _Used from .env_

- #### SECRET_KEY
    String value, A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value. _Used from .env_

- #### CONN_MAX_AGE
    Integer value, The lifetime of a database connection, as an integer of seconds. _Used from .env by variable name POSTGRES_CONN_MAX_AGE_

- #### ATOMIC_REQUESTS
    Boolean value, Set this to True to wrap each view in a transaction on this database.

 ### Development Configuration
_Inherits from Local Configuration_
**Additional Configuration**
- #### ALLOWED_HOSTS
    List value, A list of strings representing the host/domain names that this Django site can serve.

- #### ADMINS
    List value, A list of all the people who get code error notifications.

- #### MANAGERS
    List value, A list in the same format as [ADMINS](#admins) that specifies who should get broken link notifications.

- #### SERVER_EMAIL
    String value, The email address that error messages come from, such as those sent to [ADMINS](#admins) and [MANAGERS](#managers).
 
 ### Production Configuration
_Inherits from Development Configuration_
![Pending](https://img.shields.io/badge/Pending-yellow)