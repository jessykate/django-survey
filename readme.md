install requirements using `pip install -r requirements.txt`

then run using `./manage.py runserver`

## about

Using the admin interface you can create surveys, add questions, give questions
categories, and mark them as required or not. the front-end survey view then
automatically populates based on the questions that have been defined in the
admin interface.

Submitted responses can also be viewed via the admin backend. 

## credits 
some inspiration came from an older
[django-survey](https://github.com/flynnguy/django-survey) app, but this app
uses a different model architecture and different mechanism for dynamic form
generation. 
