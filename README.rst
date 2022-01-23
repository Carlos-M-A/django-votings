=====
Votings
=====

Votings is a Django app to conduct web-based votings. For each voting,
voters can choose between a fixed number of options.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "votings" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'votings',
        ...
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('', include('votings.urls')),

3. Run  ``python manage.py makemigrations`` and ``python manage.py migrate`` to create the votings models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a votings (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/votings/ to participate in the votings.
