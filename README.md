# Library_app

[![CI Tests](https://github.com/KarinaAbd/library_app/actions/workflows/priject_ci.yml/badge.svg)](https://github.com/KarinaAbd/library_app/actions/workflows/priject_ci.yml)

## About

It is library book management web-application. The website allows you to see a list of available books as well as their:

- Title
- Author
- Year of publication
- ISBN
- A link to the book's page at the publisher website

Endpoints are available for books to:

- Obtaining a list of all books.
- Get information about a specific book.
- Create a new book.
- Updating information about a book.
- Deleting a book.

Registration and authorization of users is also available on the site. After registration the user receives a welcome letter to the mail.

***

## Built With

    celery==5.3.6
    Django==4.2.7
    django-bootstrap5==23.3
    flake8==6.1.0
    gunicorn==21.2.0
    python==3.10
    python-dotenv==1.0.0
    redis==5.0.1

## How to install for develop

[Install poetry](https://python-poetry.org/docs/#installation) if you haven't already. Make a fork and clone the repository locally. Then:

```bash
cd python-project-52/
make install # install the dependencies
```

Create `.env` file (based on the `.env.sample`) in the root folder for right project work and run it local:

```bash
make migrate
make start
```

To build and run the container, use the command `make docker`.
To get to know the rest of the commands, see Makefile.
