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

#### Requirements for python
 - psycopg2 library

```bash
python cross_db.py cross_db.conf cross_db.sql cross_db.out [xml|text|json]
```

 - cross_db.conf: The configuration file containing the database credentials.
 - cross_db.sql: The SQL file containing the query to be executed on each database.
 - cross_db.out: The file to write the query output to in a more readable format.

#### Sample SQL
```sql
WITH table_sizes AS (
    SELECT
        table_schema || '.' || table_name AS table_name,
        pg_total_relation_size(table_schema || '.' || table_name) AS table_size
    FROM
        information_schema.tables
    WHERE
        table_schema NOT LIKE 'pg_%'
        AND table_schema != 'information_schema'
    ORDER BY
        table_size DESC
)
SELECT
    table_name,
    pg_size_pretty(table_size) AS pretty_size
FROM
    table_sizes
LIMIT 3;
```
#### Sample outputs in JSON
```json
{
  "postgres": [
    [
      "public.pgbench_account_postgresl",
      "4486 MB"
    ],
    [
      "public.foo",
      "346 MB"
    ],
    [
      "public.pgbench_tellers",
      "256 kB"
    ]
  ],
  "testdb": [
    [
      "public.pgbench_accounts",
      "5981 MB"
    ],
    [
      "public.test_tb",
      "422 MB"
    ],
    [
      "public.pgbench_tellers",
      "312 kB"
    ]
  ]
}
```

#### Sample outputs in XML

```xml
<?xml version="1.0" ?>
<databases>
  <database name="postgres">
    <row>('public.pgbench_account_postgresl', '4486 MB')</row>
    <row>('public.foo', '346 MB')</row>
    <row>('public.pgbench_tellers', '256 kB')</row>
  </database>
  <database name="testdb">
    <row>('public.pgbench_accounts', '5981 MB')</row>
    <row>('public.test_tb', '422 MB')</row>
    <row>('public.pgbench_tellers', '312 kB')</row>
  </database>
  <database name="foodb">
    <row>('public.pgbench_accounts', '4486 MB')</row>
    <row>('public.pgbench_tellers', '256 kB')</row>
    <row>('public.pgbench_branches', '64 kB')</row>
  </database>
</databases>
```

### RUST Script
The Rust script is a command line application that can be used to run a SQL query on all databases within a PostgreSQL server. The script connects to the PostgreSQL server, retrieves a list of all databases, and executes the specified SQL query on each database. The results of the query will be written to an output file in a more readable format.

```bash
- cargo run -- main.rs cross_db.conf cross_db.sql cross_db.out
```

 - cross_db.conf: The configuration file containing the database credentials.
 - cross_db.sql: The SQL file containing the query to be executed on each database.
 - cross_db.out: The file to write the query output to in a more readable format.


#### Requirements for RUST
 - Rust 1.51.0 or higher
 - postgres crate
 - config crate
