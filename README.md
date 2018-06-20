# Automated email sending webapp

Simple web application for sending email messages at particular date and time using Django 1.11, Celery 4.1.0 and RabbitMQ 3.6.14.
![demo](https://github.com/xbound/utas-webapp/blob/master/recording.gif)

## Requirements
* Python 3.5+ and Django 1.11+.
* Dependencies in `requirements.txt` file.
* pip, virtualenv and virtualenvwrapper installed(optional)
* [RabbitMQ](https://www.rabbitmq.com/) as message broker for Celery installed on machine.

## Setup

Clone this repo. Create virtual environment (optional but recommended):

	$ virtualenv webapp --python python3.5

After this `cd` into environment and execute following command to execute it:

	$ source bin/activate

After this `cd` into repository with project and install required dependencies from `requirements.txt` file:

	$ pip install -r requirements.txt

After installation succeeded  rename `.env.example` file to `.evn` and open it. Here you find some configurations webapp need o run properly, change configuration according your needs.

	SECRET_KEY=insert_secret_key_here
	DEBUG=True
	TIME_ZONE=insert_utc_timezone_here
	EMAIL_HOST=insert_email_host_here
	EMAIL_HOST_USER=youruser@example.com
	EMAIL_HOST_PASSWORD=yourpassword
	EMAIL_PORT=insert_email_port
	EMAIL_USE_TLS=True
	CELERY_RESULT_BACKEND=django-db
	CELERY_ENABLE_UTC=True
	CELERY_TIMEZONE=insert_celery_utc_timezone
	CELERY_BROKER_URL=insert_broker_url

 If you have RabbitMQ broker installed on your system chances are it will have `amqp://guest@localhost:5672//` connection string as a `CELERY_BROKER_URL `. `SECRET_KEY` property you can generate [here](https://www.miniwebtool.com/django-secret-key-generator/). ``EMAIL_HOST`` is server of your email server, in case you will be using Gmail it is ``smtp.gmail.com`` and ``EMAIL_PORT`` is ``587``. If you are planing to deploy app on server change ``DEBUG`` value to ``False``. After manual configurations your file should look like this:

	SECRET_KEY=#kz7xj92hbj)gq30#(7w*f!t1=vpr28qxozm2c@%2slg4^!%s7
	DEBUG=True
	TIME_ZONE=Europe/London
	EMAIL_HOST=smtp.gmail.com
	EMAIL_HOST_USER=email.sender@gmail.com
	EMAIL_HOST_PASSWORD=password1234
	EMAIL_PORT=587
	EMAIL_USE_TLS=True
	CELERY_RESULT_BACKEND=django-db
	CELERY_ENABLE_UTC=True
	CELERY_TIMEZONE=Europe/London
	CELERY_BROKER_URL=amqp://guest@localhost:5672//

More about Celery configuration in Django [here](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html). After configuration check apply migrations to project:

	$ ./manage.py makemigrations
	$ ./manage.py migrate

`db.sqlite3` database file will be created containing all the neccessary tables.

After this create admin user with this command (you will be prompted to insert username, email and password for your admin):

	$ ./manage.py createsuperuser

Now you will be able to create new users in admin page http://127.0.0.1:8000/admin.

Now start application:

	$ ./manage.py runserver
	
Start the celery worker:

	$ celery -A utas_webapp worker --loglevel=info


Open your browser and go to http://127.0.0.1:8000/login. You will be asked for your username and password. Here you can input username and password of your admin or user that you created in admin page.
