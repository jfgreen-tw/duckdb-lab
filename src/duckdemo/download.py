import sys
from argparse import ArgumentParser
from pathlib import Path

import boto3
from botocore import UNSIGNED
from botocore.config import Config


def build_prefix(category):
    prefix = "parquet"
    if category is not None:
        prefix += f"/product_category={category}"
    return prefix


def download_objects(objects, data_directory):
    for object_summary in objects:
        download_location = Path(data_directory) / object_summary.key

        parent_dir = download_location.parent
        if not parent_dir.exists():
            parent_dir.mkdir(parents=True)

        print(f"Downloading {download_location}")
        object_summary.Object().download_file(str(download_location))


def parse_arguments(args):
    parser = ArgumentParser("Review dataset downloader")
    parser.add_argument("data_directory", type=str, help="Directory to download review dataset to")
    parser.add_argument("--product-category", default=None)
    parser.add_argument("--bucket", default="amazon-reviews-pds", help="bucket holding review data")
    return parser.parse_args(args)


def main():
    args = parse_arguments(sys.argv[1:])
    s3 = boto3.resource("s3", config=Config(signature_version=UNSIGNED))
    review_bucket = s3.Bucket(args.bucket)
    prefix = build_prefix(args.product_category)
    parquet_objects = review_bucket.objects.filter(Prefix=prefix)
    download_objects(parquet_objects, args.data_directory)
