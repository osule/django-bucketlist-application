[![Build Status](https://travis-ci.org/andela-osule/django-powered-bucketlist-application.svg?branch=master)](https://travis-ci.org/andela-osule/django-powered-bucketlist-application) 
[![Coverage Status](https://coveralls.io/repos/andela-osule/django-powered-bucketlist-application/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-osule/django-powered-bucketlist-application?branch=master)

# Bucketlist Tracker

Buckletlist Tracker is a Django-powered bucketlist application that helps keep track of those things you want to do in life `before you kick the bucket` (_in Jack Nicholas' voice_). 

It comes with the following features:
  - Full tests
  - Responsive User Interface
  - Exposed API endpoints
  - Excellent documentation

> The overriding design goal for Buckletlist Tracker is
> to make it as easy to use as possible.
> The idea is that exposing an API for use can help developers
> build atop this service.

### Version
0.0.1

### Tech

Bucketlist Tracker uses a number of open source projects to work properly:

* [Django] - Django makes it easier to build better Web apps more quickly and with less code
* [Swagger] - The World's Most Popular Framework for APIs
* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [Bower] - A package manager for the web
* [Django Rest Framework ] - Django REST framework is a powerful and flexible toolkit for building Web APIs
* [HTML5 Boilerplate] - HTML5 Boilerplate helps you build fast, robust, and adaptable web apps or sites
* [Font Awesome] - Font Awesome gives you scalable vector icons that can instantly be customized
* [jQuery] - jQuery is a fast, small, and feature-rich JavaScript library

And of course, Bucketlist Tracker itself is open source with a [public repository][git-repo-url]
 on GitHub.

### Installation
You can signup for an account [here](https://bucketlist-staging.herokuapp.com).

If you wish to run your own build, you need to have python installed globally on your PC. Download a release for your environment from [here](https://www.python.org/downloads/)

After you're done installing python, run these following command in your terminal.
```bash
$ git clone [git-repo-url] dpba
$ cd dpba
$ pip install -r requirements/development.txt
```

Next, setup environment your secret key
```bash
$ touch .env.py
$ echo 'SECRET_KEY="whatever-you-wish-this-to-be"'
```

Finally, run your build
```bash
$ python bucketlist/manage.py runserver --settings=settings.development
```

### Development

Want to contribute? Great!

Fork this repository, do the awesome and then make a pull request.

### Todos

 - OAuth
 - Export lists as Notes
 - Slack integration

License
----

GNU GPL

   [git-repo-url]: <https://github.com/andela-osule/django-powered-bucketlist-application.git/>
   [Font Awesome]: <https://fortawesome.github.io/Font-Awesome/>
   [Django]: <https://www.djangoproject.com/>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [Django Rest Framework]: <http://www.django-rest-framework.org/>
   [jQuery]: <http://jquery.com>
   [Swagger]: <http://swagger.io/>
   [Bower]: <http://bower.io>
   [HTML5 Boilerplate]: <https://html5boilerplate.com/>
