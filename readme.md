# DuckDB and Python

[DuckDB](https://duckdb.org) is an embedded, columnar database for analytical
workloads.

In this workshop we will cover:

- The properties of an embedded analytical database.
- Where might you decide to use DuckDB.
- How to interact DuckDB via Python
- Data analytics with DuckDB, Jupyter and pandas.
- Recipes for TDDing DuckDB queries.

## Setup

Requires Python 3 to be installed.

We will use a python virtual environment to create a self contained collection
of the dependencies needed for this workshop.

Create a virtual environment, install dependencies, and activate it:

```
./tasks devenv
source ./venv/bin/activate
```
The following Python packages will be installed:

- [Duckdb](https://pypi.org/project/duckdb/) - the main focus of this workshop
- [Boto3](https://pypi.org/project/boto3/) - provides us with interface to Amazon
  Web Services. We will be using this to fetch datasets from S3.

## Downloading datasets

We will be using the Amazon review dataset to explore the capabilities of DuckDB.

Unless you have a very fast internet connection, you will probably want to only
download a subset of this data. This can be accomplished using the
`duckdemo-download` command, which is available once inside the projects
virtual environment.

Using the [table of product categories](product_categories.md), select a
product category and run the downloader. For example, to download reviews of
only video games, run:

```
duckdemo-download path/to/download --product-category Digital_Video_Games
```

However, if you wish to download the full 50GB dataset, simply omit a product
category.

```
duckdemo-download path/to/download
```

## Building a summary of product reviews

In our first example, we create a database describing all the reviews for each
product.

The code can be found in `src/duckdemo/products.py`

To build the database.
```
duckdemo-products path/to/data/parquet product_summaries.db
```

### Running the tests

These tests demonstrate one potential approach to writing tests for DuckDB
queries.

The tests can be found in `tests/test_products.py`

To invoke the tests:
```
./tasks test
```

### (Optional) Querying the generated database

Download the [latest cli](https://duckdb.org) version of DuckDB and run the
following:

```
duckdb product_summaries.db
```

