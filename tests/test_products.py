import duckdb
import pytest

from duckdemo.products import build_product_summary_table

CREATE_REVIEW_TABLE = """
    CREATE TABLE reviews(
        product_id VARCHAR,
        product_title VARCHAR,
        verified_purchase VARCHAR,
        star_rating INTEGER
    )
"""


@pytest.fixture
def ducktest():
    duck_connection = duckdb.connect(":memory:")
    yield DuckTestHelper(duck_connection)
    duck_connection.close()


class DuckTestHelper:
    def __init__(self, conn):
        self.conn = conn

    def exec(self, statement):
        self.conn.execute(statement)

    def populate_table(self, table, rows):
        for row in rows:
            self.conn.values(row).insert_into(table)

    def fetch_columns(self, table, columns):
        return set(self.conn.table(table).project(", ".join(columns)).execute().fetchall())


def test_build_product_summary_exposes_product_title(ducktest):
    ducktest.exec(CREATE_REVIEW_TABLE)
    ducktest.populate_table("reviews", rows=[["123", "mango", "Y", 5], ["456", "banana", "N", 3]])

    expected_product_names = {("mango",), ("banana",)}

    build_product_summary_table(ducktest.conn)

    actual_product_names = ducktest.fetch_columns("product_summary", ["product_title"])

    assert actual_product_names == expected_product_names


def test_build_product_summary_counts_reviews(ducktest):
    ducktest.exec(CREATE_REVIEW_TABLE)
    ducktest.populate_table(
        "reviews",
        rows=[["123", "mango", "Y", 5], ["456", "banana", "N", 3], ["456", "banana", "T", 2]],
    )

    expected_review_counts = {("mango", 1), ("banana", 2)}

    build_product_summary_table(ducktest.conn)

    actual_review_counts = ducktest.fetch_columns(
        "product_summary", ["product_title", "review_count"]
    )

    assert actual_review_counts == expected_review_counts


def test_build_product_summary_calculates_average_rating(ducktest):
    ducktest.exec(CREATE_REVIEW_TABLE)
    ducktest.populate_table(
        "reviews",
        rows=[["123", "mango", "Y", 4], ["456", "banana", "N", 1], ["456", "banana", "T", 5]],
    )

    expected_average_rating = {("mango", 4), ("banana", 3)}

    build_product_summary_table(ducktest.conn)

    actual_average_rating = ducktest.fetch_columns(
        "product_summary", ["product_title", "average_rating"]
    )

    assert expected_average_rating == actual_average_rating


# TODO: More tests :)
