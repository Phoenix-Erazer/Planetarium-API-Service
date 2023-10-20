# Newspaper Agency Project

## Check it out!

[//]: # ([Newspaper Agency Project deployed to Render]&#40;https://newspaper-agency-v299.onrender.com/&#41;)

[//]: # (```bash)

[//]: # ()
[//]: # (login: user  )

[//]: # ()
[//]: # (password: user12345)

[//]: # ()
[//]: # (```)


## Manual Build 

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