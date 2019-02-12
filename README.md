Hivery - Paranuara
==============

Hivery backend challenge.

Installation
============
1. Create a virtual environment running Python 3 (3.7 recommended) upon checkout

	> mkvirtualenv hivery_paranuara --python=\`which python3\`

2. Go to the project root and install requirements for the project

	> pip install -r requirements/requirements.txt

3. Copy your companies.json and people.json files in the resources folder

4. Run migrations.

	> cd source/; python manage.py migrate paranuara

5. Load data from .json files

	> python manage.py load_data

6. Run the local server

    > python manage.py runserver 8000


Running tests
=============
Run Django tests like this:

    python manage.py test
