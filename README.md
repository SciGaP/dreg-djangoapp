Provide custom output views for the dREG science gateway. Integrates with the
https://github.com/apache/airavata-django-portal

# Getting Started

First, setup the airavata-django-portal locally. See
https://github.com/apache/airavata-django-portal.

Then, activate the virtual environment for the airavata-django-portal:

```
cd ../airavata-django-portal
source venv/bin/activate
```

Then, change to the directory of this project and install this project as a
python package in the airavata-django-portal's virtual environment:

```
cd ../dreg-djangoapp
python setup.py develop
```

To test if dreg-djangoapp installed correctly, you can go to
http://localhost:8000/dreg/hello/ and you should see a **Hello World** page.
