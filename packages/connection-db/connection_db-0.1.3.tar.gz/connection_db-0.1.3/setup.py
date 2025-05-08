from setuptools import setup, find_packages

setup(
    name="connection-db",
    version="0.1.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "sqlalchemy>=1.4.0",
        "pymssql>=2.2.0",  # for SQL Server
        "psycopg2-binary>=2.9.0",  # for PostgreSQL
        "pymysql>=1.0.0",  # for MySQL
    ],
    author="Miguel Tenorio",
    author_email="deepydev42@gmail.com",
    description="Um módulo genérico para gerenciar conexões com banco de dados",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/my_libs1/connect_db",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)