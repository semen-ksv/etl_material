## Test task: Denormaliz Material records with visualization

#### Implement:
  1. used Django Web framework
  2. for showing workflow, files were loaded to Google Cloud Storage
  3. used PostgreSQL database for saving denormalized data and counted data
  4. data denormalizing with Pandas library
  5. for visualization used Chart.js
  6. locally made visualization with Metabase
  
#### Process visualisation:

##### To check server work please go to link http://34.71.37.150/

#### Keys point:


12\. visualization created with Metabase
![](img/swage_img.jpg)




### Running project

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```
virtualenv env
```

That will create a new folder `env` in your project directory. Next activate it with this command on mac/linux:

```
source env/bin/active
```
 or 
 ```
 env\Scripts\activate
```

Then install the project dependencies with

```
pip install -r req.txt
```

Migrate for creating all tables 

```
python manage.py migrate
```
Configure .env file and load Google Cloud SECRET KEY
```
DEBUG=
SECRET_KEY=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
GOOGLE_SERVICE_FILE=
BUCKET_NAME=
```

Now you can run the project with this command

```
python manage.py runserver
```

