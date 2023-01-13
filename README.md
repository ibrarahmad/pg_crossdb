# pg_crossdb

# PostgreSQL Multi-DB Query Runner

This repository contains scripts that can be used to run a SQL query on all databases within a PostgreSQL server. The scripts connect to the PostgreSQL server, retrieve a list of all databases, and execute the specified SQL query on each database. The results of the query will be written to an output file in a more readable format.

## Configuration File

```bash
[postgresql]
host = <hostname>
port = <port>
user = <username>
password = <password>
```

## Usage

### Python Script
The Python script is a command line application that can be used to run a SQL query on all databases within a PostgreSQL server. The script connects to the PostgreSQL server, retrieves a list of all databases, and executes the specified SQL query on each database. The results of the query will be written to an output file in a more readable format.

```bash
python cross_db.py cross_db.conf cross_db.sql cross_db.out
```

 - cross_db.conf: The configuration file containing the database credentials.
 - cross_db.sql: The SQL file containing the query to be executed on each database.
 - cross_db.out: The file to write the query output to in a more readable format.


#### Requirements for python
 - psycopg2 library

### Run hhe script
The Rust script is a command line application that can be used to run a SQL query on all databases within a PostgreSQL server. The script connects to the PostgreSQL server, retrieves a list of all databases, and executes the specified SQL query on each database. The results of the query will be written to an output file in a more readable format.

```bash
- cargo run -- cross_db.py cross_db.conf cross_db.sql cross_db.out
```

 - cross_db.conf: The configuration file containing the database credentials.
 - cross_db.sql: The SQL file containing the query to be executed on each database.
 - cross_db.out: The file to write the query output to in a more readable format.


#### Requirements for RUST
 - Rust 1.51.0 or higher
 - postgres crate
 - config crate
