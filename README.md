# Work at Olist
[![Build Status](https://travis-ci.org/diogum/work-at-olist.svg?branch=master)](https://travis-ci.org/diogum/work-at-olist)
[![Coverage Status](https://coveralls.io/repos/github/diogum/work-at-olist/badge.svg)](https://coveralls.io/github/diogum/work-at-olist)

This is a implementation of a Django application that provides a read only API of channels (e.g. marketplaces) and categories.

The project uses *Python 3.5* and *PostgreSQL* as relational database. 

Specifications used in this project are available [here](docs/SPECIFICATION.md).

## Installation
### Requirements
* Python 3.5+
* PostgreSQL

### Instructions 

1.  Python package dependencies
    
    *Python virtualenv is not required, but highly recommended.*

    Install the package dependencies:
    ```bash
    $ pip3 install -r requirements-local.txt
    ```

2.  Setup the database

    Login as `postgres` user: 
    ```bash
    $ sudo su - postgres
    ```

    Log into a Postgres session:
    ```bash
    $ psql
    ```

    Create the database for the project:
    ```SQL
    postgres=# CREATE DATABASE mydatabase;
    ```

    Create a user to connect with the database:
    ```SQL
    postgres=# CREATE USER myuser WITH PASSWORD 'mypassword';
    ```

    Give permissions to the previously created database user:
    ```SQL
    postgres=# GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
    ```

    Exit the SQL prompt:
    ```SQL
    postgres=# \q
    ```

    Exit the shell:
    ```bash
    $ exit
    ```

3.  Create a configuration file

    Create a `.env` file, use `local.env` as template.
    ```bash
    $ cp local.env .env
    ```

    Edit the configuration file with your settings:
    
    ```
    DEBUG=True
    SECRET_KEY=SUPER-SEKRET
    DATABASE_URL=postgresql://myuser:mypassword@localhost/mydatabase
    ALLOWED_HOSTS=127.0.0.1,localhost
    ```

4.  Migrate the database

    ```bash
    $ python manage.py migrate
    ```

6.  Running the server

    ```bash
    $ python manage.py runserver
    ```

    In your web browser, visit the following address:

    `http://127.0.0.1:8000/api/v1/`

    You should see the "API Root" page.


### Django Admin 

Django Admin is available in the following URL:

`http://127.0.0.1:8000/admin/`

All that you need to access the admin site is to create a `superuser`:

```bash
$ python manage.py createsuperuser
```
You will be asked for username, email address (optional), and password.


### Running Tests

To run the tests, you need give the database user sufficient privileges to create a new database. 

In the SQL prompt (you can see how to get there at install instructions): 
```SQL
postgres=# ALTER USER myuser CREATEDB;
```

Run the tests:
```bash
$ python manage.py test
```

## Importing data

This project provides a management command, `importcategories`, to easily import data.

```bash
$ python manage.py importcategories <channel_name> <data_file>
```

- <channel_name> is the name of the channel where the categories will be imported into.
- <data_file> is the file with categories.

### How to use

This project provides a sample file, located at the `samples` directory.

To import this sample, run the following command:

```bash
$ python manage.py importcategories "My First Channel" ../samples/categories.csv
```


## API v1

### Channels

API endpoint that allows channels to be viewed.

#### List channels

`GET /api/v1/channels/`

Returns JSON data about the list of channels.

**Return format:**

An array with the following keys and values:

- name: Channel name
- url: URL of the current channel with detailed information
- reference_id: The reference id of the channel

**Sample Call:**

  ```bash
  $ curl -i http://127.0.0.1:8000/api/v1/channels/
  ```
  
  Response:

  ```json
  [
    {
      "name": "Channel Name",
      "url": "http://127.0.0.1:8000/api/v1/channels/channel-name/",
      "reference_id":"channel-name"
    },
    {
      "name": "Another Channel Name",
      "url": "http://127.0.0.1:8000/api/v1/channels/another-channel-name/",
      "reference_id":"another-channel-name"
    }
  ] 
  ```

#### Retrieve a channel

`GET /api/v1/channels/:reference_id`

Returns JSON object about a channel.

**Parameters:**

- reference_id: The reference id of the channel

**Return format:**

A JSON object containing keys and values as follows:

- name: Channel name
- url: URL of the current channel with detailed information
- reference_id: The reference id of the channel
- categories: An array of hierarchically related categories

**Sample Call:**

  ```bash
  $ curl -i http://127.0.0.1:8000/api/v1/channels/channel-name/
  ```
  
  Response:

  ```json
  {
    "name": "Channel Name",
    "url": "http://127.0.0.1:8000/api/v1/channels/channel-name/",
    "reference_id": "channel-name",
    "categories": [
      {
        "name": "Games",
        "url": "http://127.0.0.1:8000/api/v1/categories/channel-name-games/",
        "reference_id": "channel-name-games",
        "channel": "http://127.0.0.1:8000/api/v1/channels/channel-name/",
        "subcategories": [
          {
            "name": "Playstation 4",
            "url": "http://127.0.0.1:8000/api/v1/categories/channel-name-games-playstation-4/",
            "reference_id": "channel-name-games-playstation-4",
            "channel": "http://127.0.0.1:8000/api/v1/channels/channel-name/",
            "subcategories": []
          }
        ]
      }
    ]
  }
  ```

### Categories

API endpoint that allows categories to be viewed.

#### List categories

`GET /api/v1/categories/`

Returns JSON data about the list of all root categories.

**Return format:**

An array with the following keys and values:

- name: Category name
- url: URL to retrieve the current category
- reference_id: The reference id of the category
- channel: URL to retrieve the channel that this category belongs to
- subcategories: An array of nested subcategories

**Sample Call:**

  ```bash
  $ curl -i http://127.0.0.1:8000/api/v1/categories/
  ```
  
  Response:

  ```json
  [
    {
      "name": "Games",
      "url": "http://127.0.0.1:8000/api/v1/categories/channel-name-games/",
      "reference_id": "channel-name-games",
      "channel": "http://127.0.0.1:8000/api/v1/channels/channel-name/",
      "subcategories": [
        {
          "name": "Playstation 4",
          "url": "http://127.0.0.1:8000/api/v1/categories/channel-name-games-playstation-4/",
          "reference_id": "channel-name-games-playstation-4",
          "channel": "http://127.0.0.1:8000/api/v1/channels/channel-name/",
          "subcategories": []
        }
      ]
    },
    {
      "name": "Games",
      "url": "http://127.0.0.1:8000/api/v1/categories/another-channel-name-games/",
      "reference_id": "another-channel-name-games",
      "channel": "http://127.0.0.1:8000/api/v1/channels/another-channel-name/",
      "subcategories": [
        {
          "name": "XBox One",
          "url": "http://127.0.0.1:8000/api/v1/categories/another-channel-name-games-xbox-one/",
          "reference_id": "another-channel-name-games-xbox-one",
          "channel": "http://127.0.0.1:8000/api/v1/channels/another-channel-name/",
          "subcategories": []
        }
      ]
    }
  ]
  ```

#### Retrieve a category

`GET /api/v1/categories/:reference_id`

Returns JSON object about a category.

**Parameters:**

- reference_id: The reference id of the category

**Return format:**

A JSON object containing keys and values as follows:

- name: Category name
- url: URL to retrieve the current category
- reference_id: The reference id of the category
- channel: URL to retrieve the channel that this category belongs to
- parent: URL to retrieve the parent category
- subcategories: An array of nested subcategories

**Sample Call:**

  ```bash
  $ curl -i http://127.0.0.1:8000/api/v1/categories/channel-name-games/
  ```
  
  Response:

  ```json
  {
    "name": "Games",
    "url": "http://127.0.0.1:8000/api/v1/categories/channel-name-games/",
    "reference_id": "channel-name-games",
    "channel": "http://127.0.0.1:8000/api/v1/channels/channel-name/",
    "parent": null,
    "subcategories": [
      {
        "name": "Games",
        "url": "http://127.0.0.1:8000/api/v1/categories/channel-name-games/",
        "reference_id": "channel-name-games",
        "channel": "http://127.0.0.1:8000/api/v1/channels/channel-name/",
        "subcategories": [
          {
            "name": "Playstation 4",
            "url": "http://127.0.0.1:8000/api/v1/categories/channel-name-games-playstation-4/",
            "reference_id": "channel-name-games-playstation-4",
            "channel": "http://127.0.0.1:8000/api/v1/channels/channel-name/",
            "subcategories": []
          }
        ]
      },
      {
        "name": "XBOX One",
        "url": "http://127.0.0.1:8000/api/v1/categories/channel-name-games-xbox-one/",
        "reference_id": "channel-name-games-xbox-one",
        "channel": "http://127.0.0.1:8000/api/v1/channels/channel-name/",
        "parent": "http://127.0.0.1:8000/api/v1/categories/channel-name-games/",
        "subcategories": [
          {
            "name": "Games",
            "url": "http://127.0.0.1:8000/api/v1/categories/channel-name-games-xbox-one-games/",
            "reference_id": "channel-name-games-xbox-one-games",
            "channel": "http://127.0.0.1:8000/api/v1/channels/channel-name/",
            "parent": "http://127.0.0.1:8000/api/v1/categories/channel-name-games-xbox-one/",
            "subcategories": []
          }
        ]
      }
    ]
  }
  ```
