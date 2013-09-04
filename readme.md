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

## license

this code is licensed under the [affero general public license](http://www.gnu.org/licenses/agpl-3.0.html). 

    The GNU General Public License permits making a modified version and letting the public access it on a server without     ever releasing its source code to the public... The GNU Affero General Public License is designed specifically to     
    ensure that, in such cases, the modified source code becomes available to the community. It requires the operator of a
    network server to provide the source code of the modified version running there to the users of that server. 
