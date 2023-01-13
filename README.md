# pg_crossdb

# PostgreSQL Multi-DB Query Runner

This repository contains scripts that can be used to run a SQL query on all databases within a PostgreSQL server. The scripts connect to the PostgreSQL server, retrieve a list of all databases, and execute the specified SQL query on each database. The results of the query will be written to an output file in a more readable format.

## Requirements
- Rust 1.51.0 or higher (for rust script)
- postgres crate (for rust script)
- config crate (for rust script)
- psycopg2 library (for python script)

## Configuration File
[postgresql]
host = <hostname>
port = <port>
user = <username>
password = <password>

## Usage

### Python Script
```bash
python cross_db.py cross_db.conf cross_db.sql cross_db.out
```

 - cross_db.conf: The configuration file containing the database credentials.
 - cross_db.sql: The SQL file containing the query to be executed on each database.
 - cross_db.out: The file to write the query output to in a more readable format.


### Run hhe script
 - cargo run -- cross_db.py cross_db.conf cross_db.sql cross_db.out

-  cross_db.conf: The configuration file containing the database credentials.
 - cross_db.sql: The SQL file containing the query to be executed on each database.
 - cross_db.out: The file to write the query output to in a more readable format.

### Scripts
python/cross_db.py : Python script to run query on all databases of PostgreSQL
rust/cross_db/main.rs : Rust script to run query on all databases of PostgreSQL

