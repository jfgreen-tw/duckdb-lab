from setuptools import find_packages, setup

setup(
    name="duckdb-demo",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["boto3~=1.16", "duckdb~=0.2"],
    entry_points={
        "console_scripts": [
            "duckdemo-download=duckdemo.download:main",
            "duckdemo-products=duckdemo.products:main",
        ]
    },
)
