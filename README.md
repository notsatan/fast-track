![Release][latest-release]
![Release Date][release-date]
![Language][language]
![License][license]
![Code Size][code-size]
![Black][black]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <h3 align="center">fast-track</h3>

  <p align="center">
    A simple project containing a set of CRUD API endpoints for a contact book application.    
    <br><br>
    <a href="https://github.com/demon-rem/fast-track/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/demon-rem/fast-track/issues">Bug Report</a>
    ·
    <a href="https://github.com/demon-rem/fast-track/issues">Request a Feature</a>
    ·
    <a href="https://github.com/demon-rem/fast-track/fork">Fork Repo</a>

  </p>
</p>
<br>

---
<br>

## Index

- [About](#about)
- [Features](#features)
  - [Developer Features](#developer-features)
  - [Build and Deployment](#build-and-deployment)
- [Usage](#usage)
  - [API Endpoints](#api-endpoints)
    - [Add Contact](#add-contact)
    - [Remove Contact](#remove-contact)
    - [Update Contact](#update-contact)
    - [Search Contact](#search-contact)

## About

A demonstration of the backend API for a contacts application. Uses [Flask](https://palletsprojects.com/p/flask/) as the main framework.

Uses [SQLite3](https://www.sqlite.org/index.html) as the main database by default. Includes a config file allowing to switch deployment mode between debugging and production, and modify the root directory - i.e. the directory where the database and logs are to be stored

## Features
The overall layout of the project has been inspired by [`python-package-template`](https://github.com/TezRomacH/python-package-template)

### Developer Features

- Supports Python 3.6 and above
- Uses [Poetry](https://python-poetry.org/) as the dependencies manager
- Code formatters being used: [Black](https://github.com/psf/black), [iSort](https://github.com/timothycrosley/isort), [PyUpgrade](https://github.com/asottile/pyupgrade)
- Docstring checkers with [Darglint](https://github.com/terrencepreilly/darglint)
- Type checks configured using [MyPy](https://mypy.readthedocs.io/)
- Includes [.editorconfig](https://github.com/demon-rem/fast-track/blob/master/.editorconfig) file to ensure uniformity across IDE's
- Breakdown dependencies into developer dependencies and user dependencies (the former also includes linters, code checkers, code formatters and more).

### Build and Deployment

- Uses [Github Actions](https://github.com/actions) for CI
- [Makefile](https://github.com/demon-rem/fast-track/blob/master/.editorconfig) to automate tests, linters, code formatters and more (use `make` or `make --help` for info regarding the Makefile)
- Includes [pre-commit](https://pre-commit.com/) hooks to automate code formatting

## Usage

For installation, it is recommended to use a [Virtual Environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/). Use;

```bash
make setup
```

This will download and install Poetry, and then install all required dependencies

Setup the [config file](https://github.com/demon-rem/fast-track/blob/master/config.ini.sample) as required, once done, rename the file from `config.ini.sample` to `config.ini`

To run the project, use
```bash
python runner.py
```

The python file will read values from the config, and pass them to the main project.

### API Endpoints

A list of end-points to perform add, edit, delete, and search operations.

#### Add Contact
 - Endpoint: "`/post`"
 - Method: `POST`


Input Body:
```JSON
{
    "name": "demon-rem",
    "email": "test-email@github.com",
    "phone": "007_0063"
}
```

Response Received:
```JSON
{"email": "test-email@github.com", "name": "demon-rem", "phone_number": "007_0063"}
```

Note: The database enforces a unique constraint on the email and the phone number, adding an entry that attempts to duplicate either of these values will result in a `500` status code.

#### Remove Contact

 - Endpoint: "`/delete`"
 - Method: `DELETE` 

Input Body:
```JSON
{
    "email": "test-email@github.com"
}
```

Response Received:
```JSON
{
    "result": "deleted contact successfully"
}
```

Note: An error will thrown if the email id does not match any existing contact(s)

#### Update Contact

 - Endpoint: "`/update`"
 - Method: `POST`

Input Body:
```JSON
{
    "email": "007_006@gmail.com",
    "new_name": "new-user",
    "new_email": "new-email@github.com",
    "new_phone": "324451"
}
```

Response Received:
```JSON
{
    "result": "contact modified successfully"
}
```

Note: In the input body, all three fields, i.e. `new_name`, `new_email` and `new_phone` are optional - at least one of them is required. Any missing field will not be modified in the database.

#### Search Contact
 
 - Endpoint: "`/search`"
 - Method: `GET`

Input Body:
```JSON
{
    "email": "new-user@github.com",
    "name": "new-user"
}
```

P.S. The `email` and `name` parameter are both optional - one of them should be present. Using both of them will display results where the name matches, as well as the email ID.

Response Received:
```JSON
[
    {
        "email": "new-user@github.com",
        "name": "new-user",
        "phone_number": "007324451"
    }
]
```

Note: In order to optimize searches, the project uses in-memory TTL based cache implemented through [cachetools](https://github.com/tkem/cachetools) - search results are cached in memory for 10 seconds, and up to a 100 results.

[code-size]: https://img.shields.io/github/languages/code-size/demon-rem/fast-track?style=for-the-badge
[language]: https://img.shields.io/github/languages/top/demon-rem/fast-track?style=for-the-badge
[license]: https://img.shields.io/github/license/demon-rem/fast-track?style=for-the-badge
[latest-release]: https://img.shields.io/github/v/release/demon-rem/fast-track?style=for-the-badge
[release-date]: https://img.shields.io/github/release-date/demon-rem/fast-track?style=for-the-badge
[issues-url]: https://img.shields.io/github/issues-raw/demon-rem/fast-track?style=for-the-badge
[black]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
