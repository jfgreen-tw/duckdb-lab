import sys
from argparse import ArgumentParser

import duckdb

BUILD_PRODUCT_SUMMARY_TABLE = """
    create table product_summary as
    select
        product_id,
        first(product_title) as product_title,
        count(*) as review_count,
        sum(case when verified_purchase = 'Y' then 1 else 0 end) as verified_reviews,
        avg(star_rating) as average_rating,
        stddev_pop(star_rating) as rating_std_dev
    from reviews
    group by product_id
"""


BUILD_CONTROVERSIAL_PRODUCT_VIEW = """
    create view controversial_products as
    select *
    from product_summary
    where review_count > 10000
    order by rating_std_dev desc
    limit 100
"""


def build_product_summary_table(conn):
    conn.execute(BUILD_PRODUCT_SUMMARY_TABLE)


def build_controversial_product_view(conn):
    conn.execute(BUILD_CONTROVERSIAL_PRODUCT_VIEW)


def parse_arguments(args):
    parser = ArgumentParser("Product review summary builder")
    parser.add_argument("data_directory", help="Directory containing input dataset")
    parser.add_argument("output_file", type=str, help="Path to write output database")
    parser.add_argument("--glob-pattern", default="*/*.parquet", help="To discover input files")
    parser.add_argument("--memory-limit", type=int, default=10, help="DuckDB memory limit (in GB)")
    parser.add_argument("--threads", type=int, default=12, help="Number of threads used by DuckDB")
    return parser.parse_args(args)


def main():
    args = parse_arguments(sys.argv[1:])
    conn = duckdb.connect(args.output_file)
    conn.execute(f"PRAGMA memory_limit='{args.memory_limit}GB'")
    conn.execute(f"PRAGMA threads={args.threads}")
    parquet_files = args.data_directory + "/" + args.glob_pattern
    conn.from_parquet(parquet_files).create_view("reviews")
    build_product_summary_table(conn)
    build_controversial_product_view(conn)
    conn.close()
