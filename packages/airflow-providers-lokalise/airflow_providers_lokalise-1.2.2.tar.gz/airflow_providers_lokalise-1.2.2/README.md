#  Airflow Provider Lokalise

This repository provides hook and operator to connect to the [Lokalise API](https://developers.lokalise.com/reference/lokalise-rest-api) using the [Lokalise Python SDK](https://github.com/lokalise/python-lokalise-api).

## Installation

The package is available on [pip](https://pypi.org/project/airflow-providers-lokalise/). It can be installed using

```bash
pip install airflow-providers-lokalise
```

## Connection

Hook and operator are using the following parameter to connect to Lokalise API:

* `lokalise_conn_id`: name of the connection in Airflow
* `password`: personal API token to connect to the API. Can be obtained following [this documentation](https://developers.lokalise.com/reference/api-authentication)
* `host`: name of the project in Lokalise.

##  Repo organization

* Hook is located in the `lokalise_provider/hooks` folder.
* Operator is located in the `lokalise_provider/operator` folder.
* Tests for hook and operator are located in the `tests` folder.

## Dependencies

* Python >= 3.10
* Airflow >= 2.7
* python-lokalise-api>=3.0.0

Additional dependencies are described in the [pyproject.toml file](pyproject.toml).
