# Newspaper Agency Project

## Check it out!

## ✨ Start the app in Docker

> **Step 1** - Download the code from the GH repository (using `GIT`) 

```bash
$ git clone https://github.com/Phoenix-Erazer/Planetarium-API-Service
$ cd Planetarium-API-Service
```

<br />

> **Step 2** - Start the APP in `Docker`

```bash
$ docker-compose up --build 
```

Visit `http://127.0.0.1:8000/ in your browser. The app should be up & running.

<br />


### 👉 Set Up for `Windows` 

> 👉 Download the code  

```bash
$ git clone https://github.com/Phoenix-Erazer/Planetarium-API-Service
$ cd Planetarium-API-Service
```

<br />

> 👉 Install modules via `VENV`  

```bash
$ python -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

<br />

> 👉 Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> 👉 Create the Superuser

```bash
$ python manage.py createsuperuser
```

<br />

> 👉 Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`.