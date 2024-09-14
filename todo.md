to deploy first

heroku config:set DISABLE_COLLECTSTATIC=1 -a (name ur pro)

add (Procfile) web: gunicorn project.wsgi
add (runtime.txt) python 3.10.10